"""诊断脚本：检查配置和连接"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("=" * 60)
print("配置诊断")
print("=" * 60)

# 检查环境变量
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
model = "Qwen/Qwen3-235B-A22B"

print(f"\n1. 环境变量检查:")
print(f"   OPENAI_API_KEY: {'已设置' if api_key else '未设置'}")
if api_key:
    print(f"   API Key 长度: {len(api_key)} 字符")
    print(f"   API Key 前10字符: {api_key[:10]}...")
print(f"   OPENAI_API_BASE: {api_base}")
print(f"   模型名称: {model}")

if not api_key or not api_base:
    print("\n错误: 缺少必需的配置！")
    print("请在 .env 文件中设置 OPENAI_API_KEY 和 OPENAI_API_BASE")
    exit(1)

# 测试连接
print(f"\n2. 测试 API 连接...")
try:
    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )
    
    # 尝试列出模型
    print("   尝试列出可用模型...")
    models = client.models.list()
    print(f"   成功！找到 {len(list(models.data))} 个模型")
    
    # 尝试发送一个简单的请求
    print("\n3. 测试聊天请求...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "你好"}],
        max_tokens=50
    )
    
    if response.choices and len(response.choices) > 0:
        content = response.choices[0].message.content
        print(f"   成功！收到响应: {content[:50]}...")
    else:
        print("   警告: API 返回了响应，但没有内容")
        print(f"   响应对象: {response}")
        
except Exception as e:
    print(f"   错误: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

