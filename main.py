# main.py
import streamlit as st
import os
import base64
from zhipu_api import ReviewAssistantAPI
from utils import get_association_knowledge_base, ACTIVITY_DATA, ARTICLE_DATA


# ==========================================
# 0. 全局缓存：图片转 Base64（放在最前面，以便后续使用）
# ==========================================
@st.cache_data
def get_image_base64(image_path: str) -> str:
    """读取本地图片并返回 Base64 字符串，若文件不存在返回空字符串"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ==========================================
# 1. 页面配置 & CSS 
# ==========================================
st.markdown("""
<style>
       /* 添加到你的 <style> 标签内部 */

/* 1. 隐藏左上角的侧边栏展开按钮 */
[data-testid="collapsedControl"] {
    display: none;
}

/* 2. 拓宽主界面内容区，减少上下左右的无用白边 */
.block-container {
    padding-top: 2rem !important; /* 减少顶部的多余留白 */
    padding-bottom: 2rem !important;
    max-width: 85% !important;    /* 核心魔法：让内容占据屏幕的 85%，瞬间宽敞！ */
}     
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

/* 苹果风原生卡片设计 */
.apple-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px); /* 毛玻璃特效 */
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
    margin-bottom: 30px;
    /* 丝滑回弹曲线 */
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

/* 鼠标悬浮时，图片微微放大 */
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

/* 苹果风胶囊按钮 */
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


