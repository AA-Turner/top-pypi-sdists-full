from setuptools import setup

name = "types-aws-xray-sdk"
description = "Typing stubs for aws-xray-sdk"
long_description = '''
## Typing stubs for aws-xray-sdk

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`aws-xray-sdk`](https://github.com/aws/aws-xray-sdk-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`aws-xray-sdk`.

This version of `types-aws-xray-sdk` aims to provide accurate annotations
for `aws-xray-sdk==2.14.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/aws-xray-sdk. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `b3fc7e2cece78d1e81df2af0b718c1af0fd05871` and was tested
with mypy 1.10.0, pyright 1.1.366, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.14.0.20240606",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/aws-xray-sdk.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['aws_xray_sdk-stubs'],
      package_data={'aws_xray_sdk-stubs': ['__init__.pyi', 'core/__init__.pyi', 'core/async_context.pyi', 'core/async_recorder.pyi', 'core/context.pyi', 'core/daemon_config.pyi', 'core/emitters/__init__.pyi', 'core/emitters/udp_emitter.pyi', 'core/exceptions/__init__.pyi', 'core/exceptions/exceptions.pyi', 'core/lambda_launcher.pyi', 'core/models/__init__.pyi', 'core/models/default_dynamic_naming.pyi', 'core/models/dummy_entities.pyi', 'core/models/entity.pyi', 'core/models/facade_segment.pyi', 'core/models/http.pyi', 'core/models/noop_traceid.pyi', 'core/models/segment.pyi', 'core/models/subsegment.pyi', 'core/models/throwable.pyi', 'core/models/trace_header.pyi', 'core/models/traceid.pyi', 'core/patcher.pyi', 'core/plugins/__init__.pyi', 'core/plugins/ec2_plugin.pyi', 'core/plugins/ecs_plugin.pyi', 'core/plugins/elasticbeanstalk_plugin.pyi', 'core/plugins/utils.pyi', 'core/recorder.pyi', 'core/sampling/__init__.pyi', 'core/sampling/connector.pyi', 'core/sampling/local/__init__.pyi', 'core/sampling/local/reservoir.pyi', 'core/sampling/local/sampler.pyi', 'core/sampling/local/sampling_rule.pyi', 'core/sampling/reservoir.pyi', 'core/sampling/rule_cache.pyi', 'core/sampling/rule_poller.pyi', 'core/sampling/sampler.pyi', 'core/sampling/sampling_rule.pyi', 'core/sampling/target_poller.pyi', 'core/streaming/__init__.pyi', 'core/streaming/default_streaming.pyi', 'core/utils/__init__.pyi', 'core/utils/atomic_counter.pyi', 'core/utils/compat.pyi', 'core/utils/conversion.pyi', 'core/utils/search_pattern.pyi', 'core/utils/stacktrace.pyi', 'sdk_config.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
