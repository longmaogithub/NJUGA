import streamlit as st
import os
import base64
from zhipu_api import ReviewAssistantAPI
from utils import get_association_knowledge_base, ACTIVITY_DATA, ARTICLE_DATA

# ==========================================
# 0. 全局缓存：图片转 Base64（避免重复 I/O）
# ==========================================
@st.cache_data
def get_image_base64(image_path: str) -> str:
    """读取本地图片并返回 Base64 字符串，若文件不存在返回空字符串"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ==========================================
# 1. 页面配置 & 🍎 苹果风超炫酷 CSS 动画（完整保留）
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
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 85% !important;
}     
/* 整体背景优化 */
.stApp {
    background: #fbfbfd;
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
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
    margin-bottom: 30px;
    transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
    animation: fadeSlideUp 0.8s ease-out forwards;
}
.apple-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}
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
    cursor: pointer;
}
.apple-card:hover .card-img {
    transform: scale(1.05);
}
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
.apple-btn {
    display: inline-block;
    background: #0071e3;
    color: white !important;
    padding: 10px 22px;
    border-radius: 980px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}
.apple-btn:hover {
    background: #0077ed;
    transform: scale(1.03);
}
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
/* Vision Pro 毛玻璃设计系统 */
.glass-card{
    background: rgba(255,255,255,0.22);
    backdrop-filter: blur(22px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 28px;
    box-shadow: 0 8px 32px rgba(31,38,135,0.12);
    transition: all .4s ease;
}
.glass-card:hover{
    transform: translateY(-6px);
    box-shadow: 0 18px 45px rgba(31,38,135,0.18);
}
.hero-box{
    position:relative;
    overflow:hidden;
    background: url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2000");
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
.stat-card{
    background:rgba(255,255,255,0.25);
    backdrop-filter:blur(20px);
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
.gallery-frame{
    background:rgba(255,255,255,0.25);
    backdrop-filter:blur(18px);
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
details{
    background:rgba(255,255,255,0.25)!important;
    backdrop-filter:blur(18px)!important;
    border-radius:20px!important;
    border:1px solid rgba(255,255,255,0.25)!important;
    margin-bottom:15px!important;
}
.stTabs [data-baseweb="tab-list"]{
    gap:16px;
}
.stTabs [data-baseweb="tab"]{
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding-left:20px;
    padding-right:20px;
    transition:.3s;
}
.stTabs [aria-selected="true"]{
    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(18px);
    color:#0071e3!important;
    font-weight:700!important;
}
.footer-glass{
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(16px);
    border-top: 1px solid rgba(255,255,255,0.25);
    border-radius: 24px;
    padding: 35px;
    margin-top: 60px;
}
.contact-glass{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    transition:.3s;
}
.contact-glass:hover{
    background: rgba(255,255,255,0.2);
    transform: translateY(-3px);
}
/* 手机端适配 */
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
    h1{ font-size:32px !important; }
    h2{ font-size:26px !important; }
    h3{ font-size:20px !important; }
}
/* 移动端 Banner 修复 */
@media (max-width: 768px) {
    .hero-banner-mobile { padding: 30px 20px !important; }
    .hero-banner-mobile > div[style*="display:flex"] {
        flex-direction: column !important;
        align-items: center !important;
        gap: 20px !important;
        padding: 25px 20px !important;
    }
    .hero-banner-mobile img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: clamp(80px, 25vw, 120px) !important;
    }
    .hero-banner-mobile div[style*="text-align:center"] {
        width: 100% !important;
        text-align: center !important;
    }
    .hero-banner-mobile h1 {
        font-size: clamp(28px, 6vw, 38px) !important;
        line-height: 1.3 !important;
        word-break: break-word !important;
        white-space: normal !important;
        margin-bottom: 8px !important;
    }
    .hero-banner-mobile p {
        font-size: 16px !important;
        line-height: 1.5 !important;
        word-break: break-word !important;
        padding: 0 8px !important;
    }
    .hero-banner-mobile > div[style*="background:rgba(255,255,255,0.15)"] > * {
        text-align: center !important;
    }
}
.hero-banner-mobile h1 {
    white-space: nowrap !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch;
}
/* 手机端完全重设计 */
@media (max-width: 768px) {
    .stApp { background: #f5f5f7 !important; }
    .block-container {
        max-width: 100% !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-top: 10px !important;
    }
    .hero-banner-mobile {
        background: white !important;
        padding: 20px 16px !important;
        border-radius: 28px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
        background-image: none !important;
        position: relative !important;
    }
    .hero-banner-mobile > div[style*="position:absolute"] { display: none !important; }
    .hero-banner-mobile > div[style*="display:flex"] {
        flex-direction: column !important;
        align-items: center !important;
        gap: 12px !important;
        background: transparent !important;
        backdrop-filter: none !important;
        border: none !important;
        padding: 0 !important;
    }
    .hero-banner-mobile img {
        width: 80px !important;
        border-radius: 20px !important;
        margin: 0 auto !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
    }
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        padding-bottom: 8px !important;
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
    }
    .stTabs [aria-selected="true"] {
        background: #0071e3 !important;
        color: white !important;
    }
    .apple-card {
        background: white !important;
        backdrop-filter: none !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        margin-bottom: 16px !important;
        transition: none !important;
        animation: none !important;
    }
    .apple-card:hover { transform: none !important; }
    .card-img-container { height: 160px !important; }
    .card-content { padding: 16px !important; }
    .card-title { font-size: 18px !important; }
    .card-meta { font-size: 12px !important; margin-bottom: 8px !important; }
    .card-summary { font-size: 14px !important; margin-bottom: 16px !important; color: #3a3a3c !important; }
    .apple-btn { display: block !important; text-align: center !important; padding: 12px !important; font-size: 15px !important; }
    .stat-card, .glass-card, .gallery-frame { background: white !important; backdrop-filter: none !important; border: none !important; box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important; }
    .footer-glass { background: white !important; backdrop-filter: none !important; border: none !important; box-shadow: 0 -1px 0 rgba(0,0,0,0.05) !important; padding: 24px 20px !important; margin-top: 32px !important; text-align: center !important; font-size: 13px !important; }
    .stTextInput > div, .stTextArea > div { width: 100% !important; }
    div[style*="filter: blur(100px)"] { display: none !important; }
    footer, .stActionButton, .stDecoration { display: none; }
}
/* 新 Banner 样式 - 响应式毛玻璃 */
.responsive-glass-banner {
    position: relative;
    border-radius: 32px;
    overflow: hidden;
    margin-bottom: 40px;
    background: url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2000') center/cover no-repeat;
}
.banner-overlay {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(16px);
    border-radius: 32px;
    padding: 40px 48px;
    transition: all 0.3s ease;
}
.banner-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
}
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
.banner-logo img:hover { transform: scale(1.02); }
@media (max-width: 768px) {
    .banner-overlay { padding: 28px 20px; }
    .banner-inner { flex-direction: column; gap: 20px; }
    .banner-text { text-align: center; order: 2; }
    .banner-logo { justify-content: center; order: 1; }
    .banner-text h1 { font-size: 1.8rem; margin-bottom: 8px; word-break: keep-all; white-space: normal; }
    .banner-text p { font-size: 1rem; }
    .banner-logo img { width: 90px; border-radius: 20px; }
}
</style>
""", unsafe_allow_html=True)


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
# 3. Banner (读取本地 logo)
# ==========================================
banner_img_base64 = get_image_base64("logo.png")
img_html = f'<img src="data:image/png;base64,{banner_img_base64}" alt="NJU Geo Logo" loading="lazy">' if banner_img_base64 else '<div style="width:90px;"></div>'

