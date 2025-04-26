from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
]

setup(
    name='sgmllib3k',
    version='1.0.0',
    author='Hardcoded Software',
    author_email='hsoft@hardcoded.net',
    py_modules=['sgmllib'],
    scripts=[],
    url='http://hg.hardcoded.net/sgmllib',
    license='BSD License',
    description='Py3k port of sgmllib.',
    long_description=open('README').read(),
    classifiers=CLASSIFIERS,
    test_suite='test_sgmllib',
)