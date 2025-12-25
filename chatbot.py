"""
基于 ModelScope 的聊天机器人
遵循 OpenAI API 兼容规范，支持 ModelScope 云端服务或其他兼容服务
"""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()


class ChatBot:
    """基于 ModelScope 的聊天机器人类（遵循 OpenAI API 兼容规范）"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None, model: str = "Qwen/Qwen3-235B-A22B"):
        """
        初始化聊天机器人（基于 ModelScope 或其他兼容 OpenAI API 的服务）
        
        Args:
            api_key: API Key，如果不提供则从环境变量 OPENAI_API_KEY 读取（必需）
            api_base: API Base URL，如果不提供则从环境变量 OPENAI_API_BASE 读取（必需）
            model: 使用的模型名称，默认为 qwen
        """
        # 从环境变量或参数获取 API Key（必需）
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "请设置 OPENAI_API_KEY 环境变量（在 .env 文件中），或在初始化时传入 api_key 参数。\n"
                "示例：在 .env 文件中添加 OPENAI_API_KEY=your_api_key_here"
            )
        
        # 从环境变量或参数获取 API Base URL（必需）
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")
        if not self.api_base:
            raise ValueError(
                "请设置 OPENAI_API_BASE 环境变量（在 .env 文件中），或在初始化时传入 api_base 参数。\n"
                "示例：在 .env 文件中添加 OPENAI_API_BASE=https://api.modelscope.cn/v1"
            )
        
        # 初始化 OpenAI 兼容客户端
        # ModelScope 和其他兼容服务遵循 OpenAI API 规范，可以直接使用 OpenAI 客户端
        client_kwargs = {
            "api_key": self.api_key,
            "base_url": self.api_base
        }
        
        self.client = OpenAI(**client_kwargs)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
        # 显示连接信息
        print(f"[已连接] 服务地址: {self.api_base}")
        print(f"[模型] {self.model}")
    
    def chat(self, user_input: str, stream: bool = False) -> str:
        """
        发送消息并获取回复
        
        Args:
            user_input: 用户输入的消息
            stream: 是否使用流式输出，默认为 False
        
        Returns:
            模型返回的回复内容
        """
        # 将用户消息添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # 构建消息列表（包含历史对话）
        messages = self.conversation_history.copy()
        
        try:
            if stream:
                # 流式输出（兼容 OpenAI API 规范）
                stream_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True
                )
                
                full_response = ""
                chunk_count = 0
                for chunk in stream_response:
                    chunk_count += 1
                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if delta and delta.content is not None:
                            content = delta.content
                            full_response += content
                            try:
                                print(content, end='', flush=True)
                            except UnicodeEncodeError:
                                # Windows 控制台编码问题，使用安全编码方式
                                import sys
                                safe_content = content.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8', errors='replace')
                                print(safe_content, end='', flush=True)
                
                print()  # 换行
                
                # 检查是否收到任何响应
                if not full_response:
                    error_msg = f"流式输出未收到任何内容（收到 {chunk_count} 个 chunk）"
                    print(error_msg)
                    if chunk_count == 0:
                        print("提示: 可能 API 调用失败或服务未响应")
                    return error_msg
                
                # 将助手回复添加到对话历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                
                return full_response
            else:
                # 非流式输出（兼容 OpenAI API 规范）
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                # 调试：打印响应结构
                # print(f"调试: response type = {type(response)}")
                # print(f"调试: response = {response}")
                
                # 兼容性处理：确保响应格式正确
                if response.choices and len(response.choices) > 0:
                    assistant_message = response.choices[0].message.content
                    
                    # 检查响应内容是否为空
                    if assistant_message is None or assistant_message == "":
                        error_msg = "API 返回了空响应"
                        print(error_msg)
                        print(f"调试信息: response.choices[0] = {response.choices[0]}")
                        print(f"调试信息: response.choices[0].message = {response.choices[0].message}")
                        return error_msg
                    
                    # 将助手回复添加到对话历史
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    
                    # 非流式模式下，打印响应内容（处理 Windows 控制台编码问题）
                    try:
                        print(assistant_message)
                    except UnicodeEncodeError:
                        # Windows 控制台编码问题，使用安全编码方式
                        import sys
                        safe_message = assistant_message.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8', errors='replace')
                        print(safe_message)
                    
                    return assistant_message
                else:
                    error_msg = "API 响应格式不正确：未找到 choices"
                    print(error_msg)
                    print(f"调试信息: response type = {type(response)}")
                    print(f"调试信息: response = {response}")
                    if hasattr(response, 'choices'):
                        print(f"调试信息: response.choices = {response.choices}")
                    return error_msg
                    
        except Exception as e:
            error_msg = f"调用 API 时发生错误: {str(e)}"
            print(error_msg)
            # 打印详细的错误信息
            import traceback
            print(f"\n详细错误信息:")
            traceback.print_exc()
            # 提供错误提示
            print(f"\n提示: 请检查以下配置")
            print(f"  服务地址: {self.api_base}")
            print(f"  API Key: {'已设置' if self.api_key else '未设置'}")
            print(f"  模型名称: {self.model}")
            if "localhost" in self.api_base or "127.0.0.1" in self.api_base:
                print(f"  如果是本地服务，请确保服务正在运行")
            return error_msg
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("对话历史已清空")
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        获取对话历史
        
        Returns:
            对话历史列表
        """
        return self.conversation_history.copy()
    
    def set_model(self, model: str):
        """
        设置使用的模型
        
        Args:
            model: 模型名称
        """
        self.model = model
        print(f"模型已切换为: {model}")


