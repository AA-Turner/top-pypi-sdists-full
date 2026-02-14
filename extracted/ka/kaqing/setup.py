from setuptools import setup, find_packages

setup(
    name='kaqing',
    version='2.1.41',
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'qing = adam.cli:cli'
        ]
    }
)
