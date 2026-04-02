"""Utilities and helpers for Python scripts."""

import inspect
import os
import sys
from pathlib import Path
from typing import Optional


def start_django(
    max_hops=10,
    django_project_name="myauth",
    settings_module="myauth.settings.local",
    silent=False,
) -> None:
    """Start the current Django project.

    This function encapsulates the boilerplate code needed to start the current Django
    project in a normal Python script.

    It will also try to detect the path to the current Django project.
    If it can not be found, the function will exit with code 1.

    Args:
        - max_hops: Max number of hops up on the main path to check
        - django_project_name: Name of the Django project
        - settings_module: Qualified name of the settings module in the Django project
        - silent: When True will not produce any output

    Here is an example how to use this function in a script:

    .. code-block:: python

        from app_utils.scripts import start_django

        start_django()

        def main():
            # put Django imports here
            ...

        if __name__ == "__main__":
            main()

    '''
    """

    # calc path of caller script
    previous_frame = inspect.currentframe().f_back
    traceback = inspect.getframeinfo(previous_frame)
    caller_path = Path(traceback.filename).parent

    django_path = _find_django_path(caller_path, max_hops, django_project_name)
    if not django_path:
        if not silent:
            print(
                f"FATAL: Could not find the {django_project_name} "
                f"folder within {max_hops} hops in the path above {caller_path}"
            )
        sys.exit(1)

    sys.path.insert(0, str(django_path))
    if not silent:
        print(f"Starting Django ({django_path})")
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    django.setup()


def _find_django_path(
    start_path: Path, max_search_depth: int, django_project_name: str
) -> Optional[Path]:
    parent_path = start_path
    for _ in range(max_search_depth):
        django_path = parent_path / django_project_name
        if django_path.exists() and (django_path / "manage.py").exists():
            return django_path

        parent_path = parent_path.parent

    return None
