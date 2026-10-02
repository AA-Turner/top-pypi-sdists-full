from setuptools import setup, find_packages

install_requires = [
    'zeep',
    'python-dateutil',
    'pytz',
    'unidecode',
    'requests',
    'lxml',
    'qrcode',
    'bs4; python_version >= "3"',
    'BeautifulSoup; python_version < "3"',
    'cryptography; python_version >= "3.10"',
    'M2Crypto; python_version < "3.10"',
    'pyopenssl==22.1.0; python_version < "3.10"',
]

setup(
    name='l10n_ar_api',
    version='2.18.1',
    description='Libreria para localizacion Argentina',
    long_description='Libreria para localizacion Argentina',
    url='https://github.com/odoo-arg/l10n_ar_api',
    author='BLUEORANGE GROUP SRL',
    author_email='daniel@blueorange.com.ar',
    license='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='Libreria para localizacion Argentina',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
