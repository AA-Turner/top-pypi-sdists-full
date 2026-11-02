from setuptools import setup, find_packages


setup(
    name='sendgrid-python',
    version='0.1.1',
    author='Kane Kim',
    author_email='kane@sendgrid.com',
    packages=find_packages(),
    url='https://github.com/sendgrid/sendgrid-python/',
    license='LICENSE.txt',
    description='SendGrid client',
    long_description='SendGrid client',
    install_requires=[
        'sendgrid'
    ],
)
