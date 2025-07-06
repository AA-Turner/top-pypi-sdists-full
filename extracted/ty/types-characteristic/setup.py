from setuptools import setup

name = "types-characteristic"
description = "Typing stubs for characteristic"
long_description = '''
## Typing stubs for characteristic

This is a PEP 561 type stub package for the `characteristic` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `characteristic`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/characteristic. All fixes for
types and metadata should be contributed there.

*Note:* `types-characteristic` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `60507a08a20b19c74473c30089f77ff483136a08`.
'''.lstrip()

setup(name=name,
      version="14.3.7",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/characteristic.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['characteristic-stubs'],
      package_data={'characteristic-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
