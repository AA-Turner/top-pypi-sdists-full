# flake8: noqa

"""
Script to remove all generated FAT links from the database, which have been created by the script generate_fat_links.py.

This script can be executed directly from shell.
"""

# Standard Library
import os
import sys
from pathlib import Path

myauth_dir = Path(__file__).parent.parent.parent.parent.parent / "myauth"
sys.path.insert(0, str(myauth_dir))

# Django
import django

# init and setup django project
os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="myauth.settings.local")
django.setup()

# Alliance Auth AFAT
from afat.models import FatLink

# Remove all generated FAT links
print("Removing all generated FAT links")
FatLink.objects.filter(fleet__startswith="Generated Fleet #").delete()
print("All generated FAT links have been removed")
