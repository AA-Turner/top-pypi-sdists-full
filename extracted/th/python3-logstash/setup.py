import setuptools
from distutils.core import setup


setuptools.setup(
    name='python3-logstash',
    packages=['logstash'],
    version='0.4.80',
    description='Python logging handler for Logstash.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Israel Flores',
    author_email='jobs@israelfl.com',
    license='MIT',
    url='https://github.com/israel-fl/python3-logstash'
)
