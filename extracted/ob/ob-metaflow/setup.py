import os, glob
from setuptools import setup, find_packages

with open("metaflow/version.py", mode="r") as f:
    version = f.read().splitlines()[0].split("=")[1].strip(" \"'")


def find_devtools_files():
    filepaths = []
    for path in glob.iglob("devtools/**/*", recursive=True):
        if os.path.isfile(path):
            filepaths.append(path)
    return filepaths


setup(
    include_package_data=True,
    name="ob-metaflow",
    version=version,
    description="Metaflow: More AI and ML, Less Engineering",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Netflix, Outerbounds & the Metaflow Community",
    author_email="help@outerbounds.co",
    license="Apache License 2.0",
    packages=find_packages(exclude=["metaflow_test"]),
    py_modules=[
        "metaflow",
    ],
    package_data={
        "metaflow": [
            "tutorials/*/*",
            "plugins/env_escape/configurations/*/*",
            "py.typed",
            "**/*.pyi",
        ]
    },
    data_files=[("share/metaflow/devtools", find_devtools_files())],
    entry_points="""
        [console_scripts]
        metaflow=metaflow.cmd.main_cli:start
        metaflow-dev=metaflow.cmd.make_wrapper:main
      """,
    install_requires=[
        "requests",
        "boto3",
        "pylint",
        "kubernetes",
    ],
    extras_require={
        "stubs": ["metaflow-stubs==%s" % version],
    },
)
