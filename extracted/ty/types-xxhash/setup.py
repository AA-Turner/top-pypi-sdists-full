from setuptools import setup

name = "types-xxhash"
description = "Typing stubs for xxhash"
long_description = '''
## Typing stubs for xxhash

This is a PEP 561 type stub package for the `xxhash` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`xxhash`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/xxhash. All fixes for
types and metadata should be contributed there.

*Note:* The `xxhash` package includes type annotations or type stubs
since version 3.1.0. Please uninstall the `types-xxhash`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `880c0da4045cd5ff2c29b73429629adf27e49d50`.
'''.lstrip()

setup(name=name,
      version="3.0.5.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/xxhash.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['xxhash-stubs'],
      package_data={'xxhash-stubs': ['__init__.pyi', 'version.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
