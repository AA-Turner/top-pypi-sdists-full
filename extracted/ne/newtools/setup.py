# (c) Deductive 2012-2020, all rights reserved
# This code is licensed under MIT license (see license.txt for details)
import os
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open(os.path.join(os.path.split(__file__)[0], 'requirements.txt')) as f:
    reqs = f.read().splitlines()

print(reqs)

setup(name='newtools',
      version=open('version.txt', 'r').read().strip(),  # read version from file as it's bumped by the build process
      description='Provides useful libraries for processing large data sets.',
      long_description="""
      Provides libraries for processing large data sets on AWS with Pandas.
      
      Developed by the team at [deductive.com](https://deductive.com) as we find them useful in our projects.
      
      &copy; Deductive 2012-2020, all rights reserved. This code is licensed under MIT license. See [license.txt](https://bitbucket.org/deductive/newtools/src/master/licence.txt) for details.

      For documentation see [read the docs](http://newtools.readthedocs.io)
      """,
      long_description_content_type="text/markdown",
      url='https://bitbucket.org/deductive/newtools/',
      project_urls={
          'Documentation': 'https://newtools.readthedocs.io/en/latest/',
          'Source': 'https://bitbucket.org/deductive/newtools/'
      },
      author='Deductive',
      author_email='hello@deductive.com',
      license='MIT',
      zip_safe=False,
      packages=['newtools',
                'newtools.aws',
                'newtools.db',
                'newtools.doggo',
                'newtools.log',
                'newtools.queue'],
      include_package_data=True,
      setup_requires=[
          'setuptools>=41.0.1',
          'wheel>=0.33.4'
      ],
      install_requires=[
          'numpy>=1.13.3',
          'JSON-log-formatter>=0.5.1'
      ],
      extras_require={
          "full": reqs,
      },
      python_requires='>=3.6',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.6'],
      keywords='deductive', )
