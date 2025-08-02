from setuptools import setup, find_packages
from orionis.metadata.framework import *

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url=FRAMEWORK,
    docs_url=DOCS,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(
        exclude=[
            #...
        ]
    ),
    include_package_data=True,
    classifiers = CLASSIFIERS,
    python_requires=PYTHON_REQUIRES,
    install_requires=REQUIRES,
    test_suite="tests",
    keywords=KEYWORDS,
    zip_safe=True
)