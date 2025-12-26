# 项目目录结构说明

## 目录组织

```
lesson1/
├── src/                    # 核心源代码
│   ├── chatbot/           # 聊天机器人模块
│   │   ├── __init__.py
│   │   └── chatbot.py     # 聊天机器人主类
│   ├── github/            # GitHub API 客户端
│   │   ├── __init__.py
│   │   └── server.py      # GitHub API 异步客户端
│   └── mcp/               # MCP 服务
│       ├── __init__.py
│       ├── gitcode_mcp.py    # FastMCP 服务器实现
│       └── github_tools.py    # GitHub 工具定义（Function Calling）
│
├── examples/              # 示例代码
│   ├── chatbot_with_tools.py  # 带工具的聊天机器人示例
│   ├── main.py                # GitHub API 使用示例
│   ├── diagnose.py            # 诊断脚本
│   └── chatbot_demo.ipynb     # Jupyter Notebook 演示
│
├── scripts/               # 工具脚本
│   ├── setup_cursor_mcp.ps1   # Cursor MCP 配置脚本（Windows）
│   ├── setup_cursor_mcp.sh     # Cursor MCP 配置脚本（Linux/macOS）
│   └── cursor_mcp_config.json  # Cursor MCP 配置模板
│
├── docs/                  # 项目文档
│   ├── FUNCTION_CALLING_README.md    # Function Calling 使用指南
│   ├── MCP_SERVER_README.md          # MCP 服务器文档
│   ├── MCP_INSPECTOR_GUIDE.md        # MCP Inspector 调试指南
│   ├── CURSOR_MCP_SETUP.md           # Cursor MCP 配置指南
│   └── 运行指南.md                    # 运行指南
│
├── pyproject.toml         # 项目配置和依赖
├── uv.lock                # 依赖锁定文件
└── README.md              # 项目主文档
```

## 模块说明

### src/chatbot/
聊天机器人核心模块，提供：
- OpenAI API 兼容接口
- 流式输出支持
- Function Calling 支持
- 对话历史管理

### src/github/
GitHub API 客户端模块，提供：
- 异步 HTTP 请求（aiohttp）
- 仓库搜索功能
- Pull Requests 查询
- 提交历史查询
- 变更文件查询

### src/mcp/
MCP 服务模块，提供：
- FastMCP 服务器实现
- GitHub 工具封装
- MCP 协议支持

### examples/
示例代码，展示如何使用各个模块：
- `chatbot_with_tools.py` - 使用带工具的聊天机器人
- `main.py` - GitHub API 基本使用
- `diagnose.py` - 诊断和测试脚本

### scripts/
工具脚本，用于自动化任务：
- Cursor MCP 配置脚本
- 配置模板文件

### docs/
项目文档，包含：
- 功能使用指南
- 配置说明
- 调试指南

## 导入方式

### 在项目内部导入

```python
# 导入聊天机器人
from src.chatbot.chatbot import ChatBot

# 导入 GitHub API 客户端
from src.github.server import search_repository_by_url

# 导入 MCP 工具
from src.mcp.github_tools import get_github_tools
```

### 在示例代码中导入

示例代码位于 `examples/` 目录，需要添加项目根目录到路径：

```python
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 然后可以导入模块
from src.github.server import search_repository_by_url
```

## 运行方式

### 运行模块

```bash
# 运行聊天机器人
python -m src.chatbot.chatbot

# 运行 MCP 服务器
python -m src.mcp.gitcode_mcp
```

### 运行示例

```bash
# 运行示例代码
python examples/chatbot_with_tools.py
python examples/main.py
```

## 配置路径

### Cursor MCP 配置

MCP 服务器路径应为：
```
src/mcp/gitcode_mcp.py
```

或使用模块方式：
```
python -m src.mcp.gitcode_mcp
```

### MCP Inspector 调试

```bash
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

## 优势

1. **清晰的模块划分**：按功能组织代码，易于维护
2. **可扩展性**：新功能可以轻松添加到对应模块
3. **可重用性**：模块可以在不同项目中复用
4. **文档集中**：所有文档统一放在 `docs/` 目录
5. **示例分离**：示例代码独立，不影响核心代码

