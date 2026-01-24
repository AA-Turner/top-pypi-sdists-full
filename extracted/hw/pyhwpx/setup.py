from pathlib import Path
import re
import sys
from setuptools import setup, find_packages


def read_version():
    version_file = Path(__file__).parent / "pyhwpx" / "version.py"
    content = version_file.read_text()
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Cannot find __version__ in version.py")


if sys.platform != "win32":
    raise RuntimeError("pyhwpx는 Windows에서만 동작합니다.")

this_dir = Path(__file__).parent.resolve()
long_description = (this_dir / "README.md").read_text(encoding="utf-8")
long_description_content_type = "text/markdown"

setup(
    name="pyhwpx",
    version=read_version(),
    description="아래아한글 자동화를 위한 파이썬 모듈 pyhwpx입니다.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="ilco",
    author_email="martinii.fun@gmail.com",
    url="https://martiniifun.github.io/pyhwpx/",
    python_requires=">= 3.9",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pyhwpx": ["FilePathCheckerModule.dll"],
    },
    install_requires=["numpy", "pandas", "pywin32", "openpyxl", "pyperclip", "Pillow"],
    zip_safe=False,
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ],
)
