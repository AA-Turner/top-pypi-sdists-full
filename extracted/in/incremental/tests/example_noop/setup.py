from setuptools import setup

setup(
    name="example_noop",
    version="100",
    packages=["example_noop"],
    zip_safe=False,
    setup_requires=[
        # Ensure Incremental is installed for test purposes
        # (but it won't do anything).
        "incremental",
    ],
)
