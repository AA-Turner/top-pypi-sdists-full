"""Auto-generated stub for module: validate."""
from typing import Any

# Functions
def discover_apps(root: str | Any.Any[str]) -> tuple[Any, ...]:
    """
    Every app folder under ``root``, sorted.
    
        An app folder is one that directly contains an ``app.yaml``. ``root`` itself counts, so a
        single app folder can be passed to :func:`validate_apps` as well as a tree of them. Nested
        apps are found, but an app folder is never descended into — a ``samples/`` directory that
        happens to hold an ``app.yaml`` fixture is not a second app.
    """
    ...
def validate_app(app: str | Any.Any[str]) -> Any:
    """
    Run every generated check for one app folder.
    
        Args:
            app: An app folder, a path to its ``app.yaml``, or a bare app id.
            seeds: The two ``PYTHONHASHSEED`` values the determinism check runs under.
    
        Returns:
            A :class:`~matrice_analytics.engine.testing.generate.SuiteResult`; ``.passed`` is the
            verdict and ``.report()`` explains it. A manifest that does not load is a red check, not
            an exception.
    """
    ...
def validate_apps(root: str | Any.Any[str]) -> Any:
    """
    Run every generated check for every app under ``root``.
    
        The "is the whole catalogue production-ready" call: one invocation, one verdict, and a report
        that names the app and the check for anything that is not.
    """
    ...

# Classes
class AppsResult:
    # Every app under one root, and whether the whole set is ready.

    def failures(self: Any) -> tuple[Any, ...]: ...

    def ok(self: Any) -> bool:
        """
        ``True`` when no app failed a check. An empty root is **not** ready.
        """
        ...

    def report(self: Any) -> str:
        """
        One block per app, then a one-line verdict — what a CI log should show.
        """
        ...

    def summary(self: Any) -> str:
        """
        One line per app, for when the full report is too much.
        """
        ...

