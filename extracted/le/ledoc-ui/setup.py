from setuptools import setup, find_packages

setup(
  name='ledoc-ui',
  version='0.1.0',
  packages=find_packages(),
  include_package_data=True,
  package_data={'ledoc-ui': ['static/*.*']},
  description='A bundle of static files for ledoc as a python package.',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  license='MIT'
)
