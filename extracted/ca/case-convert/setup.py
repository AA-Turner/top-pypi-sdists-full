import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="case_convert",
    version="1.1.0",
    author="SECRET Olivier",
    author_email="pypi-package-case_convert@devo.live",
    description="Cross library to convert case with permissive input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/olive007/case-convert",
    packages=["case_convert"],
    package_data={
        "": ["*.txt"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        "Operating System :: OS Independent",
    ]
)
