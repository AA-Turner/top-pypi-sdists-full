#!/usr/bin/env python

"""
A small script to update the DOAP file and commit/tag it.

Usage: ./release.py 2.0.0
"""

import fileinput
import sys
from datetime import datetime
from subprocess import check_call

version = sys.argv[1]

doap_release = f"""    <release>
        <Version>
            <revision>{version}</revision>
            <created>{datetime.now():%Y-%m-%d}</created>
            <file-release rdf:resource="https://codeberg.org/poezio/slixmpp/archive/slix-{version}.tar.gz"/>
        </Version>
    </release>
</Project>"""

try:
    proud, default, shame = (int(x) for x in version.split("."))
except ValueError:
    print("Not a valid version")
    exit(1)

for line in fileinput.input(files=["doap.xml"], inplace=True):
    if line.startswith("</Project>"):
        print(doap_release)
    else:
        print(line, end="")

check_call(["git", "commit", "doap.xml", "-m", f"build: release {version}"])
check_call(["git", "tag", "-s", f"slix-{version}"])
