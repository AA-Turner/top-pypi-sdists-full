from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='line-profiler-pycharm',
    version='1.2.0',
    author='Justen Ingels',
    author_email='jhwj.ingels@gmail.com',
    description="PyCharm Line Profiler helper package with which one can visualize profiles from "
                "the 'line-profiler' into PyCharm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/line-profiler-pycharm/line-profiler-pycharm-python/",
    install_requires=[
        'line-profiler'
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'
)
