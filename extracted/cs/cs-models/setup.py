import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


INSTALL_REQUIRES = [
    "marshmallow==3.19.0",
    "PyMySQL==1.1.1",
    "python-dateutil==2.8.2",
    "pytz==2022.1",
    "SQLAlchemy==1.4.35",
    "boto3>=1.28.30",
    "botocore>=1.31.30",
    "s3transfer>=0.6.2",
    "six==1.16.0",
    "urllib3>=1.26.19",
    "dnspython==2.6.1",
    "pymongo==4.6.3",
    "psycopg2-binary==2.9.3",
    "sshtunnel==0.4.0",
]

if __name__ == "__main__":
    setuptools.setup(
        name="cs-models",
        version="0.0.794",
        author="Shrey Verma",
        author_email="sverma@mindgram.ai",
        description="MySQL db models",
        # long_description=long_description,
        # long_description_content_type='text/markdown',
        url="https://github.com/mindgram/cs-models",
        packages=setuptools.find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=[
            "Programming Language :: Python :: 3",
        ],
        install_requires=INSTALL_REQUIRES,
        python_requires=">=3.8",
    )
