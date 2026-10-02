#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import smbc

def main():
    ctx = smbc.Context()
    uri = 'smb://localhost'
    entries = ctx.opendir(uri).getdents()
    for d in entries:
        print(d)

if __name__ == '__main__':
    main()
