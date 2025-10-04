import streamlit as st
import json
from datetime import datetime
from difflib import SequenceMatcher

# 設定頁面
st.set_page_config(
    page_title="AI職涯規劃助手",
    page_icon="🎯",
    layout="wide"
)

# 職業家族分組
CAREER_FAMILIES = {
    "軟體開發": ["15-1252", "15-1255", "15-1253", "15-1299.10"],
    "資料科學": ["15-1211", "15-1299", "15-1299.11"],
    "網路技術": ["15-1244", "15-1232", "15-1299.09"],
    "設計創意": ["15-1299.07", "27-1024", "27-1014", "27-1025", "27-4032", "27-4014", "27-1024.01"],
    "半導體工程": ["17-2199.09", "17-2072", "17-2061"],
    "電機機械": ["17-2071", "17-2061", "17-2112"],
    "維修服務": ["49-9071", "17-3023", "47-2061"],
    "商業管理": ["11-2021", "11-9199", "13-1111", "11-3012"],
    "金融會計": ["13-2051", "13-2011"],
    "業務行銷": ["41-4012", "11-2021", "43-9199", "27-3031"],
    "醫療照護": ["29-1141", "29-1071", "29-1122", "31-1120", "29-2061", "31-9092"],
    "教育培訓": ["25-3021", "25-2021", "25-3099", "25-9031", "21-1012", "25-3099.02"],
    "內容創作": ["27-3042", "27-3099.01", "27-3043"],
    "電商副業": ["41-9099.01", "41-2099", "43-9199", "27-1024.01"],
}


