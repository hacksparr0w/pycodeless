from typing import Iterable

import openai

from ._llm import LanguageModel, Message, MessageRole


def _encode_message(message: Message) -> dict:
    role = message.role.name.lower()

    return {"role": role, "content": message.content}


def _decode_message(data: dict) -> Message:
    role = MessageRole.of(data["role"].upper())
    content = data["content"]

    return Message(role, content)


class OpenAiLanguageModel(LanguageModel):
    def __init__(self, api_key, model_name: str) -> None:
        openai.api_key = api_key
        self._model_name = model_name
    
    def prompt(self, messages: Iterable[Message]) -> Message:
        response = openai.ChatCompletion.create(
            model=self._model_name,
            messages=[_encode_message(message) for message in messages]
        )

        message_data = response["choices"][0]["message"]
        message = _decode_message(message_data)

        return message
