#!/usr/bin/python
# -*- coding: utf-8 -*-

import distutils.core
import sys
import os.path
import subprocess
import shutil
import io

package_dir = os.path.abspath(os.path.dirname(__file__))

try:
    long_description_fd = io.open(os.path.join(package_dir, 'README.rst'),
                                  'r', encoding='utf-8')
    long_description = long_description_fd.read().rstrip(' \n\t\r')
    long_description_fd.close()
except IOError:
    sys.exit('README.rst file not found. Please check its existence.')

building = False
installing = False
for arg in sys.argv[1:]:
    if installing and arg == '--skip-build':
        building = False
        break
    if arg == '--help' or arg == '-h':
        break
    elif arg == 'build':
        building = True
        break
    elif arg == 'install':
        building = True
        installing = True

man_file = os.path.join(package_dir, "build/doc/man/man7/tinysegmenter.7")
if building:
    # If we have a building step, we want to build the man page as well.
    # Checking existence of rst2man.
    rst2man = None
    try:
        subprocess.check_call(["rst2man", '--version'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        rst2man = 'rst2man'
    except (subprocess.CalledProcessError, OSError):
        try:
            # The script is called rst2man or rst2man.py.
            subprocess.check_call(["rst2man.py", '--version'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            rst2man = 'rst2man.py'
        except (subprocess.CalledProcessError, OSError):
            sys.stderr.write("`rst2man` (tool included in `docutils`) does not exist. The man page won't be built.\n")
            sys.stderr.write("Re-run the script after installing `rst2man` if you wish to have the manual installed as a man page.")

    if rst2man is not None:
        rst_file = os.path.join(package_dir, "doc/man/tinysegmenter.7.rst")
        sys.stdout.write('Building the man page.\n')
        shutil.rmtree('build/doc/man/man7', True)
        try:
            os.makedirs('build/doc/man/man7')
        except os.error:
            sys.stderr.write('build/doc/man/man7 tree cannot be created.')
            sys.exit(os.EX_CANTCREAT)

        try:
            subprocess.check_call([rst2man, rst_file, man_file])
            # TODO would be better to compress the man with xz afterwards.
        except subprocess.CalledProcessError:
            sys.stderr.write("The following command failed: " + rst2man + ' ' + rst_file + ' ' + man_file + "\n")
            sys.stderr.write("The man page won't not be built.")

data_files = []
if os.path.exists(man_file):
    data_files = [('man/man7/', [man_file])]
    if installing:
        sys.stdout.write('The man page "tinysegmenter(7)" will be installed.\n')

class test(distutils.core.Command):
    '''
    Handling module test after installation.
    '''
    # user_options, initialize_options and finalize_options must be overriden.
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'tests/test.py'])
        raise SystemExit(errno)

distutils.core.setup(
    name = 'tinysegmenter',
    version = '0.4',
    author = 'Taku Kudo',
    author_email = 'taku@chasen.org',
    url = 'http://tinysegmenter.tuxfamily.org/',
    maintainer = 'Jehan',
    maintainer_email = 'tinysegmenter@zemarmot.net',
    description = 'Very compact Japanese tokenizer',
    long_description = long_description,
    license = 'New BSD',
    package_dir = {'': 'src'},
    py_modules = ['tinysegmenter'],
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic'
    ],
    cmdclass = {'test': test},
    data_files = data_files,
)
