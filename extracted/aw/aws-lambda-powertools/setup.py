# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_lambda_powertools',
 'aws_lambda_powertools.event_handler',
 'aws_lambda_powertools.event_handler.events_appsync',
 'aws_lambda_powertools.event_handler.graphql_appsync',
 'aws_lambda_powertools.event_handler.middlewares',
 'aws_lambda_powertools.event_handler.openapi',
 'aws_lambda_powertools.event_handler.openapi.swagger_ui',
 'aws_lambda_powertools.exceptions',
 'aws_lambda_powertools.logging',
 'aws_lambda_powertools.logging.buffer',
 'aws_lambda_powertools.logging.formatters',
 'aws_lambda_powertools.metrics',
 'aws_lambda_powertools.metrics.provider',
 'aws_lambda_powertools.metrics.provider.cloudwatch_emf',
 'aws_lambda_powertools.metrics.provider.datadog',
 'aws_lambda_powertools.middleware_factory',
 'aws_lambda_powertools.shared',
 'aws_lambda_powertools.tracing',
 'aws_lambda_powertools.utilities',
 'aws_lambda_powertools.utilities.batch',
 'aws_lambda_powertools.utilities.data_classes',
 'aws_lambda_powertools.utilities.data_classes.appsync',
 'aws_lambda_powertools.utilities.data_masking',
 'aws_lambda_powertools.utilities.data_masking.provider',
 'aws_lambda_powertools.utilities.data_masking.provider.kms',
 'aws_lambda_powertools.utilities.feature_flags',
 'aws_lambda_powertools.utilities.idempotency',
 'aws_lambda_powertools.utilities.idempotency.persistence',
 'aws_lambda_powertools.utilities.idempotency.serialization',
 'aws_lambda_powertools.utilities.jmespath_utils',
 'aws_lambda_powertools.utilities.kafka',
 'aws_lambda_powertools.utilities.kafka.deserializer',
 'aws_lambda_powertools.utilities.kafka.serialization',
 'aws_lambda_powertools.utilities.parameters',
 'aws_lambda_powertools.utilities.parser',
 'aws_lambda_powertools.utilities.parser.envelopes',
 'aws_lambda_powertools.utilities.parser.models',
 'aws_lambda_powertools.utilities.streaming',
 'aws_lambda_powertools.utilities.streaming.transformations',
 'aws_lambda_powertools.utilities.typing',
 'aws_lambda_powertools.utilities.validation',
 'aws_lambda_powertools.warnings']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.1,<2.0.0', 'typing-extensions>=4.11.0,<5.0.0']

extras_require = \
{'all': ['aws-xray-sdk>=2.8.0,<3.0.0',
         'fastjsonschema>=2.14.5,<3.0.0',
         'pydantic>=2.4.0,<3.0.0',
         'pydantic-settings>=2.6.1,<3.0.0',
         'aws-encryption-sdk>=3.1.1,<5.0.0',
         'jsonpath-ng>=1.6.0,<2.0.0'],
 'aws-sdk': ['boto3>=1.34.32,<2.0.0'],
 'datadog': ['datadog-lambda>=6.106.0,<7.0.0'],
 'datamasking': ['aws-encryption-sdk>=3.1.1,<5.0.0',
                 'jsonpath-ng>=1.6.0,<2.0.0'],
 'kafka-consumer-avro': ['avro>=1.12.0,<2.0.0'],
 'kafka-consumer-protobuf': ['protobuf>=6.30.2,<7.0.0'],
 'parser': ['pydantic>=2.4.0,<3.0.0'],
 'redis': ['redis>=4.4,<7.0'],
 'tracer': ['aws-xray-sdk>=2.8.0,<3.0.0'],
 'validation': ['fastjsonschema>=2.14.5,<3.0.0'],
 'valkey': ['valkey-glide>=1.3.5,<3.0']}

