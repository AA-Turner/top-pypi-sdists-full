import sys

from setuptools import setup
from setuptools import find_packages


version = '1.0.0'

install_requires = [
    'acme>=0.21.1',
    'certbot>=0.21.1',
    'dns-lexicon>=2.2.1', # Support for >1 TXT record per name
    'mock',
    'setuptools',
    'zope.interface',
    'PyNamecheap'
]

setup(
    name='certbot-dns-namecheap',
    version=version,
    description="Namecheap DNS Authenticator plugin for Certbot",
    url='https://github.com/knoxell/certbot-dns-namecheap',
    author="Knoxell",
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-namecheap = certbot_dns_namecheap.dns_namecheap:Authenticator',
        ],
    },
    test_suite='certbot_dns_namecheap',
    project_urls={
        'Source': 'https://github.com/knoxell/certbot-dns-namecheap',
        'Tracker': 'https://github.com/knoxell/certbot-dns-namecheap/issues',
    },
)
