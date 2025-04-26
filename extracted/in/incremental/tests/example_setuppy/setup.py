from setuptools import setup

setup(
    name="example_setuppy",
    package_dir={"": "src"},
    packages=["example_setuppy"],
    use_incremental=True,
    zip_safe=False,
    setup_requires=[
        "incremental",
    ],
)
