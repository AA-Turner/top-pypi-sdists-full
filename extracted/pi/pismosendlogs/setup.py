from setuptools import setup

setup(
    name='pismosendlogs',
    version='0.2.0',    
    description='A library to send logs',
    url='',
    author='Pismo Data Team',
    author_email='',
    license='BSD 2-clause',
    packages=['pismosendlogs'],
    install_requires=['boto3',
                      'uuid',
                      'datetime',                   
                      ],

    classifiers=[
    ],
)
