# MCP Inspector 调试指南

## 什么是 MCP Inspector？

MCP Inspector 是 Model Context Protocol 的官方调试工具，提供了一个交互式 Web UI 来测试和调试 MCP 服务器。

## 快速开始

### 基本命令

```bash
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

### 命令格式

```bash
npx @modelcontextprotocol/inspector <command> <args>
```

## 针对 gitcode MCP 服务器的使用

### 1. 基本调试命令

```bash
# 在项目根目录运行
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

### 2. 使用绝对路径

```bash
npx @modelcontextprotocol/inspector python D:/ai/aiproject/gf-aiproject/gfMcpCourse/lesson1/src/mcp/gitcode_mcp.py
```

### 3. 使用 uv 运行（如果使用 uv 管理依赖）

```bash
npx @modelcontextprotocol/inspector uv --directory . run python -m src.mcp.gitcode_mcp
```

### 4. 设置环境变量

#### Windows PowerShell

```powershell
$env:GITHUB_TOKEN="your_token"
$env:GITHUB_USERNAME="your_username"
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

#### Linux/macOS

```bash
GITHUB_TOKEN=your_token GITHUB_USERNAME=your_username npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

## 使用步骤

### 步骤 1: 启动 Inspector

在终端运行命令：

```bash
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

您会看到类似输出：

```
MCP Inspector
Server: python gitcode_mcp.py
Client UI: http://localhost:5173
MCP Proxy: http://localhost:3000
```

### 步骤 2: 打开浏览器

在浏览器中打开显示的 URL（通常是 `http://localhost:5173`）

### 步骤 3: 使用调试界面

Inspector 界面包含以下面板：

#### 工具面板 (Tools)

- **查看工具列表**：显示所有可用的 MCP 工具
- **查看工具定义**：查看每个工具的参数、描述和返回类型
- **测试工具**：
  1. 选择要测试的工具（如 `search_repository`）
  2. 在输入框中输入 JSON 格式的参数
  3. 点击 "Call Tool" 执行
  4. 查看返回结果

**示例：测试 search_repository**

```json
{
  "repo_url": "lesson1",
  "per_page": 10,
  "sort": "stars",
  "order": "desc"
}
```

#### 资源面板 (Resources)

- 查看服务器提供的所有资源
- 查看资源元数据
- 订阅资源更新

#### 提示模板面板 (Prompts)

- 查看可用的提示模板
- 测试提示模板
- 预览生成的消息

#### 通知面板 (Notifications)

- 查看服务器日志
- 查看错误信息
- 监控服务器状态

## 调试示例

### 示例 1: 测试仓库搜索

1. 在工具面板找到 `search_repository`
2. 输入参数：
   ```json
   {
     "repo_url": "fastapi",
     "per_page": 5
   }
   ```
3. 点击执行
4. 查看返回的仓库列表

### 示例 2: 测试获取 Pull Requests

1. 首先使用 `search_repository` 获取仓库 ID
2. 在工具面板找到 `get_pull_requests`
3. 输入参数（使用上一步获取的 repo_id）：
   ```json
   {
     "repo_id": 123456,
     "state": "open",
     "per_page": 10
   }
   ```
4. 点击执行
5. 查看返回的 PR 列表

### 示例 3: 测试获取提交历史

1. 使用 `search_repository` 获取仓库 ID
2. 在工具面板找到 `get_commits`
3. 输入参数：
   ```json
   {
     "repo_id": 123456,
     "per_page": 20
   }
   ```
4. 点击执行
5. 查看返回的提交列表

## 常见问题

### Q1: 端口被占用

**问题**：`Error: Port 5173 is already in use`

**解决**：
- Inspector 会自动尝试其他端口
- 查看终端输出获取实际使用的端口
- 或手动指定端口（如果 Inspector 支持）

### Q2: 连接失败

**问题**：无法连接到 MCP 服务器

**解决**：
- 检查 `src/mcp/gitcode_mcp.py` 路径是否正确
- 确保 Python 环境已安装 `fastmcp`：
  ```bash
  uv sync
  # 或
  pip install fastmcp
  ```
- 检查 Python 是否在系统 PATH 中

### Q3: 工具调用失败

**问题**：工具执行返回错误

**解决**：
- 检查环境变量是否正确设置（`GITHUB_TOKEN`, `GITHUB_USERNAME`）
- 查看通知面板的错误信息
- 检查网络连接
- 验证 GitHub API Token 是否有效

### Q4: 找不到工具

**问题**：工具面板为空或缺少某些工具

**解决**：
- 确保 `src/mcp/gitcode_mcp.py` 正确导入了所有工具函数
- 检查 `@mcp.tool()` 装饰器是否正确应用
- 查看终端输出是否有导入错误

## 高级用法

### 使用配置文件

如果 Inspector 支持配置文件，可以创建 `.mcp-inspector.json`：

```json
{
  "server": {
    "command": "python",
      "args": ["src/mcp/gitcode_mcp.py"],
    "env": {
      "GITHUB_TOKEN": "your_token",
      "GITHUB_USERNAME": "your_username"
    }
  }
}
```

### 调试特定工具

如果只想测试特定工具，可以在 Inspector UI 中：
1. 使用过滤器搜索工具
2. 只关注需要测试的工具
3. 保存测试用例供后续使用

## 相关资源

- [MCP Inspector GitHub](https://github.com/modelcontextprotocol/inspector)
- [FastMCP 文档](https://fastmcp.wiki/)
- [MCP 协议规范](https://modelcontextprotocol.io/)

## 总结

MCP Inspector 是调试 MCP 服务器的强大工具。使用以下命令即可开始：

```bash
npx @modelcontextprotocol/inspector python -m src.mcp.gitcode_mcp
```

然后在浏览器中打开显示的 URL，开始调试您的 `gitcode` MCP 服务器！

