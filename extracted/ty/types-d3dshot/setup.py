from setuptools import setup

name = "types-D3DShot"
description = "Typing stubs for D3DShot"
long_description = '''
## Typing stubs for D3DShot

This is a PEP 561 type stub package for the `D3DShot` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`D3DShot`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/D3DShot. All fixes for
types and metadata should be contributed there.

*Note:* `types-D3DShot` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6a37fb050a5e785482016bbd914901dde3bed553`.
'''.lstrip()

setup(name=name,
      version="0.1.0.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/D3DShot.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-Pillow'],
      packages=['d3dshot-stubs'],
      package_data={'d3dshot-stubs': ['__init__.pyi', 'capture_output.pyi', 'capture_outputs/__init__.pyi', 'capture_outputs/numpy_capture_output.pyi', 'capture_outputs/numpy_float_capture_output.pyi', 'capture_outputs/pil_capture_output.pyi', 'capture_outputs/pytorch_capture_output.pyi', 'capture_outputs/pytorch_float_capture_output.pyi', 'capture_outputs/pytorch_float_gpu_capture_output.pyi', 'capture_outputs/pytorch_gpu_capture_output.pyi', 'd3dshot.pyi', 'display.pyi', 'dll/__init__.pyi', 'dll/d3d.pyi', 'dll/dxgi.pyi', 'dll/shcore.pyi', 'dll/user32.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
