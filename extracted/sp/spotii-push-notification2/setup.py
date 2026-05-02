from os import path

from setuptools import find_packages, setup

NAME = "spotii-push-notification2"
VERSION = "1.1.4"

REQUIRES = ["aiohttp", "django", "djangorestframework", "asgiref"]


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="Spotii Push Notification",
    author_email="hello@nuclearo.com",
    url="",
    keywords=["Spotii", "Push Notification"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
