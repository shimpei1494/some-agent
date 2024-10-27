import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv(override=True)

# APIキーを設定
api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


def gpt_response(messages: list[dict], model: str) -> ChatCompletion:
    response = client.chat.completions.create(model=model, messages=messages)
    return response
