from distutils.core import setup

with open("README.rst", "r") as f:
    readme = f.read()

setup(name='zipfile36',
      version='0.1.3',
      description='Read and write ZIP files - backport of the zipfile module from Python 3.6',
      long_description = readme,
      author='Thomas Kluyver',
      author_email='thomas@kluyver.me.uk',
      url='https://gitlab.com/takluyver/zipfile36',
      py_modules=['zipfile36'],
      classifiers=[
          'License :: OSI Approved :: Python Software Foundation License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Archiving :: Compression',
      ]
)
