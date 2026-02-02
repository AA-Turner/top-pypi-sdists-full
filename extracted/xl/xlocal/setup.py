from setuptools import setup

if __name__ == "__main__":
    setup(
        name='xlocal',
        description='execution locals: killing global state (including thread locals)',
        long_description=open("README.txt").read(),
        version='0.5',
        author='Holger Krekel',
        author_email='holger.krekel@gmail.com',
        url='http://bitbucket.org/hpk42/xlocal/',
        py_modules=['xlocal', "test_xlocal"],
        #install_requires=['pytest-cache', 'pytest>=2.3.dev14', 'pep8>=1.3', ],
    )
