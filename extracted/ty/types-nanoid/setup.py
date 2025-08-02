from setuptools import setup

name = "types-nanoid"
description = "Typing stubs for nanoid"
long_description = '''
## Typing stubs for nanoid

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`nanoid`](https://github.com/puyuan/py-nanoid) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`nanoid`.

This version of `types-nanoid` aims to provide accurate annotations
for `nanoid==2.0.0`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/nanoid. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `4b6558c12ac43cd40716cd6452fe98a632ae65d7` and was tested
with mypy 1.10.0, pyright 1.1.365, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.0.0.20240601",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/nanoid.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['nanoid-stubs'],
      package_data={'nanoid-stubs': ['__init__.pyi', 'algorithm.pyi', 'generate.pyi', 'method.pyi', 'non_secure_generate.pyi', 'resources.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
