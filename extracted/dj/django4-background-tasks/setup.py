from setuptools import setup, find_packages
import codecs

version = __import__('background_task').__version__

classifiers = [c for c in open('classifiers').read().splitlines() if '#' not in c]

setup(
    name='django4-background-tasks',
    version=version,
    description='Database backed asynchronous task queue',
    long_description=open('README.rst').read(),
    author='André Meneses (adapting from arteria GmbH, John Montgomery)',
    author_email='andre@meneses.pt',
    url='http://github.com/meneses-pt/django-background-tasks',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    zip_safe=True,
    classifiers=classifiers,
)
