"""
      ___           ___           ___           ___     
     /\  \         /\  \         /\  \         /\  \    
    /::\  \       /::\  \        \:\  \       /::\  \   
   /:/\:\  \     /:/\:\  \        \:\  \     /:/\:\  \  
  /:/  \:\__\   /::\~\:\  \       /::\  \   /::\~\:\  \ 
 /:/__/ \:|__| /:/\:\ \:\__\     /:/\:\__\ /:/\:\ \:\__\
 \:\  \ /:/  / \/__\:\/:/  /    /:/  \/__/ \/__\:\/:/  /
  \:\  /:/  /       \::/  /    /:/  /           \::/  / 
   \:\/:/  /        /:/  /     \/__/            /:/  /  
    \::/__/        /:/  /                      /:/  /   
     ~~            \/__/                       \/__/    
      ___           ___           ___                       ___           ___     
     /\  \         /\__\         /\  \          ___        /\__\         /\  \    
    /::\  \       /::|  |       /::\  \        /\  \      /::|  |       /::\  \   
   /:/\:\  \     /:|:|  |      /:/\:\  \       \:\  \    /:|:|  |      /:/\:\  \  
  /::\~\:\  \   /:/|:|  |__   /:/  \:\  \      /::\__\  /:/|:|  |__   /::\~\:\  \ 
 /:/\:\ \:\__\ /:/ |:| /\__\ /:/__/_\:\__\  __/:/\/__/ /:/ |:| /\__\ /:/\:\ \:\__\
 \:\~\:\ \/__/ \/__|:|/:/  / \:\  /\ \/__/ /\/:/  /    \/__|:|/:/  / \:\~\:\ \/__/
  \:\ \:\__\       |:/:/  /   \:\ \:\__\   \::/__/         |:/:/  /   \:\ \:\__\  
   \:\ \/__/       |::/  /     \:\/:/  /    \:\__\         |::/  /     \:\ \/__/  
    \:\__\         /:/  /       \::/  /      \/__/         /:/  /       \:\__\    
     \/__/         \/__/         \/__/                     \/__/         \/__/    
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

exec(open('dataengine/version.py').read())

# Read requirements
required_packages = []
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

# Use the README as the long description
with open("README.md") as f:
    readme_text = f.read()

setup(
    name='dataengine',
    version=__version__,
    description='General purpose data engineering python package.',
    long_description=readme_text,
    url='https://github.com/leealessandrini/dataengine',
    author='Daniel Lee Alessandrini',
    author_email='alessandrinil@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.9',
    # Dependencies
    install_requires=required_packages,
    include_package_data=True,
    package_data={
        'dataengine': ["utilities/data/*.csv"],
    },
    entry_points={
        'console_scripts': [
            'script_name=dataengine.deploy_package_to_databricks:main',
        ],
    },
)
