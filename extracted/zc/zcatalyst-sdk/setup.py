from os import path
from setuptools import setup, find_packages

meta_file = path.join(path.dirname(path.abspath(__file__)),'zcatalyst_sdk','__version__.py')
meta = {}
with open(meta_file) as fp:
    exec(fp.read(), meta)

setup(
    name='zcatalyst_sdk',
    version=meta['__version__'],
    description='Zoho Catalyst SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Catalyst by Zoho',
    author_email= 'support@zohocatalyst.com',
    url='https://catalyst.zoho.com/',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests~=2.32.3', 'typing-extensions~=4.12.1'],
    license='Apache License 2.0',
    python_requires=">= 3.9",
    keywords=['zcatalyst', 'zoho', 'catalyst', 'serverless', 'cloud', 'SDK', 'development'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ],
)
