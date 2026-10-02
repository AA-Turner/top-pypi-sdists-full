from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

from pyrosetta_installer import *

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        #install_pyrosetta()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        #install_pyrosetta()

setup(
    name='pyrosetta-installer',
    version='0.1.2',
    description='Download PyRosetta wheel package from PyRosetta.org and install it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.pyrosetta.org/',
    author='Sergey Lyskov',
    license='Rosetta Software License',
    packages=['pyrosetta_installer'],
    zip_safe=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
