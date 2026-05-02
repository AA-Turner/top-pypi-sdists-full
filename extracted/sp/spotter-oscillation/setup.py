from setuptools import setup, find_packages

setup(
    name='spotter_oscillation',
    version='1.9.2',  # Increment version to reflect changes
    description='A module for detecting price oscillations in financial assets',
    author='Raziel Ella',
    author_email='ellaraziel@gmail.com',
    license='Proprietary - Educational Use Only',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        'spotter_oscillation': ['*.pyd'],  # Include compiled Cython files (e.g., .pyd files)
    },
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'pyarrow',
        'requests'
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)
