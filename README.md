# Shortdrama Basic / 分镜基础工具

An independently runnable, local MCP server for source text, generic storyboard
tables, and Excel export. Version **0.1.0** · **MIT** license.

本项目提供 8 个本地工具：创建和查询项目、保存和读取原文、读取和保存分镜表、导出
Excel，以及查询版本与能力。基础版使用独立 SQLite 数据库；不需要私有服务或私有规则包。

创作由用户或连接的模型完成。本服务器负责存取和导出，不内置模型调用、分镜生成引擎、
专有创作规则或语义审查。导出的表格是通用基础格式，不能当作其他版本的正式交付模板。

## 安装与验证

需要 Python 3.12，以及支持本地 stdio MCP 的客户端。安装脚本联网安装依赖；本地数据
存取和导出不调用外部服务，不需要 API key。模型客户端可能有自己的订阅或计费。

解压源码，在项目根目录执行。Windows PowerShell：

```powershell
python --version
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_local.ps1
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests\stdio_smoke.py
```

macOS / Linux：

```bash
python3 --version
bash scripts/setup_local.sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tests/stdio_smoke.py
```

通过 `PYTHON_BIN` 环境变量指定其他 Python 3.12 可执行文件。安装后 `.mcp.json` 会写入
本机绝对路径，供 MCP 客户端使用。[完整安装说明](docs/INSTALL.md)包含注册方式和数据位置。

## 使用示例

在已接入的客户端提出：

> 创建名为“车站示例”的基础分镜项目。保存这段原创短文：小雨捡到一把伞，等到失主回来，
> 把伞还给对方。对方说：“谢谢你。” 按我的要求整理一个简单分镜表，保存后导出 Excel。

客户端可读取 [合成分镜示例](examples/storyboard.json)。行数据包含：

| 字段 | 用途 |
| --- | --- |
| `shot_id` | 必填，表内唯一的行标识 |
| `visual` | 必填，画面描述 |
| `scene`、`dialogue`、`notes` | 可选文本 |
| `duration_seconds` | 可选的用户填写时长；不代表媒体测量 |
| `source_id` | 可选，关联同一项目中已导入的原文 |

修改时先读取 `get_storyboard`，保留未修改行，再以返回的 `revision` 调用
`save_storyboard(expected_revision=...)`。保存是整表替换；冲突会拒绝，不会静默覆盖。
基础版不保存历史表格版本，改表前可先导出备份。

原文每次导入形成独立记录，最多 200000 字符，不自动改写。每张表最多 1000 行，
单个长文本字段最多 12000 字符，完整行数据最多 2 MiB。这些是基础版存储限制。

## 发布范围与开发

- [公开与私有范围](docs/SCOPE.md)
- [贡献说明](docs/CONTRIBUTING.md)
- [数据与安全说明](docs/SECURITY.md)
- [依赖与许可证](docs/DEPENDENCIES.md)
- [MCP 使用技能](skills/shortdrama-basic/SKILL.md)

源码打包只收录 `scripts/package_source.py` 中明确列出的 24 个公开文件。
安装后先恢复可分发配置，再打包：

```powershell
.\.venv\Scripts\python.exe scripts\configure_local_mcp.py --portable
.\.venv\Scripts\python.exe scripts\package_source.py
.\.venv\Scripts\python.exe scripts\configure_local_mcp.py
```

输出在 `dist/`。macOS / Linux 使用 `.venv/bin/python` 执行相同脚本。
向 Git 提交安装后的修改前，也应恢复 `.mcp.json`，避免提交本机路径。

软件许可见 [LICENSE](LICENSE)。用户导入的原文和分镜不因使用本软件而自动获得 MIT 许可。
