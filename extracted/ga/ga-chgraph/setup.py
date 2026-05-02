from setuptools import setup, find_packages

setup(
    name='ga-chgraph',
    version=3.11,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ['GA_CHGRAPH = clickhouse_api_server.main:main']
    },
    data_files=[('clickhouse_api_server', ['clickhouse_api_server/config/graph_config.json'])],
    install_requires=[
        "tornado-swagger==1.2.8",
        "ujson==4.0.1",
        "clickhouse-driver==0.2.0",
        "tornado==5.0.2",
        "pandas==1.1.3",
        "numpy==1.19.2",
        "psycopg2==2.7.7",
        "celery==5.1.2",
        "redis==3.5.3"
    ],
    license='GNU General Public License v3.0',
    author='Liu Feng',
    author_email='18389597276@163.com',
    description='Graph Function'
)
