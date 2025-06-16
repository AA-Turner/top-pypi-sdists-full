import os
from setuptools import setup, find_packages

NAME = "gcloud-storage-emulator"
PACKAGES = find_packages()

DESCRIPTION = "A stub emulator for the Google Cloud Storage API"
URL = "https://gitlab.com/potato-oss/google-cloud/gcloud-storage-emulator"
LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

AUTHOR = "Potato London Ltd."
AUTHOR_EMAIL = "mail@p.ota.to"

if os.environ.get('CI_COMMIT_TAG'):
    VERSION = os.environ['CI_COMMIT_TAG']
else:
    VERSION = '0.0.0dev0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    zip_safe=False,
    keywords=["Google Cloud Storage", "Google App Engine", "GAE", "GCS"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    scripts=[
        "bin/gcloud-storage-emulator",
        "bin/gcloud-storage-emulator.py"
    ],
    install_requires=[
        "fs",
        "google-cloud-storage",
        "requests",
    ],
    python_requires='>=3.6',
)
