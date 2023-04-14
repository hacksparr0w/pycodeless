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
 natural language. All generated code is stored and can be edited or committed
 to your version control system.
 - [ ] Support for different language models to allow for better customization
 and offline usage.
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


# You can either specify your OpenAI API key in this way, or you can use the
# environment variable OPENAI_API_KEY.
# The same goes for specifying the model name, where the relevant environment
# variable is OPENAI_MODEL_NAME. If no model name is specified, Pycodeless
# will default to "gpt-3.5-turbo".

codeless.openai_api_key = "sk-fEaz..."
codeless.openai_model_name = "gpt-4"


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
    print(spongebob_case(greet("Patrick")))


if __name__ == "__main__":
    main()

```

## FAQ

 - **How is this different from GitHub Copilot?**
 Pycodeless has indeed very similar functionality to GitHub Copilot, but
 the goal of this project is very different. Firstly, Copilot autocompletes
 your code in place and does not differentiate between the generated part of
 the code and the original prompt. One of the main points of this project is
 to completely shift the development focus onto the prompt itself and make
 natural language a universal interface for code generation while moving the
 generated code into the background. The development experience is really
 distinct, and I encourage you to test this out for yourself. Another
 important point is that Pycodeless makes code generation from natural
 language a first-class Python citizen. The code generation happens in runtime,
 which means we can leverage the whole Python infrastructure to enhance the
 prompt specification process (think dynamic docstrings with custom tags to 
 reference various objects from the codebase and aid the LLMs, walking through
 the dependency graphs of type annotations to provide additional context, etc.).
 Also, I like the idea of not being dependent on any particular language model
 or text editor.

## Limitations

 - The current code generation and parsing features might be buggy, as there's
 currently no mechanism for telling whether an output from an LLM is actually
 runnable Python code.
 - The `@codeless` decorator may not work in all contexts (REPL, classes,
 methods, etc.).
 - There's currently no dependency management in place. This means that we
 can't track changes across the whole codebase and regenerate functions when
 their dependencies change. This also means that we can't remove any generated
 imports when removing a generated function inside a generated module, because
 there's no way of telling whether or not the import in question is used by
 any other function. Another problem with this is that if there's a custom
 type annotation in the function definition, we have no way of referencing it
 in the generated module.

## Contribution

If you'd like to report a bug or have an idea for a cool feature, issues and
pull requests are highly appreciated.
