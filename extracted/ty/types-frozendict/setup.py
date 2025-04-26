from setuptools import setup

name = "types-frozendict"
description = "Typing stubs for frozendict"
long_description = '''
## Typing stubs for frozendict

This is a PEP 561 type stub package for the `frozendict` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `frozendict`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/frozendict. All fixes for
types and metadata should be contributed there.

*Note:* The `frozendict` package includes type annotations or type stubs
since version 2.2.0. Please uninstall the `types-frozendict`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `81fd55a885e678559471710f249c7e27d02ec212`.
'''.lstrip()

setup(name=name,
      version="2.0.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/frozendict.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['frozendict-stubs'],
      package_data={'frozendict-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
