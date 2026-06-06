# zhipu_api.py
from zhipuai import ZhipuAI

class ReviewAssistantAPI:
    """
    智谱大模型 API 交互类 (南大地协专属版)
    """
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
        # 换成了更聪明且速度不错的模型
        self.model_name = "glm-4-air" 

    def optimize_chat_history(self, messages: list, max_rounds: int = 5) -> list:
        # 提取系统提示词（里面装了地协的知识库）
        system_msgs = [msg for msg in messages if msg["role"] == "system"]
        chat_msgs = [msg for msg in messages if msg["role"] != "system"]
        
        # 截断历史对话，节省 Token
        limit = max_rounds * 2
        if len(chat_msgs) > limit:
            chat_msgs = chat_msgs[-limit:]
            
        return system_msgs + chat_msgs

    # 这是旧的同步方法 (保留着防止报错)
    def generate_response(self, messages: list) -> dict:
        optimized_messages = self.optimize_chat_history(messages)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=optimized_messages,
                max_tokens=800, 
                temperature=0.5
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

    # zhipu_api.py 里的流式输出函数替换为以下版本

    def generate_stream_response(self, messages: list):
        """
        【高级功能：流式输出 + 实时联网搜索】
        开启 stream=True，并注入 web_search 工具
        """
        optimized_messages = self.optimize_chat_history(messages)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=optimized_messages,
                max_tokens=800, 
                temperature=0.5,
                stream=True,
                # 👇 核心魔法：赐予 AI 联网搜索的能力！ 👇
                tools=[{"type": "web_search", "web_search": {"enable": True, "search_result": True}}]
            )
            return response
        except Exception as e:
            return str(e)