import os
import sys
import distutils.sysconfig
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()


def check_pth(site_packages):
    pthfile = os.path.join(site_packages, "pip_system_certs.pth")
    if not os.path.exists(pthfile):
        sys.stderr.write("WARNING: pip_system_certs.pth not installed correctly, will try to correct.\n")
        sys.stderr.write("Please report an issue at https://gitlab.com/alelec/pip-system-certs with your\n")
        sys.stderr.write("python and pip versions included in the description\n")
        import shutil
        shutil.copyfile("pip_system_certs.pth", pthfile)


class InstallCheck(install):
    def run(self):
        install.run(self)
        check_pth(self.install_purelib)


class DevelopCheck(develop):
    def run(self):
        develop.run(self)
        check_pth(self.install_dir)


class BuildIncludePth(build_py):
     """Include the .pth file for this project in the generated wheel."""

     def run(self):
         super().run()

         pth_file = "pip_system_certs.pth"

         outfile = os.path.join(self.build_lib, pth_file)
         self.copy_file(pth_file, outfile, preserve_mode=0)


site_packages = distutils.sysconfig.get_python_lib()


setup(
    name='pip_system_certs',
    use_git_versioner="gitlab:desc:snapshot",
    setup_requires=["git-versioner"],
    description='Live patches pip to use system certs by default',
    long_description=long_description,
    author='Andrew Leech',
    author_email='andrew@alelec.net',
    license='BSD',
    url='https://gitlab.com/alelec/pip-system-certs',
    packages=['pip_system_certs'],
    install_requires=['wrapt>=1.10.4'],
    zip_safe=False,
    cmdclass={
        "build_py": BuildIncludePth,
        "install": InstallCheck,
        "develop": DevelopCheck,
    },
    python_requires='>=2.7.9, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
