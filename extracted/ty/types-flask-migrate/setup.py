from setuptools import setup

name = "types-Flask-Migrate"
description = "Typing stubs for Flask-Migrate"
long_description = '''
## Typing stubs for Flask-Migrate

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Flask-Migrate`](https://github.com/miguelgrinberg/Flask-Migrate) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `Flask-Migrate`. This version of
`types-Flask-Migrate` aims to provide accurate annotations for
`Flask-Migrate==4.1.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/Flask-Migrate`](https://github.com/python/typeshed/tree/main/stubs/Flask-Migrate)
directory.

This package was tested with
mypy 1.14.1,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`38d2fe81fee593468d0738f89a5b5101a86f4e53`](https://github.com/python/typeshed/commit/38d2fe81fee593468d0738f89a5b5101a86f4e53).
'''.lstrip()

setup(name=name,
      version="4.1.0.20250112",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Flask-Migrate.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['Flask-SQLAlchemy>=3.0.1', 'Flask>=2.0.0'],
      packages=['flask_migrate-stubs'],
      package_data={'flask_migrate-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
