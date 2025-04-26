#!/bin/python
# coding: utf-8

##########################################################################################################################################

from pathlib import Path

from jsoncomment import JsonComment

##########################################################################################################################################

EXAMPLE_PY = Path(__file__)
EXAMPLE_JFC = EXAMPLE_PY.with_suffix(".jsonc")
EXAMPLE_JFS = EXAMPLE_PY.with_suffix(".json")

##########################################################################################################################################

def main():
	json = JsonComment()

	json_objc = json.loadf(EXAMPLE_JFC)
	json_objs = json.loadf(EXAMPLE_JFS, default = {"test":True})

	print("\n", "*"*80, "\n")

	print(json_objc["item 1"], "\n")
	print(json_objc["Section/Subsection"], "\n")

	print(json_objs, "\n")

	print(json.dumps(json_objc), "\n")

	print("\n", "*"*80, "\n")

	json.dumpf(json_objc, EXAMPLE_JFS)

if __name__ == "__main__":
	main()

##########################################################################################################################################
