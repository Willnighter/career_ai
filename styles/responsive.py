def get_responsive_css():
    """返回響應式 CSS"""
    return """
    <style>
        /* ===== 全局設定 ===== */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* ===== 手機版 (< 768px) ===== */
        @media (max-width: 768px) {
            /* 內容區域 */
            .main .block-container {
                max-width: 100%;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            /* 側邊欄優化 */
            [data-testid="stSidebarNav"] {
                background-color: #f0f2f6;
            }
            
            /* 側邊欄開關按鈕更明顯 */
            button[kind="header"] {
                background-color: #FF4B4B;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-weight: 600;
            }
            
            /* 表單元素更大，方便點擊 */
            .stTextInput input, 
            .stTextArea textarea,
            .stNumberInput input {
                font-size: 16px !important;  /* 防止 iOS 自動縮放 */
                padding: 0.75rem !important;
            }
            
            /* 按鈕全寬且更高 */
            .stButton button {
                width: 100%;
                height: 3rem;
                font-size: 1.1rem;
            }
            
            /* 標題文字適應手機 */
            h1 {
                font-size: 1.8rem !important;
            }
            
            h2 {
                font-size: 1.4rem !important;
            }
            
            h3 {
                font-size: 1.2rem !important;
            }
            
            /* columns 改成堆疊顯示 */
            [data-testid="column"] {
                width: 100% !important;
                flex: 100% !important;
                margin-bottom: 1rem;
            }
        }
        
        /* ===== 平板版 (768px - 1024px) ===== */
        @media (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                max-width: 90%;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            
            /* 側邊欄寬度適中 */
            [data-testid="stSidebar"] {
                width: 280px;
            }
        }
        
        /* ===== 桌面版 (> 1024px) ===== */
        @media (min-width: 1025px) {
            .main .block-container {
                max-width: 1200px;
            }
            
            /* 側邊欄固定展開 */
            [data-testid="stSidebar"] {
                width: 320px;
            }
        }
        
        /* ===== 通用優化 ===== */
        
        /* 載入動畫 */
        .stSpinner > div {
            border-color: #FF4B4B !important;
        }
        
        /* 成功/錯誤訊息 */
        .stAlert {
            border-radius: 8px;
        }
        
        /* 卡片效果 */
        .element-container {
            border-radius: 8px;
        }
        
        /* 滾動條美化 */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
    """


def get_theme_css(theme="light"):
    """返回主題 CSS"""
    if theme == "dark":
        return """
        <style>
            /* 深色主題 */
            .main {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
        </style>
        """
    else:
        return """
        <style>
            /* 淺色主題（預設） */
            .main {
                background-color: #FFFFFF;
                color: #000000;
            }
        </style>
        """
