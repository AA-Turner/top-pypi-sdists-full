from setuptools import setup, Extension

NAME = 'tinybird-toolset'
VERSION = '2.5.5'

# Shared metadata for both the full (extension) build and the metadata-only
# fallback below, so the two setup() calls can't drift apart.
common_kwargs = dict(
    name=NAME,
    version=VERSION,
    url="https://gitlab.com/tinybird/clickhouse-toolset",
    author="Tinybird.co",
    author_email="support@tinybird.co",
    packages=["chtoolset"],
    package_dir={"": "src"},
    python_requires=">=3.13, <3.15",
    install_requires=[],
)

try:
    from conf import *

    chquery = Extension(
        "chtoolset._query",
        sources=[
            "src/query.cpp",
        ],
        depends=[
            "conf.py",
            "functions/AccessControl.h",
            "functions/Aggregation.h",
            "functions/CheckCompatibleTypes.h",
            "functions/CheckValidWriteQuery.h",
            "functions/ReplaceTables.h",
            "functions/Tables.h",
            "functions/TBQueryParser.h",
            "functions/ValidateTTL.h",
            "functions/Validation.h",
            "functions/simdjsonHelpers.h",
            "functions/JSONPathQuery.h",
            "functions/JSONPathTree.h",
            "functions/DateTimeParser.h",
            "functions/RowBinaryEncoder.h",
            "src/PythonThreadHandler.h",
            "ts_build/libCHToolset.a",
        ],
    )
    setup(
        **common_kwargs,
        extras_require={"test": requirements_from_file("requirements-test.txt")},
        cmdclass={
            "clickhouse": ClickHouseBuildExt,
            "toolset": ToolsetBuildWithFromCH,
            "build_ext": CustomBuildWithFromCH,
        },
        ext_modules=[chquery],
    )

except ModuleNotFoundError:
    setup(**common_kwargs)
