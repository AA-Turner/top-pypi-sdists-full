import importlib
from typing import Optional

import pytest
from packaging.version import Version


# https://github.com/pydata/xarray/blob/aa4361dafbf69e5872d8870ce73d082ac9400db0/xarray/tests/__init__.py#L49-L61
def _importorskip(modname: str, minversion: Optional[str] = None) -> tuple[bool, pytest.MarkDecorator]:
    """
    Check if a module can be imported and skip the test if it cannot.

    Args:
        modname (str): The name of the module to import.
        minversion (str | None, optional): The minimum version of the module required. Defaults to None.

    Returns:
        tuple[bool, pytest.MarkDecorator]: A tuple containing a boolean indicating whether the module was successfully imported and a pytest.MarkDecorator object to skip the test if the module was not imported.

    Raises:
        ImportError: If the required module cannot be imported or if the minimum version requirement is not satisfied.
    """
    try:
        mod = importlib.import_module(modname)
        has = True
        if minversion is not None:
            if Version(mod.__version__) < Version(minversion):
                raise ImportError("Minimum version not satisfied")
    except ImportError:
        has = False
    func = pytest.mark.skipif(not has, reason=f"requires {modname}")
    return has, func


has_typer, requires_typer = _importorskip("typer")
