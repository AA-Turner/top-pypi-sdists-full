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
        "tools/snowpark-connect-create-jvm-sproc",
        "tools/snowpark-connect-create-python-sproc",
        "tools/snowpark-connect",
        "tools/snowpark-connect-execute-jar",
        "tools/snowpark-session",
        "tools/run-snowpark-connect-local",
    ],
    python_requires=">=3.10,<3.13",
    install_requires=[
        "snowpark-connect-deps-1==3.56.6",  # Spark JAR dependencies (59MB)
        "snowpark-connect-deps-2==3.56.6",  # Other JAR dependencies (53MB)
        "certifi>=2025.1.31",  # prod-297255-inc0132291
        "cloudpickle",
        "fsspec",
        # jpype1 1.7.0 / 1.7.1 stopped shipping prebuilt macOS arm64 wheels
        # (only macosx_14_0_x86_64 is published) and require compiling against a
        # properly configured JDK on Apple Silicon, which breaks `pip install
        # snowpark-connect` out of the box for that platform. Exclude only the
        # affected versions on darwin-arm64 — every other platform (including
        # macOS x86_64, Linux, Windows) still resolves to the latest jpype1.
        # Drop the exclusion once upstream restores arm64 macOS wheels
        # (see https://github.com/jpype-project/jpype/issues/1357).
        "jpype1; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "jpype1!=1.7.0,!=1.7.1; sys_platform == 'darwin' and platform_machine == 'arm64'",
        "protobuf>=3.20.2,<6.34",
        "s3fs>=2025.3.0",  # prod-297255-inc0132291
        "snowflake.core>=1.0.5,<2",
        "snowflake-snowpark-python[pandas]>=1.54.0,<1.55.0",
        "snowflake-connector-python>=3.18.0",
        "sqlglot>=26.3.8",
        # aiobotocore is a transitive dep of s3fs (not imported directly).
        # The cap is here to keep pip's resolver fast and to allow s3fs to
        # pull in a botocore that satisfies downstream packages such as
        # boto3>=1.42 (required by sagemaker>=2.255).
        "aiobotocore>=2.23.0,<4",
        # The following are dependencies for the vendored pyspark
        "py4j>=0.10.9.7, <0.10.10.0",
        "pandas>=1.0.5,<3.0",
        "pyarrow>=14.0.1,<25.0.0,!=15.*,!=16.*,!=17.*,!=18.*,!=19.*,!=20.*,!=21.*,!=22.*,!=23.0.0",
        "grpcio>=1.48.2,<=1.78.0",
        "grpcio-status>=1.41.1,<=1.78.0",
        "googleapis-common-protos>=1.56.4",
        "numpy>=1.15",
        "gcsfs>=2025.2.0",
    ],
    extras_require={
        # Linux ARM (Graviton) is the ONLY platform with no JDK 17 jdk4py
        # wheel (aarch64 Linux wheels first appear at 21.0.4.0), so it must
        # run JRE 21 + the Arrow MemoryUtil shim. Everything else — Linux
        # x86_64, Windows, and BOTH Intel and Apple-Silicon macOS — has a
        # 17.0.9.2 wheel and stays on the Spark-3.5-supported JDK 17.
        "jdk": [
            "jdk4py>=21.0.4.0 ; platform_system=='Linux' and platform_machine=='aarch64'",
            "jdk4py==17.0.9.2 ; platform_system!='Linux' or platform_machine!='aarch64'",
        ],
        "iceberg": ["snowpark-connect-deps-iceberg>=1.0.2"],
    },
)
