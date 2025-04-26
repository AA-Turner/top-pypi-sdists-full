# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databricks_dbapi', 'databricks_dbapi.sqlalchemy_dialects']

package_data = \
{'': ['*']}

extras_require = \
{'hive': ['pyhive>=0.6.1,<0.7.0', 'thrift>=0.15.0,<0.16.0'],
 'odbc': ['pyodbc>=4.0.30,<5.0.0'],
 'sqlalchemy': ['sqlalchemy>=1.3,<2.0']}

entry_points = \
{'sqlalchemy.dialects': ['databricks.pyhive = '
                         'databricks_dbapi.sqlalchemy_dialects.hive:DatabricksPyhiveDialect',
                         'databricks.pyodbc = '
                         'databricks_dbapi.sqlalchemy_dialects.odbc:DatabricksPyodbcDialect']}

setup_kwargs = {
    'name': 'databricks-dbapi',
    'version': '0.6.0',
    'description': 'A DBAPI 2.0 interface and SQLAlchemy dialect for Databricks interactive clusters.',
    'long_description': 'databricks-dbapi\n================\n\n|pypi| |pyversions|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/databricks-dbapi.svg\n    :target: https://pypi.python.org/pypi/databricks-dbapi\n\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/databricks-dbapi.svg\n    :target: https://pypi.python.org/pypi/databricks-dbapi\n\nA thin wrapper around `pyhive <https://github.com/dropbox/PyHive>`__ and `pyodbc <https://github.com/mkleehammer/pyodbc>`__ for creating a `DBAPI <https://www.python.org/dev/peps/pep-0249/>`__ connection to Databricks Workspace and SQL Analytics clusters. SQL Analytics clusters require the `Simba ODBC driver <https://databricks.com/spark/odbc-driver-download>`__.\n\nAlso provides SQLAlchemy Dialects using ``pyhive`` and ``pyodbc`` for Databricks clusters. Databricks SQL Analytics clusters only support the ``pyodbc``-driven dialect.\n\nInstallation\n------------\n\nInstall using pip. You *must* specify at least one of the extras {``hive`` or ``odbc``}. For ``odbc`` the `Simba driver <https://databricks.com/spark/odbc-driver-download>`__ is required:\n\n.. code-block:: bash\n\n    pip install databricks-dbapi[hive,odbc]\n\n\nFor SQLAlchemy support install with:\n\n.. code-block:: bash\n\n    pip install databricks-dbapi[hive,odbc,sqlalchemy]\n\nUsage\n-----\n\nPyHive\n~~~~~~\n\nThe ``connect()`` function returns a ``pyhive`` Hive connection object, which internally wraps a ``thrift`` connection.\n\nConnecting with ``http_path``, ``host``, and a ``token``:\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import hive\n\n\n    token = os.environ["DATABRICKS_TOKEN"]\n    host = os.environ["DATABRICKS_HOST"]\n    http_path = os.environ["DATABRICKS_HTTP_PATH"]\n\n\n    connection = hive.connect(\n        host=host,\n        http_path=http_path,\n        token=token,\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100")\n\n    print(cursor.fetchone())\n    print(cursor.fetchall())\n\n\nThe ``pyhive`` connection also provides async functionality:\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import hive\n    from TCLIService.ttypes import TOperationState\n\n\n    token = os.environ["DATABRICKS_TOKEN"]\n    host = os.environ["DATABRICKS_HOST"]\n    cluster = os.environ["DATABRICKS_CLUSTER"]\n\n\n    connection = hive.connect(\n        host=host,\n        cluster=cluster,\n        token=token,\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100", async_=True)\n\n    status = cursor.poll().operationState\n    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):\n        logs = cursor.fetch_logs()\n        for message in logs:\n            print(message)\n\n        # If needed, an asynchronous query can be cancelled at any time with:\n        # cursor.cancel()\n\n        status = cursor.poll().operationState\n\n    print(cursor.fetchall())\n\n\nODBC\n~~~~\n\nThe ODBC DBAPI requires the Simba ODBC driver.\n\nConnecting with ``http_path``, ``host``, and a ``token``:\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import odbc\n\n\n    token = os.environ["DATABRICKS_TOKEN"]\n    host = os.environ["DATABRICKS_HOST"]\n    http_path = os.environ["DATABRICKS_HTTP_PATH"]\n\n\n    connection = odbc.connect(\n        host=host,\n        http_path=http_path,\n        token=token,\n        driver_path="/path/to/simba/driver",\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100")\n\n    print(cursor.fetchone())\n    print(cursor.fetchall())\n\n\nSQLAlchemy Dialects\n-------------------\n\ndatabricks+pyhive\n~~~~~~~~~~~~~~~~~\n\nInstalling registers the ``databricks+pyhive`` dialect/driver with SQLAlchemy. Fill in the required information when passing the engine URL.\n\n.. code-block:: python\n\n    from sqlalchemy import *\n    from sqlalchemy.engine import create_engine\n    from sqlalchemy.schema import *\n\n\n    engine = create_engine(\n        "databricks+pyhive://token:<databricks_token>@<host>:<port>/<database>",\n        connect_args={"http_path": "<cluster_http_path>"}\n    )\n\n    logs = Table("my_table", MetaData(bind=engine), autoload=True)\n    print(select([func.count("*")], from_obj=logs).scalar())\n\n\ndatabricks+pyodbc\n~~~~~~~~~~~~~~~~~\n\nInstalling registers the ``databricks+pyodbc`` dialect/driver with SQLAlchemy. Fill in the required information when passing the engine URL.\n\n.. code-block:: python\n\n    from sqlalchemy import *\n    from sqlalchemy.engine import create_engine\n    from sqlalchemy.schema import *\n\n\n    engine = create_engine(\n        "databricks+pyodbc://token:<databricks_token>@<host>:<port>/<database>",\n        connect_args={"http_path": "<cluster_http_path>", "driver_path": "/path/to/simba/driver"}\n    )\n\n    logs = Table("my_table", MetaData(bind=engine), autoload=True)\n    print(select([func.count("*")], from_obj=logs).scalar())\n\n\nRefer to the following documentation for more details on hostname, cluster name, and http path:\n\n* `Databricks <https://docs.databricks.com/user-guide/bi/jdbc-odbc-bi.html>`__\n* `Azure Databricks <https://docs.azuredatabricks.net/user-guide/bi/jdbc-odbc-bi.html>`__\n\n\nRelated\n-------\n\n* `pyhive <https://github.com/dropbox/PyHive>`__\n* `thrift <https://github.com/apache/thrift/tree/master/lib/py>`__\n* `pyodbc <https://github.com/mkleehammer/pyodbc>`__\n',
    'author': 'Christopher Flynn',
    'author_email': 'crf204@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/crflynn/databricks-dbapi',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
