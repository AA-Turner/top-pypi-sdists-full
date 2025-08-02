import os

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def raise_if_path_not_exists(path: str):
    if not os.path.exists(path):
        raise Exception(f"path {path} not exists")


def clear_text_file(filepath: str):
    if not os.path.exists(filepath):
        return
    with open(filepath, mode="w") as f:
        f.write("")


def create_text_file(filepath: str, text: str = ""):
    if os.path.exists(filepath):
        return
    with open(filepath, mode="w") as f:
        f.write(text)
