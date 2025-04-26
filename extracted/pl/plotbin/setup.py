from setuptools import setup, find_packages
import re

package = "plotbin"

def find_version(package):
    version_file = open(package + "/__init__.py").read()
    rex = r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    return re.search(rex, version_file).group(1)

setup(name=package,
      version=find_version(package),
      description='PlotBin: Plotting Binned Maps and Other Utilities',
      long_description_content_type='text/x-rst',
      long_description=open("README.rst").read(),
      url='https://purl.org/cappellari/software',
      author='Michele Cappellari',
      author_email='michele.cappellari@physics.ox.ac.uk',
      license='Other/Proprietary License',
      packages=find_packages(),
      install_requires=['numpy', 'scipy', 'matplotlib'],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3"],
      zip_safe=True)
