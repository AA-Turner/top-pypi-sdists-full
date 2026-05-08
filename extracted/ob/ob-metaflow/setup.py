import os, glob
from setuptools import setup, find_packages

with open("metaflow/version.py", mode="r") as f:
    version = f.read().splitlines()[0].split("=")[1].strip(" \"'")


def read_dev_requirements():
    with open("devtools/requirements-devstack.txt") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def find_devtools_files():
    # Returns a list of (install_dir, [files]) tuples preserving subdirectory structure.
    entries = {}
    for path in glob.iglob("devtools/**/*", recursive=True):
        if os.path.isfile(path):
            rel_dir = os.path.dirname(path)  # e.g. "devtools/tilt/k8s"
            install_dir = os.path.join(
                "share/metaflow", rel_dir
            )  # e.g. "share/metaflow/devtools/tilt/k8s"
            entries.setdefault(install_dir, []).append(path)
    return list(entries.items())


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
    data_files=find_devtools_files(),
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
        "dev": read_dev_requirements(),
    },
)
