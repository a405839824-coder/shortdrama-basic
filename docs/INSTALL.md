# 安装与接入

## 本地环境

安装 Python 3.12，把源码解压到固定目录。Windows 在根目录运行：

```powershell
$env:PYTHON_BIN = "C:\Python312\python.exe" # 如 python 已是 3.12，可不设置
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_local.ps1
```

将示例 Python 路径替换为本机实际路径。macOS / Linux 运行
`PYTHON_BIN=/path/to/python3.12 bash scripts/setup_local.sh`。
脚本创建 `.venv`、安装两个直接依赖，并生成本机 `.mcp.json`。
源码 ZIP 不包含 Python 或预装环境。移动项目目录后应重新运行安装脚本。

## MCP 客户端

支持 MCP 配置的客户端可以读取根目录 `.mcp.json` 中的 `mcpServers` 条目。
其中 `command`、`args`、`cwd` 已由安装脚本写入实际路径。根目录还提供可供支持
该格式的客户端使用的 `.codex-plugin/plugin.json` 和基础技能；它不是官方插件商店上架记录。

对于已安装的 Codex CLI，Windows 在根目录执行：

```powershell
$BasicPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
$BasicServer = (Resolve-Path .\server\main.py).Path
codex mcp add shortdrama-basic -- $BasicPython $BasicServer --stdio
```

macOS / Linux：

```bash
codex mcp add shortdrama-basic -- "$(pwd)/.venv/bin/python" "$(pwd)/server/main.py" --stdio
```

此注册操作由用户按需执行。打包和测试不会自动改动已有客户端连接。
连接成功后调用 `get_status`，应看到 `edition=basic`、`version=0.1.0`；共 8 个工具。
服务器只实现本地 stdio，不提供公开 HTTP 地址或多人账户服务。

## 数据与备份

默认数据库为源码根目录下 `data/shortdrama-basic.sqlite3`，导出文件在 `data/exports/`。
可在客户端启动环境中设置 `SHORTDRAMA_BASIC_DATA_DIR` 为独立绝对目录。
原文、分镜和导出文件都可能包含私人内容，不要上传该目录。

停止服务器后备份整个数据目录，恢复时同样在服务器停止期间操作。
基础版不会读取其他版本的配置、数据库或账号，也没有跨版本迁移功能。
源记录可重复导入，每次得到新的 ID；分镜保存覆盖当前整张表，修订号仅防止并发覆盖，
不提供历史版本恢复。需要保留旧表时先导出。

Excel 导出返回本机路径，客户端若运行在另一台机器，不能直接访问此路径。

## 验证和排错

Windows 使用 `.venv\Scripts\python.exe`，macOS / Linux 使用 `.venv/bin/python`：

```text
python -m unittest discover -s tests -v
python tests/stdio_smoke.py
```

把上面 `python` 换为对应虚拟环境解释器。连通性检查使用独立临时合成数据，结束后清理。
`ModuleNotFoundError` 表示没有使用正确环境或安装未完成；重新执行安装脚本。
`Revision conflict` 表示期间已有数据变化，重新读取整表后再合并修改。
`Unknown fields` / `unknown fields` 表示输入超出基础版格式，需要明确转换，不能直接套用其他模板。

本次交付的实际平台与测试结果记录在源码包外的验证报告中；工作流文件的存在不代表 CI 已执行。
