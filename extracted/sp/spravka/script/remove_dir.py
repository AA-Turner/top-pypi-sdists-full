import os
import shutil

DIRS: list = ['dist', 'spravka.egg-info']


def main() -> None:
    for dir in DIRS:
        if os.path.exists(dir):
            shutil.rmtree(dir)
