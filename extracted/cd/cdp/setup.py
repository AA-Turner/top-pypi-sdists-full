from setuptools import setup

MAJOR_VERSION = '0'
MINOR_VERSION = '0'
MICRO_VERSION = '2'
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(name = 'cdp',
      version = VERSION,
      description = 'Change Directory Plus',
      url = 'https://github.com/kootenpv/yagmail',
      author = 'Pascal van Kooten',
      author_email = 'kootenpv@gmail.com',
      license = 'GPL',
      packages = ['cdp'],
      install_requires = [ 
          'scandir',
      ], 
      entry_points = { 
          'console_scripts': ['cdp = cdp.cdp:main'] 
      },
      zip_safe = False)
