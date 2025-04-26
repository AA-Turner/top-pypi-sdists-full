from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

VERSION = "0.1.660"  # Replace with a dynamic value or placeholder

setup(
    name='fsd',
    version=VERSION,
    author='Zinley',
    author_email='dev@zinley.com',
    description='Core engine powering Zinley Studio - an AI-powered development environment',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zinley-dev/fsd_v2_universal',  # Replace with your library's URL
    packages=find_namespace_packages(include=['fsd','fsd.*']),  # Automatically find package directories
    package_data={
        'fsd': ['queries/*']  # Include all files in the queries directory
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version required
    install_requires=required,
    include_package_data=True,  # Include files listed in MANIFEST.in
)
