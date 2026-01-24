# setup.py

import os
from setuptools import setup, find_packages

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mkdocs-plugin-inline-svg',
    version='0.1.0',
    description='A MkDocs plugin that inlines SVG images into the output.',
	long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs plugin inline svg',
    url='https://gitlab.com/craig0990/mkdocs-plugin-inline-svg',
    author='Craig Roberts',
    author_email='gitlab@craig.craig0990.co.uk',
	license='MIT',
	python_requires='>=3.5',
    install_requires=[
		'mkdocs'
	],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'inline-svg = src:InlineSvgPlugin',
        ]
    }
)
