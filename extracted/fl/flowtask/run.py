#!/usr/bin/env python3
from navigator import Application

from app import Main

app = Application(Main, enable_jinja2=True)

if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        print('==== EXIT FROM DataIntegrator =====')
