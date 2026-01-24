import subprocess
import sys


class TestLinters:

    def test_flake8(self):
        subprocess.run((sys.executable, "-m", "flake8", "qemu/"), check=True)

    def test_mypy(self):
        subprocess.run((sys.executable, "-m", "mypy", "-p", "qemu"), check=True)

    def test_isort(self):
        subprocess.run(
            (sys.executable, "-m", "isort", "-c", "qemu/"),
            check=True,
        )

    def test_pylint(self):
        subprocess.run((sys.executable, "-m", "pylint", "qemu/"), check=True)
