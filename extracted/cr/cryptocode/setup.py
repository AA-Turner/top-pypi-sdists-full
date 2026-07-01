import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
  name = 'cryptocode',         # How you named your package folder (MyLib)
  packages=setuptools.find_packages(),
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_description,
  long_description_content_type="text/markdown",
  description = 'Python library used to encrypt and decrypt strings in the simplest possible way.',   # Give a short description about your library
  author = 'gdavid7',                   # Type in your name
  url = 'https://github.com/gdavid7/cryptocode',   # Provide either the link to your github or to your website
  keywords = ['cryptocode', 'key','crypto','encodestring'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pycryptodomex',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)