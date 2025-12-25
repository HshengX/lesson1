"""
带 GitHub 工具支持的聊天机器人
遵循 OpenAI Function Calling 规范
"""
import os
import json
import asyncio
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI
from github_tools import get_github_tools, call_tool, format_tool_result

# 加载环境变量
load_dotenv()


class ChatBotWithTools:
    """支持 Function Calling 的聊天机器人"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None, model: str = "Qwen/Qwen3-235B-A22B"):
        """
        初始化聊天机器人
        
        Args:
            api_key: API Key，如果不提供则从环境变量 OPENAI_API_KEY 读取
            api_base: API Base URL，如果不提供则从环境变量 OPENAI_API_BASE 读取
            model: 使用的模型名称
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")
        if not self.api_base:
            raise ValueError("请设置 OPENAI_API_BASE 环境变量")
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        self.model = model
        self.conversation_history: List[Dict[str, Any]] = []
        self.tools = get_github_tools()
        
        print(f"[已连接] 服务地址: {self.api_base}")
        print(f"[模型] {self.model}")
        print(f"[已启用] GitHub 工具（{len(self.tools)} 个）")
    
    def chat(self, user_input: str, max_iterations: int = 10) -> str:
        """
        发送消息并获取回复（支持 Function Calling）
        
        Args:
            user_input: 用户输入的消息
            max_iterations: Function Calling 最大迭代次数，默认 10
        
        Returns:
            模型返回的回复内容
        """
        # 将用户消息添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        messages = self.conversation_history.copy()
        iteration = 0
        
        try:
            while iteration < max_iterations:
                iteration += 1
                
                # 调用 API（包含工具定义）
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
                
                if not response.choices or len(response.choices) == 0:
                    return "API 响应格式不正确"
                
                message = response.choices[0].message
                assistant_message = message.content
                tool_calls = message.tool_calls if hasattr(message, 'tool_calls') and message.tool_calls else None
                
                if tool_calls:
                    # 处理工具调用
                    print(f"[工具调用] 检测到 {len(tool_calls)} 个工具调用")
                    
                    # 将助手的工具调用请求添加到对话历史
                    tool_calls_data = [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in tool_calls
                    ]
                    
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message,
                        "tool_calls": tool_calls_data
                    })
                    
                    # 执行所有工具调用
                    tool_messages = []
                    for tool_call in tool_calls:
                        tool_name = tool_call.function.name
                        tool_args_str = tool_call.function.arguments
                        
                        print(f"  - 调用工具: {tool_name}")
                        
                        try:
                            tool_args = json.loads(tool_args_str)
                            
                            # 调用异步工具函数
                            try:
                                loop = asyncio.get_event_loop()
                            except RuntimeError:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                            
                            tool_result = loop.run_until_complete(call_tool(tool_name, tool_args))
                            formatted_result = format_tool_result(tool_name, tool_result)
                            
                            tool_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_name,
                                "content": formatted_result
                            })
                            
                            print(f"    [成功] 工具执行完成")
                            
                        except Exception as e:
                            error_msg = f"工具执行失败: {str(e)}"
                            print(f"    [失败] {error_msg}")
                            tool_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_name,
                                "content": error_msg
                            })
                    
                    # 将工具执行结果添加到对话历史
                    self.conversation_history.extend(tool_messages)
                    
                    # 继续对话，让模型基于工具结果生成回复
                    messages = self.conversation_history.copy()
                    continue
                
                # 没有工具调用，返回最终回复
                if assistant_message is None or assistant_message == "":
                    return "API 返回了空响应"
                
                # 将助手回复添加到对话历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                print(assistant_message)
                return assistant_message
            
            return f"达到最大迭代次数 ({max_iterations})"
            
        except Exception as e:
            error_msg = f"调用 API 时发生错误: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return error_msg
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("对话历史已清空")


def main():
    """主函数"""
    print("=" * 60)
    print("带 GitHub 工具的聊天机器人")
    print("支持 Function Calling")
    print("=" * 60)
    print("提示:")
    print("  - 可以询问 GitHub 仓库信息")
    print("  - 可以查询 Pull Requests")
    print("  - 可以查看 PR 的变更文件")
    print("  - 输入 'quit' 退出")
    print("=" * 50)
    print()
    
    try:
        chatbot = ChatBotWithTools()
        
        while True:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            elif user_input.lower() in ['clear', '清空']:
                chatbot.clear_history()
                continue
            
            print("\n助手: ", end='', flush=True)
            chatbot.chat(user_input)
            
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")


if __name__ == "__main__":
    main()

