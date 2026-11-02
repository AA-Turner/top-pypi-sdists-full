from tablescope.engine import TableEngine
from tablescope.widget import TableScopeWidget, view, widget

__all__ = ["TableEngine", "TableScopeWidget", "view", "widget", "main"]


def main() -> None:
    from tablescope._cli import main as _main

    _main()
