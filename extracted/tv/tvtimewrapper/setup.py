import setuptools

long_description = """# TVTime Wrapper

Simple class that allows the usage of TVTime via script with APIs.

## Usage

from tvtimewrapper import TVTimeWrapper

tvtime = TVTimeWrapper("username","password")

Full documentation available here: https://github.com/seanwlk/tvtimewrapper
"""

setuptools.setup(
  name="tvtimewrapper",
  version="0.0.3",
  author="seanwlk",
  author_email="seanwlk@my.com",
  description="Python Wrapper library for TVTime App (formerly TV Show Time)",
  long_description_content_type="text/markdown",
  long_description=long_description,
  url="https://github.com/seanwlk/tvtimewrapper",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)