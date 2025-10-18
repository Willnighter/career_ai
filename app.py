import streamlit as st
from styles.responsive import get_responsive_css, get_theme_css
import json
from datetime import datetime
from openai import OpenAI

# ===== 初始化 OpenAI =====

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    st.write("✅ 成功初始化 OpenAI client")
except KeyError:
    st.error("⚠️ 找不到 OPENAI_API_KEY。\n請在 Streamlit Cloud 的 Secrets Manager 或 `.streamlit/secrets.toml` 設定它。")
    st.stop()

def analyze_career(skills, interests, goals, education_background, work_experience,
                   languages, hours):
    """使用 OpenAI API 分析職涯"""
    
    system_prompt = """你是專業的國際職涯顧問，擅長分析個人優勢並提供跨國就業與接案建議。

    **回答規則：**
    1. 必須以繁體中文回答
    2. 正職薪資建議：
       - 根據使用者的學經歷背景判斷市場（台灣/海外遠端/特定國家）
       - 如有國外學歷或相關經驗，優先推薦國際遠端或當地就業機會
       - 明確標註幣別與市場（例如：台灣 TWD 4-6萬/美國遠端 USD 4000-6000)
    3. 副業收入分析方法：
       - 興趣佔 30%：評估長期投入意願與熱情
       - 技能佔 70%：評估變現能力與市場競爭力
       - 根據此權重給出「短期可行」vs「需培養」的建議
       - 列出對應市場的接案行情（台灣、國際平台如 Upwork/Fiverr)
    4. 目標具體化處理（重要）：
       - 如果使用者目標模糊（如「財富自由」、「成功」、「賺很多錢」）：
         * 先在 key_recommendation 定義具體指標（例如：財富自由 = 被動收入月10萬)
         * 計算達成時間軸（保守估計，不要過度樂觀）
         * 拆解成可量化的階段性目標
       - 如果目標與現況差距大(超過5年):
         * 必須提供「現實檢查」：指出差距
         * 給出3-6個月、1-2年、3-5年的階段計畫
         * 明確哪些是「必須優先做」vs「長期目標」
    5. 財務建議的現實原則：
       - 副業收入預估要保守（不要給太樂觀的數字）
       - 投資報酬率假設 8-12%(不要超過15%)
       - 財富自由門檻:假設月被動收入需求為使用者目前支出的1.5-2倍
       - 時間軸要實際：一般人財富自由需要 10-20 年
    6. 回答格式必須是有效的 JSON
    7. 所有建議需具體、可執行、有時間軸
    
    **JSON 格式範例：**
    {
        "main_job": {
            "title": "職稱",
            "market": "建議就業市場",
            "match_reason": ["原因1", "原因2", "原因3"],
            "required_skills": ["已具備技能", "需補強技能"],
            "salary_range": "月薪範圍（含幣別）",
            "growth_potential": "發展潛力與升遷路徑"
        },
        "side_hustle": {
            "project": "副業項目",
            "interest_match": 85,
            "skill_match": 70,
            "weighted_score": 75,
            "time_needed": "每週X小時",
            "estimated_income": {
                "taiwan": "台灣接案行情(TWD/月）",
                "international": "國際平台行情(USD/月）"
            },
            "difficulty": "上手難度",
            "monetization_timeline": "預估多久開始有收入"
        },
        "alternatives": [
            {"option": "選項1", "brief": "說明", "fit_score": 80}
        ],
        "goal_gap_analysis": {
            "current_position": "目前狀態",
            "target_position": "目標狀態",
            "gap_description": "差距說明",
            "bridge_plan": ["步驟1(時間)", "步驟2(時間)"]
        },
        "match_score": 85,
        "key_recommendation": "核心建議"
    }"""

    user_prompt = f"""基於以下資訊，請分析並推薦最適合的職涯與副業：

    **個人背景：**
    - 技能：{skills}
    - 興趣：{interests}
    - 職涯目標：{goals}
    - 教育背景：{education_background}
    - 工作經驗：{work_experience}
    - 語言能力：{languages}
    - 每週可用於副業的時數：{hours} 小時
    
    請遵循指定的 JSON 格式，進行加權分析（興趣佔 30%，技能佔 70%）。
    如果目標是「財富自由」，請幫我定義具體指標並給出實際可行的路徑。"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1200,  
            response_format={"type": "json_object"}  # 強制 JSON 格式
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # 顯示 API 使用成本（選用）
        tokens_used = response.usage.total_tokens
        cost = (tokens_used / 1_000_000) * 0.75  # GPT-4o-mini 粗估
        st.caption(f"📊 本次使用 {tokens_used} tokens,成本約 ${cost:.4f}")
        
        return result
        
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON 解析失敗：{e}")
        return None
    except Exception as e:
        st.error(f"❌ 分析失敗：{str(e)}")
        return None


# ===== 頁面設定 =====
st.set_page_config(
    page_title="AI職涯規劃助手",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# 套用 CSS
st.markdown(get_responsive_css(), unsafe_allow_html=True)
st.markdown(get_theme_css("light"), unsafe_allow_html=True)

# ===== 主標題 =====
st.title("🎯 AI職涯規劃助手")
st.markdown("### 找到適合你的正職與副業")

# ===== 側邊欄輸入 =====
with st.sidebar:
    st.header("📝 填寫你的資料")
    
    name = st.text_input("姓名（可匿名）", value="匿名使用者")
    age = st.number_input("年齡", min_value=15, max_value=80, value=25)
    education_background = st.text_input(
        "教育背景", 
        placeholder="例如：資工系、高中畢業"
    )

    st.markdown("---")
    st.markdown("**請詳細描述**（越詳細越準確）")
    
    skills = st.text_area(
        "💪 技能",
        placeholder="例如:Python、React、數據分析、水電維修...",
        height=100
    )
    
    interests = st.text_area(
        "❤️ 興趣",
        placeholder="例如：科技、設計、投資、旅遊...",
        height=80
    )
    
    goals = st.text_area(
        "🎯 目標",
        placeholder="例如：成為工程師、遠距工作、財富自由...",
        height=80
    )
    
    work_experience = st.text_area(
        "💼 工作經驗",
        placeholder="例如:曾任職軟體工程師2年,負責前端開發...",
        height=80
    )
    
    languages = st.text_input(
        "🌐 語言能力",
        placeholder="例如：中文（母語）、英文（流利）、日文（基礎）"
    )

    st.markdown("---")
    hours = st.slider("⏰ 每週可用於副業時數", 0, 50, 10)
    
    analyze_btn = st.button(
        "🚀 開始分析", 
        type="primary", 
        use_container_width=True
    )

# ===== 主要內容區 =====
if analyze_btn:
    # 驗證輸入
    if not skills or not interests or not goals:
        st.warning("⚠️ 請填寫完整資料（技能、興趣、目標）")
    else:
        with st.spinner("🤖 AI 分析中...請稍候"):
            result = analyze_career(
                skills, interests, goals,
                education_background, work_experience,
                languages, hours
            )
        
        if result:
            st.success("✅ 分析完成！")
            
            # === 主要推薦 ===
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏆 推薦正職")
                main_job = result.get("main_job", {})
                
                st.metric(
                    "職業", 
                    main_job.get("title", "N/A"),
                    f"匹配度 {result.get('match_score', 0)}%"
                )
                
                st.info(f"💰 預估薪資：{main_job.get('salary_range', 'N/A')}")
                st.info(f"🌍 市場：{main_job.get('market', 'N/A')}")
                
                with st.expander("📋 詳細資訊"):
                    st.write("**匹配原因：**")
                    for reason in main_job.get("match_reason", []):
                        st.write(f"- {reason}")
                    
                    st.write("**需要技能：**")
                    for skill in main_job.get("required_skills", []):
                        st.write(f"- {skill}")
                    
                    st.write(f"**發展潛力：** {main_job.get('growth_potential', 'N/A')}")
            
            with col2:
                st.markdown("### 💼 推薦副業")
                side_hustle = result.get("side_hustle", {})
                
                st.metric(
                    "副業", 
                    side_hustle.get("project", "N/A"),
                    f"加權分數 {side_hustle.get('weighted_score', 0)}/100"
                )
                
                income = side_hustle.get("estimated_income", {})
                st.info(
                    f"⏰ 時間：{side_hustle.get('time_needed', 'N/A')}\n\n"
                    f"💵 台灣收入：{income.get('taiwan', 'N/A')}\n\n"
                    f"🌏 國際收入：{income.get('international', 'N/A')}"
                )
                
                with st.expander("📋 詳細資訊"):
                    st.write(f"**興趣契合度：** {side_hustle.get('interest_match', 0)}/100")
                    st.write(f"**技能契合度：** {side_hustle.get('skill_match', 0)}/100")
                    st.write(f"**難度：** {side_hustle.get('difficulty', 'N/A')}")
                    st.write(f"**變現時間：** {side_hustle.get('monetization_timeline', 'N/A')}")
            
            # === 目標差距分析 ===
            st.markdown("---")
            st.markdown("### 🎯 目標可行性分析")
            
            gap_analysis = result.get("goal_gap_analysis", {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**目前狀態：** {gap_analysis.get('current_position', 'N/A')}")
            with col2:
                st.write(f"**目標狀態：** {gap_analysis.get('target_position', 'N/A')}")
            
            st.write(f"**差距分析：** {gap_analysis.get('gap_description', 'N/A')}")
            
            st.write("**行動計畫：**")
            for step in gap_analysis.get("bridge_plan", []):
                st.write(f"✅ {step}")
            
            # === 其他選項 ===
            st.markdown("---")
            st.markdown("### 📊 其他潛在選項")
            
            alternatives = result.get("alternatives", [])
            if alternatives:
                for alt in alternatives:
                    with st.expander(
                        f"{alt.get('option', 'N/A')} - 契合度 {alt.get('fit_score', 0)}/100"
                    ):
                        st.write(alt.get("brief", "N/A"))
            else:
                st.info("暫無其他選項")
            
            # === 核心建議 ===
            st.markdown("---")
            st.markdown("### 💡 核心建議")
            st.success(result.get("key_recommendation", "N/A"))
            
            # === 反饋區 ===
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
                would_pay = st.checkbox("願意為更詳細報告付費(NT$99-299)")
            
            feedback = st.text_area(
                "其他建議或意見", 
                placeholder="請分享你的想法..."
            )
            
            if st.button("提交反饋", type="primary"):
                feedback_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "satisfaction": satisfaction,
                    "would_pay": would_pay,
                    "feedback": feedback,
                    "main_job": main_job.get("title", "N/A"),
                    "side_hustle": side_hustle.get("project", "N/A"),
                    "match_score": result.get("match_score", 0),
                    "skills": skills[:100],
                    "goals": goals[:100]
                }
                
                try:
                    with open("feedback.json", "a", encoding="utf-8") as f:
                        json.dump(feedback_data, f, ensure_ascii=False)
                        f.write("\n")
                    st.success("✅ 感謝你的反饋！")
                except Exception as e:
                    st.info(f"反饋已記錄（本地測試模式）- {e}")

else:
    # === 歡迎頁面 ===
    st.markdown("""
    ## 歡迎使用 AI 職涯規劃助手！

    ### 這個工具能幫你：
    - 🎯 找到適合的正職方向（基於 AI 智能分析）
    - 💼 推薦合適的副業選項（考慮你的時間與技能）
    - 📊 提供具體可行的行動計畫

    ### 使用步驟：
    1. 在左側**詳細**填寫你的資料
    2. 描述越具體，推薦越準確
    3. 點擊「開始分析」

    **提示**：可以用中文或英文描述技能
    """)

    # 範例
    with st.expander("💡 查看填寫範例"):
        st.markdown("""
        **技能範例**:
        - 軟體:Python, JavaScript, React, 網頁開發
        - 設計:Photoshop, Illustrator, 平面設計, 排版
        - 分析:Excel, SQL, 數據分析, 報表
        - 其他：水電維修, 烹飪, 寫作, 教學

        **興趣範例**:
        - 科技、程式設計、解決問題、自動化
        - 創意、視覺設計、美學、品牌
        - 教育、分享知識、幫助他人
        - 投資、理財、數位遊牧

        **目標範例**:
        - 成為軟體工程師，想要遠距工作
        - 增加收入,發展副業每月多賺3萬
        - 轉職到科技業，學習新技能
        - 財富自由,月被動收入10萬
        """)

    st.info("💡 **測試版**：填寫後可在反饋區勾選「願意付費」來幫助驗證商業模式")

# 頁尾
st.markdown("---")
st.caption("*本工具使用 OpenAI GPT-4o-mini | 基於興趣30%/技能70%加權分析*")
