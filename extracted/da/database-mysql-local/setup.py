import setuptools

PACKAGE_NAME = "database-mysql-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/database-mysql-local
    version='0.1.43',
    author="Circles",
    author_email="info@circlez.ai",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="Database MySQL Local",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # https://pypi.org/project/mysql-connector-python/
        "mysql-connector-python>=9.0.0",
        "url-remote>=0.0.119",  # https://pypi.org/project/url-remote/
        "logger-local>=0.0.166",  # https://pypi.org/project/logger-local/
        # database-infrastructure-local 0.0.35 generic_crud_abstract.py GenericCrudAbstract
        # https://pypi.org/project/database-infrastructure-local/
        "database-infrastructure-local>=0.1.4",
        "language-remote>=0.0.24",  # https://pypi.org/project/language-remote/
        "sql-to-code-local>=0.0.18",  # https://pypi.org/project/sql-to-code-local/
        "python-sdk-remote==0.0.145",
        # Commented because of a problem with serverless, TODO We should add a test to spot such case
        # "sshtunnel>=0.4.0", # https://pypi.org/project/sshtunnel/
    ]
)
