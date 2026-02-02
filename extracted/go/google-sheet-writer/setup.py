import os
from setuptools import setup


DIR = os.path.dirname(os.path.abspath(__file__))


def get_version():
    version = {}
    with open(
        os.path.join(DIR, "google_sheet_writer", "version.py"), encoding="utf8"
    ) as f:
        exec(f.read(), version)
    return version["__version__"]


with open(os.path.join(DIR, "README.md"), "r", encoding="utf8") as f:
    long_description = f.read()


setup(
    name="google_sheet_writer",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="Easy wrapper around gspread and gspread-formatting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/google_sheet_writer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["google_sheet_writer"],
    install_requires=[
        "gspread",
        "gspread-formatting"
    ],
)
