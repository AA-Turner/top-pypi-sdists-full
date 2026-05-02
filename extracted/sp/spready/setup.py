from setuptools import setup, find_packages
import sys
sys.path[0:0] = ['src/spready']


setup(
    name='spready',
    version='1.12',
    description='Spready APP',
    long_description='Spready distributed API',
    author='muthugit',
    author_email='base.muthupandian@gmail.com',
    url='https://muthupandian.in',
    packages=(find_packages(where="src")),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'spready=spready:cliApp'
        ]
    },
    requires=['redis', 'rq', 'typer', 'pyjwt', 'requests', 'loguru'],
)