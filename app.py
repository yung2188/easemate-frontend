import streamlit as st
import requests

st.set_page_config(page_title="EaseMate AI", page_icon="🤖")

st.title("🤖 EaseMate 全能助手")
st.caption("現在我能記住我們聊過什麼了！")

# 1. 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好！我是 EaseMate。請問今天有什麼我可以幫您的？"}
    ]

# 2. 顯示歷史對話
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. 處理用戶輸入
if prompt := st.chat_input("請輸入問題..."):
    
    # 顯示用戶訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. 呼叫後端 API
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                # 準備傳送給後端的資料 (包含歷史紀錄)
                payload = {
                    "client_name": "Web_User",
                    "history": st.session_state.messages[:-1] # 傳送除了剛輸入的這一則以外的所有歷史
                }
                
                if prompt.startswith("http"):
                    payload["url"] = prompt
                else:
                    payload["keyword"] = prompt
                
                # 呼叫 Render API
                api_url = "https://law-ai-api.onrender.com/research"
                response = requests.post(api_url, json=payload, timeout=120)
                
                if response.status_code == 200:
                    answer = response.json().get("report")
                    st.markdown(answer)
                    # 存入記憶
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("連線失敗")
            except Exception as e:
                st.error(f"錯誤: {e}")

# 側邊欄
with st.sidebar:
    if st.button("🧹 清除對話"):
        st.session_state.messages = []
        st.rerun()
