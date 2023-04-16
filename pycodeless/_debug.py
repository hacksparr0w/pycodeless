import inspect
import os
import sys
import traceback

from pathlib import Path

from ._llm import LanguageModel, Message


def _extract_source_information(exception_traceback) -> str:
    python_path = Path(sys.executable).parent
    buffer = []
    frames = traceback.walk_tb(exception_traceback)

    for frame, _ in frames:
        code = frame.f_code
        module = inspect.getmodule(code)
        module_name = module.__name__

        if module_name in sys.builtin_module_names:
            continue

        path = Path(inspect.getabsfile(code))

        if python_path in path.parents or "site-packages" in str(path):
            continue

        frame_info = inspect.getframeinfo(frame)

        source = None

        if frame_info.function == "<module>":
            source = inspect.getsource(module)
        else:
            source = inspect.getsource(code)

        buffer.append(
            f"File \"{frame_info.filename}\", "
            f"function '{frame_info.function}': "
        )

        buffer.append(source)

    return "\n".join(buffer)


def _format_traceback(
        exception_type,
        exception_value,
        exception_traceback
) -> str:
    buffer = []

    buffer.append("Traceback (most recent call last):\n")

    for line in traceback.format_tb(exception_traceback):
        buffer.append(line)
    
    buffer.append(f"{exception_type.__name__}: {exception_value}")

    return "".join(buffer)


def handle_exception(
        llm: LanguageModel,
        exception_type,
        exception_value,
        exception_traceback
) -> None:
    if issubclass(exception_type, KeyboardInterrupt):
        sys.__excepthook__(
            exception_type,
            exception_value,
            exception_traceback
        )

        return

    traceback_message = _format_traceback(
        exception_type,
        exception_value,
        exception_traceback
    )

    source_information = _extract_source_information(exception_traceback)

    print(traceback_message)
    print()
    print("Generating error analysis...")

    response = llm.prompt((
        Message.user(
            "You are a large language model tasked with debugging Python "
            "code given a traceback message. Please provide a succint and "
            "concise analysis of the error and a potential solution to the "
            "problem.\n\n"
            f"The following is the traceback message:\n{traceback_message}\n\n"
            f"Here's the source:\n{source_information}"
        ),
    ))

    print(response.content)
