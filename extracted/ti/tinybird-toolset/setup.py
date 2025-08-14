from setuptools import setup, Extension

NAME = 'tinybird-toolset'
VERSION = '1.3.1'

try:
    from conf import *
    chquery = Extension(
        'chtoolset._query',
        sources=['src/query.cpp',],
        depends=['conf.py',
                 'functions/AccessControl.h',
                 'functions/Aggregation.h',
                 'functions/CheckCompatibleTypes.h',
                 'functions/CheckValidWriteQuery.h',
                 'functions/ReplaceTables.h',
                 'functions/Tables.h',
                 'functions/TBQueryParser.h',
                 'functions/Validation.h',
                 'functions/simdjsonHelpers.h',
                 'functions/JSONPathQuery.h',
                 'functions/JSONPathTree.h',
                 'functions/DateTimeParser.h',
                 'functions/RowBinaryEncoder.h',
                 'src/PythonThreadHandler.h',
                 'ts_build/libCHToolset.a'],
    )
    setup(
        name=NAME,
        version=VERSION,
        url='https://gitlab.com/tinybird/clickhouse-toolset',
        author='Tinybird.co',
        author_email='support@tinybird.co',
        packages=['chtoolset'],
        package_dir={'': 'src'},
        python_requires='>=3.9, <3.14',
        install_requires=[],
        extras_require={
            'test': requirements_from_file('requirements-test.txt')
        },
        cmdclass={
            'clickhouse': ClickHouseBuildExt,
            'toolset': ToolsetBuildWithFromCH,
            'build_ext': CustomBuildWithFromCH,
        },
        ext_modules=[chquery]
    )

except ModuleNotFoundError:
    setup(
        name=NAME,
        version=VERSION,
        url='https://gitlab.com/tinybird/clickhouse-toolset',
        author='Tinybird.co',
        author_email='support@tinybird.co',
        packages=['chtoolset'],
        package_dir={'': 'src'},
        python_requires='>=3.8, <3.14',
        install_requires=[],
    )
