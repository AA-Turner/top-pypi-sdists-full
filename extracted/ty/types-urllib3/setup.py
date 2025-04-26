from setuptools import setup

name = "types-urllib3"
description = "Typing stubs for urllib3"
long_description = '''
## Typing stubs for urllib3

This is a PEP 561 type stub package for the `urllib3` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`urllib3`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/urllib3. All fixes for
types and metadata should be contributed there.

*Note:* The `urllib3` package includes type annotations or type stubs
since version 2.0.0. Please uninstall the `types-urllib3`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="1.26.25.14",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/urllib3.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['urllib3-stubs'],
      package_data={'urllib3-stubs': ['__init__.pyi', '_collections.pyi', 'connection.pyi', 'connectionpool.pyi', 'contrib/__init__.pyi', 'contrib/socks.pyi', 'exceptions.pyi', 'fields.pyi', 'filepost.pyi', 'packages/__init__.pyi', 'poolmanager.pyi', 'request.pyi', 'response.pyi', 'util/__init__.pyi', 'util/connection.pyi', 'util/queue.pyi', 'util/request.pyi', 'util/response.pyi', 'util/retry.pyi', 'util/ssl_.pyi', 'util/ssl_match_hostname.pyi', 'util/timeout.pyi', 'util/url.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
