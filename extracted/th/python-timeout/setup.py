from setuptools import setup

setup(
    name = 'python_timeout',
    packages = ['timeout'],
    install_requires = ['python-dateutil', 'python-printr'],
    version = '2026.6.30',
    description = 'Random timeout between minimum and maximum values',
    url = 'https://github.com/xjxckk/python-timeout/',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
    )