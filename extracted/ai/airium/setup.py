import os

from setuptools import find_packages, setup


def read(*file_path_parts):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(this_dir, *file_path_parts)
    with open(fp) as f:
        return f.read()


long_description = read('README.md')
dev_requires = read('requirements_dev.txt').splitlines()
parse_requires = read('requirements_for_parsing.txt').splitlines()

version_identifier = '0.3.2'

setup(
    name='airium',
    version=version_identifier,
    author='Michał Kaczmarczyk',
    author_email='michal.s.kaczmarczyk@gmail.com',
    maintainer='Michał Kaczmarczyk',
    maintainer_email='michal.s.kaczmarczyk@gmail.com',
    license='MIT',
    url='https://gitlab.com/kamichal/airium',
    description='Easy and quick html builder with natural syntax correspondence (python->html). '
                'No templates needed. Serves pure pythonic library with no dependencies.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests"]),
    package_data={
        'airium': ['py.typed', '*.pyi'],
    },
    requires=[],
    install_requires=[],
    keywords='natural html generator compiler template-less',
    python_requires='>=3.8',
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'airium = airium.__main__:entry_main'
        ],
    },
    extras_require={
        'dev': dev_requires,
        'parse': parse_requires,
    }
)
