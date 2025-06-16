import sys
import os

from shutil import rmtree
from setuptools import find_packages, setup, Command, Extension
from Cython.Build import cythonize
from aimrocks import lib_utils
# TODO This `setup.py` assumes that `Cython` and `aimrocks` are installed.
# This is okay for now as users are expected to install `aim` from wheels.

version_file = 'src/aim/VERSION'

with open(version_file) as vf:
    __version__ = vf.read().strip()

here = os.path.abspath(os.path.dirname(__file__))
client_only = os.getenv('BUILD_AIMHUB_CLIENT')

# Package meta-data.
if client_only:
    NAME = 'aimhub-client'
else:
    NAME = 'aim-server'

DESCRIPTION = 'A super-easy way to record, search and compare AI experiments.'
VERSION = __version__
REQUIRES_PYTHON = '>=3.7.0'


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            # compensate for the src-based setup by adding ../../
            paths.append(os.path.join('..', '..', path, filename))
    return paths


aim_package_files = package_files('src/aim/_ext/notifier')
if not client_only:
    aim_package_files += package_files('src/aim/_ext/web/migrations')

readme_file = 'README.md'
readme_text = open('/'.join((here, readme_file)), encoding="utf-8").read()
LONG_DESCRIPTION = readme_text.strip()

SETUP_REQUIRED = [
    'Cython==3.0.0a11',
]

# What packages are required for this module to be executed?
REQUIRED = [
    'aimrocks==0.5.1',
    'cachetools>=4.0.0',
    'click>=7.0',
    'cryptography>=3.0',
    'filelock<4,>=3.3.0',
    'numpy<2,>=1.12.0',
    'psutil>=5.6.7',
    'RestrictedPython>=5.1',
    'tqdm>=4.20.0',
    'Pillow>=8.0.0',
    'packaging>=15.0',
    'websockets',
    'requests',
    'importlib_metadata',
    'tabulate',
    'boto3',
]

