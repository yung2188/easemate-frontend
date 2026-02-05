import streamlit as st
import requests

# 1. 網頁設定 (隱藏 Streamlit 預設選單)
st.set_page_config(page_title="EaseMate AI", page_icon="🤖", layout="centered")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# 2. 標題與 Logo
st.title("🤖 EaseMate AI 助手")
st.subheader("您的智慧法規與對話夥伴")

# 3. 對話記憶初始化
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "您好！我是 EaseMate，有什麼我可以幫您的？"}]

# 4. 顯示對話
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 用戶輸入
if prompt := st.chat_input("輸入問題或貼上網址..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("EaseMate 正在思考中..."):
            try:
                # 呼叫你已經部署在 Render 的後端
                api_url = "https://law-ai-api.onrender.com/research"
                payload = {"client_name": "Mobile_User"}
                if prompt.startswith("http"):
                    payload["url"] = prompt
                else:
                    payload["keyword"] = prompt
                
                response = requests.post(api_url, json=payload, timeout=120)
                answer = response.json().get("report", "抱歉，暫時無法回應。")
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except:
                st.error("連線超時，請稍後再試。")
