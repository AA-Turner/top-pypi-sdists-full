from . import *


preloader={
	f'{uuid1()}':{
						'cmds':['volume',],
						'desc':f'find the volume of height*width*length without dimensions',
						'exec':volume
					},
	f'{uuid1()}':{
						'cmds':['volume pint',],
						'desc':f'find the volume of height*width*length using pint to normalize the values',
						'exec':volume_pint
					},
	f'{uuid1()}':{
						'cmds':['self-inductance pint',],
						'desc':f'find self-inductance using pint to normalize the values for self-inductance=relative_permeability*(((turns**2)*area)/length)*1.26e-6',
						'exec':inductance_pint
					},
	f'{uuid1()}':{
						'cmds':['required resonant LC inductance',],
						'desc':f'find the resonant inductance for LC using L = 1 / (4π²f²C)',
						'exec':resonant_inductance
					},
	f'{uuid1()}':{
						'cmds':['air coil',],
						'desc':f''' 
The formula for inductance - using toilet rolls, PVC pipe etc. can be well approximated by:

                (0.394) * (r**2) * (N**2)
Inductance L = _________________________
              	( 9 * r ) + ( 10 * Len)
Here:
	N = Number of Turns 
	r = radius of the coil i.e. form diameter (in cm.) divided by 2
	Len = length of the coil - again in cm.
	L = inductance in uH.
	* = multiply by
	math.pi**2==0.394
						''',
						'exec':air_coil
					},
					f'{uuid1()}':{
						'cmds':['circumference of a circle using diameter',],
						'desc':f'C=2πr',
						'exec':circumference_diameter
					},
					f'{uuid1()}':{
						'cmds':['circumference of a circle using radius',],
						'desc':f'C=2πr',
						'exec':circumference_radius
					},
					f'{uuid1()}':{
						'cmds':['area of a circle using diameter',],
						'desc':f'A = πr²',
						'exec':area_of_circle_diameter
					},
					f'{uuid1()}':{
						'cmds':['area of a circle using radius',],
						'desc':f'A = πr²',
						'exec':area_of_circle_radius
					},
					f'{uuid1()}':{
						'cmds':['get capacitance for desired frequency with specific inductance',],
						'desc':f'C = 1 / (4π²f²L)²',
						'exec':air_coil_cap,
					},
					f'{uuid1()}':{
						'cmds':['get resonant frequency for lc circuit',],
						'desc':f'f = 1 / (2π√(LC))',
						'exec':lc_frequency,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['area','a'])],
						'desc':f'A=BH/2 = area of a triangle',
						'exec':area_triangle,
					},
					f'{uuid1()}':{
						'cmds':['taxable kombucha',],
						'desc':f'is kombucha taxable?[taxable=True,non-taxable=False]',
						'exec':lambda: Taxable.kombucha(None),
					},
					f'{uuid1()}':{
						'cmds':['taxable item',],
						'desc':f'is item taxable?[taxable=True,non-taxable=False]',
						'exec':lambda: Taxable.general_taxable(None),
					},
					f'{uuid1()}':{
						'cmds':['price * rate = tax',],
						'desc':f'multiply a price times its tax rate ; {Fore.orange_red_1}Add this value to the price for the {Fore.light_steel_blue}Total{Style.reset}',
						'exec':lambda: price_by_tax(total=False),
					},
					f'{uuid1()}':{
						'cmds':['( price + crv ) * rate = tax',],
						'desc':f'multiply a (price+crv) times its tax rate ; {Fore.orange_red_1}Add this value to the price for the {Fore.light_steel_blue}Total{Style.reset}',
						'exec':lambda: price_plus_crv_by_tax(total=False),
					},
					f'{uuid1()}':{
						'cmds':['(price * rate) + price = total',],
						'desc':f'multiply a price times its tax rate + price return the total',
						'exec':lambda: price_by_tax(total=True),
					},
					f'{uuid1()}':{
						'cmds':['( price + crv ) + (( price + crv ) * rate) = total',],
						'desc':f'multiply a (price+crv) times its tax rate plus (price+crv) and return the total',
						'exec':lambda: price_plus_crv_by_tax(total=True),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cylinder','clndr'],endCmd=['vol rad','volume radius'])],
						'desc':f'obtain the volume of a cylinder using radius',
						'exec':lambda: volumeCylinderRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cylinder','clndr'],endCmd=['vol diam','volume diameter'])],
						'desc':f'obtain the volume of a cylinder using diameter',
						'exec':lambda: volumeCylinderDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cone',],endCmd=['vol rad','volume radius'])],
						'desc':f'obtain the volume of a cone using radius, a cone is 1/3 of a cylinder at the same height and radius',
						'exec':lambda: volumeConeRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cone',],endCmd=['vol diam','volume diameter'])],
						'desc':f'obtain the volume of a cone using diameter, a code is 1/3 of a cylinder at the same height and diameter',
						'exec':lambda: volumeConeDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['hemisphr','hemisphere'],endCmd=['vol rad','volume radius'])],
						'desc':f'obtain the volume of a hemisphere using radius',
						'exec':lambda: volumeHemisphereRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['hemisphr','hemisphere'],endCmd=['vol diam','volume diameter'])],
						'desc':f'obtain the volume of a hemisphere using diameter',
						'exec':lambda: volumeHemisphereDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['circle',],endCmd=['area radius','area rad'])],
						'desc':f'obtain the area of a circle using radius',
						'exec':lambda: areaCircleRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['circle',],endCmd=['area diameter','area diam'])],
						'desc':f'obtain the area of a circle using diameter',
						'exec':lambda: areaCircleDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['sudoku',],endCmd=['candidates','cd'])],
						'desc':f'obtain candidates for sudoku cell',
						'exec':lambda: sudokuCandidates(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['sudoku',],endCmd=['candidates auto','cda'])],
						'desc':f'obtain candidates for sudoku cell for the whole grid',
						'exec':lambda: candidates(),
					},
					f'{uuid1()}':{
						'cmds':['herons formula','hrns fmla'],
						'desc':f'''
Heron's formula calculates the area of any 
triangle given only the lengths of its 
three sides (a, b, and c). The formula is: 
Area = √(s(s-a)(s-b)(s-c)). To use it, first
 calculate the semi-perimeter, s = (a + b 
 + c) / 2, and then substitute this value 
 and the side lengths into the formula to 
 find the area. 
						''',
						'exec':lambda: heronsFormula(),
					},
					f'{uuid1()}':{
						'cmds':['tax add',],
						'desc':'''AddNewTaxRate() -> None

add a new taxrate to db.''',
						'exec':lambda: AddNewTaxRate(),
					},
					f'{uuid1()}':{
						'cmds':['tax get',],
						'desc':	'''GetTaxRate() -> TaxRate:Decimal

search for and return a Decimal/decc
taxrate for use by prompt.
''',
						'exec':lambda: GetTaxRate(),
					},
					f'{uuid1()}':{
						'cmds':['tax delete',],
						'desc':'''DeleteTaxRate() -> None

search for and delete selected
taxrate.
''',
						'exec':lambda: DeleteTaxRate(),
					},
					f'{uuid1()}':{
						'cmds':['tax edit',],
						'desc':'''EditTaxRate() -> None

search for and edit selected
taxrate.
''',
						'exec':lambda: EditTaxRate(),
					},
}
