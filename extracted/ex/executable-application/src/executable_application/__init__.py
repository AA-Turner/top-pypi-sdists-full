import argparse
from importlib.metadata import version


def get_version() -> str:
    return version("executable-application")


def main() -> None:
    parser = argparse.ArgumentParser(description="Executable application")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {get_version()}"
    )

    args = parser.parse_args()

    if len(vars(args)) == 0:
        print("Hello from app!")
