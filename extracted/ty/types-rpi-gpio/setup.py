from setuptools import setup

name = "types-RPi.GPIO"
description = "Typing stubs for RPi.GPIO"
long_description = '''
## Typing stubs for RPi.GPIO

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`RPi.GPIO`](https://sourceforge.net/p/raspberry-gpio-python/code/) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `RPi.GPIO`. This version of
`types-RPi.GPIO` aims to provide accurate annotations for
`RPi.GPIO==0.7.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/RPi.GPIO`](https://github.com/python/typeshed/tree/main/stubs/RPi.GPIO)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.396,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b93eae52affaedfda79c00f662f50a2ef3b24c46`](https://github.com/python/typeshed/commit/b93eae52affaedfda79c00f662f50a2ef3b24c46).
'''.lstrip()

setup(name=name,
      version="0.7.0.20250318",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/RPi.GPIO.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['RPi-stubs'],
      package_data={'RPi-stubs': ['GPIO/__init__.pyi', '__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
