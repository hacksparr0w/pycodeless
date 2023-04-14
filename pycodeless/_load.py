import importlib.util
import sys

from pathlib import Path
from types import ModuleType


def load_module(path: Path, name: str) -> ModuleType:
    module = sys.modules.get(name)

    if module:
        return module

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module
