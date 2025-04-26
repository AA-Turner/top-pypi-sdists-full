from setuptools import setup, find_packages

setup(
    name="2to3",
    description="Adds the 2to3 command directly to entry_points.",
    license="MIT",
    version="1.0",
    author="xoviat",
    author_email="xoviat@gmail.com",
    keywords=["2to3"],
    long_description="",
    packages=find_packages(),
    entry_points={
        'console_scripts' : [
            '2to3 = cmd_2to3.__main__:main',
        ],
    },
)
