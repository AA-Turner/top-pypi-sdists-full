import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="maseya-z3pr",
    version="1.0.0.rc1",
    author="Nelson Garcia",
    author_email="swr.ngarcia@gmail.com",
    description="Randomize palette data for Legend of Zelda: A Link to the Past.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/maseya/z3pr-py",
    packages=setuptools.find_packages(),
    package_data={"maseya.z3pr": ["data/*.json"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics :: Editors",
        "Topic :: Utilities",
    ],
    python_requires=">=3.4",
)
