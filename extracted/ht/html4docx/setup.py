from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "Convert docx files to html"
LONG_DESCRIPTION = """# html4docx

A package to convert docx files to html with added features on top of mammoth library.

Developed by Paras Jain (c) 2023

## Features

- Added support for all-types of images.
- Images like .emf are converted to .png type.
- Image dimensions present in the file are converted for html with preset same width and height.

**Note**
To convert .emf image types to .png, linux env is necessary with inkscape installed.

## Examples of How To Use

Convert docx to html

```python
from html4docx.convert import docx_to_html

html = docx_to_html("your_docx_filepath_here", is_convert)
```

- your_docx_filepath_here: Your docx file path
- is_convert: is a boolean to convert .emf imgs to .png
"""

# Setting up
setup(
    name="html4docx",
    version=VERSION,
    author="Paras Jain",
    author_email="<paras.2426@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["mammoth", "beautifulsoup4", "python-docx"],
    keywords=[
        "python",
        "docx",
        "html",
        "docx-2-html",
        "docx2html",
        "docx-to-html",
        "convert",
        "docx_to_html",
        "html4docx",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
