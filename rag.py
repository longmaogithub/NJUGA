import os
import pdfplumber
from typing import List, Tuple
import streamlit as st

# 核心组件：从 langchain 核心包导入
from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore[import]  # [reference:5][reference:6]
from langchain.embeddings.base import Embeddings  # [reference:7]

# 社区包：用于加载需要外部依赖的组件
# HuggingFaceEmbeddings 属于社区集成，从 langchain_community 导入
from langchain_community.embeddings import HuggingFaceEmbeddings  # [reference:8]
from langchain_community.vectorstores import Chroma


class PDFKnowledgeBase:
    """
    PDF 知识库管理类：加载 PDF、分块、向量化、持久化存储与检索
    """

    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = knowledge_dir
        self.vectorstore = None
        self.persist_dir = "./vector_store"
        self.embeddings = None
        self.embedding_model_name = "BAAI/bge-m3"

    def _init_embeddings(self):
        """初始化 Embedding 模型（使用 HuggingFace 本地模型）"""
        with st.spinner("正在加载 Embedding 模型，首次运行需要下载...请稍候"):
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
        return self.embeddings

    def _extract_pdf_text(self, pdf_path: str) -> str:
        """提取单个 PDF 文件中的文本"""
        if not os.path.exists(pdf_path):
            return ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"PDF 解析失败 {pdf_path}: {e}")
            return ""

    def _get_all_pdf_texts(self) -> List[Tuple[str, str]]:
        """获取 knowledge_dir 下所有 PDF 的 (文件名, 文本内容)"""
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            return []

        pdf_files = [
            f for f in os.listdir(self.knowledge_dir) if f.lower().endswith(".pdf")
        ]
        results = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.knowledge_dir, pdf_file)
            text = self._extract_pdf_text(pdf_path)
            if text:
                results.append((pdf_file, text))
        return results

    @st.cache_resource(ttl=3600)
    def _build_vectorstore():
        """构建并持久化向量存储"""
        pass

    def build_vectorstore(self, force_rebuild: bool = False):
        """
        构建向量数据库（带缓存，自动跳过已构建）
        :param force_rebuild: 是否强制重建（当 PDF 文件更新时设为 True）
        """
        # 1. 初始化 Embedding 模型
        self._init_embeddings()

        # 2. 检查是否已有持久化存储且无需重建
        if not force_rebuild and os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
            )
            return

        # 3. 获取所有 PDF 文本
        pdf_texts = self._get_all_pdf_texts()
        if not pdf_texts:
            return

        # 4. 文本分块
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
        )

        all_chunks = []
        for pdf_name, text in pdf_texts:
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                # 添加元数据，便于溯源
                all_chunks.append(
                    (chunk, {"source": pdf_name, "chunk_length": len(chunk)})
                )

        if not all_chunks:
            return

        # 5. 构建向量存储并持久化
        texts, metadatas = zip(*all_chunks) if all_chunks else ([], [])
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=list(metadatas),
            persist_directory=self.persist_dir,
        )
        self.vectorstore.persist()

    def retrieve_relevant_chunks(self, query: str, k: int = 4) -> str:
        """根据用户问题检索最相关的知识块，返回拼接的文本上下文"""
        if self.vectorstore is None:
            return ""

        docs = self.vectorstore.similarity_search_with_score(query, k=k)
        if not docs:
            return ""

        context_parts = []
        for doc, score in docs:
            source = doc.metadata.get("source", "未知来源")
            # 只保留相关性较高的结果
            if score < 1.2:
                context_parts.append(f"【来源：{source}】\n{doc.page_content}")

        return "\n\n---\n\n".join(context_parts)

    def get_retriever(self):
        """返回检索器对象，用于 LangChain 兼容"""
        if self.vectorstore is None:
            self.build_vectorstore()
        return self.vectorstore.as_retriever(search_kwargs={"k": 4})