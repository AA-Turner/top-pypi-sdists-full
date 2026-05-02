from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='spreadsheet-migrator',
    version='1.0',
    author="Daniel",
    author_email="danielsheh02@gmail.com",
    description='Plugin to migrate your data from spreadsheets',
    long_description=long_description,
    long_description_content_type="text/markdown",
    readme="README.md",
    install_requires=[
        'openpyxl==3.1.1'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
