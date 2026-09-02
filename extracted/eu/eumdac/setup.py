import os
from setuptools import setup

about = {}
with open(os.path.join("eumdac", "__version__.py")) as f:
    exec(f.read(), about)

with open("README.md", mode="r") as file:
    readme = file.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    project_urls={
        "User guide": about["__documentation__"],
        "API reference": about["__api_documentation__"],
    },
    license=about["__license__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
    packages=["eumdac"],
    package_data={"eumdac": ["endpoints.ini", "py.typed"]},
    python_requires=">=3.7",
    install_requires=["requests>=2.5.0", "pyyaml", "urllib3", "paho-mqtt"],
    extras_require={
        "test": [
            "mypy",
            "pytest<9",
            "pytest-cov",
            "responses",
            "types-requests<2.32.0.20240905",
            "types-setuptools",
            "sh",
        ]
    },
    entry_points={"console_scripts": ["eumdac=eumdac.cli:cli"]},
)
