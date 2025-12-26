# Lesson1 - GitHub API MCP 服务

一个基于 FastMCP 的 GitHub API MCP (Model Context Protocol) 服务项目，提供聊天机器人功能和 GitHub API 集成。

## 项目结构

```
lesson1/
├── src/                    # 核心源代码
│   ├── chatbot/           # 聊天机器人模块
│   │   ├── __init__.py
│   │   └── chatbot.py
│   ├── github/            # GitHub API 客户端
│   │   ├── __init__.py
│   │   └── server.py
│   └── mcp/               # MCP 服务
│       ├── __init__.py
│       ├── gitcode_mcp.py
│       └── github_tools.py
├── examples/              # 示例代码
│   ├── chatbot_with_tools.py
│   ├── main.py
│   └── diagnose.py
├── scripts/               # 工具脚本
│   ├── setup_cursor_mcp.ps1
│   ├── setup_cursor_mcp.sh
│   └── cursor_mcp_config.json
├── docs/                  # 文档
│   ├── FUNCTION_CALLING_README.md
│   ├── MCP_SERVER_README.md
│   ├── MCP_INSPECTOR_GUIDE.md
│   ├── CURSOR_MCP_SETUP.md
│   └── 运行指南.md
├── pyproject.toml         # 项目配置
├── uv.lock                # 依赖锁定文件
└── README.md              # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# OpenAI API 配置（必需）
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.modelscope.cn/v1

# GitHub API 配置（可选，但推荐）
GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_username_here
```

### 3. 运行示例

#### 运行聊天机器人

```bash
python -m src.chatbot.chatbot
```

#### 运行带工具的聊天机器人

```bash
python examples/chatbot_with_tools.py
```

#### 运行 GitHub API 示例

```bash
python examples/main.py
```

### 4. 运行 MCP 服务器

```bash
python -m src.mcp.gitcode_mcp
```

## 功能特性

### 聊天机器人

- 支持 OpenAI API 兼容服务
- 支持流式输出
- 支持 Function Calling（工具调用）
- 对话历史管理

### GitHub API 客户端

- 异步 HTTP 请求（使用 aiohttp）
- 仓库搜索（支持模糊搜索）
- Pull Requests 查询
- 提交历史查询
- 变更文件查询

### MCP 服务

- 基于 FastMCP 的 MCP 服务器
- 提供 4 个工具：
  - `search_repository` - 搜索仓库
  - `get_pull_requests` - 获取 PR 列表
  - `get_pull_request_files` - 获取 PR 变更文件
  - `get_commits` - 获取提交历史

## 配置 MCP 服务

### Cursor IDE

运行自动配置脚本：

```powershell
# Windows
.\scripts\setup_cursor_mcp.ps1

# Linux/macOS
chmod +x scripts/setup_cursor_mcp.sh
./scripts/setup_cursor_mcp.sh
```

详细说明请参考：[docs/CURSOR_MCP_SETUP.md](docs/CURSOR_MCP_SETUP.md)

### Claude Desktop

编辑配置文件（`%APPDATA%\Claude\claude_desktop_config.json` 或 `~/Library/Application Support/Claude/claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": ["path/to/src/mcp/gitcode_mcp.py"],
      "env": {
        "GITHUB_TOKEN": "your_token",
        "GITHUB_USERNAME": "your_username"
      }
    }
  }
}
```

## 调试 MCP 服务

使用 MCP Inspector：

```bash
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

详细说明请参考：[docs/MCP_INSPECTOR_GUIDE.md](docs/MCP_INSPECTOR_GUIDE.md)

## 文档

- [Function Calling 使用指南](docs/FUNCTION_CALLING_README.md)
- [MCP 服务器文档](docs/MCP_SERVER_README.md)
- [MCP Inspector 调试指南](docs/MCP_INSPECTOR_GUIDE.md)
- [Cursor MCP 配置指南](docs/CURSOR_MCP_SETUP.md)
- [运行指南](docs/运行指南.md)

## 开发

### 项目结构说明

- `src/` - 核心源代码，按功能模块组织
- `examples/` - 示例代码，展示如何使用各个模块
- `scripts/` - 工具脚本，用于自动化任务
- `docs/` - 项目文档

### 导入模块

```python
# 导入聊天机器人
from src.chatbot.chatbot import ChatBot

# 导入 GitHub API 客户端
from src.github.server import search_repository_by_url

# 导入 MCP 工具
from src.mcp.github_tools import get_github_tools
```

## 许可证

MIT License

