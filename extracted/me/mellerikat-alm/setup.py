import shutil
import os
from setuptools import setup

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'alm', '__version__.py')
    with open(version_file, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Cannot find version information")

def get_install_requires():
    # if check platform using sys.platform == "darwin"
    requires = [
        'gitpython>=3.1.43',
        'pyyaml>=6.0.1',
        'pytz>=2021.3',
        'boto3==1.33.13;python_version<="3.7"',
        'boto3==1.34.41;python_version>"3.7"',
        'botocore==1.33.13;python_version<="3.7"',
        'botocore==1.34.41;python_version>"3.7"',
        'psutil>=5.9.5',
        'requests>=2.31.0',
        'redis>=5.0.1',
        'docker>=7.0.0;python_version>"3.7"',
        'docker==6.1.3;python_version<="3.7"',
        'tabulate>=0.9.0',
        'colorama>=0.4.6',
        'pyfiglet==0.8.post1;python_version<="3.8"',
        'pyfiglet==1.0.2;python_version>"3.8"',
        'pydantic==2.5.3;python_version<="3.7"',
        'pydantic>=2.7.4;python_version>"3.7"',
        'pydantic-settings==2.0.3;python_version<="3.7"',
        'pydantic-settings>=2.3.3;python_version>"3.7"',
        'google-cloud-storage==2.18.2',
        'uvicorn==0.32.1',
        'fastapi==0.115.5',
        'kubernetes==31.0.0',
        'python-dotenv==1.0.1',
        'python-multipart==0.0.20',
        'aiofiles',
        'sqlmodel',
        'uv'
    ]

    return requires

# remove old dir
for target in ['build', 'dist', 'llo.egg-info']:
    build_path = os.path.join(os.path.abspath(__file__), target)
    if os.path.exists(build_path):
        shutil.rmtree(build_path)

setup(
    name='mellerikat-alm',
    version=get_version(),
    description="ALO-LLM (AI Logic Organizer-LLM)",
    long_description="ALO-LLM (AI Logic Organizer-LLM)",
    author='LGE',
    author_email='mellerikat@lge.com',
    url='https://mellerikat.com',
    license='LGE License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages=['alm', 'template', 'alm.router'],
    platforms=['Linux', 'FreeBSD', 'Solaris'],
    python_requires='>=3.10',
    install_requires=get_install_requires(),
    entry_points={
     'console_scripts': [
            'alm = alm.main:main',
        ]
    },
    include_package_data=True,
)
