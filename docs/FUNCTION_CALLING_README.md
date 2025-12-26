# GitHub 工具 Function Calling 使用说明

本项目已将三个 GitHub API 工具集成到聊天机器人中，遵循 OpenAI Function Calling 规范。

## 可用工具

### 1. `search_repository_by_url`
通过仓库地址模糊查找仓库信息

**参数：**
- `repo_url` (必需): 仓库地址，支持多种格式
  - 完整 URL: `https://github.com/owner/repo`
  - GitHub URL: `github.com/owner/repo`
  - 简短格式: `owner/repo`
  - 仓库名称: `repo` (会进行模糊搜索)
- `per_page` (可选): 每页返回数量，默认 30，范围 1-100
- `page` (可选): 页码，默认 1
- `sort` (可选): 排序方式，可选值: `stars`, `forks`, `updated`，默认 `stars`
- `order` (可选): 排序顺序，可选值: `desc`, `asc`，默认 `desc`

**返回：** 仓库列表，包含仓库 ID、名称、描述、Stars、Forks 等信息

### 2. `get_pull_requests_by_repo_id`
根据仓库 ID 获取该仓库的所有 Pull Requests

**参数：**
- `repo_id` (必需): 仓库 ID（整数）
- `state` (可选): PR 状态筛选，可选值: `open`, `closed`, `all`，默认 `open`
- `per_page` (可选): 每页返回数量，默认 30，范围 1-100
- `page` (可选): 页码，默认 1
- `sort` (可选): 排序方式，可选值: `created`, `updated`, `popularity`，默认 `created`
- `direction` (可选): 排序顺序，可选值: `asc`, `desc`，默认 `desc`

**返回：** Pull Requests 列表，包含 PR 编号、标题、状态、作者等信息

### 3. `get_pull_request_files_by_repo_id`
根据仓库 ID 和 Pull Request 编号获取变更文件和变更内容

**参数：**
- `repo_id` (必需): 仓库 ID（整数）
- `pr_number` (必需): Pull Request 编号（整数）

**返回：** 变更文件列表，包含文件名、变更统计、diff 补丁等信息

## 使用方法

### 方法 1: 使用增强版 ChatBot（推荐）

`chatbot.py` 已集成 Function Calling 支持，默认启用：

```python
from chatbot import ChatBot

# 初始化聊天机器人（默认启用工具）
chatbot = ChatBot()

# 直接对话，模型会自动调用工具
response = chatbot.chat("帮我搜索一下 lesson1 这个仓库")
```

### 方法 2: 使用独立工具模块

```python
import asyncio
from github_tools import get_github_tools, call_tool, format_tool_result

# 获取工具定义（可用于 OpenAI API）
tools = get_github_tools()

# 直接调用工具
async def example():
    # 搜索仓库
    result = await call_tool("search_repository_by_url", {
        "repo_url": "lesson1"
    })
    
    # 格式化结果
    formatted = format_tool_result("search_repository_by_url", result)
    print(formatted)

asyncio.run(example())
```

### 方法 3: 使用独立示例文件

运行 `chatbot_with_tools.py`：

```bash
python chatbot_with_tools.py
```

## 工具定义格式

工具定义遵循 OpenAI Function Calling 规范：

```python
{
    "type": "function",
    "function": {
        "name": "search_repository_by_url",
        "description": "工具描述",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_url": {
                    "type": "string",
                    "description": "参数描述"
                }
            },
            "required": ["repo_url"]
        }
    }
}
```

## 工作流程

1. **用户提问** → 聊天机器人接收用户输入
2. **模型分析** → 模型判断是否需要调用工具
3. **工具调用** → 如果需要，模型返回工具调用请求
4. **执行工具** → 系统执行相应的 GitHub API 调用
5. **返回结果** → 工具执行结果返回给模型
6. **生成回复** → 模型基于工具结果生成最终回复

## 示例对话

**用户：** "帮我搜索一下 lesson1 这个仓库"

**系统：**
```
[工具调用] 检测到 1 个工具调用
  - 调用工具: search_repository_by_url
    [成功] 工具执行完成
```

**助手：** "我找到了以下仓库：1. HshengX/lesson1 (ID: xxx) ..."

**用户：** "这个仓库有哪些 Pull Requests？"

**系统：**
```
[工具调用] 检测到 1 个工具调用
  - 调用工具: get_pull_requests_by_repo_id
    [成功] 工具执行完成
```

**助手：** "仓库 ID xxx 的 open 状态 Pull Requests（共 X 个）：..."

## 注意事项

1. **流式输出限制**：Function Calling 不支持流式输出，如果启用了工具，会自动切换到非流式模式
2. **异步函数**：所有工具函数都是异步的，系统会自动处理事件循环
3. **迭代限制**：默认最大迭代次数为 10 次，防止无限循环
4. **错误处理**：工具执行失败时会返回错误信息，模型会基于错误信息生成回复

## 文件说明

- `github_tools.py`: 工具定义和调用函数
- `chatbot.py`: 集成 Function Calling 的聊天机器人
- `chatbot_with_tools.py`: 独立的工具示例文件

