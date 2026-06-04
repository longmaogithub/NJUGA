# zhipu_api.py
from zhipuai import ZhipuAI

class ReviewAssistantAPI:
    """
    智谱大模型 API 交互类
    """
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
        self.model_name = "glm-4-flash" 

    def optimize_chat_history(self, messages: list, max_rounds: int = 5) -> list:
        # 提取系统提示词（里面装了地协的知识库）
        system_msgs = [msg for msg in messages if msg["role"] == "system"]
        chat_msgs = [msg for msg in messages if msg["role"] != "system"]
        
        # 截断历史对话，节省 Token
        limit = max_rounds * 2
        if len(chat_msgs) > limit:
            chat_msgs = chat_msgs[-limit:]
            
        return system_msgs + chat_msgs

    def generate_response(self, messages: list) -> dict:
        optimized_messages = self.optimize_chat_history(messages)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=optimized_messages,
                max_tokens=800, 
                temperature=0.5  # 降低随机性，让客服回答更准确严谨
            )
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "tokens": response.usage.total_tokens,
                "error_msg": ""
            }
        except Exception as e:
            return {
                "success": False,
                "content": "",
                "tokens": 0,
                "error_msg": f"接口调用失败: {str(e)}"
            }
    
    def generate_stream_response(self, messages: list):
        """
        【高级功能：流式输出】
        开启 stream=True，让 AI 像打字机一样一个字一个字返回
        """
        optimized_messages = self.optimize_chat_history(messages)
        try:
            # 注意这里多了一个 stream=True 参数
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=optimized_messages,
                max_tokens=800, 
                temperature=0.5,
                stream=True  # <--- 核心魔法在这里
            )
            return response # 返回的是一个数据流对象
        except Exception as e:
            return str(e) # 报错时返回字符串