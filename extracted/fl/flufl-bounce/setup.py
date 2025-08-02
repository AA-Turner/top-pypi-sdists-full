from setup_helpers import description, get_version, require_python
from setuptools import setup, find_packages


require_python(0x30400f0)
__version__ = get_version('flufl/bounce/__init__.py')


setup(
    name='flufl.bounce',
    version=__version__,
    namespace_packages=['flufl'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    maintainer='Barry Warsaw',
    maintainer_email='barry@python.org',
    description=description('README.rst'),
    license='ASLv2',
    url='https://fluflbounce.readthedocs.io/en/latest/',
    download_url='https://pypi.python.org/pypi/flufl.bounce',
    install_requires=[
        'atpublic',
        'zope.interface',
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
