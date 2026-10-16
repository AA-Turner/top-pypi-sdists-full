#! /usr/bin/python3
from pathlib import Path
import sys
import os
root=Path('/home/carl/Desktop/RadBoy/radboy')
root_cmd=Path('renderQR.py')
readme=Path('renderQR.py.README')
dirs=['sku','name','price','Tags']
for dir in dirs:
	cmdStr=f"cd {dir} && python renderQR.py & cd {root}"
	px=Path(dir)

	if not px.exists():
		px.mkdir(parents=True)
		with open(px/root_cmd,"w") as o:
			o.write((root/root_cmd).open("r").read())

		with open(px/readme,"w") as o:
			o.write((root/readme).open("r").read())

	else:
		with open(px/root_cmd,"w") as o:
			o.write((root/root_cmd).open("r").read())

		with open(px/readme,"w") as o:
			o.write((root/readme).open("r").read())
	os.system(cmdStr)