CAREERS = {
    # 科技類 (10個)
    "15-1252": {
        "title": "軟體開發工程師",
        "keywords": [
            # 通用
            "programming", "coding", "software", "developer", "程式", "開發", "軟體",
            # 語言
            "python", "java", "javascript", "c++", "go", "rust", "typescript",
            # 技術
            "api", "backend", "frontend", "fullstack", "全端", "後端", "前端",
            "git", "github", "版本控制", "debug", "測試", "部署"
        ],
        "type": "full_time",
        "skills": ["Python/Java", "演算法", "Git", "API設計"],
        "salary_tw": "60-150K",
        "growth": "22%"
    },
    "15-1299": {
        "title": "AI/機器學習工程師",
        "keywords": [
            "ai", "machine learning", "deep learning", "ml", "人工智慧", "機器學習",
            "tensorflow", "pytorch", "keras", "scikit-learn",
            "neural network", "nlp", "computer vision", "神經網路", "自然語言",
            "hugging face", "transformers", "llm", "大型語言模型"
        ],
        "type": "full_time",
        "skills": ["Python ML", "數學統計", "深度學習", "雲端部署"],
        "salary_tw": "70-200K",
        "growth": "35%"
    },
    "15-1211": {
        "title": "數據分析師",
        "keywords": [
            "data", "analysis", "analytics", "數據", "分析", "資料",
            "sql", "excel", "tableau", "power bi", "視覺化",
            "統計", "statistics", "pandas", "numpy", "報表", "dashboard"
        ],
        "type": "full_time",
        "skills": ["SQL", "Python/R", "視覺化工具", "統計學"],
        "salary_tw": "55-130K",
        "growth": "25%"
    },
    "15-1255": {
        "title": "網頁開發者",
        "keywords": [
            "web", "website", "html", "css", "javascript", "網頁", "前端",
            "react", "vue", "angular", "next.js", "tailwind",
            "responsive", "ui", "響應式", "介面"
        ],
        "type": "full_time",
        "skills": ["HTML/CSS", "JavaScript", "React/Vue", "RWD"],
        "salary_tw": "50-120K",
        "growth": "13%"
    },

    # 工程類（擴充關鍵字）
    "49-9071": {
        "title": "維修技術員",
        "keywords": [
            # 通用
            "maintenance", "technician", "repair", "維修", "技師", "修理",
            # 水電專業
            "水電", "plumbing", "配線", "electrical wiring", "水管", "管路",
            "抓漏", "leak detection", "裝修", "installation",
            # 設備
            "冷氣", "air conditioning", "家電", "appliances", "馬桶", "toilet",
            "故障排除", "troubleshooting", "保養", "維護"
        ],
        "type": "both",
        "skills": ["故障診斷", "工具使用", "安全規範", "客戶溝通"],
        "salary_tw": "35-80K",
        "growth": "8%"
    },
    "17-2072": {
        "title": "電子工程師",
        "keywords": [
            "electronics", "circuits", "pcb", "電子", "電路",
            "嵌入式", "embedded", "arduino", "raspberry pi",
            "焊接", "soldering", "示波器", "oscilloscope", "設計驗證"
        ],
        "type": "full_time",
        "skills": ["電路設計", "PCB布局", "嵌入式系統", "測試驗證"],
        "salary_tw": "60-140K",
        "growth": "7%"
    },
    "17-2199.09": {
        "title": "半導體製程工程師",
        "keywords": [
            "semiconductor", "fab", "tsmc", "半導體", "晶圓", "台積電",
            "製程", "process", "良率", "yield", "設備", "equipment",
            "蝕刻", "etching", "微影", "lithography", "薄膜", "thin film"
        ],
        "type": "full_time",
        "skills": ["製程控制", "良率分析", "設備操作", "SPC統計"],
        "salary_tw": "65-150K",
        "growth": "12%"
    },

    # 商業金融
    "13-2051": {
        "title": "金融分析師",
        "keywords": [
            "finance", "investment", "analyst", "金融", "投資", "分析師",
            "財務模型", "financial modeling", "評價", "valuation",
            "excel", "bloomberg", "股票", "債券", "基金", "fund"
        ],
        "type": "both",
        "skills": ["財務模型", "Excel VBA", "投資評價", "產業研究"],
        "salary_tw": "60-180K",
        "growth": "11%"
    },
    "11-2021": {
        "title": "行銷經理",
        "keywords": [
            "marketing", "brand", "digital", "行銷", "品牌", "數位",
            "seo", "sem", "google ads", "facebook ads", "廣告",
            "社群", "social media", "內容", "content", "策略"
        ],
        "type": "both",
        "skills": ["數位行銷", "數據分析", "社群經營", "品牌策略"],
        "salary_tw": "60-180K",
        "growth": "13%"
    },

    # 醫療健康
    "29-1141": {
        "title": "註冊護理師",
        "keywords": [
            "nurse", "rn", "healthcare", "護理", "照護", "護士",
            "病患", "patient care", "急救", "emergency", "用藥", "medication",
            "ICU", "急診", "住院", "衛教"
        ],
        "type": "full_time",
        "skills": ["病患照護", "急救技能", "用藥管理", "醫療記錄"],
        "salary_tw": "45-90K",
        "growth": "9%"
    },
    "31-1120": {
        "title": "居家照護助理",
        "keywords": [
            "home health", "caregiver", "elderly", "照服員", "長照", "看護",
            "失能", "disability", "老人", "elderly care", "陪伴", "companion",
            "日常照護", "ADL", "協助", "assistance"
        ],
        "type": "both",
        "skills": ["基礎照護", "生活協助", "陪伴溝通", "緊急應變"],
        "salary_tw": "30-60K",
        "growth": "34%"
    },

    # 教育培訓
    "25-3021": {
        "title": "自雇教師/補習班老師",
        "keywords": [
            "tutor", "teacher", "education", "家教", "補習", "教學",
            "數學", "英文", "物理", "化學", "國文", "升學",
            "課輔", "tutoring", "一對一", "小班", "線上教學"
        ],
        "type": "both",
        "skills": ["學科專業", "教學技巧", "班級管理", "溝通能力"],
        "salary_tw": "40-150K",
        "growth": "8%"
    },
    "25-3099.02": {
        "title": "線上家教",
        "keywords": [
            "online tutor", "remote teaching", "線上教學", "遠距",
            "zoom", "google meet", "語言", "programming", "程式教學",
            "英文", "日文", "python教學", "數學線上"
        ],
        "type": "side_hustle",
        "skills": ["視訊教學", "數位工具", "課程設計", "互動技巧"],
        "income_tw": "10-60K",
        "time": "3-15h"
    },

    # 創意設計
    "27-1024": {
        "title": "平面設計師",
        "keywords": [
            "graphic design", "designer", "平面設計", "美編",
            "illustrator", "photoshop", "indesign", "ai", "ps",
            "logo", "海報", "排版", "品牌", "視覺設計"
        ],
        "type": "both",
        "skills": ["AI/PS", "排版設計", "品牌識別", "印刷知識"],
        "salary_tw": "40-120K",
        "growth": "5%"
    },
    "27-4032": {
        "title": "影片編輯",
        "keywords": [
            "video editor", "editing", "剪輯", "影片",
            "premiere", "final cut", "davinci resolve", "調色",
            "youtube", "短影音", "tiktok", "reels", "特效"
        ],
        "type": "both",
        "skills": ["Premiere/Final Cut", "調色", "音效處理", "節奏掌控"],
        "salary_tw": "40-120K",
        "growth": "18%"
    },

    # 副業專區
    "27-3042": {
        "title": "自由撰稿人",
        "keywords": [
            "freelance writer", "blogger", "writing", "寫作", "文案",
            "部落格", "medium", "matters", "seo文章", "內容創作",
            "撰稿", "編輯", "稿件", "投稿"
        ],
        "type": "side_hustle",
        "skills": ["寫作能力", "SEO知識", "研究能力", "時間管理"],
        "income_tw": "5-50K",
        "time": "3-10h"
    },
    "27-3099.01": {
        "title": "YouTuber/內容創作者",
        "keywords": [
            "youtuber", "content creator", "influencer", "創作者", "網紅",
            "拍片", "剪輯", "直播", "streaming", "訂閱",
            "youtube", "tiktok", "instagram", "shorts", "抖音"
        ],
        "type": "side_hustle",
        "skills": ["影片製作", "社群經營", "創意發想", "持續產出"],
        "income_tw": "0-100K+",
        "time": "5-20h"
    },
    "41-9099.01": {
        "title": "聯盟行銷者",
        "keywords": [
            "affiliate marketing", "聯盟行銷", "推廣",
            "amazon associate", "博客來", "momo", "推薦連結",
            "部落格變現", "流量", "轉換率", "佣金"
        ],
        "type": "side_hustle",
        "skills": ["內容創作", "SEO", "流量分析", "轉換優化"],
        "income_tw": "2-30K",
        "time": "2-8h"
    },
    "27-1024.01": {
        "title": "POD設計師",
        "keywords": [
            "print on demand", "pod", "merch", "商品設計",
            "redbubble", "teespring", "printful", "etsy",
            "t恤設計", "貼紙", "杯子", "手機殼", "被動收入"
        ],
        "type": "side_hustle",
        "skills": ["平面設計", "趨勢研究", "電商平台", "行銷推廣"],
        "income_tw": "3-40K",
        "time": "4-10h"
    },
    "41-2099": {
        "title": "蝦皮/網拍賣家",
        "keywords": [
            "reseller", "ecommerce", "網拍", "電商", "賣家",
            "shopee", "蝦皮", "pchome", "露天", "yahoo",
            "選品", "批貨", "dropshipping", "代購", "轉售"
        ],
        "type": "side_hustle",
        "skills": ["選品眼光", "商品攝影", "客服", "物流管理"],
        "income_tw": "5-50K",
        "time": "5-15h"
    },
    "15-1299.10": {
        "title": "自由接案工程師",
        "keywords": [
            "freelance developer", "contractor", "接案", "外包",
            "upwork", "fiverr", "freelancer", "遠距接案",
            "網站開發", "app開發", "scraping", "爬蟲", "api串接"
        ],
        "type": "side_hustle",
        "skills": ["程式開發", "專案管理", "客戶溝通", "報價估算"],
        "income_tw": "20-100K",
        "time": "5-20h"
    },
}


