# 基于 ModelScope 的聊天机器人

这是一个遵循 OpenAI API 兼容规范的聊天机器人项目，支持 ModelScope 云端服务或其他兼容 OpenAI API 的服务。

## 功能特性

- ✅ 支持 ModelScope 云端服务或其他兼容 OpenAI API 的服务
- ✅ 遵循 OpenAI API 兼容规范
- ✅ 支持对话历史记录
- ✅ 支持流式输出和非流式输出
- ✅ 交互式命令行界面
- ✅ 可编程 API，方便集成到其他项目

## 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install openai python-dotenv
```

## 配置

### 必需配置

项目**必须**配置以下环境变量才能运行：

创建 `.env` 文件（在项目根目录）：

```env
# 必需：API Key
OPENAI_API_KEY=your_api_key_here

# 必需：API Base URL（服务地址）
OPENAI_API_BASE=https://api.modelscope.cn/v1
```

### 配置示例

#### 示例 1: ModelScope 云端服务

```env
# ModelScope 云端 API Key（从 ModelScope 控制台获取）
OPENAI_API_KEY=your_modelscope_api_key

# ModelScope 云端服务地址
OPENAI_API_BASE=https://api.modelscope.cn/v1
```

#### 示例 2: 其他兼容服务（如 OpenAI 官方）

```env
# OpenAI API Key
OPENAI_API_KEY=sk-...

# OpenAI 官方服务地址（如果不设置，OpenAI 客户端会使用默认地址）
# OPENAI_API_BASE=https://api.openai.com/v1
```

#### 示例 3: 本地部署的服务

```env
# 本地服务可能不需要真实的 API Key，但需要设置一个值
OPENAI_API_KEY=EMPTY

# 本地服务地址
OPENAI_API_BASE=http://localhost:8000/v1
```

#### 示例 4: 自定义兼容服务

```env
# 自定义服务的 API Key
OPENAI_API_KEY=your_custom_api_key

# 自定义服务的地址
OPENAI_API_BASE=https://your-custom-api-endpoint.com/v1
```

**重要提示**：
- `OPENAI_API_KEY` 和 `OPENAI_API_BASE` 都是**必需**的配置项
- 如果不配置，程序启动时会提示错误并说明如何配置
- 根据你使用的服务类型，配置相应的 API Key 和地址

## 使用方法

### 方式一：交互式聊天界面

```bash
# 使用 uv run（推荐）
uv run python chatbot.py

# 或直接使用 python
python chatbot.py
```

在交互界面中：
- 直接输入消息与机器人对话
- 输入 `quit` 或 `exit` 退出
- 输入 `clear` 清空对话历史
- 输入 `history` 查看对话历史
- 输入 `stream` 切换流式输出模式
- 输入 `model <模型名>` 切换模型（如：`model qwen`）

### 方式二：在代码中使用

```python
from chatbot import ChatBot

# 方式 1: 从 .env 文件读取配置（推荐）
chatbot = ChatBot()

# 方式 2: 手动传入配置
chatbot = ChatBot(
    api_key="your_api_key",
    api_base="https://api.modelscope.cn/v1",
    model="qwen"  # 可选，默认模型
)

# 发送消息
response = chatbot.chat("你好，介绍一下你自己")
print(response)

# 继续对话（会自动保留历史）
response = chatbot.chat("刚才你说的是什么？")
print(response)

# 清空对话历史
chatbot.clear_history()

# 切换模型
chatbot.set_model("qwen2")

# 使用流式输出
chatbot.chat("写一首关于春天的诗", stream=True)
```

## 支持的模型和服务

### ModelScope 云端服务

支持 ModelScope 提供的各种模型，包括：
- **Qwen 系列**：`qwen`、`qwen2`、`qwen-turbo` 等
- **通义千问系列**：`Qwen/Qwen2-7B-Instruct`、`Qwen/Qwen2-14B-Instruct` 等
- 更多模型请访问 [ModelScope 模型库](https://modelscope.cn/models)

### 其他兼容服务

支持所有遵循 OpenAI API 规范的服务，包括：
- OpenAI 官方服务
- 本地部署的服务（如 vLLM、Ollama 等）
- 其他云服务商的兼容 API

## 项目结构

```
lesson1/
├── chatbot.py          # 聊天机器人主程序
├── main.py             # 项目入口文件
├── pyproject.toml      # 项目配置和依赖
├── README.md           # 项目说明文档
└── .env                # 环境变量文件（必需，需要自己创建）
```

## 常见问题

### 1. 配置错误

**问题**：提示 "请设置 OPENAI_API_KEY" 或 "请设置 OPENAI_API_BASE"

**解决方案**：
- 确保在项目根目录创建了 `.env` 文件
- 确保 `.env` 文件中包含了 `OPENAI_API_KEY` 和 `OPENAI_API_BASE`
- 检查配置值是否正确（没有多余的空格）

### 2. 连接失败

**问题**：提示连接错误或超时

**解决方案**：
- 检查 `OPENAI_API_BASE` 地址是否正确
- 检查网络连接是否正常
- 如果是本地服务，确认服务正在运行
- 检查 API Key 是否有效

### 3. 模型不存在

**问题**：提示模型不存在或无法找到

**解决方案**：
- 确认模型名称是否正确
- 检查该模型是否在你使用的服务中可用
- 可以通过 API 查看可用模型列表

### 4. API Key 无效

**问题**：提示 API Key 无效

**解决方案**：
- 检查 API Key 是否正确
- 确认 API Key 是否已过期
- 如果是 ModelScope，请从控制台重新获取 API Key

## 获取 API Key

### ModelScope

1. 访问 [ModelScope 控制台](https://www.modelscope.cn/)
2. 注册/登录账号
3. 在控制台中创建 API Key
4. 将 API Key 配置到 `.env` 文件中

### 其他服务

根据你使用的服务提供商，按照其文档获取 API Key。

## 注意事项

- 请妥善保管你的 API Key，不要提交到版本控制系统
- `.env` 文件已添加到 `.gitignore` 中，不会被提交
- 使用 API 可能会产生费用，请注意控制使用量
- 确保你的服务完全兼容 OpenAI API 格式

## 相关资源

- [ModelScope 官网](https://www.modelscope.cn/)
- [ModelScope 模型库](https://modelscope.cn/models)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)

## 许可证

MIT License
