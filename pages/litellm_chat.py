import streamlit as st

from model_use_module.litellm_api import litellm_response
from utils.chat_message_builder import chat_message_builder

st.title("LiteLLMチャット")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

## オプションを定義
model_options = [
    "gpt-4o-mini",
    "gpt-4o",
    "gemini/gemini-1.5-flash",
    "gemini/gemini-1.5-pro",
]

## セレクトボックスをサイドバーに作成
selected_model_option = st.sidebar.selectbox("モデルを選択してください:", model_options)

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# チャットログを表示する関数
def display_chat_history():
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])


# チャットログを表示
display_chat_history()

user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # 最新のユーザーメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    new_messages = chat_message_builder(st.session_state.chat_log, user_msg)
    response = litellm_response(new_messages, selected_model_option, True)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = ""
        assistant_response_area = st.empty()
        for chunk in response:
            if chunk.choices[0].finish_reason is not None:
                break
            # 回答を逐次表示
            assistant_msg += chunk.choices[0].delta.content
            assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"role": USER_NAME, "content": user_msg})
    st.session_state.chat_log.append({"role": ASSISTANT_NAME, "content": assistant_msg})
