from os import path
from setuptools import setup, find_packages
from elmax_api import __name__ as target_name
from elmax_api import __version__ as target_version
from elmax_api import __url__ as target_url
from elmax_api import __license__ as target_license
from elmax_api import __author__ as target_author
from elmax_api import __description__ as target_description
from elmax_api import __keywords__ as target_keywords
from elmax_api import __author_email__ as target_author_email

here = path.abspath(path.dirname(__file__))

# Read the readme and put it into the description field of setup.py
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements file and set the dependencies accordingly
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = [line.strip() for line in f]

setup(
    name=target_name,
    version=target_version,
    packages=find_packages(exclude=("tests",)),
    url=target_url,
    license=target_license,
    author=target_author,
    author_email=target_author_email,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    description=target_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=target_keywords,
    project_urls={
        "Documentation": target_url,
        "Source": target_url,
        "Tracker": target_url,
    },
    data_files=[('.', ['requirements.txt'])],
    install_requires=requirements,
    python_requires=">=3.7",
    test_suite="tests",
)
