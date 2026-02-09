import os

_dirs_created = set()

def creating_dir(dir):
    if dir not in _dirs_created:
        _dirs_created.add(dir)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    return dir