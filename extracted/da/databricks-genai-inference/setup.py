import io
import setuptools
from setuptools import setup

# pylint: disable-next=exec-used,consider-using-with
exec(open('databricks_genai_inference/version.py', 'r', encoding='utf-8').read())

install_requires = [
    'pyyaml>=5.4.1',
    'requests>=2.26.0,<3',
    'databricks-sdk==0.19.1',
    'pydantic>=2.4.2',
    'typing_extensions>=4.7.1',
    'tenacity==8.2.3',
    'httpx>=0.23.0, <1',
]

extra_deps = {}

extra_deps['dev'] = [
    'build>=0.10.0',
    'isort>=5.9.3',
    'pre-commit>=2.17.0',
    'pylint>=2.12.2',
    'pyright==1.1.256',
    'pytest-cov>=4.0.0',
    'pytest-mock>=3.7.0',
    'pytest-asyncio>=0.23.3',
    'pytest>=6.2.5',
    'radon>=5.1.0',
    'twine>=4.0.2',
    'toml>=0.10.2',
    'yapf>=0.33.0',
]

extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name='databricks-genai-inference',
    version=__version__,  # type: ignore pylint: disable=undefined-variable
    author='Databricks',
    author_email='eng-genai-inference@databricks.com',
    description='Interact with the Databricks Foundation Model API from python',
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://docs.databricks.com/en/machine-learning/foundation-models/query-foundation-model-apis.html',
    include_package_data=True,
    package_data={},
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=install_requires,
    extras_require=extra_deps,
    python_requires='>=3.9',
    ext_package='databricks_genai_inference',
)
