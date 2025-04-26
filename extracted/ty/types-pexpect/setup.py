from setuptools import setup

name = "types-pexpect"
description = "Typing stubs for pexpect"
long_description = '''
## Typing stubs for pexpect

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pexpect`](https://github.com/pexpect/pexpect) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pexpect`. This version of
`types-pexpect` aims to provide accurate annotations for
`pexpect==4.9.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pexpect`](https://github.com/python/typeshed/tree/main/stubs/pexpect)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`4aad825db39b10cc8bce721b92a45c256cb3c5b6`](https://github.com/python/typeshed/commit/4aad825db39b10cc8bce721b92a45c256cb3c5b6).
'''.lstrip()

setup(name=name,
      version="4.9.0.20241208",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pexpect.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pexpect-stubs'],
      package_data={'pexpect-stubs': ['ANSI.pyi', 'FSM.pyi', '__init__.pyi', '_async.pyi', 'exceptions.pyi', 'expect.pyi', 'fdpexpect.pyi', 'popen_spawn.pyi', 'pty_spawn.pyi', 'pxssh.pyi', 'replwrap.pyi', 'run.pyi', 'screen.pyi', 'socket_pexpect.pyi', 'spawnbase.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
