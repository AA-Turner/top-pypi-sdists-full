import setuptools


with open("README.md") as f:
    long_description = f.read()

with open("VERSION") as f:
    version = f.read()

setuptools.setup(
    name="python-md",
    version=version,
    author="Marina Valverde",
    author_email="mdval.eh@gmail.com",
    description="A simple Markdown writer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mdval/python-md",
    project_urls={
        "Bug Tracker": "https://gitlab.com/mdval/python-md/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["markdown", "md", "python", "python3"],
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    python_requires=">=3.6",
    py_modules=["python_md"],
    install_requires=[],
)
