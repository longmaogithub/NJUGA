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
    # 卷首语：极具氛围感的引入
    st.markdown("### ✨ 认识我们：解锁城市的隐藏图层")
    st.info("""
    > *你有没有想过——你每天在玄武湖畔散步，可能正踩过明代黄册库的遗址；你在浦口火车站拍照，镜头里漏掉了整个20世纪的移民史诗；你在钟山的林间走过，可能错过了地层里叠压的六朝古意与近代风云。*
    > 
    > **这座城市还有很多图层没被打开。而我们，需要更多一起解锁它的人。**
    """)
    
    st.divider() # 分割线
    
    # 第一部分：年度回顾 (使用两列布局)
    st.markdown("#### 📍 一、这一年，我们打开了这些图层")
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
    
    # 第二 & 第三部分：远行与制图
    st.markdown("#### 🗺️ 二、山河作为课堂 & 绘制专属地图")
    st.markdown("""
    我们的探索，从来不止于南京。去年端午，我们穿行**苏州**老城，在太湖之畔读懂生态保护；去年盛夏，我们奔赴**宁夏**贺兰山下，在石嘴山洗煤厂追问黑金之城的涅槃。这不是走马观花的旅游，而是奔赴真实现场的田野调查。
    
    不止用脚步丈量，我们还将地理信息转化为可触摸的地图。过去一年，我们绘制了：
    ☕ 《南大仙林咖啡地图》 | 🍂 《南大仙林桂花地图》 | 🌺 《南京市赏花地图》
    """)
    
    st.divider()

    # 第四部分：招募宣言 (高亮显示)
    st.success("""
    #### 👋 现在，我们需要你！
    你可能会问：**我不是地理专业的，能加入吗？**
    **能！** 我们欢迎所有专业、所有年级。地理不是门槛，好奇才是。我们只教你一种方法：**用空间的逻辑理解时间，用土地的肌理解读文明。**
    
    **加入后，你将获得：**
    1. 👁️ **独家的城市视角**：看懂水利智慧与空间逻辑。
    2. 🗺️ **现成的探索路线**：不用做攻略，带上好奇心跟着走。
    3. 🛤️ **走出校园的机会**：从周末 Citywalk 到暑期社会实践。
    4. ✍️ **内容创作的舞台**：你的文字、摄影、地图将成为南大的集体记忆。
    """)
    
    st.divider()

    # 附录：部门介绍 (使用折叠面板，节省空间又清晰)
    st.markdown("#### 🏢 附录 | 五大核心部门简介")
    st.markdown("无论你是否有经验，只要愿意认真做一件事，我们都期待你的到来。")
    
    with st.expander("🏃‍♂️ 活动部 | 山川未涉，筹画先成"):
        st.write("负责协会活动的策划与执行，是把想法落到现实的一线部门。从路线设计、踩点联络到现场组织，如果你喜欢解决问题、喜欢热闹，欢迎加入。")
    with st.expander("📸 宣传部 | 山河可观，风物当书"):
        st.write("记录每一次行走与相遇。负责海报设计、公众号推送、摄影摄像与视频剪辑。如果你喜欢文字、设计或讲故事，欢迎加入。")
    with st.expander("📖 学术部 | 既可游目，尤宜穷理"):
        st.write("协会“地理味”最浓的部门。负责学术讲座策划、科普材料撰写，协助把游历观察转化为系统的知识表达。对地理和 GIS 感兴趣的同学首选。")
    with st.expander("🤝 联络部 | 延师问道，会友联群"):
        st.write("负责对内对外的沟通协调，对接老师、嘉宾和合作机构。如果你乐于沟通、做事稳妥，喜欢连接资源，欢迎加入。")
    with st.expander("💼 办公室 | 庶务有经，斯志可久"):
        st.write("负责日常事务、物资准备、财务报销和志愿时长录入，是社团稳定运转的基石。如果你细心认真、责任感强，欢迎加入。")

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