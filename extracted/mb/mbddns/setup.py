from setuptools import setup

setup(name='mbddns',
      version='0.1.2',
      description='Mythic Beasts Dynamic DNS updater',
      url='https://github.com/thinkl33t/mb-ddns',
      author='Bob Clough',
      author_email='bob@clough.me',
      license='MIT',
      packages=['mbddns'],
      install_requires=[
          'aiohttp',
      ],
      zip_safe=False)