def enhanced_keyword_match(user_input, keywords, boost_factor=1.0):
    """增強關鍵字匹配"""
    user_input_lower = user_input.lower()
    matches = 0

    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in user_input_lower:
            matches += 1.5 * boost_factor
            continue

        for user_word in user_input_lower.split():
            user_word = user_word.strip(",，、")
            if len(user_word) < 2:
                continue

            if user_word == keyword_lower:
                matches += 1.2 * boost_factor
                continue

            if len(user_word) >= 3:
                similarity = SequenceMatcher(None, keyword_lower, user_word).ratio()
                if similarity > 0.7:
                    matches += 0.8 * boost_factor
                elif similarity > 0.5:
                    matches += 0.4 * boost_factor

    return matches


def get_career_family_bonus(career_code, matched_codes):
    """同家族職業加分"""
    bonus = 0
    for family, codes in CAREER_FAMILIES.items():
        if career_code in codes:
            family_matches = [c for c in matched_codes if c in codes and c != career_code]
            if family_matches:
                bonus = min(len(family_matches) * 5, 15)
    return bonus


def calculate_smart_match(skills, interests, goals, hours):
    """智能匹配算法"""
    all_matches = []
    high_score_codes = []

    for code, career in CAREERS.items():
        score = 0

        # 技能匹配 (40%)
        skill_matches = enhanced_keyword_match(skills, career["keywords"], boost_factor=1.2)
        score += min(skill_matches * 10, 40)

        # 興趣匹配 (25%)
        interest_matches = enhanced_keyword_match(interests, career["keywords"])
        score += min(interest_matches * 8, 25)

        # 目標匹配 (25%)
        if career["title"] in goals:
            score += 25
        else:
            goal_matches = enhanced_keyword_match(goals, career["keywords"])
            score += min(goal_matches * 8, 20)

        # 職業類型適配性 (10%)
        if career["type"] == "side_hustle":
            if hours >= 5:
                score += 10
            elif hours >= 3:
                score += 5
        elif career["type"] == "both":
            if hours >= 10:
                score += 10
            elif hours >= 5:
                score += 7
        elif career["type"] == "full_time":
            score += 5

        career["match_score"] = min(int(score), 100)
        all_matches.append((code, career))

        if career["match_score"] >= 30:
            high_score_codes.append(code)

    # 家族加分
    for code, career in all_matches:
        family_bonus = get_career_family_bonus(code, high_score_codes)
        career["match_score"] = min(career["match_score"] + family_bonus, 100)

    # 分類排序
    full_time = [(c, i) for c, i in all_matches if i["type"] == "full_time"]
    side_hustle = [(c, i) for c, i in all_matches if i["type"] == "side_hustle"]
    both = [(c, i) for c, i in all_matches if i["type"] == "both"]

    full_time.sort(key=lambda x: x[1]["match_score"], reverse=True)
    side_hustle.sort(key=lambda x: x[1]["match_score"], reverse=True)
    both.sort(key=lambda x: x[1]["match_score"], reverse=True)

    return full_time, side_hustle, both


