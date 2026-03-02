# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_models',
 'odd_models.api_client',
 'odd_models.api_client.api',
 'odd_models.api_client.v2',
 'odd_models.discovery',
 'odd_models.discovery.data_assets',
 'odd_models.models']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=2.0,<3.0',
 'loguru>=0.7.2,<0.8.0',
 'oddrn-generator>=0.1.101,<0.2.0',
 'pydantic>=2.7.0,<3.0.0',
 'requests>=2.31.0,<3.0.0',
 'sql-metadata>=2.6.0,<3.0.0',
 'sqllineage>=1.4.7,<2.0.0',
 'sqlparse>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'odd-models',
    'version': '2.0.51',
    'description': 'Open Data Discovery Models',
    'long_description': '[![PyPI version](https://badge.fury.io/py/odd-models.svg)](https://badge.fury.io/py/odd-models)\n\n# OpenDataDiscovery Models package\nHas some useful tools for working with OpenDataDiscovery. Such as:\n1. Generated Python models from OpenDataDiscovery specification.\n2. API Client for working with OpenDataDiscovery.\n3. API for manual discovering data entities.\n\n### Installation\n```bash\npip install odd-models\n```\n\n### Models using example\n**odd-models.models** package provides automatically generated Python model by OpenDataDiscovery specification.\nIt can be used for creating data entities for uploading them into the Platform.\n\nCode example ([full code](./examples/postgres_models.py)):\n```python\nfrom oddrn_generator import PostgresqlGenerator\nfrom odd_models.models import DataEntity, DataSet, DataSetField, DataSetFieldType, DataEntityType, Type, MetadataExtension\ngenerator = PostgresqlGenerator(host_settings="localhost", databases="my_database", schemas="public")\nDataEntity(\n    oddrn=generator.get_oddrn_by_path("tables", "my_table"),\n    name="my_table",\n    type=DataEntityType.TABLE,\n    metadata=[MetadataExtension(schema_url="https://example.com/schema.json", metadata={"env": "DEV"})],\n    dataset=DataSet(\n        field_list=[\n            DataSetField(\n                oddrn=generator.get_oddrn_by_path("tables_columns", "name"),\n                name="name",\n                type=DataSetFieldType(\n                    type=Type.TYPE_STRING,\n                    logical_type=\'str\',\n                    is_nullable=False\n                ),\n            )\n        ]\n    )\n)\n```\n\n\n### HTTP Client for OpenDataDiscovery\n___\n**odd-models.client** package provides API client for OpenDataDiscovery API.\nClient provides an API for working with OpenDataDiscovery Platform.\nIt has various methods for working with data sources, data entities, management etc.\n\nCode example([full code](./examples/client.py)):\n\n```python\nfrom examples.postgres_models import data_entity_list, generator\nfrom odd_models.api_client.v2.odd_api_client import Client\n\nclient = Client(host="http://localhost:8080")\nclient.auth(name="postgres", description="Token for dev AWS account data sources")\n\nclient.create_data_source(\n    data_source_oddrn=generator.get_data_source_oddrn(),\n    data_source_name="Postgres data source",\n)\nclient.ingest_data_entity_list(data_entities=data_entity_list)\n```\n\n### Manual Discovery API\n___\nWhen there is no programmatic way to discover data sources and data entities, **odd-models.discovery** package provides API for manual discovery of data sources and data entities.\n\nCode example([full code](./examples/lambda_discovery.py)):\n\n```python\nfrom odd_models.discovery import DataSource\nfrom odd_models.discovery.data_assets import AWSLambda, S3Artifact\nfrom odd_models.discovery.data_assets.data_asset_list import DataAssetsList\n\nwith DataSource("//cloud/aws/dev") as data_source:\n    validation_lambda = AWSLambda.from_params(\n        region="eu-central-1", account="0123456789", function_name="validation"\n    )\n    input_artifact = S3Artifact.from_url("s3://bucket/folder/test_data.csv")\n\n    results = S3Artifact.from_url("s3://bucket/folder/test_result.csv")\n    metrics = S3Artifact.from_url("s3://bucket/folder/test_metrics.json")\n\n    input_artifact >> validation_lambda >> DataAssetsList([results, metrics])\n\n    data_source.add_data_asset(validation_lambda)\n```\n\n# Development\n\n### Installation\n```bash\n# Install dependencies\npoetry install\n\n# Activate virtual environment\npoetry shell\n```\n\n### Generating models\n```bash\n# Generate models. Will generate models pydantic into odd_models/models\nmake generate_models\n\n# Generate api client. Will generate api client into odd_models/api_client\nmake generate_client\n```\n\n### Tests\n```bash\npytest .\n```\n\n### Docker build\n```bash\ndocker build -t odd-models .\n```\n',
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opendatadiscovery/odd-models-package',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
