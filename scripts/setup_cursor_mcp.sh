#!/bin/bash
# Cursor MCP 配置脚本 (Bash)
# 将 gitcode MCP 服务器配置添加到 Cursor

CURSOR_CONFIG_DIR="$HOME/.config/Cursor/User"
MCP_CONFIG_FILE="$CURSOR_CONFIG_DIR/mcp.json"
PROJECT_PATH="$(pwd)"
GITCODE_SCRIPT="$PROJECT_PATH/src/mcp/gitcode_mcp.py"

# 创建配置目录（如果不存在）
mkdir -p "$CURSOR_CONFIG_DIR"
echo "配置目录: $CURSOR_CONFIG_DIR"

# 读取现有配置（如果存在）
if [ -f "$MCP_CONFIG_FILE" ]; then
    echo "已读取现有 MCP 配置"
    CONFIG=$(cat "$MCP_CONFIG_FILE")
else
    echo "创建新配置"
    CONFIG='{"mcpServers":{}}'
fi

# 使用 jq 添加或更新 gitcode 配置（如果安装了 jq）
if command -v jq &> /dev/null; then
    CONFIG=$(echo "$CONFIG" | jq --arg cmd "python" \
        --arg script "$GITCODE_SCRIPT" \
        '.mcpServers.gitcode = {
            command: $cmd,
            args: [$script],
            env: {
                GITHUB_TOKEN: "",
                GITHUB_USERNAME: ""
            }
        }')
    
    echo "$CONFIG" | jq . > "$MCP_CONFIG_FILE"
    echo "MCP 配置已保存到: $MCP_CONFIG_FILE"
    echo ""
    echo "配置内容:"
    cat "$MCP_CONFIG_FILE"
else
    # 如果没有 jq，创建基本配置
    cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "gitcode": {
      "command": "python",
      "args": [
        "$GITCODE_SCRIPT"
      ],
      "env": {
        "GITHUB_TOKEN": "",
        "GITHUB_USERNAME": ""
      }
    }
  }
}
EOF
    echo "MCP 配置已保存到: $MCP_CONFIG_FILE"
    echo ""
    echo "配置内容:"
    cat "$MCP_CONFIG_FILE"
fi

echo ""
echo "请编辑配置文件，填入 GITHUB_TOKEN 和 GITHUB_USERNAME（如果需要在配置文件中设置）"
echo "或者确保环境变量已设置。"
echo ""
echo "配置完成后，请重启 Cursor 以使配置生效。"

