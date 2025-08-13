
import sys
from setuptools import setup, find_packages
from distutils.cmd import Command
from setuptools.command.install import install
from setuptools.command.build import build
import subprocess
import platform
import tempfile
from zipfile import ZipFile
from pathlib import Path
import shutil


class BuildCommand(build):
    def run(self):
        tmpdir = tempfile.mkdtemp()
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--no-input",
                "--timeout",
                "1000",
                "--platform",
                "musllinux_1_1_" + platform.machine(),
                "--only-binary=:all:",
                "deltachat-rpc-server==2.11.0",
            ],
            cwd=tmpdir,
        )

        wheel_path = next(Path(tmpdir).glob("*.whl"))
        with ZipFile(wheel_path, "r") as wheel:
            exe_path = wheel.extract("deltachat_rpc_server/deltachat-rpc-server", "src")
            Path(exe_path).chmod(0o700)
            wheel.extract("deltachat_rpc_server/__init__.py", "src")

        shutil.rmtree(tmpdir)
        return super().run()


setup(
    cmdclass={"build": BuildCommand},
    package_data={"deltachat_rpc_server": ["deltachat-rpc-server"]},
)
