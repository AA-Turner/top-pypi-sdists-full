# Copyright 2021 EnICS Labs, Bar-Ilan University.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

mode = input('Choose base class: 1) Component\t2)ComponentXY\t')

in_name = input('Enter Verilog (.v) file to be read and processed: ')
input_file = open(in_name,'r')
print ('opened file: [ %s ]\n' % in_name)

dev_name = ''
Lefs = {}

if mode == '2' or mode == 'ComponentXY':
	lef_name = input('Enter name of lef file: ')
	lef_file = open(lef_name, 'r')
	print('Reading lef file: [%s]\n' % lef_name)
	for line in lef_file:
		words = line.split()
		if words and words[0] == 'MACRO':
			dev_name = words[1]
		if words and words[0] == 'SIZE':
			Lefs[dev_name] = [ words[1] , words[3] ]
	lef_file.close()

dev_name = ''
sequentials = set()
lib_name = input('Enter name of lib file: ')
lib_file = open(lib_name, 'r')
print('Reading lib file: [%s]\n' % lib_name)
for line in lib_file:
	if line.startswith('  cell('):
		dev_name = line.replace(')','(').split('(')[1]
	if line == "      clock : true ; \n":
		sequentials.add(dev_name)
lib_file.close()

out_name = input('Enter name of output file: ')
output_file = open(out_name, 'w+')




output_file.write('from salamandra import *\n\n')

temp_line = []
temp_name = ''
for line in input_file:
	words = line.split() # split line
	outputs = []
	inputs = []
	if words:
		if words[0] == 'module':
			temp_name = words[1]
			if len(words) == 2:
				output_file.write('class ' + temp_name[:-1] +'(ComponentXY):\n')
				output_file.write('\t__defaultName = \'' + temp_name[:-1] +'\'\n\n')			
			else:
				output_file.write('class ' + temp_name +'(ComponentXY):\n')
				output_file.write('\t__defaultName = \'' + temp_name +'\'\n\n')
		if words[0] == 'endmodule':
			output_file.write('\n')
		if words[0] == 'output':
			temp_line = words
			if not len(temp_line):
				break
		if words[0] == 'input':
			output_file.write('\tdef __init__(self, name = __defaultName, ')
			for k in range(1,len(words) ):
				inputs.append(words[k][:-1])
			for k in range(0,len(inputs) ):
				output_file.write('in'+ str(k+1) + '=\'' + inputs[k]+'\'' )
				if k != len(inputs):
					output_file.write(', ')
				elif len(temp_line) == 0:
					output_file.write('):\n')
				else: 
					output_file.write(', ')
			for k in range(1, len(temp_line) ):
				outputs.append(temp_line[k][:-1] )
			for k in range(0,len(outputs) ):
				output_file.write('out' + str(k+1) + '=\''+ outputs[k] + '\'')
				if k != len(outputs)-1:
					output_file.write(', ')
				else:
					output_file.write('):\n')
			if mode == '2' or mode == 'ComponentXY':
				output_file.write('\t\tComponentXY.__init__(self,name)\n')
			else:
				output_file.write('\t\tComponent.__init__(self,name)\n')
			for k in range(0,len(inputs) ):
				output_file.write('\t\tself.add_pin(Input(in'+ str(k+1) + ') )\n' )
			
			for k in range(0,len(outputs) ):
				output_file.write('\t\tself.add_pin(Output(out'+ str(k+1) + ') )\n' )
			if mode == '2' or mode == 'ComponentXY':
				output_file.write('\t\tself.set_component_dimensions('+Lefs[temp_name][0]+', '+Lefs[temp_name][1]+')\n' )

			output_file.write('\t\tself.set_dont_uniq(True)\n')
			output_file.write('\t\tself.set_dont_write_verilog(True)\n')
			output_file.write('\t\tself.set_is_physical(True)\n')
			output_file.write('\t\tself.set_is_sequential('+ ('True' if temp_name in sequentials else 'False') +')\n')


input_file.close()
output_file.close()

