# utils.py

# ==========================================
# 1. 网站展示用数据 (保持原样)
# ==========================================
ACTIVITY_DATA = [
    {"title": "⛰️ 2024 紫金山春季毅行", "date": "2024-04-15", "status": "报名中", "desc": "南京大学地理协会传统项目！从仙林校区出发，登顶紫金山，领略南京地貌之美。免费提供饮用水和向导。集合地点：仙林校区方肇周体育馆门前。"},
    {"title": "🌍 趣味地理知识竞赛", "date": "2024-05-10", "status": "筹备中", "desc": "不限院系！寻找南大最懂地理的你。一等奖可获赠精美地球仪一台及大疆无人机体验券。"},
]

# utils.py

# ==========================================
# 核心改变：把原本的 [] 变成了 {}，支持无限个专栏分区！
# ==========================================
ARTICLE_DATA = {
    "🌅 九州风物系列": [
        {
            "title": "话说温州：一片繁华海上头", 
            "author": "王瓯", 
            "date":"2026年4月9日",
            "summary": "形散而神不散，才是这片被嶙峋地形、曲折水道所切割的土地的状态。本文从地理视角带你重新认识温州。",
            "url": "https://mp.weixin.qq.com/s/076ZCx_8UUuihcRr7U8f4w",
            "url_image": "https://mmbiz.qpic.cn/mmbiz_jpg/ODzib5gpRWTxqdcPr1Bpkb4D6frzMVFRllWzPFcCzo6sYia0Izwia7JbdI2eJzLePpkvgz7ajbs6NcYlOsaZN4CianYqmI7yLv6skJPAkxKRDw4/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1"
        },
        {
            "title": "从南大出发，探寻中国最美丹霞地貌", 
            "author": "宣传部", 
            "date":"2026年4月9日",
            "summary": "本期推文带你走进张掖，用地理学的视角解构色彩斑斓的丹霞奇观...",
            "url": "https://mp.weixin.qq.com/",
            "url_image": "https://mmbiz.qpic.cn/mmbiz_jpg/ODzib5gpRWTxqdcPr1Bpkb4D6frzMVFRllWzPFcCzo6sYia0Izwia7JbdI2eJzLePpkvgz7ajbs6NcYlOsaZN4CianYqmI7yLv6skJPAkxKRDw4/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1"
        }
    ],
    "💻 GIS 技能工坊": [
        {
            "title": "GIS 软件零基础入门指南（上）", 
            "author": "学术部", 
            "date":"2026年4月9日",
            "summary": "很多同学问如何画出高大上的地图？本期手把手教你安装和使用 ArcGIS...",
            "url": "https://mp.weixin.qq.com/",
            "url_image": "https://mmbiz.qpic.cn/mmbiz_jpg/ODzib5gpRWTxqdcPr1Bpkb4D6frzMVFRllWzPFcCzo6sYia0Izwia7JbdI2eJzLePpkvgz7ajbs6NcYlOsaZN4CianYqmI7yLv6skJPAkxKRDw4/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1"
        }
    ],
    "👣 行走南大 (活动回顾)": [
        {
            "title": "紫金山毅行回顾：用脚步丈量春天", 
            "author": "活动部", 
            "date":"2026年4月9日",
            "summary": "上周末，我们和百名南大同学一起登顶紫金山，来看前方发回的绝美照片！",
            "url": "https://mp.weixin.qq.com/",
            "url_image": "https://mmbiz.qpic.cn/mmbiz_jpg/ODzib5gpRWTxqdcPr1Bpkb4D6frzMVFRllWzPFcCzo6sYia0Izwia7JbdI2eJzLePpkvgz7ajbs6NcYlOsaZN4CianYqmI7yLv6skJPAkxKRDw4/640?wx_fmt=jpeg&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1"
        }
    ]
}



# ==========================================
# 2. 地协核心万字知识库 (AI 的超级大脑)
# ==========================================
# 把你的招新长文存为一个长字符串
NJUGA_CORE_KNOWLEDGE = """
【核心精神】：丈量祖国大地，普及地理科学。用空间的逻辑理解时间，用土地的肌理解读文明。不打卡景点，打捞附近。不生产攻略，生产理解。
【过往足迹-南京篇】：
1. 玄武湖：探访明代黄册库遗址、武庙闸水利智慧。
2. 津浦铁路(浦口火车站)：了解唐山工人南下移民史，追寻朱自清《背影》的发生地。
3. 雨花台：从高座寺到烈士陵园，理解精神高地与集体记忆。
4. 白下区：在消失的行政区划里，解码城市街道命名学。
5. 钟山：从中山植物园到无梁殿，在草木间读懂六朝古意与近代风云。
【过往足迹-远方篇】：
1. 苏州：探访老城街巷与南大苏州校区，环游西山岛看乡村振兴。
2. 宁夏：贺兰山下酒庄、西夏陵、石嘴山洗煤厂，进行真实的田野调查。
【特色产出】：绘制过《南大仙林咖啡地图》、《桂花地图》、《南京市赏花地图》。
【招新要求】：欢迎所有专业、所有年级。不需要背诵山川河流，只需要好奇心。
【五大部门介绍】：
1. 活动部：策划执行，路线设计踩点，解决现场问题。
2. 宣传部：海报设计，推文撰写，摄影剪辑，新媒体运营。
3. 学术部：学术讲座策划，科普材料撰写，专业地理/GIS知识探讨。
4. 联络部：对外沟通，邀请嘉宾，社团合作联络。
5. 办公室：物资准备，财务报销，志愿时长录入，后勤保障。
【加入福利】：志同道合的朋友、实用技能培训(PS/PR/推文/策划)、志愿时长、活动优先报名。
"""

def get_association_knowledge_base() -> str:
    """
    组装喂给 AI 的提示词 (动态组装版 - 支持专栏分类)
    """
    kb = "你现在是南京大学地理协会(NJUGA)的官方AI智能答疑小助手。\n"
    kb += "你的任务是热情、准确地回答同学们关于协会的提问。你的语气应该像一个亲切的学长/学姐。\n"
    kb += "以下是关于协会的全部权威信息。当同学问及相关内容时，请基于以下信息进行解答：\n\n"
    kb += NJUGA_CORE_KNOWLEDGE
    
    # 注入【最新活动】数据
    kb += "\n\n【最新动态与活动通知（重要！）】：\n"
    if not ACTIVITY_DATA:
        kb += "当前暂无最新活动。\n"
    else:
        for act in ACTIVITY_DATA:
            kb += f"- 活动名称：{act['title']}\n  举办时间：{act['date']}\n  当前状态：{act['status']}\n  详细介绍：{act['desc']}\n"
            
    # 👇 修改了这里：让 AI 知道推文是分了专栏的
    kb += "\n【往期精选推文（已分类，如果同学问起相关资料，请把链接直接发给他们）】：\n"
    if not ARTICLE_DATA:
        kb += "当前暂无推文。\n"
    else:
        # .items() 可以同时拿出专栏名字(category)和里面的文章列表(articles)
        for category, articles in ARTICLE_DATA.items():
            kb += f"\n--- 专栏：{category} ---\n"
            for art in articles:
                kb += f"- 推文标题：《{art['title']}》\n"
                kb += f"  作者：{art['author']}\n"
                kb += f"  摘要：{art['summary']}\n"
                if "url" in art:
                    kb += f"  原文链接：{art['url']}\n"
                
    return kb