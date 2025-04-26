from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='pip-install-test',
      version='0.5',
      description='A minimal stub package to test success of pip install',
      long_description=long_description,
      author='Simon Krughoff',
      author_email='krughoff@lsst.org',
      license='MIT',
      packages=['pip_install_test'],
      zip_safe=False)
