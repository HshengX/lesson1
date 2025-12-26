# GitCode MCP 服务器使用说明

## 概述

`src/mcp/gitcode_mcp.py` 是一个基于 FastMCP 的 MCP (Model Context Protocol) 服务器，将 GitHub API 客户端封装为 MCP 服务，名为 `gitcode`。

## 安装依赖

首先安装 fastmcp：

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install fastmcp
```

## 运行 MCP 服务器

### 方式 1: 直接运行

```bash
# 方式 1: 直接运行
python -m src.mcp.gitcode_mcp

# 方式 2: 使用完整路径
python src/mcp/gitcode_mcp.py
```

### 方式 2: 使用 MCP 客户端连接

MCP 服务器通过 stdio (标准输入输出) 与客户端通信。客户端可以通过以下方式连接：

```json
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": ["src/mcp/gitcode_mcp.py"]
    }
  }
}
```

## 可用工具

MCP 服务器提供以下 4 个工具：

### 1. `search_repository`

搜索 GitHub 仓库

**参数：**
- `repo_url` (str, 必需): 仓库地址，支持多种格式
  - 完整 URL: `https://github.com/owner/repo`
  - GitHub URL: `github.com/owner/repo`
  - 简短格式: `owner/repo`
  - 仓库名称: `repo` (会进行模糊搜索)
- `per_page` (int, 可选): 每页返回数量，默认 30
- `page` (int, 可选): 页码，默认 1
- `sort` (str, 可选): 排序方式，可选值: `stars`, `forks`, `updated`，默认 `stars`
- `order` (str, 可选): 排序顺序，可选值: `desc`, `asc`，默认 `desc`

**返回：** 包含搜索结果和状态的字典

### 2. `get_pull_requests`

获取仓库的 Pull Requests

**参数：**
- `repo_id` (int, 必需): 仓库 ID
- `state` (str, 可选): PR 状态，可选值: `open`, `closed`, `all`，默认 `open`
- `per_page` (int, 可选): 每页返回数量，默认 30
- `page` (int, 可选): 页码，默认 1
- `sort` (str, 可选): 排序方式，可选值: `created`, `updated`, `popularity`，默认 `created`
- `direction` (str, 可选): 排序顺序，可选值: `asc`, `desc`，默认 `desc`

**返回：** 包含 Pull Requests 数据和状态的字典

### 3. `get_pull_request_files`

获取 PR 的变更文件

**参数：**
- `repo_id` (int, 必需): 仓库 ID
- `pr_number` (int, 必需): Pull Request 编号

**返回：** 包含变更文件数据和状态的字典

### 4. `get_commits`

获取仓库的提交历史

**参数：**
- `repo_id` (int, 必需): 仓库 ID
- `sha` (str, 可选): 分支或提交 SHA，默认为默认分支
- `path` (str, 可选): 只返回包含指定路径的提交
- `author` (str, 可选): 只返回指定作者的提交（GitHub 用户名或邮箱）
- `since` (str, 可选): 只返回此日期之后的提交（ISO 8601 格式，如 `2024-01-01T00:00:00Z`）
- `until` (str, 可选): 只返回此日期之前的提交（ISO 8601 格式）
- `per_page` (int, 可选): 每页返回数量，默认 30，最大 100
- `page` (int, 可选): 页码，默认 1

**返回：** 包含提交数据和状态的字典

## 环境变量配置

MCP 服务器使用与 `src/github/server.py` 相同的环境变量：

```env
# GitHub API Token（可选，但可以提高 API 限制）
GITHUB_TOKEN=your_github_token_here

# GitHub Username（可选，会添加到请求头中）
GITHUB_USERNAME=your_username_here
```

## 在 Claude Desktop 中使用

1. 找到 Claude Desktop 的配置文件：
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. 编辑配置文件，添加 MCP 服务器：

```json
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": ["D:/ai/aiproject/gf-aiproject/gfMcpCourse/lesson1/src/mcp/gitcode_mcp.py"],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here",
        "GITHUB_USERNAME": "your_username_here"
      }
    }
  }
}
```

3. 重启 Claude Desktop

## 在 Cursor 中使用

1. 打开 Cursor 设置
2. 找到 MCP 服务器配置
3. 添加 gitcode 服务器配置

## 测试 MCP 服务器

### 使用 MCP Inspector 调试

MCP Inspector 是一个交互式调试工具，用于测试和调试 MCP 服务器。

#### 安装和运行

```bash
# 使用 npx 直接运行（无需安装）
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

#### 完整命令格式

```bash
# 基本格式
npx @modelcontextprotocol/inspector <command> <args>

# 对于 Python 脚本
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp

# 如果使用 uv 运行
npx @modelcontextprotocol/inspector uv --directory . run python -m src.mcp.gitcode_mcp

# 如果需要指定工作目录
npx @modelcontextprotocol/inspector python D:/ai/aiproject/gf-aiproject/gfMcpCourse/lesson1/src/mcp/gitcode_mcp.py
```

#### 使用步骤

1. **启动 Inspector**：
   ```bash
   npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
   ```

2. **打开浏览器**：
   - Inspector 会启动一个 Web UI，默认地址：`http://localhost:5173`
   - 如果端口被占用，会使用其他可用端口

3. **连接服务器**：
   - Inspector 会自动连接到您的 MCP 服务器
   - 如果使用 stdio 传输，连接会自动建立

4. **调试功能**：
   - **资源面板**：查看所有可用资源
   - **提示模板面板**：测试提示模板
   - **工具面板**：测试工具调用
     - 查看工具定义和参数
     - 输入参数测试工具
     - 查看执行结果
   - **通知面板**：查看服务器日志和通知

#### 示例：测试 search_repository 工具

1. 在 Inspector 的工具面板中找到 `search_repository`
2. 输入参数：
   ```json
   {
     "repo_url": "lesson1",
     "per_page": 10
   }
   ```
3. 点击执行，查看返回结果

#### 环境变量

如果需要在 Inspector 中设置环境变量：

```bash
# Windows PowerShell
$env:GITHUB_TOKEN="your_token"; $env:GITHUB_USERNAME="your_username"; npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp

# Linux/macOS
GITHUB_TOKEN=your_token GITHUB_USERNAME=your_username npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

#### 故障排除

- **端口被占用**：Inspector 会自动尝试其他端口，查看终端输出获取实际地址
- **连接失败**：确保 `src/mcp/gitcode_mcp.py` 路径正确，且 Python 环境已安装 `fastmcp`
- **工具调用失败**：检查环境变量是否正确设置，查看通知面板的错误信息

## 故障排除

### 问题 1: 导入错误

如果遇到 `ModuleNotFoundError: No module named 'fastmcp'`，请确保已安装依赖：

```bash
uv sync
# 或
pip install fastmcp
```

### 问题 2: 环境变量未加载

确保 `.env` 文件在项目根目录，或通过环境变量直接设置：

```bash
export GITHUB_TOKEN=your_token
export GITHUB_USERNAME=your_username
python -m src.mcp.gitcode_mcp
```

### 问题 3: 权限错误

确保有执行 `gitcode_mcp.py` 的权限：

```bash
chmod +x src/mcp/gitcode_mcp.py
```

## 相关文档

- [FastMCP 官方文档](https://fastmcp.wiki/)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [GitHub API 文档](https://docs.github.com/en/rest)

