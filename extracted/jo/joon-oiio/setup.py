from setuptools import setup, find_packages


setup(
  name = 'joon_oiio',
  version = '0.1',
  license = 'MIT',
  description = 'OpenImageIO (OIIO) for Python',
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  author = 'joon',
  author_email = 'postmann@kakao.com',
  url = 'https://github.com/Correct-Syntax/py-oiio',
  keywords = ['openimageio', 'oiio'],
  classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3.7', #3.10
  ],
  packages=find_packages(exclude=[]),
  package_data={
    # If any package (!) contains ... files, include them:
    "": [
        "*.pyd",
        "*.dll",
        "*.so",
    ]
  },
)
