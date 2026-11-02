import os
import sys
from setuptools import setup

VERSION = '1.1.3'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print(f"You probably want to tag the version now:\n  git tag -a {VERSION} -m 'version {VERSION}'\n  git push --tags")
    sys.exit()

setup(
    name="markdown_inline_graphviz_extension",
    version=VERSION,
    py_modules=["markdown_inline_graphviz"],
    install_requires=['Markdown>=3.3'],
    author="Cesar Morel",
    author_email="cesaremoreln@gmail.com",
    description="Render inline graphs with Markdown and Graphviz (python3 version)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/cesaremorel/markdown-inline-graphviz",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing :: Markup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
)
