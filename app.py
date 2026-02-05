import streamlit as st
import requests

st.set_page_config(page_title="EaseMate AI", page_icon="🤖")

st.title("🤖 EaseMate 全能助手")
st.caption("我現在能理解您的上下文，並根據對話主題持續交流。")

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
if prompt := st.chat_input("請輸入問題或貼上網址..."):
    
    # 顯示用戶訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. 呼叫後端 API
    with st.chat_message("assistant"):
        with st.spinner("EaseMate 正在思考中..."):
            try:
                # 傳送完整的歷史紀錄給後端
                payload = {
                    "client_name": "Web_User",
                    "history": st.session_state.messages[:-1] # 包含之前的對話
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
                    st.error("連線失敗，請檢查 Render 狀態。")
            except Exception as e:
                st.error(f"連線異常: {e}")

# 側邊欄
with st.sidebar:
    st.header("控制面板")
    if st.button("🧹 清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("提示：輸入簡短問題（如：例如呢？）時，AI 會根據前文回答；輸入長句時，AI 會啟動聯網搜尋。")