st.markdown(f"""
<div class="responsive-glass-banner">
    <div class="banner-overlay">
        <div class="banner-inner">
            <div class="banner-text">
                <h1>南京大学地理协会</h1>
                <p>地理无界 · 世界相连</p>
            </div>
            <div class="banner-logo">{img_html}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. 主界面：四选项卡
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 首页", "🔥 活动通知", "📚 相关推文", "🤖 AI 智能答疑"])

# ----------------- 首页 -----------------
with tab1:
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
    with col2:
        stats_bg_base64 = get_image_base64("images/rocklion.jpg")
        bg_style = f"url('data:image/jpeg;base64,{stats_bg_base64}') center/cover" if stats_bg_base64 else "linear-gradient(135deg, #e0eafc, #cfdef3)"
        st.markdown(f"""
<div style="background: {bg_style}; padding: 30px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 20px; height: 100%;">
<div style="background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(10px); padding: 40px 20px; border-radius: 16px; text-align: center;">
<h2 style="margin:0; color:#0071e3; font-size:48px;">30+</h2>
<p style="margin:10px 0 0 0; color:#515154;">协会成员</p>
</div>
<div style="background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(10px); padding: 40px 20px; border-radius: 16px; text-align: center;">
<h2 style="margin:0; color:#0071e3; font-size:48px;">500+</h2>
<p style="margin:10px 0 0 0; color:#515154;">活动群人数</p>
</div>
</div>
""", unsafe_allow_html=True)
    st.divider()

    # 图集 Gallery（支持全屏点击）
    st.markdown("## 📸 图集 Gallery")
    st.caption("过去一年，我们走过的地方")
    gallery_images = [
        {"path": "images/wenzhou.jpg", "caption": "温州"},
        {"path": "images/星光集市.jpg", "caption": "星光集市"},
        {"path": "images/午朝门.jpg", "caption": "午朝门"}
    ]
    cols = st.columns(3)
    for idx, img in enumerate(gallery_images):
        with cols[idx]:
            img_base64 = get_image_base64(img["path"])
            if img_base64:
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{img_base64}" class="fullscreen-img" style="width: 100%; border-radius: 18px; cursor: pointer;" loading="lazy">
                    <p style="margin-top: 8px; color: #666;">{img['caption']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center'>⚠️ 图片缺失: {img['path']}</div>", unsafe_allow_html=True)
    st.divider()

    # 关于我们
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

    # 底部招募卡片
    st.markdown("""
<div style="background: linear-gradient(145deg, #0f172a, #1a1a2e, #2d2a4a); border-radius: 24px; padding: clamp(25px, 5vw, 50px); display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); overflow: hidden; margin-top: 20px; position: relative;">
<div style="position: absolute; top: -50px; right: -20px; width: 250px; height: 250px; background: #7c3aed; filter: blur(90px); opacity: 0.4; border-radius: 50%;"></div>
<div style="position: absolute; bottom: -50px; left: -20px; width: 200px; height: 200px; background: #2563eb; filter: blur(80px); opacity: 0.3; border-radius: 50%;"></div>
<div style="flex: 1 1 250px; max-width: 100%; z-index: 1;">
<h2 style="margin: 0 0 15px 0; font-size: clamp(26px, 8vw, 46px); font-weight: 800; background: linear-gradient(90deg, #c4b5fd, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; word-break: break-word;">Ready to Explore?</h2>
<p style="color: #cbd5e1; font-size: 16px; line-height: 1.8; margin: 0;">无论你来自什么专业，<br>只要对土地、城市与世界保持好奇，<br>我们都欢迎你加入。</p>
</div>
<div style="flex: 1 1 250px; max-width: 100%; z-index: 1; display: flex; flex-direction: column; gap: 12px;">
<div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 16px; padding: 12px 20px; display: flex; align-items: center; gap: 15px;">
<span style="font-size: 20px;">💬</span>
<div><span style="color: #94a3b8;">活动 QQ 群</span><br><span style="color: white; font-weight: 700; word-break: break-all;">720915627</span></div>
</div>
<div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 16px; padding: 12px 20px; display: flex; align-items: center; gap: 15px;">
<span style="font-size: 20px;">📱</span>
<div><span style="color: #94a3b8;">微信公众号</span><br><span style="color: white; font-weight: 700;">山河南观</span></div>
</div>
<div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 16px; padding: 12px 20px; display: flex; align-items: center; gap: 15px;">
<span style="font-size: 20px;">📕</span>
<div><span style="color: #94a3b8;">小红书账号</span><br><span style="color: white; font-weight: 700;">南大地理协会</span></div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #666; font-size: 14px; border-top: 1px solid #eee; margin-top: 60px;">
    南京大学 安邦书院<br>
    251830038 杨宝鑫 | 251830056 陈琪睿 | 251200015 张跃恒<br>
    &copy; 2026 南京大学地理协会. 保留所有权利
</div>
""", unsafe_allow_html=True)


# ----------------- 标签页 2：活动通知（改为苹果卡片样式） -----------------
with tab2:
    st.markdown("### 🔥 最新活动")
    st.markdown("脚步丈量大地。")
    act_categories = list(ACTIVITY_DATA.keys())
    act_sub_tabs = st.tabs(act_categories)
    for tab_obj, category in zip(act_sub_tabs, act_categories):
        with tab_obj:
            activities = ACTIVITY_DATA.get(category, [])
            if not activities:
                st.info(f"暂无 {category} 的活动")
                continue
            cols = st.columns(2, gap="large")
            for i, act in enumerate(activities):
                with cols[i % 2]:
                    img_base64 = get_image_base64(act.get("cover", ""))
                    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="card-img" loading="lazy">' if img_base64 else '<div style="width:100%; height:100%; background: linear-gradient(135deg, #e0eafc, #cfdef3);"></div>'
                    status = act.get('status', '未定义')
                    btn_text = "立即报名 ↗" if status == "报名中" else "查看详情 ↗"
                    st.markdown(f"""
                    <div class="apple-card">
                        <div class="card-img-container">{img_html}</div>
                        <div class="card-content">
                            <div class="card-title">{act.get('title', '无标题')}</div>
                            <div class="card-meta">📅 {act.get('date','未知日期')} ｜ 📌 {status}</div>
                            <div class="card-summary">{act.get('desc', '')}</div>
                            <a href="{act.get('url','#')}" target="_blank" class="apple-btn">{btn_text}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# ----------------- 标签页 3：推文 -----------------
with tab3:
    st.markdown("### 📚 往期精选推文")
    st.markdown("探索我们过去的脚步，发现大地的故事。")
    categories = list(ARTICLE_DATA.keys())
    sub_tabs = st.tabs(categories)
    for tab, category in zip(sub_tabs, categories):
        with tab:
            articles = ARTICLE_DATA[category]
            cols = st.columns(2, gap="large")
            for i, art in enumerate(articles):
                with cols[i % 2]:
                    img_base64 = get_image_base64(art.get("cover", ""))
                    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="card-img" loading="lazy">' if img_base64 else '<div style="width:100%; height:100%; background: linear-gradient(135deg, #e0eafc, #cfdef3);"></div>'
                    st.markdown(f"""
                    <div class="apple-card">
                        <div class="card-img-container">{img_html}</div>
                        <div class="card-content">
                            <div class="card-title">{art['title']}</div>
                            <div class="card-meta">✍️ {art['author']} ｜ 📅 {art['date']}</div>
                            <div class="card-summary">{art['summary']}</div>
                            <a href="{art['url']}" target="_blank" class="apple-btn">阅读全文 ↗</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# ----------------- 标签页 4：AI 答疑 -----------------
with tab4:
    st.markdown("### 🤖 NJUGA 智能百事通")
    st.markdown("你可以问我：*最近有什么活动吗？* 或者 *九州风物的推文有链接吗？*")
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{"role": "assistant", "content": "你好！我是南大地协的 AI 小助手，关于协会的任何问题都可以问我哦！🌍"}]
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if "cached_knowledge" not in st.session_state:
        st.session_state.cached_knowledge = get_association_knowledge_base()
    if user_input := st.chat_input("输入关于地协的问题..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        full_messages = [{"role": "system", "content": st.session_state.cached_knowledge}] + st.session_state.chat_messages
        with st.chat_message("assistant"):
            stream_response = api_client.generate_stream_response(full_messages)
            if isinstance(stream_response, str):
                st.error(f"网络异常: {stream_response}")
            else:
                def stream_gen():
                    for chunk in stream_response:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                full_answer = st.write_stream(stream_gen())
                st.session_state.chat_messages.append({"role": "assistant", "content": full_answer})


# ==========================================
# 5. 全局全屏图片预览 JavaScript（保证可用）
# ==========================================
st.markdown("""
<script>
(function() {
    // 创建全屏模态框（只创建一次）
    if (!document.getElementById('fullscreen-modal')) {
        const modal = document.createElement('div');
        modal.id = 'fullscreen-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            backdrop-filter: blur(10px);
            z-index: 999999;
            display: none;
            justify-content: center;
            align-items: center;
            cursor: pointer;
        `;
        const modalImg = document.createElement('img');
        modalImg.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
        `;
        modal.appendChild(modalImg);
        document.body.appendChild(modal);
        
        modal.addEventListener('click', function() {
            modal.style.display = 'none';
        });
        // 存储到全局以便调试
        window.__fullscreenModal = modal;
        window.__fullscreenModalImg = modalImg;
    }
    
    // 为所有符合条件的图片绑定点击事件
    function bindFullscreen() {
        // 选择所有 .card-img 和 .fullscreen-img 以及苹果卡片中的图片（以防万一）
        const selectors = '.card-img, .fullscreen-img, .apple-card img';
        const images = document.querySelectorAll(selectors);
        images.forEach(img => {
            // 避免重复绑定
            if (img.getAttribute('data-fs-bound') === 'true') return;
            img.setAttribute('data-fs-bound', 'true');
            img.style.cursor = 'pointer';
            img.addEventListener('click', function(e) {
                e.stopPropagation();
                const modalImg = window.__fullscreenModalImg;
                if (modalImg) {
                    modalImg.src = this.src;
                    window.__fullscreenModal.style.display = 'flex';
                } else {
                    console.error('Modal not found');
                }
            });
        });
    }
    
    // 初始绑定
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindFullscreen);
    } else {
        bindFullscreen();
    }
    
    // 监听动态内容（Streamlit 切换 Tab 时重新绑定）
    const observer = new MutationObserver(function() {
        bindFullscreen();
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)