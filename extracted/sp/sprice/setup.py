from setuptools import setup, find_packages

setup(
    name='sprice',
    version='0.1.1',
    packages=find_packages(),
    # This tells setuptools to include files listed in MANIFEST.in
    include_package_data=True,
    package_data={
        # Include all .h5 files under the data directory
        'sprice': ['data/*.h5'],
    },
    install_requires=[
        'pandas',  # Add other dependencies needed for your package
        'h5py'
    ],
    description='Consumer price data package for Saudi Arabia',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amjad-alt/sprice',  # Update with the actual URL
    author='Amjad Altuwayjiri',
    author_email='amjadibrahim1994@gmail.com'
)
