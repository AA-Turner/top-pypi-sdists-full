import os

from setuptools import find_namespace_packages, setup

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.join(THIS_DIR, "src")
VERSION_FILE = os.path.join(SRC_DIR, "snowflake", "snowpark_connect", "version.py")

# read the version
VERSION = ()
with open(VERSION_FILE, encoding="utf-8") as f:
    exec(f.read())
if not VERSION:
    raise ValueError("version can't be read")
version = ".".join([str(v) for v in VERSION if v is not None])

setup(
    name="snowpark-connect",
    version=version,
    description="Snowpark Connect for Spark",
    keywords=["snowflake", "snowpark", "connect", "spark"],
    long_description="Snowpark Connect for Spark enables developers to run their Spark workloads directly to Snowflake using the Spark Connect protocol. This approach decouples the client and server, allowing Spark code to run remotely against Snowflake's compute engine without managing a Spark cluster. It offers a streamlined way to integrate Snowflake's governance, security, and scalability into Spark-based workflows, supporting a familiar PySpark experience with pushdown optimizations into Snowflake.",
    long_description_content_type="text/markdown",
    author="Snowflake, Inc",
    license="Apache License, Version 2.0",
    license_files=["LICENSE.txt", "LICENSE-binary", "NOTICE-binary"],
    packages=find_namespace_packages(where="src"),
    package_data={
        "": ["*.json"],
        "snowflake.snowpark_connect": ["resources/*.jar"],
        "snowflake.snowpark_connect.includes": ["jars/*.jar"],
    },
    package_dir={"": "src"},
    scripts=[
        "tools/snowpark-connect",
        "tools/snowpark-session",
        "tools/snowpark-submit",
    ],
    python_requires=">=3.10,<3.13",
    install_requires=[
        "snowpark-connect-deps-1==3.56.4",  # Spark JAR dependencies (59MB)
        "snowpark-connect-deps-2==3.56.4",  # Other JAR dependencies (53MB)
        "certifi>=2025.1.31",  # prod-297255-inc0132291
        "cloudpickle",
        "fsspec",
        "jpype1",
        "protobuf>=4.25.3,<6.32.0",
        "s3fs>=2025.3.0",  # prod-297255-inc0132291
        "snowflake.core>=1.0.5,<2",
        "snowflake-snowpark-python[pandas]>=1.44.0,<1.45.0",
        "snowflake-connector-python>=3.18.0,<4.2.0",
        "sqlglot>=26.3.8",
        "aiobotocore>=2.23.0,<=2.26.0",
        # The following are dependencies for the vendored pyspark
        "py4j==0.10.9.7",
        "pandas>=1.0.5",
        "pyarrow>=4.0.0,<=18.1.0",  # Newer pyarrow versions have stricter checks for nullability which breaks scala code
        "grpcio>=1.56.0,<=1.76.0",
        "grpcio-status>=1.56.0,<=1.76.0",
        "googleapis-common-protos>=1.56.4",
        "numpy>=1.15,<2",
        "gcsfs>=2025.2.0",
    ],
    extras_require={
        "jdk": ["jdk4py==17.0.9.2"],
    },
)
