import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sprinkler_util",
    author="Henry Jones",
    author_email="henryivesjones@gmail.com",
    url="https://github.com/henryivesjones/sprinkler/sprinkler_util/python",
    description="Utilities for sprinkler tasks.",
    packages=["sprinkler_util"],
    package_dir={"sprinkler_util": "sprinkler_util"},
    package_data={
        "sprinkler_util": [
            "py.typed",
        ],
    },
    include_package_data=True,
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
    ],
)
