import setuptools
with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynum",
    version="0.0.1",
    author="Arunima Bhattacharya",
    description="Playing with packages",
    long_description=long_description,
    long_description_content_typt="text/markdown",
    url="https://github.com/Arunima505/pynum",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
