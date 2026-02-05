import streamlit as st
import requests

# 網頁設定
st.set_page_config(page_title="EaseMate AI 助手", page_icon="🤖", layout="centered")

# 自定義 CSS 讓對話框更漂亮
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 EaseMate 全能 AI 助手")
st.caption("🚀 支援通用對話、法規搜尋、網址分析")

# --- 1. 初始化對話紀錄 ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好！我是 EaseMate，您的智慧助手。今天有什麼我可以幫您的嗎？\n\n您可以直接跟我聊天，或是貼上法規網址讓我分析。"}
    ]

# --- 2. 顯示歷史對話 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. 處理用戶輸入 ---
if prompt := st.chat_input("請輸入您的問題或貼上網址..."):
    
    # 顯示用戶訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 4. 呼叫後端 API ---
    with st.chat_message("assistant"):
        with st.spinner("EaseMate 正在思考中..."):
            try:
                # 自動判斷輸入類型
                payload = {"client_name": "Web_User"}
                if prompt.startswith("http"):
                    payload["url"] = prompt
                else:
                    payload["keyword"] = prompt
                
                # 呼叫 Render API (請確保網址正確)
                api_url = "https://law-ai-api.onrender.com/research"
                response = requests.post(api_url, json=payload, timeout=120)
                
                if response.status_code == 200:
                    full_response = response.json().get("report")
                    st.markdown(full_response)
                    # 存入記憶
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("連線失敗，請稍後再試。")
            except Exception as e:
                st.error(f"連線異常: {e}")

# 側邊欄：清除對話
with st.sidebar:
    st.header("功能選單")
    if st.button("🧹 清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("提示：輸入網址可進行深度法規分析。")