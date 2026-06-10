# zhipu_api.py
from zhipuai import ZhipuAI

class ReviewAssistantAPI:
    """
    智谱大模型 API 交互类 (南大地协专属版)
    """
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
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


from zhipuai import ZhipuAI
from rag import PDFKnowledgeBase
import streamlit as st

class ReviewAssistantAPI:
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
        self.model_name = "glm-4-flash"  # 推荐免费版本
        self.kb = PDFKnowledgeBase()

    def optimize_chat_history(self, messages: list, max_rounds: int = 5) -> list:
        system_msgs = [msg for msg in messages if msg["role"] == "system"]
        chat_msgs = [msg for msg in messages if msg["role"] != "system"]
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

    def generate_stream_response(self, messages: list, use_rag: bool = True):
        """
        RAG 增强的流式输出
        :param messages: 原始对话消息列表
        :param use_rag: 是否启用知识库检索
        """
        # 1. 提取用户最新问题
        user_query = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_query = msg.get("content", "")
                break

        # 2. 检索相关知识（RAG 核心）
        context = ""
        if use_rag and user_query:
            with st.spinner("🔍 正在检索知识库..."):
                # 先构建向量库（缓存机制，不会重复构建）
                self.kb.build_vectorstore()
                context = self.kb.retrieve_relevant_chunks(user_query, k=4)

        # 3. 构建增强后的消息列表
        enhanced_messages = []
        for msg in messages:
            if msg["role"] == "system":
                # 在系统提示词中追加知识库上下文
                new_content = msg["content"]
                if context:
                    new_content += f"\n\n【补充知识库内容（来自上传的 PDF 文档）】\n{context}\n\n请优先使用上述补充内容回答用户问题，若补充内容中找不到答案，再结合你原有的知识回答。"
                enhanced_messages.append({"role": "system", "content": new_content})
            else:
                enhanced_messages.append(msg)

        optimized_messages = self.optimize_chat_history(enhanced_messages)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=optimized_messages,
                max_tokens=800,
                temperature=0.5,
                stream=True,
                tools=[{"type": "web_search", "web_search": {"enable": True, "search_result": True}}]
            )
            return response
        except Exception as e:
            return str(e)