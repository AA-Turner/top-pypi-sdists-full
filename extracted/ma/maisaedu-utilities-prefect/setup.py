from setuptools import setup, find_packages

setup(
    name="maisaedu_utilities_prefect",
    version="1.2.24",
    description="Utilities for interaction with Prefect, for +A Education",
    license="MIT License",
    author="A+ Educação",
    author_email="dataeng@maisaedu.com.br",
    packages=find_packages(),
    scripts=[
        "maisaedu_utilities_prefect/scripts/refresh-secrets",
        "maisaedu_utilities_prefect/scripts/flow-mem-limit",
    ],
    install_requires=[
        "pandas",
        "scipy",
        "numpy",
        "wheel",
        "prefect",
        "papermill",
        "psycopg2-binary",
        "aiopg",
        "aiochannel",
        "gspread",
        "sshtunnel",
        "retry"
    ],  # external packages as dependencies
)