def filter_by_time(careers, available_hours):
    """根據時間篩選副業"""
    suitable = []
    for code, career in careers:
        time_str = career.get("time", "3-10h")
        try:
            min_time = int(time_str.split("-")[0].replace("h", ""))
        except (ValueError, IndexError):
            min_time = 3

        if career["match_score"] > 20 and min_time <= available_hours + 2:
            suitable.append((code, career))

    if not suitable:
        for code, career in careers:
            time_str = career.get("time", "3-10h")
            try:
                min_time = int(time_str.split("-")[0].replace("h", ""))
            except:
                min_time = 3
            if career["match_score"] > 10 and min_time <= 10:
                suitable.append((code, career))

    return suitable


# ===== Streamlit UI =====

st.title("🎯 AI職涯規劃助手")
st.markdown("### 找到適合你的正職與副業")

# 側邊欄輸入
with st.sidebar:
    st.header("📝 填寫你的資料")
    name = st.text_input("姓名（可匿名）", value="匿名使用者")
    age = st.number_input("年齡", min_value=15, max_value=80, value=25)
    education = st.text_input("教育背景", placeholder="例如：資工系、高中畢業")

    st.markdown("---")
    st.markdown("**請詳細描述**（越詳細越準確）")
    skills = st.text_area(
        "💪 技能",
        placeholder="軟體：Python, Java, React\n水電：配線, 水管維修, 抓漏\n設計：Photoshop, 平面設計",
        height=100
    )
    interests = st.text_area(
        "❤️ 興趣",
        placeholder="例如：科技、教育、創意、維修",
        height=80
    )
    goals = st.text_area(
        "🎯 目標",
        placeholder="例如：成為工程師、遠距工作、增加收入",
        height=80
    )

    st.markdown("---")
    hours = st.slider("⏰ 每週可用於副業時數", 0, 50, 10)
    leisure_usage = st.text_input("時間用途", placeholder="例如：學習、賺錢、興趣")

    analyze_btn = st.button("🚀 開始分析", type="primary", use_container_width=True)

