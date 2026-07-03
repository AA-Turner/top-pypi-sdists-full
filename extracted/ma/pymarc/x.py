#!/usr/bin/env python3

import pymarc

for record in pymarc.reader.MARCReader(open("BooksAll.2016.part01.utf8","rb")):
    print(record.title)


