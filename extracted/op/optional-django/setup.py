from setuptools import setup, find_packages
import optional_django

setup(
    name='optional-django',
    version=optional_django.__version__,
    packages=find_packages(exclude=('tests',)),
    description='Utils for providing optional support for django',
    long_description='Documentation at https://github.com/markfinger/optional-django',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/optional-django',
)