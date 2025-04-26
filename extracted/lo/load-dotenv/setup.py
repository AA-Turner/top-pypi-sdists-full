import os.path
from distutils.command.build import build

from setuptools import setup


class BuildPyWithPth(build):
    def run(self) -> None:
        super().run()
        outfile = os.path.join(self.build_lib, "load_dotenv.pth")
        self.copy_file("load_dotenv.pth", outfile)


with open("README.md") as f:
    long_description = f.read()

setup(
    cmdclass={"build": BuildPyWithPth},
    name="load-dotenv",
    version="0.1.0",
    py_modules=["load_dotenv"],
    url="https://github.com/fly/load-dotenv",
    author="fly",
    description="Automatically and implicitly load environment variables from .env file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["python-dotenv"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    keywords=["environment variables", "env", ".env", "dotenv"],
    project_urls={
        "Source": "https://github.com/fly/load-dotenv",
        "Tracker": "https://github.com/fly/load-dotenv/issues",
    },

)
