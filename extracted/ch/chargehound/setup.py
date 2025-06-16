try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

try:
    from pypandoc import convert
    long_description = convert('README.md', 'rst')
except:
    """
    Don't fail if pandoc or pypandoc are not installed.
    However, it is better to publish the package with
    a formatted README.
    """
    print("""
Warning: Missing pypandoc, which is used to format \
the README. Install pypandoc before publishing \
a new version.""")
    long_description = open('README.md').read()

setup(
    name='chargehound',
    version='2.5.0',
    author='Chargehound',
    author_email='support@chargehound.com',
    packages=['chargehound'],
    description='Chargehound Python Bindings',
    long_description=long_description,
    url='https://www.chargehound.com',
    license='MIT',
    test_suite='test.all',
    install_requires=[
        'requests',
        'munch'
        ],
    )
