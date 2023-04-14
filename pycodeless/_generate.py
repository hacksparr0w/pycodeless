import hashlib
import inspect
import json
import platform

from pathlib import Path
from typing import Callable

from ._llm import LanguageModel, Message
from ._parse import Module, parse_module


_GENERATED_PACKAGE_NAME = "__pycodeless__"


def _cut(text: str, start_index: int, end_index: int) -> str:
    return text[:start_index] + text[end_index:]


def _checksum(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def _generate_function_source(llm: LanguageModel, template: str) -> str:
    messages = (
        Message.system(
            "You are a large language model tasked with completing Python"
            " functions given their template with an optional docstring. "
            "When writing code, make sure to follow these rules:\n"
            " 1. Respond only with a valid Python code including the original"
            " function definition and imports. Do NOT add any additional "
            "commentary. Do NOT wrap the code in quotes or backticks.\n"
            " 2. Always remove the @codeless decorator from the function "
            "definition. It must not be present in our output!\n"
            " 3. Preserve the original function definition in your output \n"
            "including the original docstring."
            " 4. Make sure the code is compatible with Python version "
            f"{platform.python_version()}."
        ),
        Message.user(
            "The following is the function to be completed:\n\n"
            f"{template}"
        )
    )

    result = llm.prompt(messages).content

    return result


def _decode_module_generation_metadata(module: Module) -> dict[str, str]:
    if not module.docstring:
        return {}

    return json.loads(module.docstring.content)


def _encode_module_generation_metadata(data: dict[str, str]) -> str:
    contents = json.dumps(data, indent=4)
    docstring = f'"""\n{contents}\n"""\n'

    return docstring


def _generate_module_source(
        metadata: dict,
        previous_module: Module,
        generated_function_name: str,
        generated_function_source: str
) -> str:
    docstring = _encode_module_generation_metadata(metadata)
    source = previous_module.source

    previous_generated_function = previous_module.functions.get(
        generated_function_name
    )

    if previous_generated_function: 
        source = _cut(
            source,
            previous_generated_function.start_index,
            previous_generated_function.end_index
        )

    if previous_module.docstring:
        source = _cut(
            source,
            previous_module.docstring.start_index,
            previous_module.docstring.end_index
        )

    source = source.strip()

    if not source:
        source = f"{docstring}\n{generated_function_source}"
    else:
        source = f"{docstring}\n{source}\n\n\n{generated_function_source}"

    return source


def _generate_module_name(name: str) -> str:
    parts = name.split(".")

    return ".".join(parts[:-1] + [_GENERATED_PACKAGE_NAME, parts[-1]])


def _generate_module_path(path: Path) -> Path:
    return path.parent / _GENERATED_PACKAGE_NAME / path.name


def generate(
        llm: LanguageModel,
        template_function: Callable
) -> tuple[Path, str]:
    function_name = template_function.__name__

    template_module = inspect.getmodule(template_function)
    template_module_name = template_module.__name__
    template_module_path = Path(template_module.__file__)
    template_function_source = inspect.getsource(template_function)
    current_template_function_checksum = _checksum(template_function_source)

    generated_module_name = _generate_module_name(template_module_name)
    generated_module_path = _generate_module_path(template_module_path)

    if not generated_module_path.exists():
        generated_module_path.parent.mkdir(exist_ok=True)
        generated_module_path.touch()

    generated_module_source = generated_module_path.read_text("utf-8")
    generated_module_parsed = parse_module(generated_module_source)
    generation_metadata = _decode_module_generation_metadata(
        generated_module_parsed
    )

    previous_template_function_checksum = generation_metadata.get(
        function_name
    )

    if (
        previous_template_function_checksum ==
            current_template_function_checksum and
        function_name in generated_module_parsed.functions
    ):
        return generated_module_path, generated_module_name

    generation_metadata[function_name] = current_template_function_checksum
    generated_function_source = _generate_function_source(
        llm,
        template_function_source
    )

    generated_module_source = _generate_module_source(
        generation_metadata,
        generated_module_parsed,
        function_name,
        generated_function_source
    )

    generated_module_path.write_text(generated_module_source, "utf-8")

    return generated_module_path, generated_module_name
