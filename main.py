# main.py
import streamlit as st
import os
import base64
from zhipu_api import ReviewAssistantAPI
from utils import get_association_knowledge_base, ACTIVITY_DATA, ARTICLE_DATA

# ==========================================
# 1. 页面配置 & 🍎 苹果风超炫酷 CSS 动画
# ==========================================
st.markdown("""
<style>
/* 整体背景优化 */
.stApp {
    background: #fbfbfd; /* 苹果官网经典的极浅灰背景 */
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* 进场动画：丝滑上浮淡入 */
@keyframes fadeSlideUp {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* 🍎 苹果风原生卡片设计 */
.apple-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px); /* 毛玻璃特效 */
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
    margin-bottom: 30px;
    /* 核心动画魔法：丝滑回弹曲线 */
    transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
    animation: fadeSlideUp 0.8s ease-out forwards;
}

/* 卡片悬浮特效：整体上浮 + 阴影加深 */
.apple-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

/* 图片容器：用于限制图片溢出并做放大动画 */
.card-img-container {
    width: 100%;
    height: 200px;
    overflow: hidden;
}

.card-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
}

/* 鼠标悬浮时，图片微微放大（极具高级感） */
.apple-card:hover .card-img {
    transform: scale(1.05);
}

/* 卡片文本区排版 */
.card-content {
    padding: 24px 28px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #1d1d1f;
    margin-bottom: 8px;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta {
    font-size: 13px;
    color: #86868b;
    margin-bottom: 16px;
    font-weight: 500;
}

.card-summary {
    font-size: 15px;
    line-height: 1.6;
    color: #515154;
    margin-bottom: 24px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* 🍎 苹果风胶囊按钮 */
.apple-btn {
    display: inline-block;
    background: #0071e3;
    color: white !important;
    padding: 10px 22px;
    border-radius: 980px; /* 经典的胶囊形状 */
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}

.apple-btn:hover {
    background: #0077ed;
    transform: scale(1.03);
}

/* 美化 Streamlit 原生的 Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
}
.stTabs [aria-selected="true"] {
    color: #0071e3 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

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
    st.image("slogan.png", width=240)
    st.title("🎓 创作者版权信息")
    st.info("南京大学 安邦书院\n")
    st.success("\n- 251830038 杨宝鑫\n- 251830056 陈琪睿\n- 251200015 张跃恒")
    st.markdown("---")
    st.markdown("💡 **Tip**: 欢迎体验右侧的 `AI 智能答疑` 模块！它已经学习了本站的所有活动与推文信息。")

# ==========================================
# 4. 主界面：大横幅 (Banner)
# ==========================================
st.markdown("""
<div style="
padding:50px;
border-radius:24px;
background: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80') center/cover;
color:white;
box-shadow: inset 0 0 0 2000px rgba(0, 0, 0, 0.4);
margin-bottom: 30px;
">
<h1 style="font-size: 48px; font-weight: 800; color: white; margin-bottom: 10px;">🌍 南京大学地理协会</h1>
<h3 style="font-weight: 400; color: #f5f5f7;">地理无界 · 世界相连</h3>
<p style="font-size: 18px; color: #d2d2d7; margin-top: 20px;">丈量祖国大地，普及地理科学</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 主界面：四选项卡 (Tabs) 排版设计
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 首页", "🔥 活动通知", "📚 相关推文", "🤖 AI 智能答疑"])

# ----------------- 标签页 1：首页 -----------------
with tab1:
    st.markdown("### ✨ 认识我们：解锁城市的隐藏图层")
    st.info("""
    > *你有没有想过——你每天在玄武湖畔散步，可能正踩过明代黄册库的遗址；你在浦口火车站拍照，镜头里漏掉了整个20世纪的移民史诗；你在钟山的林间走过，可能错过了地层里叠压的六朝古意与近代风云。*
    > 
    > **南京这座城市还有很多图层没被打开。而我们，需要更多一起解锁它的人。**
    """)
    st.divider() 
    st.markdown("#### 一、2025年，我们打开了这些图层")
    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True):
            st.markdown("🌊 **4月 | 玄武湖的折叠时代**\n\n自六朝皇家园林，到明代保存天下户籍的黄册库，再到民国公园。我们找到了江浙沪罕见的藏传佛教寺庙，看懂了武庙闸六百年不倒的水利智慧，在九华山上读懂南京城的轴线设计。")
        with st.container(border=True):
            st.markdown("🚂 **5月 | 津浦铁路与移民史诗**\n\n从朱自清《背影》的浦口火车站出发，穿过铁路轮渡栈桥。我们在龙虎巷的津派建筑群和当地口音里，看见一部写在土地上的工业移民史诗。")
        with st.container(border=True):
            st.markdown("🍁 **10月 | 消失的白下区**\n\n在三条巷、四条巷的地名里打捞往事。我们学会了用街道命名学解码城市，在消失的行政区划中，打捞被城市更新覆盖的旧图层。")
    with col_b:
        with st.container(border=True):
            st.markdown("🔥 **5月末 | 雨花台的精神海拔**\n\n从高座寺的西晋禅意，到烈士陵园的信仰之火。层层历史在此堆叠，如地层般清晰。一片台地，承载的是一座城市的精神海拔。")
        with st.container(border=True):
            st.markdown("🌸 **2026年3月 | 钟山的六朝古意**\n\n从中山植物园的樱花到无梁殿的砖石。草木深处，既有六朝古意，也有近代风云。我们寻的不仅是春色，更是留在山林旧迹间的追怀。")

    st.divider()
    st.markdown("#### 二、山河作为课堂 & 绘制专属地图")
    st.markdown("""
    我们的探索，从来不止于南京。去年端午，我们穿行**苏州**老城，在太湖之畔读懂生态保护；去年盛夏，我们奔赴**宁夏**贺兰山下，在石嘴山洗煤厂追问黑金之城的涅槃。
    不止用脚步丈量，我们还将地理信息转化为可触摸的地图。过去一年，我们绘制了：
    ☕ 《南大仙林咖啡地图》 | 🍂 《南大仙林桂花地图》 | 🌺 《南京市赏花地图》
    """)
    st.divider()
    st.success("""
    #### 👋 现在，我们需要你！
    你可能会问：**我不是地理专业的，能加入吗？**
    **能！** 我们欢迎所有专业、所有年级。地理不是门槛，好奇才是。我们只教你一种方法：**用空间的逻辑理解时间，用土地的肌理解读文明。**
    """)
    st.divider()
    st.markdown("#### 🏢 附录 | 五大核心部门简介")
    with st.expander("🏃‍♂️ 活动部 | 山川未涉，筹画先成"):
        st.write("负责协会活动的策划与执行，是把想法落到现实的一线部门。")
    with st.expander("📸 宣传部 | 山河可观，风物当书"):
        st.write("记录每一次行走与相遇。负责海报设计、公众号推送、摄影摄像与视频剪辑。")
    with st.expander("📖 学术部 | 既可游目，尤宜穷理"):
        st.write("协会“地理味”最浓的部门。负责学术讲座策划、科普材料撰写。")
    with st.expander("🤝 联络部 | 延师问道，会友联群"):
        st.write("负责对内对外的沟通协调，对接老师、嘉宾和合作机构。")
    with st.expander("💼 办公室 | 庶务有经，斯志可久"):
        st.write("负责日常事务、物资准备、财务报销和志愿时长录入。")

