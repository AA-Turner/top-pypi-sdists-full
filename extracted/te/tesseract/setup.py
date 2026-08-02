from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name = 'tesseract',
    packages = ['tesseract'],
    package_dir = {'tesseract': 'tesseract'},
    package_data = {'tesseract': ['README.md','default_config.ini','halos/*.snap',
				  'qhull2002.1.tar','example.param',
                                  'vorovol/*.c','vorovol/*.h','vorovol/Makefile']},
    version = '0.1.3',
    author = 'Meagan Lang',
    author_email = 'meagan.lang@vanderbilt.edu',
    url = 'http://vpac00.phy.vanderbilt.edu/~langmm/index.html',
    description = 'Tesselation based Recovery of Amorphous halo Concentrations',
    classifiers = ["Programming Language :: Python","Operating System :: OS Independent",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Intended Audience :: Science/Research","Natural Language :: English",
                   "Topic :: Scientific/Engineering","Topic :: Scientific/Engineering :: Astronomy",
                   "Development Status :: 3 - Alpha"], #"Programming Language :: C" 
    long_description = long_description
)
