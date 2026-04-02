# pylint: skip-file
# flake8: noqa
"""script for testing client with live requests to ESI

Run this script directly. Make sure to also set the environment variable
DJANGO_PROJECT_PATH and DJANGO_SETTINGS_MODULE to match your setup:

You can see the result in your main log file of your Django installation.

Example:
export DJANGO_PROJECT_PATH="/home/erik997/dev/python/aa/aa-dev-3/myauth"
export DJANGO_SETTINGS_MODULE="myauth.settings.local"

"""

# start django project
import os
import sys

if not "DJANGO_PROJECT_PATH" in os.environ:
    print("DJANGO_PROJECT_PATH is not set")
    exit(1)

if not "DJANGO_SETTINGS_MODULE" in os.environ:
    print("DJANGO_SETTINGS_MODULE is not set")
    exit(1)

sys.path.insert(0, os.environ["DJANGO_PROJECT_PATH"])
import django

django.setup()

# normal imports
import logging

from django.core.cache import cache

from eveuniverse.models import *
from eveuniverse.providers import esi

cache.clear()
logger = logging.getLogger("__name__")


def main():
    # EveType.objects.update_or_create_esi(603)
    # EveType.objects.update_or_create_esi(608)
    EveStation.objects.update_or_create(id=60015068)

    # EveBloodline.objects.load_esi()


if __name__ == "__main__":
    print("Script started...")
    main()
    print("DONE")
