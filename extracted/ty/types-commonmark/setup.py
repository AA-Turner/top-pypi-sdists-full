from setuptools import setup

name = "types-commonmark"
description = "Typing stubs for commonmark"
long_description = '''
## Typing stubs for commonmark

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`commonmark`](https://github.com/rtfd/commonmark.py) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `commonmark`. This version of
`types-commonmark` aims to provide accurate annotations for
`commonmark==0.9.*`.

`commonmark` is deprecated in favor of [markdown-it-py](https://pypi.org/project/markdown-it-py/).
See [this issue](https://github.com/readthedocs/commonmark.py/issues/308) for background and discussion.

*Note:* `types-commonmark` is unmaintained and won't be updated.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/commonmark`](https://github.com/python/typeshed/tree/main/stubs/commonmark)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.398,
and pytype 2024.10.11.
It was generated from typeshed commit
[`8c9451154e7f24b997892dc82bb4326531e165a6`](https://github.com/python/typeshed/commit/8c9451154e7f24b997892dc82bb4326531e165a6).
'''.lstrip()

setup(name=name,
      version="0.9.2.20250330",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/commonmark.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['commonmark-stubs'],
      package_data={'commonmark-stubs': ['__init__.pyi', 'blocks.pyi', 'cmark.pyi', 'common.pyi', 'dump.pyi', 'entitytrans.pyi', 'inlines.pyi', 'main.pyi', 'node.pyi', 'normalize_reference.pyi', 'render/__init__.pyi', 'render/html.pyi', 'render/renderer.pyi', 'render/rst.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
