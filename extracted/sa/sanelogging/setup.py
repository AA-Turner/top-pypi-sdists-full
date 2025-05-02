from setuptools import setup

setup(
    name='sanelogging',
    version='1.1.0',
    author='Jeffrey Paul',
    author_email='sneak@sneak.berlin',
    packages=['sanelogging'],
    url='https://github.com/sneak/sanelogging/',
    license='Public Domain',
    description='Python logging for humans',
    install_requires=[
        "colorlog",
        "pytz",
        "datetime"
    ],
)
