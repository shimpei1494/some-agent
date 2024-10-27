import streamlit as st

from model_use_module.litellm_api import litellm_response

st.title("LiteLLMテスト")

## オプションを定義
model_options = [
    "gpt-4o-mini",
    "gpt-4o",
    "gemini/gemini-1.5-flash",
    "gemini/gemini-1.5-pro",
]

## セレクトボックスをサイドバーに作成
selected_model_option = st.sidebar.selectbox("モデルを選択してください:", model_options)

# ユーザー入力
user_input = st.text_input("質問入力欄", "")

if st.button("送信"):
    if user_input:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
        with st.spinner("回答生成中..."):
            response = litellm_response(messages, selected_model_option)
        st.write("## 回答のみ")
        st.write(response.choices[0].message.content)
        st.write("## リクエストのmessages")
        st.write(messages)
        st.write("## レスポンスそのまま")
        st.write(response)
