from setuptools import setup, find_packages


with open('README.rst') as f:
    description = f.read()


setup(
    name='distconfig3',
    version='1.0.1',
    url='http://github.com/alexferl/distconfig/',
    packages=find_packages(),
    maintainer='Alexandre Ferland',
    maintainer_email='aferlandqc@gmail.com',
    description='Library to manage configuration using Zookeeper, Etcd, Consul',
    keywords='Configuration management zookeeper etcd consul',
    long_description=description,
    include_package_data=True,
    install_requires=[],
    extras_require={
        'zookeeper': ['kazoo>=2.0'],
        'etcd': ['python-etcd>=0.3.3'],
        'consul': ['python-consul>=0.3.15'],
        'gevent': ['gevent>=1.4.0'],
    },
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
