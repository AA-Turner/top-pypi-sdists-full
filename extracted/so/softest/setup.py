import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="softest",
    version="1.2.0.0",
    author="Nick Umble",
    author_email="privately.maintained@for.now",
    description="Supports lightweight soft assertions by extending the unittest.TestCase class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://privately.maintained.for.now",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Freeware",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing"
    ),
)
