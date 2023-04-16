import os

from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    openai_api_key: Optional[str] = None
    openai_model_name: Optional[str] = None

    def _load(self):
        if not self.openai_api_key:
            self.openai_api_key = os.environ.get("OPENAI_API_KEY")

        if not self.openai_model_name:
            self.openai_model_name = os.environ.get(
                "OPENAI_MODEL_NAME",
                "gpt-3.5-turbo"
            )

        if self.openai_api_key is None:
            raise RuntimeError("OpenAI API key was not set")


config = Config()
