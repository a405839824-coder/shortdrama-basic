# Contributing

Install with `scripts/setup_local.ps1` or `scripts/setup_local.sh`. Keep changes
focused on the basic edition's documented capabilities. Add a reproducible
behavior check for changes to storage, export or the tool interface.

Run `python -m unittest discover -s tests -v` and `python tests/stdio_smoke.py`
with the project's virtual environment. Before packaging or committing local
configuration, run `python scripts/configure_local_mcp.py --portable`.
Use `python scripts/configure_local_mcp.py` to restore local launch paths afterward.

Use synthetic examples in reports and tests. Never attach customer text,
credentials, database files, or proprietary implementation material.
Contributions to this public edition are made under its MIT license.

The included GitHub Actions workflow defines checks for Windows and Linux;
its presence is not evidence that those jobs have already run.
