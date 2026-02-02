import datetime
import re

now = datetime.datetime.now()
date = '{}{:02}{:02}'.format(now.year, now.month, now.day)
version = ''

# Get version from Cargo.toml
with open('Cargo.toml', 'r+') as f:
    text = f.read()
    versions = re.findall(r'version = "(.*)"', text)
    version = versions[0]

# Overwrite project name and version with date in pyproject.toml
with open('pyproject.toml', 'r+') as f:
    text = f.read()
    text = re.sub('name = "eclipse-zenoh"', 'name = "eclipse-zenoh-nightly"\nversion = "{}{}"'.format(version, date), text)
    f.seek(0)
    f.write(text)
    f.truncate()

