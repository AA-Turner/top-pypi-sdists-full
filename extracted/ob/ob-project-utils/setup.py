from setuptools import setup, find_packages, find_namespace_packages

setup(
    name="ob-project-utils",
    version="0.1.42",
    packages=find_packages()
    + find_namespace_packages(include=["metaflow_extensions.*"]),
    entry_points={
        "console_scripts": [
            "obproject-deploy=deploy.deploy_obproject:main",
        ],
    },
    install_requires=["requests", "toml; python_version<'3.11'"],
    author="Ville Tuulos",
    author_email="ville@outerbounds.co",
    description="Utilities for Outerbounds projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"": ["base.html"]},
    include_package_data=True,
)