if not client_only:
    REQUIRED += [
        'aim-ui==3.29.1',
        'aimhub-license==0.7.0',
        'khash==0.6.0',
        'fastapi<1,>=0.69.0',
        'jinja2<4,>=2.10.0',
        'SQLAlchemy>=1.4.1',
        'uvicorn<1,>=0.12.0',
        'alembic<2,>=1.5.0',
        'psycopg2-binary<3',
        'redis',
    ]


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = [
        ('rc', None, 'Tag version as a release candidate'),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        self.rc = 0

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Cleaning build directory')
        os.system('{} setup.py clean --all'.format(sys.executable))

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(f'{sys.executable} setup.py sdist bdist_wheel --universal')

        # self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        if not self.rc:
            self.status('Pushing git tags…')
            os.system('git tag v{0}'.format(VERSION))
            os.system('git push --tags')

        sys.exit()


INCLUDE_DIRS = [lib_utils.get_include_dir()]
LIB_DIRS = [lib_utils.get_lib_dir()]
LIBS = lib_utils.get_libs()
COMPILE_ARGS = [
    '-std=c++11',
    '-O3',
    '-Wall',
    '-Wextra',
    '-Wconversion',
    '-fno-strict-aliasing',
    '-fno-rtti',
    '-fPIC'
]

CYTHON_SCRIPTS = [
    # hashing
    ('aim._core.storage.hashing.c_hash', 'src/aim/_core/storage/hashing/c_hash.pyx'),
    ('aim._core.storage.hashing.hashing', 'src/aim/_core/storage/hashing/hashing.py'),
    ('aim._core.storage.hashing', 'src/aim/_core/storage/hashing/__init__.py'),
    # encoding utilities
    ('aim._core.storage.encoding.encoding_native', 'src/aim/_core/storage/encoding/encoding_native.pyx'),
    ('aim._core.storage.encoding.encoding', 'src/aim/_core/storage/encoding/encoding.pyx'),
    ('aim._core.storage.encoding', 'src/aim/_core/storage/encoding/__init__.py'),
    ('aim._core.storage.treeutils', 'src/aim/_core/storage/treeutils.pyx'),
    # storage interfaces
    ('aim._core.storage.arrayview', 'src/aim/_core/storage/arrayview.py'),
    ('aim._core.storage.treearrayview', 'src/aim/_core/storage/treearrayview.py'),
    ('aim._core.storage.treeview', 'src/aim/_core/storage/treeview.py'),
    ('aim._core.storage.utils', 'src/aim/_core/storage/utils.py'),
    ('aim._core.storage.inmemorytreeview', 'src/aim/_core/storage/inmemorytreeview.py'),
]

if not client_only:
    CYTHON_SCRIPTS += [
        ('aim._core.storage.embedded.container', 'src/aim/_core/storage/embedded/container.py'),
        ('aim._core.storage.embedded.rockscontainer', 'src/aim/_core/storage/embedded/rockscontainer.pyx'),
        ('aim._core.storage.embedded.containertreeview', 'src/aim/_core/storage/embedded/containertreeview.py'),
        ('aim._core.storage.embedded.prefixcontainer', 'src/aim/_core/storage/embedded/prefixcontainer.py'),
        # web APIs
        ('aim._ext.web.api.utils', 'src/aim/_ext/web/api/utils.py'),
    ]


def configure_extension(name: str, path: str):
    """Configure an extension and bind with third-party libs"""
    if isinstance(path, str):
        path = [path]
    return Extension(
        name,
        path,
        language='c++',
        include_dirs=INCLUDE_DIRS,
        libraries=LIBS,
        library_dirs=LIB_DIRS,
        extra_compile_args=COMPILE_ARGS,
    )


def cytonize_extensions(scripts):
    """Configure and Cythonize all the extensions"""
    extensions = []
    for name, path in scripts:
        extensions.append(configure_extension(name, path))
    return cythonize(extensions, show_all_warnings=True)


if client_only:
    exclude_list = (
        'aim._core.storage.embedded', 'aim._core.storage.embedded.*',
        'aim._ext.web', 'aim._ext.web.*',
        'aim._ext.tracking', 'aim._ext.tracking.*',
        'aim._ext.cli.init', 'aim._ext.cli.init.*',
        'aim._ext.cli.server', 'aim._ext.cli.server.*',
        'aim._ext.cli.ui', 'aim._ext.cli.ui.*',
        'aim._ext.cli.migrate', 'aim._ext.cli.migrate.*',
        'aim._sdk.local_storage', 'aim._sdk.local_storage.*',
    )
else:
    exclude_list = (
        'aim._sdk.integrations', 'aim._sdk.integrations.*',
        'aim.acme',
        'aim.catboost',
        'aim.fastai',
        'aim.hugging_face',
        'aim.keras',
        'aim.keras_tuner',
        'aim.lightgbm',
        'aim.mxnet',
        'aim.optuna',
        'aim.paddle',
        'aim.prophet',
        'aim.pytorch',
        'aim.pytorch_ignite',
        'aim.pytorch_lightning',
        'aim.sb3',
        'aim.tensorflow',
        'aim.xgboost',
    )

# Where the magic happens
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    python_requires=REQUIRES_PYTHON,
    setup_requires=SETUP_REQUIRED,
    install_requires=REQUIRED,
    packages=(
        find_packages(where='src', exclude=exclude_list)
    ),
    package_dir={
        '': 'src',
    },
    package_data={
        'aim': aim_package_files
    },
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    ext_modules=cytonize_extensions(CYTHON_SCRIPTS),
    entry_points={
        'console_scripts': [
            'aim=aim._ext.cli.cli:cli_entry_point',
            # 'aim-watcher=aim._ext.cli.watcher_cli:cli_entry_point',
        ],
    },
    cmdclass={
        'upload': UploadCommand
    }
)