# 主要內容區
if analyze_btn:
    if not skills or not interests or not goals:
        st.warning("⚠️ 請填寫完整資料（技能、興趣、目標）")
    else:
        with st.spinner("分析中..."):
            # 使用原本的匹配算法
            full_time, side_hustle, both = calculate_smart_match(
                skills.lower(),
                interests.lower(),
                goals.lower(),
                hours
            )

            # 篩選副業
            suitable_sides = filter_by_time(side_hustle + both, hours)

            st.success("✅ 分析完成！")

            # Top推薦
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🏆 推薦正職")
                if full_time and full_time[0][1]["match_score"] > 0:
                    best = full_time[0][1]
                    st.metric("職業", best["title"], f"匹配度 {best['match_score']}%")
                    st.info(f"💰 薪資：{best.get('salary_tw', 'N/A')}/月  \n📈 成長率：{best.get('growth', 'N/A')}")
                    if "skills" in best:
                        st.caption(f"核心技能：{', '.join(best['skills'][:3])}")
                else:
                    st.warning("未找到高匹配正職，建議調整技能描述")

            with col2:
                st.markdown("### 💼 推薦副業")
                if suitable_sides and suitable_sides[0][1]["match_score"] > 0:
                    best_side = suitable_sides[0][1]
                    st.metric("副業", best_side["title"], f"匹配度 {best_side['match_score']}%")
                    time_req = best_side.get('time', '3-10h')
                    income = best_side.get('income_tw', best_side.get('salary_tw', 'N/A'))
                    st.info(f"⏰ 時間：{time_req}/週  \n💵 收入：{income}/月")
                    if "skills" in best_side:
                        st.caption(f"核心技能：{', '.join(best_side['skills'][:3])}")
                else:
                    if hours < 3:
                        st.warning(f"你的時間較少（{hours}h/週），建議增加到至少3小時")
                    else:
                        st.warning("未找到高匹配副業，建議擴充技能或調整目標")

            # 完整清單
            st.markdown("---")
            st.markdown("### 📊 完整匹配清單（Top 15）")

            all_results = full_time + both + side_hustle
            all_results.sort(key=lambda x: x[1]['match_score'], reverse=True)

            for i, (code, career) in enumerate(all_results[:15], 1):
                if career['match_score'] > 0:
                    type_emoji = {"full_time": "💼", "side_hustle": "🎯", "both": "⚡"}
                    type_label = {"full_time": "正職", "side_hustle": "副業", "both": "兩可"}

                    with st.expander(f"{type_emoji[career['type']]} {i}. {career['title']} - {career['match_score']}%"):
                        st.write(f"**類型**：{type_label[career['type']]}")

                        if career['type'] in ['full_time', 'both']:
                            st.write(f"**薪資**：{career.get('salary_tw', 'N/A')}/月")
                            st.write(f"**成長率**：{career.get('growth', 'N/A')}")

                        if career['type'] in ['side_hustle', 'both']:
                            st.write(f"**時間需求**：{career.get('time', '3-10h')}/週")
                            if 'income_tw' in career:
                                st.write(f"**收入潛力**：{career['income_tw']}/月")

                        if 'skills' in career and career['skills']:
                            st.write(f"**核心技能**：{', '.join(career['skills'])}")

            # 反饋區
            st.markdown("---")
            st.markdown("### 💬 使用反饋")

            col1, col2 = st.columns([2, 1])
            with col1:
                satisfaction = st.radio(
                    "推薦結果是否符合預期？",
                    ["非常滿意😊", "滿意👍", "普通😐", "不滿意😞"],
                    horizontal=True
                )
            with col2:
                would_pay = st.checkbox("願意為更詳細報告付費（NT$99-299）")

            feedback = st.text_area("其他建議或意見", placeholder="請分享你的想法...")

            if st.button("提交反饋", type="primary"):
                feedback_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "satisfaction": satisfaction,
                    "would_pay": would_pay,
                    "feedback": feedback,
                    "top_full": full_time[0][1]["title"] if full_time else "無",
                    "top_side": suitable_sides[0][1]["title"] if suitable_sides else "無",
                    "skills": skills[:100],
                    "goals": goals[:100]
                }

                try:
                    with open("feedback.json", "a", encoding="utf-8") as f:
                        json.dump(feedback_data, f, ensure_ascii=False)
                        f.write("\n")
                    st.success("✅ 感謝你的反饋！")
                except:
                    st.info("反饋已記錄（本地測試模式）")

