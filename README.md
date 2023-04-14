# pycodeless

> **Warning**
> This project is in a very early stage of development and may not always
> produce desired results. See the [limitations](#limitations) section for
> more information.

Pycodeless integrates the power of LLMs into the Python programming language
and allows you to use natural language as a universal interface for code
generation.

## Features

 - [x] The `@codeless` decorator allows you to define your functions using
 natural language.
 - [x] All generated code is stored and can be edited or commited to your
 version control. 
 - [ ] Support for different models to allow for customization and offline
 usage.
 - [ ] Custom docstring formatting to allow for referencing objects across the
 whole codebase.

## Installation

You can install pycodeless using pip:

```
pip install pycodeless
```

## Usage

Following is a sample code using pycodeless.

```python
from pycodeless import codeless


codeless.openai_api_key = (
    "Paste your OpenAI API key here or set the 'OPENAI_API_KEY' environment
    "variable!"
)


@codeless
def greet(name: str) -> str:
    """
    Make greeting for a person with the given name
    """


@codeless
def spongebob_case(text: str) -> str:
    """
    Convert the passed text into spongebob case
    """


def main():
    print(spongebob_case(greet("Bob")))


if __name__ == "__main__":
    main()

```

## Limitations

 - The current code generation and parsing features might be buggy, as there's
 currently no mechanism for telling whether an output from an LLM is actually
 runnable Python code.
 - The `@codeless` decorator may not work in all contexts.

## Contribution

If you'd like to report a bug or have an idea for a cool feature, issues and pull requests are highly appreciated.
