try:
    from setuptools import setup
except:
    from distutils.core import setup

import rfc3339

setup(name='rfc3339',
      version=rfc3339.__version__,
      py_modules=['rfc3339'],
      # metadata for upload to PyPI
      author=rfc3339.__author__,
      author_email='henry@precheur.org',
      description='Format dates according to the RFC 3339.',
      long_description=rfc3339.__doc__,
      license=rfc3339.__license__,
      url='http://pypi.python.org/pypi/rfc3339/',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Topic :: Internet',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ])
