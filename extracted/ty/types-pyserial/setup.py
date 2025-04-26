from setuptools import setup

name = "types-pyserial"
description = "Typing stubs for pyserial"
long_description = '''
## Typing stubs for pyserial

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyserial`](https://github.com/pyserial/pyserial) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pyserial`. This version of
`types-pyserial` aims to provide accurate annotations for
`pyserial==3.5.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pyserial`](https://github.com/python/typeshed/tree/main/stubs/pyserial)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.397,
and pytype 2024.10.11.
It was generated from typeshed commit
[`4fff7b7d0165120bf79928534c88dffffdcb5da2`](https://github.com/python/typeshed/commit/4fff7b7d0165120bf79928534c88dffffdcb5da2).
'''.lstrip()

setup(name=name,
      version="3.5.0.20250326",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyserial.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['serial-stubs'],
      package_data={'serial-stubs': ['__init__.pyi', '__main__.pyi', 'rfc2217.pyi', 'rs485.pyi', 'serialcli.pyi', 'serialjava.pyi', 'serialposix.pyi', 'serialutil.pyi', 'serialwin32.pyi', 'threaded/__init__.pyi', 'tools/__init__.pyi', 'tools/hexlify_codec.pyi', 'tools/list_ports.pyi', 'tools/list_ports_common.pyi', 'tools/list_ports_linux.pyi', 'tools/list_ports_osx.pyi', 'tools/list_ports_posix.pyi', 'tools/list_ports_windows.pyi', 'tools/miniterm.pyi', 'urlhandler/__init__.pyi', 'urlhandler/protocol_alt.pyi', 'urlhandler/protocol_cp2110.pyi', 'urlhandler/protocol_hwgrep.pyi', 'urlhandler/protocol_loop.pyi', 'urlhandler/protocol_rfc2217.pyi', 'urlhandler/protocol_socket.pyi', 'urlhandler/protocol_spy.pyi', 'win32.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
