from setuptools import setup
import re

VERSIONFILE = "eventregistry/_version.py"
with open(VERSIONFILE, "rt", encoding="utf-8") as f:
    verstrline = f.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def readme():
    with open('README.md', encoding="utf-8") as f:
        return f.read()


setup(name='eventregistry',
      version = verstr,
      description = "A package that can be used to query information in Event Registry (https://eventregistry.org/)",
      long_description = readme(),
      long_description_content_type = "text/markdown",
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Text Processing :: General',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Intended Audience :: Information Technology'
      ],
      url = 'https://github.com/EventRegistry/event-registry-python',
      author = 'Gregor Leban',
      author_email = 'gregor@eventregistry.org',
      license = 'MIT',
      packages = ['eventregistry'],
      python_requires = '>=3.8',
      install_requires = [
          'requests'
      ],
      zip_safe=False)