# ----------------- 标签页 2：活动通知 -----------------
# ----------------- 标签页 2：活动通知（🍎 苹果风卡片展示） -----------------
with tab2:
    st.markdown("### 🔥 最新活动")
    st.markdown("脚步丈量大地。")
    st.write("") # 留白

    # 获取所有专栏名称
    categories = list(ARTICLE_DATA.keys())
    
    # 🌟 核心魔法 1：在 Tab 3 内部再创建一组子 Tabs！
    sub_tabs = st.tabs(categories)

    # 遍历每个专栏和对应的子标签页
    for tab, category in zip(sub_tabs, categories):
        with tab:
            articles = ARTICLE_DATA[category]
            col1, col2 = st.columns(2, gap="large")

            for i, art in enumerate(articles):
                target_col = col1 if i % 2 == 0 else col2
                with target_col:
                    
                    # 🌟 核心魔法 2：将本地图片转为 Base64，彻底融入 HTML 卡片
                    img_base64 = ""
                    if "cover" in art and os.path.exists(art["cover"]):
                        with open(art["cover"], "rb") as img_file:
                            img_base64 = base64.b64encode(img_file.read()).decode()
                    
                    # 生成图片 HTML 代码（如果没有本地图，放一张炫酷的渐变占位图）
                    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="card-img">' if img_base64 else '<div style="width:100%; height:100%; background: linear-gradient(135deg, #e0eafc, #cfdef3);"></div>'

                    # 渲染带有极其丝滑特效的苹果风卡片
                    st.markdown(f"""
                    <div class="apple-card">
                        <div class="card-img-container">
                            {img_html}
                        </div>
                        <div class="card-content">
                            <div class="card-title">{art['title']}</div>
                            <div class="card-meta">📅 {art['date']} ｜  {art['status']}</div>
                            <div class="card-summary">{art['desc']}</div>
                            <a href="{art['url']}" target="_blank" class="apple-btn">阅读全文 ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------- 标签页 3：推文 (🍎 苹果级子选项卡排版) -----------------
with tab3:
    st.markdown("### 📚 往期精选推文")
    st.markdown("探索我们过去的脚步，发现大地的故事。")
    st.write("") # 留白

    # 获取所有专栏名称
    categories = list(ARTICLE_DATA.keys())
    
    # 🌟 核心魔法 1：在 Tab 3 内部再创建一组子 Tabs！
    sub_tabs = st.tabs(categories)

    # 遍历每个专栏和对应的子标签页
    for tab, category in zip(sub_tabs, categories):
        with tab:
            articles = ARTICLE_DATA[category]
            col1, col2 = st.columns(2, gap="large")

            for i, art in enumerate(articles):
                target_col = col1 if i % 2 == 0 else col2
                with target_col:
                    
                    # 🌟 核心魔法 2：将本地图片转为 Base64，彻底融入 HTML 卡片
                    img_base64 = ""
                    if "cover" in art and os.path.exists(art["cover"]):
                        with open(art["cover"], "rb") as img_file:
                            img_base64 = base64.b64encode(img_file.read()).decode()
                    
                    # 生成图片 HTML 代码（如果没有本地图，放一张炫酷的渐变占位图）
                    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="card-img">' if img_base64 else '<div style="width:100%; height:100%; background: linear-gradient(135deg, #e0eafc, #cfdef3);"></div>'

                    # 渲染带有极其丝滑特效的苹果风卡片
                    st.markdown(f"""
                    <div class="apple-card">
                        <div class="card-img-container">
                            {img_html}
                        </div>
                        <div class="card-content">
                            <div class="card-title">{art['title']}</div>
                            <div class="card-meta">✍️ {art['author']} ｜ 📅 {art['date']}</div>
                            <div class="card-summary">{art['summary']}</div>
                            <a href="{art['url']}" target="_blank" class="apple-btn">阅读全文 ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------- 标签页 4：AI 答疑模块 -----------------
with tab4:
    st.markdown("### 🤖 NJUGA 智能百事通")
    st.markdown("你可以问我：*这周末有活动吗？* 或者 *九州风物的推文有链接吗？*")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "你好！我是南大地协的 AI 小助手，关于协会的任何问题都可以问我哦！🌍"})

    latest_knowledge = get_association_knowledge_base()
    st.session_state.messages = [msg for msg in st.session_state.messages if msg["role"] != "system"]
    st.session_state.messages.insert(0, {"role": "system", "content": latest_knowledge})

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
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