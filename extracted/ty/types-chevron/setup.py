from setuptools import setup

name = "types-chevron"
description = "Typing stubs for chevron"
long_description = '''
## Typing stubs for chevron

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`chevron`](https://github.com/noahmorrison/chevron) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `chevron`. This version of
`types-chevron` aims to provide accurate annotations for
`chevron==0.14.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/chevron`](https://github.com/python/typeshed/tree/main/stubs/chevron)
directory.

This package was tested with
mypy 1.14.1,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`33d1b169c1780529e8c2b91858caf58852d73220`](https://github.com/python/typeshed/commit/33d1b169c1780529e8c2b91858caf58852d73220).
'''.lstrip()

setup(name=name,
      version="0.14.2.20250103",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/chevron.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['chevron-stubs'],
      package_data={'chevron-stubs': ['__init__.pyi', 'main.pyi', 'metadata.pyi', 'renderer.pyi', 'tokenizer.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
