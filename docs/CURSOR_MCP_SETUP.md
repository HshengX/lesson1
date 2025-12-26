# Cursor MCP 配置指南

本指南将帮助您将 `gitcode` MCP 服务器配置到 Cursor IDE 中。

## 方法 1: 使用自动配置脚本（推荐）

### Windows (PowerShell)

```powershell
# 在项目根目录运行
.\setup_cursor_mcp.ps1
```

### Linux/macOS (Bash)

```bash
# 在项目根目录运行
chmod +x setup_cursor_mcp.sh
./setup_cursor_mcp.sh
```

## 方法 2: 手动配置

### 步骤 1: 找到 Cursor 配置目录

- **Windows**: `%APPDATA%\Cursor\User\mcp.json`
  - 完整路径通常是: `C:\Users\你的用户名\AppData\Roaming\Cursor\User\mcp.json`
- **Linux**: `~/.config/Cursor/User/mcp.json`
- **macOS**: `~/Library/Application Support/Cursor/User/mcp.json`

### 步骤 2: 创建或编辑配置文件

创建或编辑 `mcp.json` 文件，添加以下内容：

```json
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": [
        "D:\\ai\\aiproject\\gf-aiproject\\gfMcpCourse\\lesson1\\src\\mcp\\gitcode_mcp.py"
      ],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here",
        "GITHUB_USERNAME": "your_username_here"
      }
    }
  }
}
```

**重要提示：**
- 将 `D:\\ai\\aiproject\\gf-aiproject\\gfMcpCourse\\lesson1\\src\\mcp\\gitcode_mcp.py` 替换为您的实际项目路径
- 在 Windows 中，路径中的反斜杠需要转义为 `\\`
- 或者使用正斜杠 `/`（Python 也支持）

### 步骤 3: 配置环境变量（可选）

您可以选择在配置文件中设置环境变量，或者使用系统环境变量：

**选项 A: 在配置文件中设置**
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

**选项 B: 使用系统环境变量**
```json
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": ["path/to/gitcode_mcp.py"]
    }
  }
}
```
然后在系统环境变量或 `.env` 文件中设置 `GITHUB_TOKEN` 和 `GITHUB_USERNAME`。

### 步骤 4: 重启 Cursor

配置完成后，重启 Cursor IDE 以使配置生效。

## 验证配置

1. 打开 Cursor
2. 打开命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）
3. 搜索 "MCP" 或查看设置中的 MCP 服务器列表
4. 确认 `gitcode` 服务器显示为已连接状态

## 使用 MCP 工具

配置成功后，您可以在 Cursor 中使用以下工具：

- `search_repository` - 搜索 GitHub 仓库
- `get_pull_requests` - 获取仓库的 Pull Requests
- `get_pull_request_files` - 获取 PR 的变更文件
- `get_commits` - 获取仓库的提交历史

## 故障排除

### 问题 1: MCP 服务器未显示

- 检查配置文件路径是否正确
- 检查 JSON 格式是否正确（可以使用 JSON 验证器）
- 确保 Python 可执行文件在系统 PATH 中

### 问题 2: 工具调用失败

- 检查 `src/mcp/gitcode_mcp.py` 文件路径是否正确
- 检查 Python 环境是否安装了 `fastmcp` 依赖
- 查看 Cursor 的开发者工具控制台是否有错误信息

### 问题 3: GitHub API 调用失败

- 检查 `GITHUB_TOKEN` 是否正确设置
- 检查网络连接
- 查看 `server.py` 中的错误处理逻辑

## 项目级配置（可选）

如果您希望仅在当前项目中使用 MCP 服务器，可以在项目根目录创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": ["gitcode_mcp.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}",
        "GITHUB_USERNAME": "${env:GITHUB_USERNAME}"
      }
    }
  }
}
```

注意：项目级配置的优先级高于全局配置。

## 相关文件

- `src/mcp/gitcode_mcp.py` - MCP 服务器实现
- `src/github/server.py` - GitHub API 客户端
- `MCP_SERVER_README.md` - MCP 服务器详细文档

