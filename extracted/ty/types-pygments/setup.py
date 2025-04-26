from setuptools import setup

name = "types-Pygments"
description = "Typing stubs for Pygments"
long_description = '''
## Typing stubs for Pygments

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Pygments`](https://github.com/pygments/pygments) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `Pygments`. This version of
`types-Pygments` aims to provide accurate annotations for
`Pygments==2.19.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/Pygments`](https://github.com/python/typeshed/tree/main/stubs/Pygments)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.396,
and pytype 2024.10.11.
It was generated from typeshed commit
[`714c99bbdbdc4af11ffc506e71a8c29bffb3b520`](https://github.com/python/typeshed/commit/714c99bbdbdc4af11ffc506e71a8c29bffb3b520).
'''.lstrip()

setup(name=name,
      version="2.19.0.20250305",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Pygments.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-docutils'],
      packages=['pygments-stubs'],
      package_data={'pygments-stubs': ['__init__.pyi', 'cmdline.pyi', 'console.pyi', 'filter.pyi', 'filters/__init__.pyi', 'formatter.pyi', 'formatters/__init__.pyi', 'formatters/_mapping.pyi', 'formatters/bbcode.pyi', 'formatters/html.pyi', 'formatters/img.pyi', 'formatters/irc.pyi', 'formatters/latex.pyi', 'formatters/other.pyi', 'formatters/pangomarkup.pyi', 'formatters/rtf.pyi', 'formatters/svg.pyi', 'formatters/terminal.pyi', 'formatters/terminal256.pyi', 'lexer.pyi', 'lexers/__init__.pyi', 'lexers/javascript.pyi', 'lexers/jsx.pyi', 'lexers/kusto.pyi', 'lexers/ldap.pyi', 'lexers/lean.pyi', 'lexers/lisp.pyi', 'lexers/prql.pyi', 'lexers/vip.pyi', 'lexers/vyper.pyi', 'modeline.pyi', 'plugin.pyi', 'regexopt.pyi', 'scanner.pyi', 'sphinxext.pyi', 'style.pyi', 'styles/__init__.pyi', 'token.pyi', 'unistring.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
