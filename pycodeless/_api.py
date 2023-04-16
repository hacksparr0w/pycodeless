import sys

from typing import Callable

from ._config import config
from ._debug import handle_exception
from ._generate import generate
from ._load import load_module
from ._openai_llm import OpenAiLanguageModel


def codeless(function: Callable) -> Callable:
    config._load()

    llm = OpenAiLanguageModel(
        config.openai_api_key,
        config.openai_model_name
    )

    result = generate(llm, function)

    def wrapper(*args, **kwargs):
        module = load_module(*result)
        callable = getattr(module, function.__name__)

        return callable(*args, **kwargs)

    return wrapper


def install_debugger():
    config._load()

    llm = OpenAiLanguageModel(
        config.openai_api_key,
        config.openai_model_name
    )

    def hook(*args, **kwargs):
        handle_exception(llm, *args, **kwargs)

    sys.excepthook = hook
