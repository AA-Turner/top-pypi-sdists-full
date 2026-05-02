import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="cidp", # Replace with your own username
    version="0.0.11",
    author="mccho",
    author_email="skt.mccho@sk.com",
    description="CIDP Python SDK",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://gitlab.cidp.io/common/pypi/cidp",
    packages=setuptools.find_packages(),
    install_requires=[
        "boto3",
        "pyspark",
        "kubernetes",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)