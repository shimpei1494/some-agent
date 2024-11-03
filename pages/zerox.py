import asyncio
import os

import streamlit as st
from dotenv import load_dotenv
from pyzerox import zerox
from pyzerox.core.types import ZeroxOutput

load_dotenv(override=True)

st.title("zerox資料テキスト変換")

## オプションを定義
model_options = [
    "gemini/gemini-1.5-flash",
    "gemini/gemini-1.5-pro",
    "gpt-4o-mini",
    "gpt-4o",
]

## セレクトボックスをサイドバーに作成
selected_model_option: str = st.sidebar.selectbox(
    "モデルを選択してください:", model_options
)

# ファイルアップロード機能を追加
uploaded_file = st.file_uploader(
    "テキスト化したいファイルをアップロードしてください", type=["pdf"]
)

if uploaded_file is not None and st.button("テキスト変換実行"):
    with st.spinner("テキスト変換中..."):
        # ファイルの拡張子を取得
        file_extension = uploaded_file.name.split(".")[-1].lower()

        # 一時ファイルとして保存（拡張子付きで）
        temp_filename = f"temp_file.{file_extension}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ファイルパスを設定
        file_path = temp_filename

        # 非同期関数を定義
        async def process_file():
            result: ZeroxOutput = await zerox(
                file_path=file_path, model=selected_model_option
            )
            return result

        # 非同期関数を実行
        try:
            zeroxoutput_result: ZeroxOutput = asyncio.run(process_file())
        except Exception as e:
            # エラー発生した際は、エラー内容を表示し、streamlitの処理を停止
            st.error(f"エラーが発生しました: {e}")
            st.error("エラー内容を確認し、再度実行してください")
            st.stop()

        # 結果を表示
        st.markdown("## テキスト変換結果")
        st.info(f"モデル：{selected_model_option}")
        with st.expander("ZeroxOutputオブジェクトの出力を表示"):
            st.markdown(zeroxoutput_result)
        # 全てのページを順番に表示
        for i, page in enumerate(zeroxoutput_result.pages):
            st.markdown(f"### ページ {i+1}")
            st.text(page.content)
            with st.expander("ページの内容をマークダウン表示"):
                st.write(page.content)
        # 一時ファイルを削除
        os.remove(temp_filename)
