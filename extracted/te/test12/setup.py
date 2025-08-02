from setuptools import setup, find_packages

setup(
    name="test12",
    version="0.1",
    packages=find_packages(),
    install_requires=[
    ],
    author="lpz",
    author_email="yywfqq@live.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
