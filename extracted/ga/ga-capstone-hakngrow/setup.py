import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ga-capstone-hakngrow", # Replace with your own username
    version="0.0.18",
    author="Howie Ng",
    author_email="hakngrow@gmail.com",
    description="GA Capstone project",
    long_description="GA Capstone project on timeseries stock price predicition.",
    long_description_content_type="text/markdown",
    url="https://github.com/hakngrow/capstone.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)