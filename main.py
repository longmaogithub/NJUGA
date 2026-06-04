# main.py
import streamlit as st
import os
from zhipu_api import ReviewAssistantAPI
from utils import get_association_knowledge_base, ACTIVITY_DATA, ARTICLE_DATA

# ==========================================
# 1. 页面配置 
# ==========================================
st.set_page_config(
    page_title="南京大学地理协会",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# 2. 动态密钥加载与 AI 实例化
# ==========================================
ZHIPU_API_KEY = None
try:
    ZHIPU_API_KEY = st.secrets["MY_ZHIPU_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    ZHIPU_API_KEY = os.getenv("MY_ZHIPU_KEY")

if not ZHIPU_API_KEY:
    st.error("🚨 找不到 API Key！")
    st.stop()

api_client = ReviewAssistantAPI(api_key=ZHIPU_API_KEY)

# ==========================================
# 3. 侧边栏：版权信息 & 导航提示
# ==========================================
with st.sidebar:
    # 只要图片和 main.py 放在同一个文件夹里，直接写名字就行！
    st.image("slogan.png", width=240)
    st.title("🎓 创作者版权信息")
    st.info("南京大学 安邦书院\n")
    st.success("\n- 251830038 杨宝鑫\n- 251830056 陈琪睿\n- 251200015 张跃恒")
    st.markdown("---")
    st.markdown("💡 **Tip**: 欢迎体验右侧的 `AI 智能答疑` 模块！它已经学习了本站的所有活动与推文信息。")

# ==========================================
# 4. 主界面：三选项卡 (Tabs) 排版设计
# ==========================================
st.title("南京大学地理协会")
st.markdown("地理无界 世界相连")

# ==========================================
# 4. 主界面：四选项卡 (Tabs) 排版设计
# ==========================================
# 把原本的 3 个 tab 升级为 4 个
tab1, tab2, tab3, tab4 = st.tabs(["🏠 首页", "🔥 活动通知", "📚 相关推文", "🤖 AI 智能答疑"])

# ----------------- 标签页 1：首页 -----------------
with tab1:
    st.header("✨ 认识我们")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **南京大学地理协会 (NJUGA)** 成立于上世纪90年代，是全校规模最大、最活跃的学术实践类社团之一。
        我们致力于将课本上的地理知识带向户外，无论是**紫金山地貌考察**、**星空摄影**，还是**GIS技术沙龙**，
        在这里，你都能找到志同道合的“地理人”。
        """)
        st.info("📢 招新季即将来临，请密切关注我们的微信公众号：『南大地协』")
    with col2:
        # 放一张地质/风景相关的占位图，提升逼格
        st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80", caption="用脚步丈量大地", use_column_width=True)

# ----------------- 标签页 2：活动通知 -----------------
with tab2:
    st.header("🔥 最新活动")
    # 动态渲染字典里的活动数据
    for act in ACTIVITY_DATA:
        with st.expander(f"{act['title']} (状态: {act['status']})"):
            st.write(f"**⏰ 时间**：{act['date']}")
            st.write(f"**📍 详情**：{act['desc']}")
            if act['status'] == "报名中":
                st.button("🔗 点击前往报名表单", key=act['title']) 

# ----------------- 标签页 3：相关推文 (你的新需求) -----------------
with tab3:
    st.header("📚 往期精选推文")
    # 我在这里给你加了一个外边框 (border=True)，让推文看起来像一张张卡片，更美观！
    for art in ARTICLE_DATA:
        with st.container(border=True):
            st.markdown(f"#### {art['title']}")
            st.caption(f"✍️ 作者: {art['author']}")
            st.write(art['summary'])
            # 增加一个模拟的阅读按钮
            st.button("📖 阅读原文", key=art['title']+"_btn")

# ----------------- 标签页 4：AI 答疑模块 -----------------
with tab4:
    st.header("🤖 NJUGA 智能百事通")
    st.markdown("你可以问我：*这周末有活动吗？* 或者 *你们怎么教 GIS？*")
    
    # 注入知识库作为 System Prompt
    if "messages" not in st.session_state:
        knowledge_base = get_association_knowledge_base()
        st.session_state.messages = [{"role": "system", "content": knowledge_base}]
        st.session_state.messages.append({"role": "assistant", "content": "你好！我是南大地协的 AI 小助手，关于协会的任何问题都可以问我哦！🌍"})

    # 渲染聊天记录
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # 处理聊天输入 (保留了之前的高级流式打字机效果)
    if user_input := st.chat_input("输入关于地协的问题..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            stream_response = api_client.generate_stream_response(st.session_state.messages)
            
            if isinstance(stream_response, str):
                st.error(f"网络异常: {stream_response}")
            else:
                def stream_generator():
                    for chunk in stream_response:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                
                full_answer = st.write_stream(stream_generator())
                st.session_state.messages.append({"role": "assistant", "content": full_answer})