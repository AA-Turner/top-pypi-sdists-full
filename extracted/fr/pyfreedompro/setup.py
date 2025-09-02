import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfreedompro", # Replace with your own username
    version="1.1.0",
    author="Stefano Cartisano",
    author_email="stefano055415@gmail.com",
    description="Freedompro API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefano055415/pyfreedompro",
    project_urls={
        "Bug Tracker": "https://github.com/stefano055415/pyfreedompro/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
