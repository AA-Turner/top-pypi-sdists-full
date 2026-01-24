import sys
from setuptools import setup, find_packages

if sys.argv[1] == 'sdist':
	setup(
		name="otree-core",
		version='1.6.1',
		description="",
	    url='http://www.otree.org',
		author='Chris',
		author_email='chris@otree.org',
		license='MIT',
		packages=find_packages(),
		zip_safe=False,
	)
else:
	raise Exception('otree-core has been replaced by otree. If otree-core is in your requirements file, delete it.')