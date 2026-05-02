import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='g2m-snowflake-sdk-python',
    version='1.0.15',
    description='Python SDK for the G2M Platform API',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/g2mai/g2m-snowflake-sdk-python",
    author='G2M Team',
    author_email='support@g2m.ai',
    license='Apache 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=['g2mclient'],
    install_requires=[
    ]
)
