def chat_message_builder(old_messages: list[dict], user_msg: str) -> list[dict]:
    new_messages = old_messages.copy()
    new_messages.append({"role": "user", "content": user_msg})
    return new_messages
