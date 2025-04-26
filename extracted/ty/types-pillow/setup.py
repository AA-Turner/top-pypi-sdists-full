from setuptools import setup

name = "types-Pillow"
description = "Typing stubs for Pillow"
long_description = '''
## Typing stubs for Pillow

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Pillow`](https://github.com/python-pillow/Pillow) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Pillow`.

This version of `types-Pillow` aims to provide accurate annotations
for `Pillow==10.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Pillow. All fixes for
types and metadata should be contributed there.

*Note:* The `Pillow` package includes type annotations or type stubs
since version 10.3.0. Please uninstall the `types-Pillow`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`7865a78de1929ee54797baca0fe07ac33567739f`](https://github.com/python/typeshed/commit/7865a78de1929ee54797baca0fe07ac33567739f) and was tested
with mypy 1.11.1, pyright 1.1.377, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="10.2.0.20240822",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Pillow.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['PIL-stubs'],
      package_data={'PIL-stubs': ['BdfFontFile.pyi', 'BlpImagePlugin.pyi', 'BmpImagePlugin.pyi', 'BufrStubImagePlugin.pyi', 'ContainerIO.pyi', 'CurImagePlugin.pyi', 'DcxImagePlugin.pyi', 'DdsImagePlugin.pyi', 'EpsImagePlugin.pyi', 'ExifTags.pyi', 'FitsImagePlugin.pyi', 'FliImagePlugin.pyi', 'FontFile.pyi', 'FpxImagePlugin.pyi', 'FtexImagePlugin.pyi', 'GbrImagePlugin.pyi', 'GdImageFile.pyi', 'GifImagePlugin.pyi', 'GimpGradientFile.pyi', 'GimpPaletteFile.pyi', 'GribStubImagePlugin.pyi', 'Hdf5StubImagePlugin.pyi', 'IcnsImagePlugin.pyi', 'IcoImagePlugin.pyi', 'ImImagePlugin.pyi', 'Image.pyi', 'ImageChops.pyi', 'ImageCms.pyi', 'ImageColor.pyi', 'ImageDraw.pyi', 'ImageDraw2.pyi', 'ImageEnhance.pyi', 'ImageFile.pyi', 'ImageFilter.pyi', 'ImageFont.pyi', 'ImageGrab.pyi', 'ImageMath.pyi', 'ImageMode.pyi', 'ImageMorph.pyi', 'ImageOps.pyi', 'ImagePalette.pyi', 'ImagePath.pyi', 'ImageQt.pyi', 'ImageSequence.pyi', 'ImageShow.pyi', 'ImageStat.pyi', 'ImageTk.pyi', 'ImageTransform.pyi', 'ImageWin.pyi', 'ImtImagePlugin.pyi', 'IptcImagePlugin.pyi', 'Jpeg2KImagePlugin.pyi', 'JpegImagePlugin.pyi', 'JpegPresets.pyi', 'McIdasImagePlugin.pyi', 'MicImagePlugin.pyi', 'MpegImagePlugin.pyi', 'MpoImagePlugin.pyi', 'MspImagePlugin.pyi', 'PSDraw.pyi', 'PaletteFile.pyi', 'PalmImagePlugin.pyi', 'PcdImagePlugin.pyi', 'PcfFontFile.pyi', 'PcxImagePlugin.pyi', 'PdfImagePlugin.pyi', 'PdfParser.pyi', 'PixarImagePlugin.pyi', 'PngImagePlugin.pyi', 'PpmImagePlugin.pyi', 'PsdImagePlugin.pyi', 'PyAccess.pyi', 'QoiImagePlugin.pyi', 'SgiImagePlugin.pyi', 'SpiderImagePlugin.pyi', 'SunImagePlugin.pyi', 'TarIO.pyi', 'TgaImagePlugin.pyi', 'TiffImagePlugin.pyi', 'TiffTags.pyi', 'WalImageFile.pyi', 'WebPImagePlugin.pyi', 'WmfImagePlugin.pyi', 'XVThumbImagePlugin.pyi', 'XbmImagePlugin.pyi', 'XpmImagePlugin.pyi', '__init__.pyi', '_binary.pyi', '_imaging.pyi', '_tkinter_finder.pyi', '_version.pyi', 'features.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
