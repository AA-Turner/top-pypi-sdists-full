import distutils.text_file
from pathlib import Path
from typing import List, Optional

from setuptools import setup, find_packages


def parse_requirements(file_name: Optional[str] = 'requirements.txt') -> List[str]:
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(file_name))).readlines()


def get_long_description():
    with open('README.md', 'r') as fh:
        return fh.read()


setup(
    name='airflow_mcd',
    use_scm_version=True,
    license='Apache Software License (Apache 2.0)',
    description='Monte Carlo\'s Apache Airflow Provider',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Monte Carlo Data, Inc',
    author_email='info@montecarlodata.com',
    url='https://www.montecarlodata.com/',
    packages=find_packages(exclude=['tests*', 'examples*']),
    include_package_data=True,
    install_requires=parse_requirements(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.7',
    setup_requires=['setuptools', 'setuptools_scm'],
    entry_points=dict(apache_airflow_provider=["provider_info=airflow_mcd:get_provider_info"])
)
