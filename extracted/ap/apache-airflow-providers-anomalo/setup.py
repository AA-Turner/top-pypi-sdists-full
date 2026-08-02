# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['airflow',
 'airflow.providers.anomalo',
 'airflow.providers.anomalo.example_dags',
 'airflow.providers.anomalo.hooks',
 'airflow.providers.anomalo.operators',
 'airflow.providers.anomalo.sensors']

package_data = \
{'': ['*']}

install_requires = \
['anomalo>=0.17.0,<0.18.0', 'importlib-resources>=6.1.1,<7.0.0']

entry_points = \
{'apache_airflow_provider': ['provider_info = '
                             'airflow.providers.anomalo.__init__:get_provider_info']}

setup_kwargs = {
    'name': 'apache-airflow-providers-anomalo',
    'version': '0.2.2',
    'description': 'An Apache Airflow provider for Anomalo',
    'long_description': '# Apache Airflow Provider for Anomalo\nA set of native Airflow operators for [Anomalo](https://www.anomalo.com/)\n\n### Requirements\n\npython >=3.9.0\nairflow >=2.8.0\n\n\n### Installation\n\n\n```\npip install apache-airflow-providers-anomalo\n```\nYou can validate that it is correctly installed by running `airflow providers list` on the command line and seeing if `apache-airflow-providers-anomalo` is a listed providers package.\n\n### Airflow Setup\n\nFrom the airflow UI, go to Admin > Connections and hit the `+` button at the top to add a new connection.\n\nFrom the "Connection Type" drop down, select "Anomalo".\n![connection](https://github.com/anomalo-hq/anomalo-airflow-provider/blob/main/docs/connection.png?raw=True)\nThen fill in the fields for "Connection Id" (`anomalo-default` is the default connection id), "Host", and "API Secret Token".\n\n## Usage\n\n1. Obtain Anomalo table name from GUI. For example\n   ![table](https://github.com/anomalo-hq/anomalo-airflow-provider/blob/main/docs/table.png?raw=True)\n   would be `public-bq.covid19_nyt.us_counties`\n\n2. This package includes 3 different operators. You can find documentation for them on the operator code itself.\n   1. Run checks Operator: `airflow.providers.anomalo.operators.anomalo.AnomaloRunCheckOperator`\n   2. Job Sensor `airflow.providers.anomalo.sensors.anomalo.AnomaloJobCompleteSensor`\n   3. Validate table checks: `airflow.providers.anomalo.operators.anomalo.AnomaloPassFailOperator`\n\n3. See `example_anomalo.py` for usage example\n\n## Releasing to PyPi\n\nTo release a new version to PyPi, you will need to\n\n1. Configure your pypi token by running:\n   ```poetry config pypi-token.pypi [token here]```\n   The token can be found in the AWS secrets manager\n2. Bump the version number in pyproject.toml. Make sure that this change is committed.\n3. run\n   ```poetry publish --build```\n\n',
    'author': 'Anomalo',
    'author_email': 'opensource@anomalo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/anomalo-hq/anomalo-airflow-provider',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
