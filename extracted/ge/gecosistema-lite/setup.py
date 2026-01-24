from distutils.core import setup
import setuptools

setup(name='gecosistema_lite',
      version='0.0.918',
      description='A simple python package',
      author='Valerio Luzzi',
      author_email='valerio.luzzi@gecosistema.it',
      url='https://github.com/valluzzi/libcore/',
      license='MIT',
      packages=['gecosistema_lite'],

      package_data={
          "gecosistema_lite": ["R/qkrige_v4.r"]
      },
      install_requires=['pyproj', 'rarfile', 'xlrd', 'xlwt', 'xlutils', 'jinja2', 'xmljson',
                        'openpyxl',
                        #'pycrypto', #some problems id msvc is not installed
                        'pyodbc',
                        #'future',  #troubles in python3
                        'six',
                        'argparse'
                        ]
      )
