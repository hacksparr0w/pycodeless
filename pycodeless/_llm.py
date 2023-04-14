from dataclasses import dataclass
from enum import Enum, auto

from typing import Iterable


class MessageRole(Enum):
    ASSISTANT = auto()
    SYSTEM = auto()
    USER = auto()

    @classmethod
    def of(cls, name: str) -> "MessageRole":
        for role in cls:
            if role.name == name:
                return role

        raise ValueError


@dataclass
class Message:
    role: MessageRole
    content: str

    @classmethod
    def assistant(cls, content: str) -> "Message":
        return cls(MessageRole.ASSISTANT, content)

    @classmethod
    def system(cls, content: str) -> "Message":
        return cls(MessageRole.SYSTEM, content)

    @classmethod
    def user(cls, content: str) -> "Message":
        return cls(MessageRole.USER, content)


class LanguageModel:
    def prompt(messages: Iterable[Message]) -> Message:
        raise NotImplementedError
