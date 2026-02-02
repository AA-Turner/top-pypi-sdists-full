import codecs
from setuptools import find_packages
from setuptools import setup

with codecs.open('README.rst', 'r', 'utf-8') as f:
    README = f.read()

with codecs.open('CHANGES.rst', 'r', 'utf-8') as f:
    CHANGES = f.read()

with codecs.open('CONTRIBUTORS.rst', 'r', 'utf-8') as f:
    CONTRIBUTORS = f.read()

setup(
    name='TGScheduler',
    version='1.7.0',
    description='Pure Python Scheduler',
    long_description=u"{}\n{}\n{}".format(README, CONTRIBUTORS, CHANGES),
    author='Vince Spicer',
    author_email='vinces1979@gmail.com',
    url='https://bitbucket.org/xcg/tgscheduler',
    keywords='turbogears tg tg2 scheduler',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'python-dateutil',
        'six',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tgscheduler.tests',
)
