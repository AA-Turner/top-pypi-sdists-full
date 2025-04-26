from setuptools import setup

name = "types-dataclasses"
description = "Typing stubs for dataclasses"
long_description = '''
## Typing stubs for dataclasses

This is a PEP 561 type stub package for the `dataclasses` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `dataclasses`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/dataclasses. All fixes for
types and metadata should be contributed there.

*Note:* `types-dataclasses` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `ec7ab6d4d6147adf01565d3b2bb2ae4d750f6b1e`.
'''.lstrip()

setup(name=name,
      version="0.6.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dataclasses.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dataclasses-stubs'],
      package_data={'dataclasses-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
