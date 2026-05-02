import os
import os.path
from os import path

def pythonprints(dpath):

	path_exist = path.exists(dpath)
	listfiles = []
	if path_exist == True:
		files = os.listdir(dpath)
		for i in files:	
			if i.endswith('.py'):
				listfiles.append(i)
		for file in listfiles:
			busqueda = "print("
			with open(file, "r") as files:
				string = files.read()
			found_count = string.count(busqueda)
			print(f"{file}:{found_count}")

		return True
	else:
		return None