setup_kwargs = {
    'name': 'aws_lambda_powertools',
    'version': '3.16.0',
    'description': 'Powertools for AWS Lambda (Python) is a developer toolkit to implement Serverless best practices and increase developer velocity.',
    'long_description': '<!-- markdownlint-disable MD013 MD041 MD043  -->\n# Powertools for AWS Lambda (Python)\n\n[![Build](https://github.com/aws-powertools/powertools-lambda-python/actions/workflows/quality_check.yml/badge.svg)](https://github.com/aws-powertools/powertools-lambda-python/actions/workflows/python_build.yml)\n[![codecov.io](https://codecov.io/github/aws-powertools/powertools-lambda-python/branch/develop/graphs/badge.svg)](https://app.codecov.io/gh/aws-powertools/powertools-lambda-python)\n![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.9|%203.10|%203.11|%203.12|%203.13&color=blue?style=flat-square&logo=python) ![PyPI version](https://badge.fury.io/py/aws-lambda-powertools.svg) ![PyPi monthly downloads](https://img.shields.io/pypi/dm/aws-lambda-powertools) [![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/aws-powertools/powertools-lambda-python/badge)](https://api.securityscorecards.dev/projects/github.com/aws-powertools/powertools-lambda-python) [![Join our Discord](https://dcbadge.vercel.app/api/server/B8zZKbbyET?style=flat-square)](https://discord.gg/B8zZKbbyET)\n\nPowertools for AWS Lambda (Python) is a developer toolkit to implement Serverless [best practices and increase developer velocity](https://docs.powertools.aws.dev/lambda/python/latest/#features).\n\n> Also available in [Java](https://github.com/aws-powertools/powertools-lambda-java), [Typescript](https://github.com/aws-powertools/powertools-lambda-typescript), and [.NET](https://github.com/aws-powertools/powertools-lambda-dotnet).\n\n**[📜Documentation](https://docs.powertools.aws.dev/lambda/python/)** | **[🐍PyPi](https://pypi.org/project/aws-lambda-powertools/)** | **[Roadmap](https://docs.powertools.aws.dev/lambda/python/latest/roadmap/)** | **[Detailed blog post](https://aws.amazon.com/blogs/opensource/simplifying-serverless-best-practices-with-lambda-powertools/)**\n\n![hero-image](https://user-images.githubusercontent.com/3340292/198254617-d0fdb672-86a6-4988-8a40-adf437135e0a.png)\n\n## Features\n\n* **[Tracing](https://docs.powertools.aws.dev/lambda/python/latest/core/tracer/)** - Decorators and utilities to trace Lambda function handlers, and both synchronous and asynchronous functions\n* **[Logging](https://docs.powertools.aws.dev/lambda/python/latest/core/logger/)** - Structured logging made easier, and decorator to enrich structured logging with key Lambda context details\n* **[Metrics](https://docs.powertools.aws.dev/lambda/python/latest/core/metrics/)** - Custom Metrics created asynchronously via CloudWatch Embedded Metric Format (EMF)\n* **[Event handler: AppSync](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/appsync/)** - AWS AppSync event handler for Lambda Direct Resolver and Amplify GraphQL Transformer function\n* **[Event handler: API Gateway and ALB](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/)** - Amazon API Gateway REST/HTTP API and ALB event handler for Lambda functions invoked using Proxy integration\n* **[Event handler: Agents for Amazon Bedrock](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/bedrock_agents/)** - Create Agents for Amazon Bedrock, automatically generating OpenAPI schemas\n* **[Bring your own middleware](https://docs.powertools.aws.dev/lambda/python/latest/utilities/middleware_factory/)** - Decorator factory to create your own middleware to run logic before, and after each Lambda invocation\n* **[Parameters utility](https://docs.powertools.aws.dev/lambda/python/latest/utilities/parameters/)** - Retrieve and cache parameter values from Parameter Store, Secrets Manager, or DynamoDB\n* **[Batch processing](https://docs.powertools.aws.dev/lambda/python/latest/utilities/batch/)** - Handle partial failures for AWS SQS batch processing\n* **[Typing](https://docs.powertools.aws.dev/lambda/python/latest/utilities/typing/)** - Static typing classes to speedup development in your IDE\n* **[Validation](https://docs.powertools.aws.dev/lambda/python/latest/utilities/validation/)** - JSON Schema validator for inbound events and responses\n* **[Event source data classes](https://docs.powertools.aws.dev/lambda/python/latest/utilities/data_classes/)** - Data classes describing the schema of common Lambda event triggers\n* **[Parser](https://docs.powertools.aws.dev/lambda/python/latest/utilities/parser/)** - Data parsing and deep validation using Pydantic\n* **[Idempotency](https://docs.powertools.aws.dev/lambda/python/latest/utilities/idempotency/)** - Convert your Lambda functions into idempotent operations which are safe to retry\n* **[Data Masking](https://docs.powertools.aws.dev/lambda/python/latest/utilities/data_masking/)** -  Protect confidential data with easy removal or encryption\n* **[Feature Flags](https://docs.powertools.aws.dev/lambda/python/latest/utilities/feature_flags/)** - A simple rule engine to evaluate when one or multiple features should be enabled depending on the input\n* **[Streaming](https://docs.powertools.aws.dev/lambda/python/latest/utilities/streaming/)** - Streams datasets larger than the available memory as streaming data.\n\n### Installation\n\nWith [pip](https://pip.pypa.io/en/latest/index.html) installed, run: ``pip install aws-lambda-powertools``\n\n## Tutorial and Examples\n\n* [Tutorial](https://docs.powertools.aws.dev/lambda/python/latest/tutorial)\n* [Serverless Shopping cart](https://github.com/aws-samples/aws-serverless-shopping-cart)\n* [Serverless Airline](https://github.com/aws-samples/aws-serverless-airline-booking)\n* [Serverless E-commerce platform](https://github.com/aws-samples/aws-serverless-ecommerce-platform)\n* [Serverless GraphQL Nanny Booking Api](https://github.com/trey-rosius/babysitter_api)\n\n## How to support Powertools for AWS Lambda (Python)?\n\n### Becoming a reference customer\n\nKnowing which companies are using this library is important to help prioritize the project internally. If your company is using Powertools for AWS Lambda (Python), you can request to have your name and logo added to the README file by raising a [Support Powertools for AWS Lambda (Python) (become a reference)](https://github.com/aws-powertools/powertools-lambda-python/issues/new?assignees=&labels=customer-reference&template=support_powertools.yml&title=%5BSupport+Lambda+Powertools%5D%3A+%3Cyour+organization+name%3E) issue.\n\nThe following companies, among others, use Powertools:\n\n* [Alma Media](https://www.almamedia.fi/en/)\n* [Banxware](https://www.banxware.com/)\n* [Brsk](https://www.brsk.co.uk/)\n* [BusPatrol](https://buspatrol.com/)\n* [Capital One](https://www.capitalone.com/)\n* [Caylent](https://caylent.com/)\n* [CHS Inc.](https://www.chsinc.com/)\n* [CPQi (Exadel Financial Services)](https://cpqi.com/)\n* [CloudZero](https://www.cloudzero.com/)\n* [CyberArk](https://www.cyberark.com/)\n* [Flyweight](https://flyweight.io/)\n* [globaldatanet](https://globaldatanet.com/)\n* [Guild](https://guild.com/)\n* [IMS](https://ims.tech/)\n* [Instil](https://instil.co/)\n* [Jit Security](https://www.jit.io/)\n* [LocalStack](https://www.localstack.cloud/)\n* [Propellor.ai](https://www.propellor.ai/)\n* [Pushpay](https://pushpay.com/)\n* [Recast](https://getrecast.com/)\n* [TopSport](https://www.topsport.com.au/)\n* [Transformity](https://transformity.tech/)\n* [Trek10](https://www.trek10.com/)\n* [Vertex Pharmaceuticals](https://www.vrtx.com/)\n\n### Sharing your work\n\nShare what you did with Powertools for AWS Lambda (Python) 💞💞. Blog post, workshops, presentation, sample apps and others. Check out what the community has already shared about Powertools for AWS Lambda (Python) [here](https://docs.powertools.aws.dev/lambda/python/latest/we_made_this/).\n\n### Using Lambda Layer or SAR\n\nThis helps us understand who uses Powertools for AWS Lambda (Python) in a non-intrusive way, and helps us gain future investments for other Powertools for AWS Lambda languages. When [using Layers](https://docs.powertools.aws.dev/lambda/python/latest/#lambda-layer), you can add Powertools for AWS Lambda (Python) as a dev dependency (or as part of your virtual env) to not impact the development process.\n\n## Credits\n\n* Structured logging initial implementation from [aws-lambda-logging](https://gitlab.com/hadrien/aws_lambda_logging)\n* Powertools for AWS Lambda (Python) idea [DAZN Powertools](https://github.com/getndazn/dazn-lambda-powertools/)\n\n## Connect\n\n* **Powertools for AWS Lambda on Discord**: `#python` - **[Invite link](https://discord.gg/B8zZKbbyET)**\n* **Email**: <aws-powertools-maintainers@amazon.com>\n\n## Security disclosures\n\nIf you think you’ve found a potential security issue, please do not post it in the Issues.  Instead, please follow the instructions [here](https://aws.amazon.com/security/vulnerability-reporting/) or [email AWS security directly](mailto:aws-security@amazon.com).\n\n## License\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n',
    'author': 'Amazon Web Services',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aws-powertools/powertools-lambda-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
