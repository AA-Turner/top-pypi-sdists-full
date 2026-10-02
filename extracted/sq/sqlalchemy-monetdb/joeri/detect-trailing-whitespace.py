#!/usr/bin/env python3

import os

for dir, subdirs, files in os.walk('.'):
    if '.venv' in dir or '/.' in dir or '/_' in dir:
        continue
    for filename in files:
        p = os.path.join(dir, filename)
        if not os.path.isfile(p):
            continue
        with open(p, 'rb') as f:
            content = f.read()
            if not content.endswith(b'\n'):
                print(f'No trailing newline: {p}')

