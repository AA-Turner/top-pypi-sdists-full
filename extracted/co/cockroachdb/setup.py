from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cockroachdb',
    version='0.3.5',
    author='Cockroach Labs',
    author_email='cockroach-db@googlegroups.com',
    url='https://github.com/cockroachdb/cockroachdb-python',
    description='CockroachDB adapter for SQLAlchemy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],

    packages=['cockroachdb', 'cockroachdb.sqlalchemy'],
    entry_points={
        'sqlalchemy.dialects': [
            'cockroachdb = cockroachdb.sqlalchemy.dialect:CockroachDBDialect',
        ],
    },
)
