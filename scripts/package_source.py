"""Build a source ZIP from a fixed public-file list, excluding all runtime data."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "server"))
from basic import VERSION

PUBLIC_FILES = (
    ".codex-plugin/plugin.json", ".gitattributes", ".gitignore", ".mcp.json",
    ".github/workflows/validate.yml", "LICENSE", "README.md", "requirements.txt",
    "docs/INSTALL.md", "docs/SCOPE.md", "docs/CONTRIBUTING.md", "docs/SECURITY.md", "docs/DEPENDENCIES.md",
    "server/basic.py", "server/main.py", "skills/shortdrama-basic/SKILL.md",
    "examples/storyboard.json", "scripts/atomic_io.py", "scripts/configure_local_mcp.py",
    "scripts/setup_local.ps1", "scripts/setup_local.sh", "scripts/package_source.py",
    "tests/test_basic.py", "tests/stdio_smoke.py",
)
SECRET = re.compile(r"(?:github_pat_|ghp_|sk-proj-)[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")


def build(root: Path, output: Path):
    root = root.resolve()
    config = json.loads((root / ".mcp.json").read_text(encoding="utf-8"))
    expected = {"mcpServers": {"shortdrama-basic": {"cwd": ".", "command": "./.venv/bin/python", "args": ["./server/main.py", "--stdio"], "env": {"PYTHONUTF8": "1"}}}}
    if config != expected:
        raise ValueError("Run scripts/configure_local_mcp.py --portable before packaging")
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if manifest["name"] != "shortdrama-basic" or manifest["version"] != VERSION:
        raise ValueError("Plugin identity/version mismatch")
    contents = {}
    for name in PUBLIC_FILES:
        path = root / name
        chain = [path, *path.parents]
        for component in chain:
            if component == root:
                break
            if component.is_symlink() or (hasattr(component, "is_junction") and component.is_junction()):
                raise ValueError(f"Linked paths cannot be packaged: {name}")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Missing or unsafe public file: {name}")
        content = path.read_bytes()
        decoded = content.decode("utf-8")
        if SECRET.search(decoded) or re.search(r"[A-Z]:[/\\]Users[/\\]", decoded, re.I):
            raise ValueError(f"Credential or personal local path detected in {name}")
        contents[name] = content
    output = output.absolute()
    if output.is_symlink() or output.resolve() in {(root / name).resolve() for name in PUBLIC_FILES}:
        raise ValueError("Output must not replace a source file or symbolic link")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in contents.items():
            archive.writestr(f"shortdrama-basic/{name}", content)
    return {"status": "pass", "version": VERSION, "files": len(contents),
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "dist" / f"shortdrama-basic-{VERSION}.zip")
    args = parser.parse_args()
    report = build(root, args.output)
    args.output.with_suffix(".zip.sha256").write_text(f"{report['sha256']}  {args.output.name}\n", encoding="utf-8")
    print(json.dumps(report))
