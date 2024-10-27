import base64

import streamlit as st

from model_use_module.openai_api import gpt_response


# 画像アップロードとOCR機能
def encode_image(image):
    return base64.b64encode(image.read()).decode("utf-8")


st.title("マルチモーダルテスト")

## オプションを定義
model_options = ["gpt-4o-mini"]
image_resolution_options = ["auto", "high", "low"]

## セレクトボックスをサイドバーに作成
selected_model_option = st.sidebar.selectbox("モデルを選択してください:", model_options)
selected_image_resolution_option = st.sidebar.selectbox(
    "画像の処理解像度:", image_resolution_options
)

# ユーザー入力
user_input = st.text_input("質問入力欄", "")
uploaded_file = st.file_uploader("画像", type=("png", "jpg", "jpeg"))

if uploaded_file is not None:
    base64_image = encode_image(uploaded_file)

if st.button("送信"):
    if user_input:
        if uploaded_file is not None:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_input},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": selected_image_resolution_option,
                            },
                        },
                    ],
                },
            ]
        else:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        with st.spinner("回答生成中..."):
            response = gpt_response(messages, selected_model_option)
        st.write("## 回答のみ")
        st.write(response.choices[0].message.content)
        st.write("## リクエストのmessages")
        st.write(messages)
        st.write("## レスポンスそのまま")
        st.write(response)
