#!/usr/bin/env python3

from igwn_ligolw import utils as ligolw_utils

if __name__ == "__main__":
    while True:
        ligolw_utils.load_filename("ligo_lw_test_01.xml", verbose=True).unlink()
