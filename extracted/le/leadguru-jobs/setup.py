import json
from urllib import request
from packaging.version import parse
from setuptools import setup, find_packages

package_name = "leadguru_jobs"


def versions():
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = list(json.loads(request.urlopen(url).read())['releases'].keys())
    return sorted(releases, key=parse, reverse=True)


try:
    version_parts: list = versions()[0].split(".")
except:
    version_parts: list = "0.0.0".split(".")

version_parts[1] = f'{float(version_parts[1]) + 1}'
last_version = ".".join(version_parts[0:-1])

install_requires = [
    'cachetools==3.1.0',
    'pydantic',
    'wheel',
    'setuptools<81',
    'twine',
    'build',
    'kubernetes',
    'pyyaml',
    'pymongo',
    'pytz',
    'requests',
    'mongoengine',
    'google',
    'google-cloud-pubsub',
    'google-cloud-storage',
    'google-cloud-logging',
    'websockets',
    'aiohttp',
    'nameparser',
    'loguru',
    'redmail',
    'tenacity'
]

setup(name=package_name,
      version=f'{last_version}',
      description='LGT jobs builds',
      packages=find_packages(include=['lgt_jobs', 'lgt_jobs.*']),
      package_data={'lgt_jobs': ['templates/new_message.html',
                                 'assets/images/arrow.png',
                                 'assets/images/arrow_blue.png',
                                 'assets/images/firework.png',
                                 'assets/images/lock.png',
                                 'assets/images/logo.png',
                                 'assets/images/mail.png']},
      include_package_data=True,
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'Environment :: Console',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet',
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)
