from setuptools import setup

name = "types-paho-mqtt"
description = "Typing stubs for paho-mqtt"
long_description = '''
## Typing stubs for paho-mqtt

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`paho-mqtt`](https://github.com/eclipse/paho.mqtt.python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`paho-mqtt`.

This version of `types-paho-mqtt` aims to provide accurate annotations
for `paho-mqtt==1.6.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/paho-mqtt. All fixes for
types and metadata should be contributed there.

*Note:* The `paho-mqtt` package includes type annotations or type stubs
since version 2.0.0. Please uninstall the `types-paho-mqtt`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `5c75292f26aec8e6348a17d32077f408a1337988` and was tested
with mypy 1.9.0, pyright 1.1.354, and
pytype 2024.3.19.
'''.lstrip()

setup(name=name,
      version="1.6.0.20240321",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/paho-mqtt.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['paho-stubs'],
      package_data={'paho-stubs': ['__init__.pyi', 'mqtt/__init__.pyi', 'mqtt/client.pyi', 'mqtt/matcher.pyi', 'mqtt/packettypes.pyi', 'mqtt/properties.pyi', 'mqtt/publish.pyi', 'mqtt/reasoncodes.pyi', 'mqtt/subscribe.pyi', 'mqtt/subscribeoptions.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
