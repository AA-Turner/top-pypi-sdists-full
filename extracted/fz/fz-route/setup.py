from setuptools import setup, find_packages

VERSION = '0.1.2' 
DESCRIPTION = 'FZ Route Forecast'
LONG_DESCRIPTION = 'Base Working file data generation for route forecast'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="fz_route", 
        version=VERSION,
        author="Sami",
        author_email="<edsami17@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'pandas',
            'numpy',
            'sqlalchemy'
        ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)