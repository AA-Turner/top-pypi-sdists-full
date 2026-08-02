from setuptools import setup, find_packages

setup(
    name='gigaml_secrets',
    version='0.50',
    packages=find_packages(),
    install_requires=[
        'boto3',  # Add any other dependencies your package needs
        'botocore',
    ],
    author='GigaML',
    author_email='eng@gigaml.com',
    description='A library to manage AWS secrets with caching and environment variable integration',
    url='https://github.com/GigaML/GigaML-Secrets',
)