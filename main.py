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



st.markdown("""
<style>

/* 首页专属 */

.hero-box{
    background:
    linear-gradient(
        rgba(0,0,0,0.35),
        rgba(0,0,0,0.35)
    ),
    url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=2000");
    
    background-size:cover;
    background-position:center;

    border-radius:32px;
    padding:90px 60px;
    margin-bottom:50px;
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
    background:white;
    border-radius:24px;
    padding:30px;
    text-align:center;
    box-shadow:0 4px 20px rgba(0,0,0,0.05);
}

.stat-number{
    font-size:42px;
    font-weight:800;
    color:#0071e3;
}

.stat-label{
    color:#666;
}

.gallery-img{
    width:100%;
    border-radius:22px;
    transition:0.5s;
}

.gallery-img:hover{
    transform:scale(1.03);
}

.join-box{
    text-align:center;
    padding:70px;
    border-radius:30px;
    background:linear-gradient(
        135deg,
        #0071e3,
        #3b82f6
    );
    color:white;
    margin-top:40px;
}

.join-title{
    font-size:42px;
    font-weight:800;
}

.join-text{
    font-size:18px;
    opacity:0.95;
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
# 4. 主界面：大横幅 (Banner)
# ==========================================
# 1. 读取本地 logo.png 转成 Base64
banner_img_base64 = ""
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as img_file:
        banner_img_base64 = base64.b64encode(img_file.read()).decode()

img_html = f"""<img src="data:image/png;base64,{banner_img_base64}" style="width: clamp(100px, 15vw, 160px); height: auto; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">""" if banner_img_base64 else ""

# 2. 渲染弹性布局 (Flexbox) 横幅
# ⚠️ 注意：下面的 HTML 代码绝对不能有任何空格缩进，必须顶格写！
st.markdown(f"""
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: clamp(20px, 4vw, 40px); padding: clamp(30px, 5vw, 50px); border-radius: 24px; background: linear-gradient(135deg, #2c1a3b, #110a17); margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
{img_html}
<div style="text-align: center; min-width: 260px;">
<h1 style="font-size: clamp(30px, 6vw, 48px); font-weight: 800; color: #ffffff; margin: 0 0 10px 0; line-height: 1.2;">南京大学地理协会</h1>
<h3 style="font-size: clamp(18px, 4vw, 24px); font-weight: 400; color: #d1c4e9; margin: 0;">地理无界 · 世界相连</h3>
</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 主界面：四选项卡 (Tabs) 排版设计
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 首页", "🔥 活动通知", "📚 相关推文", "🤖 AI 智能答疑"])

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
        你有没有想过：

        - 玄武湖为何成为南京城市发展的核心？
        - 浦口火车站如何改变长江两岸的人口流动？
        - 钟山为什么能成为六朝文化高地？

        我们相信：

        **地理不仅是地图上的经纬度，更是理解城市、文明与社会的一种方式。**

        在这里，我们把南京变成课堂，把山河变成教材。
        """)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">30+</div>
            <div class="stat-label">协会成员</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">500+</div>
            <div class="stat-label">活动群人数</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

# =========================
    # 图集
    # =========================

    st.markdown("## 📸 图集 Gallery")
    st.caption("过去一年，我们走过的地方")

    g1,g2,g3 = st.columns(3)

    with g1:
        st.image(
            "images/wenzhou.jpg",
            use_container_width=True
        )

        st.caption("温州")

        st.image(
            "images/午朝门.jpg",
            use_container_width=True
        )

        st.caption("午朝门")

    with g2:
        st.image(
            "images/星光集市.jpg",
            use_container_width=True
        )

        st.caption("星光集市")

        st.image(
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
            use_container_width=True
        )

        st.caption("测试图片")

    with g3:
        st.image(
            "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
            use_container_width=True
        )

        st.caption("测试图片")

        st.image(
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
            use_container_width=True
        )

        st.caption("测试图片")

    st.divider()

    # =========================
    # 关于我们
    # =========================

    st.markdown("## 🏛 关于我们")

    with st.expander("📌 社团简介", expanded=False):
        st.write("""
南京大学地理协会成立于2025年。

协会以“地理无界 · 世界相连”为宗旨，
致力于通过实地考察、城市漫步、学术讲座与地图制作，
帮助同学们理解人与土地、历史与空间之间的关系。
""")

    with st.expander("🏢 组织架构", expanded=False):
        st.markdown("""
### 活动部
路线设计、踩点与活动执行

### 宣传部
公众号运营、摄影摄像、海报设计

### 学术部
讲座策划、科普写作、GIS交流

### 联络部
嘉宾邀请、对外合作

### 办公室
财务、物资、志愿时长管理
""")

    #with st.expander("👥 人员构成", expanded=False):
      #  st.markdown("""

#""")

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

<div style="box-sizing: border-box; width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 16px; display: flex; align-items: center; backdrop-filter: blur(10px);">
<span style="font-size: 20px; margin-right: 15px; flex-shrink: 0;">💬</span>
<div style="display: flex; flex-direction: column; overflow: hidden;">
<span style="color: #94a3b8; font-size: 12px; font-weight: 600; white-space: nowrap;">官方招新 QQ 群</span>
<span style="color: #ffffff; font-size: 16px; font-weight: 700; word-break: break-all;">720915627</span>
</div>
</div>

<div style="box-sizing: border-box; width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 16px; display: flex; align-items: center; backdrop-filter: blur(10px);">
<span style="font-size: 20px; margin-right: 15px; flex-shrink: 0;">📱</span>
<div style="display: flex; flex-direction: column; overflow: hidden;">
<span style="color: #94a3b8; font-size: 12px; font-weight: 600; white-space: nowrap;">微信公众号</span>
<span style="color: #ffffff; font-size: 16px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">山河南观</span>
</div>
</div>

<div style="box-sizing: border-box; width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 12px 20px; border-radius: 16px; display: flex; align-items: center; backdrop-filter: blur(10px);">
<span style="font-size: 20px; margin-right: 15px; flex-shrink: 0;">📕</span>
<div style="display: flex; flex-direction: column; overflow: hidden;">
<span style="color: #94a3b8; font-size: 12px; font-weight: 600; white-space: nowrap;">小红书账号</span>
<span style="color: #ffffff; font-size: 16px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">南大地理协会</span>
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