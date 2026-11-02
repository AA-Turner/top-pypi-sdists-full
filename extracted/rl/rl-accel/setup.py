from setuptools import setup, Extension
try:
    from setuptools.command.bdist_wheel import bdist_wheel, get_abi_tag
except ImportError:
    try:
        from wheel.bdist_wheel import bdist_wheel, get_abi_tag
    except ImportError:
        from wheel._bdist_wheel import bdist_wheel, get_abi_tag
from os.path import join as pjoin
import sys, os, sysconfig, re

def make_la_info():
    '''compute limited api and abi info'''
    global py_limited_kwds, cpstr
    cpstr = get_abi_tag()
    if cpstr.startswith("cp"):
        lav = '0x03070000'
        cpstr = 'cp37'
        if sys.platform == "darwin":
            machine = sysconfig.get_platform().split('-')[-1]
            if machine=='arm64' or os.environ.get('ARCHFLAGS','')=='-arch arm64':
                #according to cibuildwheel/github M1 supports pythons >= 3.8
                lav = '0x03080000'
                cpstr = 'cp38'
        py_limited_kwds = dict(
                                define_macros=[("Py_LIMITED_API", lav)],
                                py_limited_api=True,
                                )
    else:
        py_limited_kwds = {}

make_la_info()

class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            abi = 'abi3'
            python = cpstr
        return python,abi,plat

def getVersionFromCCode(fn):
    with open(fn,'r') as _:
        code = _.read()
    tag = re.search(r'^#define\s+VERSION\s+"([^"]*)"',code,re.M)
    return tag and tag.group(1) or ''

setup(
    ext_modules=[
        Extension(
            "_rl_accel",
            sources=[pjoin('src','_rl_accel.c')],
            **py_limited_kwds,
        )
    ],
    name="rl_accel",
    version=getVersionFromCCode(pjoin('src','_rl_accel.c')),
    license="BSD license (see LICENSE.txt for details), Copyright (c) 2000-2022, ReportLab Inc.",
    description="Acclerator for ReportLab",
    long_description="""This is an accelerator module for the ReportLab Toolkit Open Source Python library for generating PDFs and graphics.""",
    author="Andy Robinson, Robin Becker, the ReportLab team and the community",
    author_email="reportlab-users@lists2.reportlab.com",
    url="http://www.reportlab.com/",
    packages=[],
    package_data = {},
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Printing',
        'Topic :: Text Processing :: Markup',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        ],
    license_files = ['LICENSE.txt'],
            
    #this probably only works for setuptools, but distutils seems to ignore it
    install_requires=[],
    python_requires='>=3.7,<4',
    extras_require={
        },
    cmdclass={"bdist_wheel": bdist_wheel_abi3},
)
