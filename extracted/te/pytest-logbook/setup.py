import setuptools


setuptools.setup(
    name='pytest-logbook',
    description='py.test plugin to capture logbook log messages',
    long_description=open('README').read(),
    version='1.2.0',
    author='Floris Bruynooghe',
    author_email='flub@devork.be',
    url='http://bitbucket.org/flub/pytest-logbook',
    license='MIT',
    py_modules=['pytest_logbook'],
    entry_points={'pytest11': ['_logbook = pytest_logbook']},
    install_requires=['pytest>=2.8', 'Logbook>=0.11.3'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing'
    ],
)
