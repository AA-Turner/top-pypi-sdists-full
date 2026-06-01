#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='telegram',
      version='0.0.1',
      keywords=('telegram', 'api'),
      description='Telegram APIs',
      license='MIT',

      url='https://github.com/liluo/telegram',
      author='liluo',
      author_email='i@liluo.org',

      packages=find_packages(),
      include_package_data=True)
