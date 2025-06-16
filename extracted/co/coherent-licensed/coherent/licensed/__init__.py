import datetime
import re
import urllib.request


def inject_year(text):
    pattern = re.compile(r'\[yyyy\]|<year>')
    return pattern.sub(str(datetime.date.today().year), text)


def resolve(expression):
    """
    Resolve an SPDX license expression into a license text.

    >>> resolve('MIT')
    'MIT License...'
    """
    url = f"https://raw.githubusercontent.com/spdx/license-list-data/main/text/{expression}.txt"
    with urllib.request.urlopen(url) as response:
        return inject_year(response.read().decode('utf-8'))
