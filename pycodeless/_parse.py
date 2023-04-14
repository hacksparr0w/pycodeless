import re

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Union


@dataclass
class _Bounded:
    start_index: int
    end_index: int


class _ModuleParserToken:
    STRING_QUOTES = ("'''", '"""', "'", '"')
    FUNCTION_DEFINITION = "def"
    FUNCTION_ARGUMENT_START = "("


class _ModuleSeekingState:
    pass


@dataclass
class _ModuleParsingDocstringState:
    string_quote: str


@dataclass
class _ModuleParsingFunctionState:
    name: str


_ModuleParserState = Union[
    _ModuleSeekingState,
    _ModuleParsingDocstringState,
    _ModuleParsingFunctionState
]


@dataclass
class Docstring(_Bounded):
    source: str
    content: str


@dataclass
class Function(_Bounded):
    name: str
    source: str


@dataclass
class Module:
    source: str
    docstring: Optional[Docstring]
    functions: Mapping[str, Function]

    @classmethod
    def empty(cls) -> "Module":
        return cls("", None, {})


def _starts_with(text: str, prefixes: Iterable[str]) -> Optional[str]:
    for prefix in prefixes:
        if text.startswith(prefix):
            return prefix

    return None


def _parse_function_name(header: str) -> str:
    start_index = (
        header.find(_ModuleParserToken.FUNCTION_DEFINITION) +
        len(_ModuleParserToken.FUNCTION_DEFINITION)
    )

    end_index = header.find(_ModuleParserToken.FUNCTION_ARGUMENT_START)

    return header[start_index:end_index].strip()


def _is_function_body(line: str) -> bool:
    return re.match(r"\s", line) or line == "\n"


def parse_module(module_source: str) -> Module:
    lines = module_source.splitlines(keepends=True)

    if not lines:
        return Module.empty()

    character_index = 0
    line_index = 0
    buffer = []
    state: _ModuleParserState = _ModuleSeekingState()

    docstring = None
    functions = {}

    while True:
        line = lines[line_index]
        is_last_line = line_index == len(lines) - 1

        if isinstance(state, _ModuleSeekingState):
            string_quote = _starts_with(
                line,
                _ModuleParserToken.STRING_QUOTES
            )

            if string_quote:
                state = _ModuleParsingDocstringState(string_quote)
                buffer.append(line)
            elif line.startswith(_ModuleParserToken.FUNCTION_DEFINITION):
                name = _parse_function_name(line)
                buffer.append(line)
                state = _ModuleParsingFunctionState(name)
            else:
                character_index += len(line)
        elif isinstance(state, _ModuleParsingDocstringState):
            buffer.append(line)

            if line.rstrip().endswith(state.string_quote):
                start_index = character_index
                docstring_source = "".join(buffer)
                character_index += len(docstring_source)
                end_index = character_index

                if not docstring:
                    content = docstring_source.replace(state.string_quote, "")

                    docstring = Docstring(
                        start_index,
                        end_index,
                        docstring_source,
                        content
                    )

                buffer = []
                state = _ModuleSeekingState()
        elif isinstance(state, _ModuleParsingFunctionState):
            is_function_body = _is_function_body(line)

            if is_function_body:
                buffer.append(line)

            if not is_function_body or is_last_line:
                start_index = character_index
                function_source = "".join(buffer)
                character_index += len(function_source)
                end_index = character_index
                name = state.name
                function = Function(
                    start_index,
                    end_index,
                    name,
                    function_source
                )

                functions[name] = function

                buffer = []
                state = _ModuleSeekingState()

            if not is_function_body:
                continue

        if is_last_line:
            break

        line_index += 1

    if not isinstance(state, _ModuleSeekingState):
        raise RuntimeError

    return Module(module_source, docstring, functions)
