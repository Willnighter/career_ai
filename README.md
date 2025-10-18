# 🎯 AI職涯規劃助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

> 基於 OpenAI GPT-4o-mini 的智能職涯與副業分析工具

## ✨ 功能特色

- 🎯 智能職涯推薦（興趣30%/技能70%加權）
- 💼 副業建議與收入預估
- 📊 目標可行性分析與行動計畫
- 🌍 支援台灣與國際市場

## 🚀 快速開始

### 前置需求

- Python 3.9+
- OpenAI API Key

### 安裝步驟

1. Clone 專案
```bash
git clone https://github.com/willnighter/career-ai.git
cd career-advisor
```

2. 安裝套件
```bash
pip install -r requirements.txt
```

3. 設定 API Key
建立 `.streamlit/secrets.toml`：
```toml
OPENAI_API_KEY = "sk-your-api-key-here"
```

4. 執行
```bash
streamlit run app.py
```

## 💰 成本說明

使用 GPT-4o-mini API：
- 每次分析約 $0.001（NT$0.03）
- 新用戶有 $5 免費額度

## ⚠️ 使用限制

本專案使用 OpenAI API，使用前請注意：

1. **API Key 安全**：請勿將 API key 上傳到 GitHub
2. **使用成本**：OpenAI API 按用量計費
3. **服務條款**：需遵守 [OpenAI 使用政策](https://openai.com/policies/usage-policies)
4. **內容政策**：
   - 不得用於非法用途
   - 不得生成有害內容
   - 需遵守數據隱私法規

## 免責聲明

本工具僅供參考，不構成專業職涯建議。使用者需自行判斷建議的適用性。
開發者不對使用本工具產生的任何決策負責。

AI 生成的內容可能不準確，請謹慎評估。
```
## 📝 License

本專案採用 [MIT License](LICENSE)。

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

## 📧 聯絡

有問題？請開 [Issue](https://github.com/willnighter/career-advisor/issues)

---

Made with ❤️ by [will reginald]
