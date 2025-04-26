from setuptools import setup

name = "types-tzlocal"
description = "Typing stubs for tzlocal"
long_description = '''
## Typing stubs for tzlocal

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`tzlocal`](https://github.com/regebro/tzlocal) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`tzlocal`.

This version of `types-tzlocal` aims to provide accurate annotations
for `tzlocal==5.1`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/tzlocal. All fixes for
types and metadata should be contributed there.

*Note:* The `tzlocal` package includes type annotations or type stubs
since version 5.2. Please uninstall the `types-tzlocal`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `40caa050ce66a8dd62a62c4b4631767c4092d998` and was tested
with mypy 1.6.1, pyright 1.1.332, and
pytype 2023.10.17.
'''.lstrip()

setup(name=name,
      version="5.1.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tzlocal.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pytz'],
      packages=['tzlocal-stubs'],
      package_data={'tzlocal-stubs': ['__init__.pyi', 'utils.pyi', 'windows_tz.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
