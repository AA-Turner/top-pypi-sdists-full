from setuptools import setup, find_packages

version = {}
with open("proglog/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="proglog",
    version=version["__version__"],
    author="Zulko",
    description="Log and progress bar manager for console, notebooks, web...",
    long_description=open("pypi-readme.rst").read(),
    license="MIT",
    keywords="logger log progress bar",
    install_requires=["tqdm"],
    packages=find_packages(exclude="docs"),
)
