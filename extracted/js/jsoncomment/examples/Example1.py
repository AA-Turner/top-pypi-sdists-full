#!/bin/python
# coding: utf-8

##########################################################################################################################################

from jsoncomment import JsonComment

##########################################################################################################################################

def main():
	string = """
		/******************
		Comment 1
		Comment 2
		******************/
		[
			# Objects
			{
				"key" : "value",
				"another key" :
				\"\"\"
				\\n
				A multiline string.\\n
				It will wrap to single line, 
				but a trailing space per line is kept.
				\"\"\",
			},
			; Other Values
			81,
			// Allow a non standard trailing comma
			true,
		]
		"""

	json = JsonComment()
	json_obj = json.loads(string)

	print("\n", "*"*80, "\n")

	print(json_obj[0]["another key"], "\n")

	print(json.dumps(json_obj), "\n")

	print("\n", "*"*80, "\n")

if __name__ == "__main__":
	main()

##########################################################################################################################################
