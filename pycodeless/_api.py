import os

from typing import Callable, Optional

from ._generate import generate
from ._load import load_module
from ._openai_llm import OpenAiLanguageModel


def codeless(function: Callable) -> Callable:
    if not codeless.openai_api_key:
        raise RuntimeError("OpenAI API key was not set")

    llm = OpenAiLanguageModel(
        codeless.openai_api_key,
        codeless.openai_model_name
    )

    result = generate(llm, function)

    def wrapper(*args, **kwargs):
        module = load_module(*result)
        callable = getattr(module, function.__name__)

        return callable(*args, **kwargs)

    return wrapper


codeless.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
codeless.openai_model_name: str = os.getenv(
    "OPENAI_MODEL_NAME",
    "gpt-3.5-turbo"
)