def main():
    """主函数 - 交互式聊天界面"""
    print("=" * 60)
    print("基于 ModelScope 的聊天机器人")
    print("遵循 OpenAI API 兼容规范")
    print("=" * 60)
    print("提示:")
    print("  - 输入消息后按回车发送")
    print("  - 输入 'quit' 或 'exit' 退出")
    print("  - 输入 'clear' 清空对话历史")
    print("  - 输入 'history' 查看对话历史")
    print("  - 输入 'stream' 切换流式输出模式")
    print("  - 输入 'model' 切换模型")
    print("=" * 50)
    print()
    
    try:
        # 初始化聊天机器人
        chatbot = ChatBot()
        stream_mode = False
        
        while True:
            # 获取用户输入
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            # 处理特殊命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            elif user_input.lower() in ['clear', '清空']:
                chatbot.clear_history()
                continue
            elif user_input.lower() in ['history', '历史']:
                history = chatbot.get_history()
                if history:
                    print("\n对话历史:")
                    for msg in history:
                        role = "用户" if msg["role"] == "user" else "助手"
                        print(f"  {role}: {msg['content']}")
                else:
                    print("对话历史为空")
                continue
            elif user_input.lower() in ['stream', '流式']:
                stream_mode = not stream_mode
                print(f"流式输出模式: {'开启' if stream_mode else '关闭'}")
                continue
            elif user_input.lower().startswith('model '):
                new_model = user_input[6:].strip()
                if new_model:
                    chatbot.set_model(new_model)
                else:
                    print(f"当前模型: {chatbot.model}")
                continue
            
            # 发送消息并获取回复
            print("\n助手: ", end='', flush=True)
            try:
                response = chatbot.chat(user_input, stream=stream_mode)
                # 非流式模式下，如果 chat 方法返回了内容，确保显示
                if not stream_mode and response:
                    # 如果返回的不是错误消息，说明已经在 chat 方法中打印了
                    # 如果返回的是错误消息，需要额外处理
                    if response.startswith("调用 API 时发生错误") or response.startswith("API"):
                        print(response)  # 确保错误信息显示
                elif stream_mode:
                    # 流式模式下，内容已经在 chat 方法中实时打印了
                    pass
            except Exception as e:
                print(f"\n发生未预期的错误: {str(e)}")
                import traceback
                traceback.print_exc()
            
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")


if __name__ == "__main__":
    main()
