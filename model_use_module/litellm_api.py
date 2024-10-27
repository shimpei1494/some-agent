from dotenv import load_dotenv
from litellm import completion

load_dotenv(override=True)


def litellm_response(messages: list[dict], model: str) -> dict:
    response = completion(
        model=model,
        messages=messages,
    )
    return response
