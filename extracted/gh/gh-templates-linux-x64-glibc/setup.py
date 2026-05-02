from setuptools import setup, find_packages
import platform

setup(
    name='gh-templates-linux-x64-glibc',
    version='0.1.39',
    description='GitHub Templates CLI tool',
    packages=find_packages(),
    package_data={'gh_templates_bin': ['*']},
    entry_points={'console_scripts': ['gh-templates=gh_templates_bin:main']},
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.7',
)