st.markdown("""
<style>

/* ==========================
   Vision Pro 毛玻璃设计系统
   ========================== */

.glass-card{
    background: rgba(255,255,255,0.22);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);

    border: 1px solid rgba(255,255,255,0.25);

    border-radius: 28px;

    box-shadow:
    0 8px 32px rgba(31,38,135,0.12);

    transition: all .4s ease;
}

.glass-card:hover{
    transform: translateY(-6px);

    box-shadow:
    0 18px 45px rgba(31,38,135,0.18);
}


/* ==========================
   Hero
   ========================== */

.hero-box{
    position:relative;

    overflow:hidden;

    background:
    url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2000");

    background-size:cover;
    background-position:center;

    border-radius:36px;

    padding:90px 60px;

    margin-bottom:50px;
}

.hero-overlay{
    display:inline-block;

    background:rgba(255,255,255,0.15);

    backdrop-filter:blur(24px);
    -webkit-backdrop-filter:blur(24px);

    border:1px solid rgba(255,255,255,0.25);

    border-radius:28px;

    padding:40px;
}

.hero-title{
    font-size:64px;
    font-weight:800;
    color:white;
    margin-bottom:10px;
}

.hero-sub{
    font-size:24px;
    color:white;
    opacity:0.95;
}


/* ==========================
   统计卡
   ========================== */

.stat-card{
    background:rgba(255,255,255,0.25);

    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);

    border-radius:24px;

    border:1px solid rgba(255,255,255,0.25);

    padding:30px;

    text-align:center;

    transition:.3s;
}

.stat-card:hover{
    transform:translateY(-4px);
}

.stat-number{
    font-size:42px;
    font-weight:800;
    color:#0071e3;
}

.stat-label{
    color:#666;
}


/* ==========================
   图集
   ========================== */

.gallery-frame{

    background:rgba(255,255,255,0.25);

    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);

    border-radius:24px;

    padding:12px;

    border:1px solid rgba(255,255,255,0.25);

    transition:.35s;
}

.gallery-frame:hover{
    transform:translateY(-5px);
}

.gallery-img{
    width:100%;
    border-radius:18px;

    transition:.45s;
}

.gallery-img:hover{
    transform:scale(1.03);
}


/* ==========================
   Expander
   ========================== */

details{
    background:rgba(255,255,255,0.25)!important;

    backdrop-filter:blur(18px)!important;

    border-radius:20px!important;

    border:1px solid rgba(255,255,255,0.25)!important;

    margin-bottom:15px!important;
}


/* ==========================
   Tabs
   ========================== */

.stTabs [data-baseweb="tab-list"]{
    gap:16px;
}

.stTabs [data-baseweb="tab"]{

    background:
    rgba(255,255,255,0.18);

    backdrop-filter:
    blur(12px);

    border-radius:
    16px;

    padding-left:20px;
    padding-right:20px;

    transition:.3s;
}

.stTabs [aria-selected="true"]{

    background:
    rgba(255,255,255,0.4);

    backdrop-filter:
    blur(18px);

    color:#0071e3!important;

    font-weight:700!important;
}


/* ==========================
   Footer
   ========================== */

.footer-glass{

    background:
    rgba(255,255,255,0.2);

    backdrop-filter:
    blur(16px);

    -webkit-backdrop-filter:
    blur(16px);

    border-top:
    1px solid rgba(255,255,255,0.25);

    border-radius:
    24px;

    padding:
    35px;

    margin-top:
    60px;
}


/* ==========================
   招募联系方式卡
   ========================== */

.contact-glass{

    background:
    rgba(255,255,255,0.15);

    backdrop-filter:
    blur(20px);

    -webkit-backdrop-filter:
    blur(20px);

    border:
    1px solid rgba(255,255,255,0.18);

    border-radius:
    18px;

    transition:.3s;
}

.contact-glass:hover{

    background:
    rgba(255,255,255,0.2);

    transform:
    translateY(-3px);
}
/* =========================
   手机端适配
========================= */

@media (max-width:768px){

    .block-container{
        max-width:100% !important;
        padding-left:12px !important;
        padding-right:12px !important;
    }

    .stTabs [data-baseweb="tab"]{
        font-size:14px !important;
        padding-left:8px !important;
        padding-right:8px !important;
        white-space:nowrap !important;
    }

    h1{
        font-size:32px !important;
    }

    h2{
        font-size:26px !important;
    }

    h3{
        font-size:20px !important;
    }

}
            
/* ==========================================
   移动端 Banner 终极修复（居中 + 文字优化）
   ========================================== */
@media (max-width: 768px) {
    .hero-banner-mobile {
        padding: 30px 20px !important;   /* 减小手机上的上下左右内边距 */
    }

    /* 毛玻璃卡片容器（内层 flex 容器） */
    .hero-banner-mobile > div[style*="display:flex"] {
        flex-direction: column !important;   /* 改为垂直排列 */
        align-items: center !important;      /* 所有子项水平居中 */
        gap: 20px !important;
        padding: 25px 20px !important;       /* 减小卡片内部填充 */
    }

    /* 包裹 logo 的 div ：强制让图片居中 */
    .hero-banner-mobile img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: clamp(80px, 25vw, 120px) !important; /* 适当缩小，但依然舒适 */
    }

    /* 文本容器（标题 + 副标题） */
    .hero-banner-mobile div[style*="text-align:center"] {
        width: 100% !important;
        text-align: center !important;
    }

    /* 主标题：防止强行换行，允许换行但控制字号 */
    .hero-banner-mobile h1 {
        font-size: clamp(28px, 6vw, 38px) !important;
        line-height: 1.3 !important;
        word-break: break-word !important;
        white-space: normal !important;
        margin-bottom: 8px !important;
    }

    /* 副标题 */
    .hero-banner-mobile p {
        font-size: 16px !important;
        line-height: 1.5 !important;
        word-break: break-word !important;
        padding: 0 8px !important;
    }

    /* 如果毛玻璃卡片内还有其他复杂结构，做一个保险，让所有直接子元素都居中 */
    .hero-banner-mobile > div[style*="background:rgba(255,255,255,0.15)"] > * {
        text-align: center !important;
    }
}

.hero-banner-mobile h1 {
    white-space: nowrap !important;
    overflow-x: auto !important;   /* 允许横向滑动，优雅降级 */
    -webkit-overflow-scrolling: touch;
}
            
/* ==========================================
   手机端完全重设计 (宽度 ≤ 768px)
   ========================================== */
@media (max-width: 768px) {

    /* 1. 全局背景简化 */
    .stApp {
        background: #f5f5f7 !important;  /* 苹果浅灰，比纯白柔和 */
    }

    /* 2. 内容区宽度占满，去除多余留白 */
    .block-container {
        max-width: 100% !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-top: 10px !important;
    }

    /* 3. 重写电脑版的大横幅（Hero）：手机版简洁卡片式 */
    .hero-banner-mobile {
        background: white !important;
        padding: 20px 16px !important;
        border-radius: 28px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
        /* 去掉原背景图、大阴影 */
        background-image: none !important;
        position: relative !important;
    }

    /* 隐藏原来的毛玻璃背景层和彩色光晕 */
    .hero-banner-mobile > div[style*="position:absolute"] {
        display: none !important;
    }

    /* 手机版内层 flex 容器：垂直 + 居中 */
    .hero-banner-mobile > div[style*="display:flex"] {
        flex-direction: column !important;
        align-items: center !important;
        gap: 12px !important;
        background: transparent !important;
        backdrop-filter: none !important;
        border: none !important;
        padding: 0 !important;
    }

    /* logo 图片：圆角适中，居中 */
    .hero-banner-mobile img {
        width: 80px !important;
        height: auto !important;
        border-radius: 20px !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
    }

    /* 标题文字容器 */
    .hero-banner-mobile div[style*="text-align:center"] {
        text-align: center !important;
        width: 100% !important;
    }

    .hero-banner-mobile h1 {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #1d1d1f !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -0.3px !important;
    }

    .hero-banner-mobile p {
        font-size: 16px !important;
        color: #86868b !important;
        margin: 0 !important;
        line-height: 1.4 !important;
    }

    /* 4. 手机端 Tabs 改为可滑动 + 更友好的胶囊样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        flex-wrap: nowrap !important;
        padding-bottom: 8px !important;
        scrollbar-width: thin;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(0,0,0,0.04) !important;
        backdrop-filter: none !important;
        border-radius: 30px !important;
        padding: 8px 18px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #1d1d1f !important;
        white-space: nowrap !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #0071e3 !important;
        color: white !important;
    }

    /* 5. 手机端卡片（活动/推文）完全重设计 */
    .apple-card {
        background: white !important;
        backdrop-filter: none !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        margin-bottom: 16px !important;
        transition: none !important;
        animation: none !important; /* 去掉入场动画 */
    }

    .apple-card:hover {
        transform: none !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }

    .card-img-container {
        height: 160px !important;
    }

    .card-content {
        padding: 16px !important;
    }

    .card-title {
        font-size: 18px !important;
        line-height: 1.35 !important;
        -webkit-line-clamp: 2 !important;
    }

    .card-meta {
        font-size: 12px !important;
        margin-bottom: 8px !important;
    }

    .card-summary {
        font-size: 14px !important;
        -webkit-line-clamp: 3 !important;
        margin-bottom: 16px !important;
        color: #3a3a3c !important;
    }

    /* 胶囊按钮改为块级，方便点按 */
    .apple-btn {
        display: block !important;
        text-align: center !important;
        padding: 12px !important;
        font-size: 15px !important;
    }

    /* 6. 隐藏电脑端的毛玻璃统计卡、复杂footer里的多余装饰（如果有） */
    .stat-card, .glass-card, .gallery-frame {
        background: white !important;
        backdrop-filter: none !important;
        border: none !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }

    /* 7. 页脚（footer）手机版轻量化 */
    .footer-glass {
        background: white !important;
        backdrop-filter: none !important;
        border: none !important;
        box-shadow: 0 -1px 0 rgba(0,0,0,0.05) !important;
        padding: 24px 20px !important;
        margin-top: 32px !important;
        text-align: center !important;
        font-size: 13px !important;
    }

    /* 8. AI 聊天框等组件自适应宽度 */
    .stTextInput > div, .stTextArea > div {
        width: 100% !important;
    }

    /* 9. 隐藏电脑端可能会有的大光晕（绝对定位的圆） */
    div[style*="filter: blur(100px)"] {
        display: none !important;
    }
}

@media (max-width: 768px) {
    footer {
        visibility: hidden;
        height: 0;
    }
    /* 隐藏 Streamlit 自带的菜单按钮等 */
    .stActionButton, .stDecoration {
        display: none;
    }
}
            
/* 新 Banner 样式 - 响应式毛玻璃 */
.responsive-glass-banner {
    position: relative;
    border-radius: 32px;
    overflow: hidden;
    margin-bottom: 40px;
    background: url('images/doubleflags.jpg') center/cover no-repeat;
}

/* 毛玻璃遮罩层 */
.banner-overlay {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 32px;
    padding: 40px 48px;
    transition: all 0.3s ease;
}

/* 内部容器：电脑端默认水平布局 */
.banner-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
}

/* 左侧内容区 */
.banner-text {
    flex: 2;
    text-align: left;
}

.banner-text h1 {
    font-size: 3.2rem;
    font-weight: 700;
    color: white;
    margin: 0 0 12px 0;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.banner-text p {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.95);
    margin: 0;
    line-height: 1.5;
}

/* 右侧 logo 区 */
.banner-logo {
    flex: 1;
    display: flex;
    justify-content: flex-end;
}

.banner-logo img {
    width: 120px;
    height: auto;
    border-radius: 24px;
    box-shadow: 0 20px 35px -10px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.banner-logo img:hover {
    transform: scale(1.02);
}

/* ========== 手机端响应式 ========== */
@media (max-width: 768px) {
    .banner-overlay {
        padding: 28px 20px;
    }
    
    .banner-inner {
        flex-direction: column;
        text-align: center;
        gap: 20px;
    }
    
    .banner-text {
        text-align: center;
        order: 2;  /* 文字在下 */
    }
    
    .banner-logo {
        justify-content: center;
        order: 1;  /* 图片在上 */
    }
    
    .banner-text h1 {
        font-size: 1.8rem;
        margin-bottom: 8px;
        word-break: keep-all;  /* 防止强制换行 */
        white-space: normal;
    }
    
    .banner-text p {
        font-size: 1rem;
    }
    
    .banner-logo img {
        width: 90px;
        border-radius: 20px;
    }
}
            

</style>
""", unsafe_allow_html=True)