else:
    # 歡迎頁面
    st.markdown("""
    ## 歡迎使用 AI 職涯規劃助手！

    ### 這個工具能幫你：
    - 🎯 找到適合的正職方向（基於50+職業資料庫）
    - 💼 推薦合適的副業選項（考慮你的時間）
    - 📊 智能語意匹配（支援模糊搜尋和家族推薦）

    ### 使用步驟：
    1. 在左側**詳細**填寫你的資料
    2. 描述越具體，推薦越準確
    3. 點擊「開始分析」

    **提示**：可以用中文或英文描述技能
    """)

    # 範例
    with st.expander("💡 查看填寫範例"):
        st.markdown("""
        **技能範例**：
        - 軟體：Python, JavaScript, React, 網頁開發
        - 維修：水電維修, 配線, 水管, 抓漏, 冷氣
        - 設計：Photoshop, Illustrator, 平面設計, 排版
        - 分析：Excel, SQL, 數據分析, 報表

        **興趣範例**：
        - 科技、程式設計、解決問題、自動化
        - 創意、視覺設計、美學、品牌
        - 教育、分享知識、幫助他人
        - 維修、動手做、解決實際問題

        **目標範例**：
        - 成為軟體工程師，想要遠距工作
        - 增加收入，發展副業賺錢
        - 轉職到科技業，學習新技能
        - 做自己喜歡的事，時間彈性
        """)

    st.info("💡 **開發者測試模式**：填寫後可在反饋區勾選「願意付費」來幫助驗證商業模式")

# 頁尾
st.markdown("---")
st.caption("*本工具基於O*NET職業分類系統 | v6.0 智能語意匹配*")
