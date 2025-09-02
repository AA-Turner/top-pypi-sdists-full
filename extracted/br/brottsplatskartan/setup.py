"""Setup Brottsplatskartan API wrapper"""

from setuptools import find_packages, setup

setup(
    name='brottsplatskartan',
    version='1.0.5',
    description='Simple API wrapper to brottsplatskartan.se.',
    url='https://github.com/chrillux/brottsplatskartan',
    license='MIT',
    author='chrillux',
    author_email='christianbiamont@gmail.com',
    packages=find_packages(),
    install_requires=['requests>=2.20.0'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