# 将本地 banner 背景图转为 Base64 并覆盖 CSS 背景
banner_bg_base64 = get_image_base64("images/doubleflags.jpg")  # 使用你已有的缓存函数
if banner_bg_base64:
    st.markdown(
        f"""
        <style>
        .responsive-glass-banner {{
            background: url('data:image/jpeg;base64,{banner_bg_base64}') center/cover no-repeat !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("未找到 images/doubleflags.jpg，Banner 背景将使用默认图片。")
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
# 4. 主界面：大横幅 (Banner)
# ==========================================
# 读取 logo（你原来已经有这部分，直接复用 banner_img_base64）
banner_img_base64 = ""
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as img_file:
        banner_img_base64 = base64.b64encode(img_file.read()).decode()
img_html = f'<img src="data:image/png;base64,{banner_img_base64}" alt="NJU Geo Logo">' if banner_img_base64 else '<div style="width:90px;"></div>'

st.markdown(f"""
<div class="responsive-glass-banner">
    <div class="banner-overlay">
        <div class="banner-inner">
            <div class="banner-text">
                <h1>南京大学地理协会</h1>
                <p>地理无界 · 世界相连</p>
            </div>
            <div class="banner-logo">
                {img_html}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



# ==========================================
# 5. 主界面：四选项卡 (Tabs) 排版设计
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 首页", "🔥 活动通知", "📚 相关推文", "📷 图集", "🤖 AI 智能答疑"])

# ----------------- 标签页 4：AI 答疑模块 -----------------
with tab5:
    st.markdown("### 🤖 NJUGA 智能百事通")
    st.markdown("你可以问我：*最近有什么活动吗？* 或者 *九州风物的推文有链接吗？*")
    
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

# ----------------- 标签页 1：首页 -----------------
with tab1:

    # =========================
    # Hero
    # =========================

    

    # =========================
    # 社团介绍
    # =========================

    st.markdown("## ✨ 欢迎来到南京大学地理协会")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
玄武湖里藏着明代黄册库的遗址，  
浦口火车站的铁轨上还走着整个20世纪的移民史诗，  
钟山的草木之下，六朝古意与近代风云层层叠压。

这座城市还有很多图层没被打开。

我们是一群带着“地理眼”行走的人。  
不打卡景点，打捞附近。  
不生产攻略，生产理解。

用空间的逻辑理解时间，  
用土地的肌理解读文明。

南京是我们的教室，山河是我们的课本。  
从苏州的太湖湿地到宁夏的贺兰山下，  
从一张校园咖啡地图到一条城市轴线设计——  
我们把零散的地理信息，绘制成人人可触摸的坐标。

**地理无界 · 世界相连**  
一起走，一起看见。   
        """)

    # === 找到你的首页分列代码，替换右边这一列 ===
    # 假设你之前是 col_a, col_b = st.columns([1.5, 1]) 或者类似的
    
    with col2:
        # 1. 把本地背景图转为 Base64
        stats_bg_base64 = ""
        if os.path.exists("images/rocklion.jpg"):  # 确保你的图片名字是这个
            with open("images/rocklion.jpg", "rb") as img_file:
                stats_bg_base64 = base64.b64encode(img_file.read()).decode()
        
        # 2. 生成背景 CSS
        bg_style = f"url('data:image/jpeg;base64,{stats_bg_base64}') center/cover" if stats_bg_base64 else "linear-gradient(135deg, #e0eafc, #cfdef3)"
        
        # 3. 渲染带背景的大容器 (⚠️ 绝对不能有前置空格！)
        st.markdown(f"""
<div style="background: {bg_style}; padding: 30px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 20px; height: 100%;">
<!-- 第一张卡片：30+ -->
<div style="background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 40px 20px; border-radius: 16px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
<h2 style="margin: 0; color: #0071e3; font-size: 48px; font-weight: 800;">30+</h2>
<p style="margin: 10px 0 0 0; color: #515154; font-size: 16px; font-weight: 500;">协会成员</p>
</div>
<!-- 第二张卡片：500+ -->
<div style="background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 40px 20px; border-radius: 16px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
<h2 style="margin: 0; color: #0071e3; font-size: 48px; font-weight: 800;">500+</h2>
<p style="margin: 10px 0 0 0; color: #515154; font-size: 16px; font-weight: 500;">活动群人数</p>
</div>
</div>
""", unsafe_allow_html=True)

    st.divider()

# =========================
    # 图集
    # =========================

    st.markdown("## 📸 图集")
    st.caption("过去一年，我们走过的地方")

    g1,g2,g3 = st.columns(3)

    with g1:
        st.image(
            "images/钟山.jpg",
            use_container_width=True
        )

        st.caption("钟山")

        

    with g2:
        st.image(
            "images/星光集市.jpg",
            use_container_width=True
        )

        st.caption("南大星光集市")

       
    with g3:
        st.image(
            "images/午朝门.jpg",
            use_container_width=True
        )

        st.caption("午朝门")

    st.divider()

    # =========================
    # 关于我们
    # =========================

    st.markdown("## 🏛 关于我们")

    with st.expander("📚 社团简介", expanded=False):
        st.markdown("""
    南京大学地理协会成立于2025年。
    
    **我们做什么？**  
    组织城市漫步、野外考察、学术讲座、地图制作等活动，带你走出课堂，用地理的视角观察真实的世界。
    
    **为什么加入？**  
    - 你会发现：玄武湖不只是一个公园，它背后藏着明朝的户籍制度；浦口火车站不只是一个网红打卡点，它记录了一段跨世纪的移民史。  
    - 你会学到：如何看懂一座城市的轴线设计，如何从一条路的命名读出区划变迁，如何用GIS把零散的信息变成一张有用的地图。  
    - 你会去到：南京的大街小巷，苏州的太湖湿地，宁夏的贺兰山下……把山河变成教材。
    
    **我们的宗旨**：地理无界 · 世界相连  
    **我们的风格**：不打卡景点，而是理解土地；不生产攻略，而是分享知识。
    
    欢迎所有专业、所有年级的同学。不需要地理基础，只需要一颗好奇的心。
    """)

    with st.expander("🏢 组织架构", expanded=False):
         st.markdown("""
    ### 活动部
    路线设计、实地踩点、活动执行。每一次行走的背后，都有我们提前丈量过的安全与精彩。
    
    ### 宣传部
    公众号运营、摄影摄像、海报设计。把你的文字、镜头和创意，变成南大人共同的地理记忆。
    
    ### 学术部
    讲座策划、科普写作、GIS与地理技能交流。让硬核知识也能有温度地落地。
    
    ### 联络部
    嘉宾邀请、对外合作、社团联动。帮协会链接更多有趣的灵魂和资源。
    
    ### 办公室
    财务、物资、志愿时长管理。做协会最稳的后盾，让每一次出发都没有后顾之忧。
    
    ---
    **无论你是什么专业、什么年级**，只要你对土地与空间有好奇心，这里就有一个位置等你。
    """)



    st.divider()

    
    # =========================
    # 加入我们
    # =========================

    # ==========================================
# ==========================================
# 底部招募卡片 (Ready to Explore)
# ==========================================
st.markdown(f"""
<div style="box-sizing: border-box; width: 100%; position: relative; background: linear-gradient(145deg, #0f172a, #1a1a2e, #2d2a4a); border-radius: 24px; padding: clamp(25px, 5vw, 50px); display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); overflow: hidden; margin-top: 20px;">
<!-- 背景炫光特效 (右上角的紫色光晕) -->
<div style="position: absolute; top: -50px; right: -20px; width: 250px; height: 250px; background: #7c3aed; filter: blur(90px); opacity: 0.4; border-radius: 50%;"></div>
<div style="position: absolute; bottom: -50px; left: -20px; width: 200px; height: 200px; background: #2563eb; filter: blur(80px); opacity: 0.3; border-radius: 50%;"></div>

<!-- 左侧：文案区 -->
<div style="flex: 1 1 250px; max-width: 100%; box-sizing: border-box; z-index: 1;">
<h2 style="margin: 0 0 15px 0; font-size: clamp(26px, 8vw, 46px); font-weight: 800; background: linear-gradient(90deg, #c4b5fd, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; word-break: break-word;">Ready to Explore?</h2>
<p style="color: #cbd5e1; font-size: 16px; line-height: 1.8; margin: 0; font-weight: 400; word-break: break-word;">无论你来自什么专业，<br>只要对土地、城市与世界保持好奇，<br>我们都欢迎你加入。</p>
</div>

<!-- 右侧：联系方式卡片区 -->
<div style="flex: 1 1 250px; max-width: 100%; box-sizing: border-box; z-index: 1; display: flex; flex-direction: column; gap: 12px;">

<div style="box-sizing: border-box; width: 100%; background: rgba(255,255,255,0.15);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border:1px solid rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 16px; display: flex; align-items: center; backdrop-filter: blur(10px);">
<span style="font-size: 20px; margin-right: 15px; flex-shrink: 0;">💬</span>
<div style="display: flex; flex-direction: column; overflow: hidden;">
<span style="color: #94a3b8; font-size: 16px; font-weight: 600; white-space: nowrap;">活动 QQ 群</span>
<span style="color: #ffffff; font-size: 20px; font-weight: 700; word-break: break-all;">720915627</span>
</div>
</div>

<div style="box-sizing: border-box; width: 100%; background: rgba(255,255,255,0.15);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border:1px solid rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 16px; display: flex; align-items: center; backdrop-filter: blur(10px);">
<span style="font-size: 20px; margin-right: 15px; flex-shrink: 0;">📱</span>
<div style="display: flex; flex-direction: column; overflow: hidden;">
<span style="color: #94a3b8; font-size: 16px; font-weight: 600; white-space: nowrap;">微信公众号</span>
<span style="color: #ffffff; font-size: 20px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">山河南观</span>
</div>
</div>

<div style="box-sizing: border-box; width: 100%; background: rgba(255,255,255,0.15);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border:1px solid rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 16px; display: flex; align-items: center; backdrop-filter: blur(10px);">
<span style="font-size: 20px; margin-right: 15px; flex-shrink: 0;">📕</span>
<div style="display: flex; flex-direction: column; overflow: hidden;">
<span style="color: #94a3b8; font-size: 16px; font-weight: 600; white-space: nowrap;">小红书账号</span>
<span style="color: #ffffff; font-size: 20px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">南大地理协会</span>
</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

# ----------------- 页面底部版权信息 -----------------



st.markdown("""
<div style="
    width: 100%;
    padding: 40px 20px;
    text-align: center;
    color: #666;
    font-size: 14px;
    border-top: 1px solid #eee;
    margin-top: 60px;
">
    南京大学 安邦书院<br>
    251830038 杨宝鑫 | 251830056 陈琪睿 | 251200015 张跃恒<br>
    &copy; 2026 南京大学地理协会. 保留所有权利
</div>
""", unsafe_allow_html=True)


# ----------------- 标签页 2：活动通知 -----------------

with tab2:
    st.markdown("### 🔥 最新活动")
    st.markdown("脚步丈量大地。")
    st.write("")  # 留白

    # 活动分类
    act_categories = list(ACTIVITY_DATA.keys())
    
    # 子 Tabs
    act_sub_tabs = st.tabs(act_categories)

    # 遍历每个分类
    for tab_obj, category in zip(act_sub_tabs, act_categories):
        with tab_obj:
            activities = ACTIVITY_DATA.get(category, [])
            if not activities:
                st.info(f"暂无 {category} 的活动")
                continue

            col1, col2 = st.columns(2, gap="large")

            for i, act in enumerate(activities):
                target_col = col1 if i % 2 == 0 else col2
                with target_col:
                    # 读取图片 base64
                    img_base64 = ""
                    if act.get("cover") and os.path.exists(act["cover"]):
                        try:
                            with open(act["cover"], "rb") as img_file:
                                img_base64 = base64.b64encode(img_file.read()).decode()
                        except:
                            img_base64 = ""

                    # 图片 HTML（如果没有图片就用渐变占位图）
                    img_html = (
                        f'<img src="data:image/jpeg;base64,{img_base64}" class="card-img" style="width:100%; border-radius:10px;">'
                        if img_base64 else
                        '<div style="width:100%; height:200px; border-radius:10px; background: linear-gradient(135deg, #ff9a9e, #fecfef);"></div>'
                    )

                    # 按钮文字
                    status = act.get('status', '未定义')
                    btn_text = "立即报名 ↗" if status == "报名中" else "查看详情 ↗"

                    # 多行描述处理：使用 white-space: pre-line
                    desc = act.get('desc', '')
                    st.markdown(f"""
                    <div style="
                        border:1px solid #eee; 
                        border-radius:10px; 
                        padding:15px; 
                        margin-bottom:20px; 
                        box-shadow:0 4px 6px rgba(0,0,0,0.1);
                    ">
                        <div style="text-align:center;margin-bottom:10px;">{img_html}</div>
                        <h3 style="margin-bottom:5px;">{act.get('title', '无标题')}</h3>
                        <p style="color:#555;font-size:14px;">📅 {act.get('date','未知日期')} | 📌 {status}</p>
                        <p style="white-space: pre-line; font-size:14px; color:#333;">{desc}</p>
                        <a href="{act.get('url','#')}" target="_blank" style="
                            display:inline-block;
                            padding:8px 16px;
                            background-color:#007bff;
                            color:white;
                            border-radius:5px;
                            text-decoration:none;
                            margin-top:5px;
                        ">{btn_text}</a>
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



with tab4:
    st.markdown("## 📷 活动图集")
    st.markdown("点击下方折叠面板，查看每次活动的精彩照片。")

    # 定义图集数据：每个图集包含名称和图片列表（图片路径）
    album_data = {
        "星光集市": [
            "images/星光集市.jpg",
        ],
        "午朝门石刻考察": [
            "images/午朝门.jpg",
        ],
        "工业烟云·南朝遗梦": [
            "activity_images/工业烟云.jpg",
        ],
    }

    # 遍历每个图集，生成折叠面板
    for album_name, img_paths in album_data.items():
        with st.expander(f"📁 {album_name}"):
            if not img_paths:
                st.info("该图集暂无图片。")
                continue
            # 每行显示3列图片
            cols_per_row = 3
            for i in range(0, len(img_paths), cols_per_row):
                row_cols = st.columns(cols_per_row)
                for j, col in enumerate(row_cols):
                    idx = i + j
                    if idx < len(img_paths):
                        img_path = img_paths[idx]
                        img_base64 = get_image_base64(img_path)
                        if img_base64:
                            # 使用与 tab2 活动卡片图片相同的 HTML 结构
                            img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="card-img" style="width:100%; height:100%; object-fit: cover;">'
                            col.markdown(f"""
                            <div class="card-img-container" style="height:200px; margin-bottom:10px;">
                                {img_html}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            col.markdown(f"<div style='text-align:center'>⚠️ 图片缺失: {img_path}</div>", unsafe_allow_html=True)
                    else:
                        col.empty()
            st.markdown("---")