import os
import sys
import yaml
from .make import make
from .html import html
from .coverage import coverage

BASE_DIR = os.getcwd()
CONFIG_PATH = os.path.join(BASE_DIR, "spravka.yml")

with open(CONFIG_PATH, 'r') as stream:
    data_loaded = yaml.safe_load(stream)


def main():
    try:
        command = sys.argv[1]
    except IndexError:
        command = ''
    if command in ['make', 'm']:
        make()
    elif command in ['html', 'h']:
        html()
    elif command in ['coverage', 'c']:
        coverage()
    else:
        print("""
SPRAVKA

command:
    make, m - create directory for documentation
    html, h - generate html documentation
    coverage, c - coverage for files
            """)
