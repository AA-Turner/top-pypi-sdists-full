from . import *

def volume():
	height=Prompt.__init2__(None,func=FormBuilderMkText,ptext="height?: ",helpText="height=1",data="dec.dec")
	if height is None:
		return
	elif height in ['d',]:
		height=Decimal('1')
	
	width=Prompt.__init2__(None,func=FormBuilderMkText,ptext="width?: ",helpText="width=1 ",data="dec.dec")
	if width is None:
		return
	elif width in ['d',]:
		width=Decimal('1')
	


	length=Prompt.__init2__(None,func=FormBuilderMkText,ptext="length?: ",helpText="length=1",data="dec.dec")
	if length is None:
		return
	elif length in ['d',]:
		length=Decimal('1')

	return length*width*height

def volume_pint():
	height=Prompt.__init2__(None,func=FormBuilderMkText,ptext="height?: ",helpText="height=1",data="string")
	if height is None:
		return
	elif height in ['d',]:
		height='1'
	
	width=Prompt.__init2__(None,func=FormBuilderMkText,ptext="width?: ",helpText="width=1 ",data="string")
	if width is None:
		return
	elif width in ['d',]:
		width='1'
	


	length=Prompt.__init2__(None,func=FormBuilderMkText,ptext="length?: ",helpText="length=1",data="string")
	if length is None:
		return
	elif length in ['d',]:
		length='1'

	return unit_registry.Quantity(length)*unit_registry.Quantity(width)*unit_registry.Quantity(height)

def inductance_pint():
	relative_permeability=Prompt.__init2__(None,func=FormBuilderMkText,ptext="relative_permeability?: ",helpText="relative_permeability(air)=1",data="string")
	if relative_permeability is None:
		return
	elif relative_permeability in ['d',]:
		relative_permeability='1'
	relative_permeability=float(relative_permeability)

	turns_of_wire_on_coil=Prompt.__init2__(None,func=FormBuilderMkText,ptext="turns_of_wire_on_coil?: ",helpText="turns_of_wire_on_coil=1",data="string")
	if turns_of_wire_on_coil is None:
		return
	elif turns_of_wire_on_coil in ['d',]:
		turns_of_wire_on_coil='1'
	turns_of_wire_on_coil=int(turns_of_wire_on_coil)

	#convert to meters
	core_cross_sectional_area_meters=Prompt.__init2__(None,func=FormBuilderMkText,ptext="core_cross_sectional_area_meters?: ",helpText="core_cross_sectional_area_meters=1",data="string")
	if core_cross_sectional_area_meters is None:
		return
	elif core_cross_sectional_area_meters in ['d',]:
		core_cross_sectional_area_meters='1m'
	try:
		core_cross_sectional_area_meters=unit_registry.Quantity(core_cross_sectional_area_meters).to("meters")
	except Exception as e:
		print(e,"defaulting to meters")
		core_cross_sectional_area_meters=unit_registry.Quantity(f"{core_cross_sectional_area_meters} meters")

	length_of_coil_meters=Prompt.__init2__(None,func=FormBuilderMkText,ptext="length_of_coil_meters?: ",helpText="length_of_coil_meters=1",data="string")
	if length_of_coil_meters is None:
		return
	elif length_of_coil_meters in ['d',]:
		length_of_coil_meters='1m'
	try:
		length_of_coil_meters=unit_registry.Quantity(length_of_coil_meters).to('meters')
	except Exception as e:
		print(e,"defaulting to meters")
		length_of_coil_meters=unit_registry.Quantity(f"{length_of_coil_meters} meters")
	
	numerator=((turns_of_wire_on_coil**2)*core_cross_sectional_area_meters)
	f=relative_permeability*(numerator/length_of_coil_meters)*1.26e-6
	f=unit_registry.Quantity(f"{f.magnitude} H")
	return f

def resonant_inductance():
	hertz=1e9
	while True:
		try:
			hertz=Control(func=FormBuilderMkText,ptext="frequency in hertz[530 kilohertz]? ",helpText="frequency in hertz",data="string")
			if hertz is None:
				return
			elif hertz in ['d','']:
				hertz="530 megahertz"
			print(hertz)
			x=unit_registry.Quantity(hertz)
			if x:
				hertz=x.to("hertz")
			else:
				hertz=1e6
			break
		except Exception as e:
			print(e)

	
	while True:
		try:
			capacitance=Control(func=FormBuilderMkText,ptext="capacitance[365 picofarads]? ",helpText="capacitance in farads",data="string")
			if capacitance is None:
				return
			elif capacitance in ['d',]:
				capacitance="365 picofarads"
			x=unit_registry.Quantity(capacitance)
			if x:
				x=x.to("farads")
			farads=x.magnitude
			break
		except Exception as e:
			print(e)

	inductance=1/(decc(4*math.pi**2)*decc(hertz.magnitude**2,cf=13)*decc(farads,cf=13))

	L=unit_registry.Quantity(inductance,"henry")
	return L

def air_coil_cap():
	'''C = 1 / (4π²f²L)'''
	while True:
		try:
			frequency=Control(func=FormBuilderMkText,ptext="frequency? ",helpText="frequency",data="string")
			if frequency is None:
				return
			elif frequency in ['d',]:
				frequency="1410 kilohertz"
			x=unit_registry.Quantity(frequency)
			if x:
				x=x.to("hertz")
			frequency=decc(x.magnitude**2)
			break
		except Exception as e:
			print(e)
	
	while True:
		try:
			inductance=Control(func=FormBuilderMkText,ptext="inductance(356 microhenry): ",helpText="coil inductance",data="string")
			if inductance is None:
				return
			elif inductance in ['d',]:
				inductance="356 microhenry"
			x=unit_registry.Quantity(inductance)
			if x:
				x=x.to("henry")
			inductance=decc(x.magnitude,cf=20)
			break
		except Exception as e:
			print(e)
	

	
	farads=1/(inductance*frequency*decc(4*math.pi**2))
	return unit_registry.Quantity(farads,"farad")

def air_coil():
	'''
	The formula for inductance - using toilet rolls, PVC pipe etc. can be well approximated by:


	                  0.394 * r2 * N2
	Inductance L = ________________
	                 ( 9 *r ) + ( 10 * Len)
	Here:
	N = number of turns
	r = radius of the coil i.e. form diameter (in cm.) divided by 2
	Len = length of the coil - again in cm.
	L = inductance in uH.
	* = multiply by
	'''
	while True:
		try:
			diameter=Control(func=FormBuilderMkText,ptext="diameter in cm [2 cm]? ",helpText="diamater of coil",data="string")
			if diameter is None:
				return
			elif diameter in ['d',]:
				diameter="2 cm"
			x=unit_registry.Quantity(diameter)
			if x:
				x=x.to("centimeter")
			diameter=x.magnitude
			break
		except Exception as e:
			print(e)
	radius=decc(diameter/2)
	while True:
		try:
			length=Control(func=FormBuilderMkText,ptext="length in cm [2 cm]? ",helpText="length of coil",data="string")
			if length is None:
				return
			elif length in ['d',]:
				length="2 cm"
			x=unit_registry.Quantity(length)
			if x:
				x=x.to("centimeter")
			length=x.magnitude
			break
		except Exception as e:
			print(e)
	while True:
		try:
			turns=Control(func=FormBuilderMkText,ptext="number of turns? ",helpText="turns of wire",data="integer")
			if turns is None:
				return
			elif turns in ['d',]:
				turns=1
			LTop=decc(0.394)*decc(radius**2)*decc(turns**2)
			LBottom=(decc(9)*radius)+decc(length*10)
			L=LTop/LBottom
			print(pint.Quantity(L,'microhenry'))
			different_turns=Control(func=FormBuilderMkText,ptext="use a different number of turns?",helpText="yes or no",data="boolean")
			if different_turns is None:
				return
			elif different_turns in ['d',True]:
				continue
			break
		except Exception as e:
			print(e)

	
	return pint.Quantity(L,'microhenry')

def circumference_diameter():
	radius=0
	while True:
		try:
			diameter=Control(func=FormBuilderMkText,ptext="diameter unit[4 cm]? ",helpText="diamater with unit",data="string")
			if diameter is None:
				return
			elif diameter in ['d',]:
				diameter="4 cm"
			x=unit_registry.Quantity(diameter)
			radius=pint.Quantity(decc(x.magnitude/2),x.units)
			break
		except Exception as e:
			print(e)
	if isinstance(radius,pint.registry.Quantity):
		result=decc(2*math.pi)*decc(radius.magnitude)

		return pint.Quantity(result,radius.units)
	else:
		return

def circumference_radius():
	radius=0
	while True:
		try:
			diameter=Control(func=FormBuilderMkText,ptext="radius unit[2 cm]? ",helpText="radius with unit",data="string")
			if diameter is None:
				return
			elif diameter in ['d',]:
				diameter="2 cm"
			x=unit_registry.Quantity(diameter)
			radius=pint.Quantity(decc(x.magnitude),x.units)
			break
		except Exception as e:
			print(e)
	if isinstance(radius,pint.registry.Quantity):
		result=decc(2*math.pi)*decc(radius.magnitude)

		return pint.Quantity(result,radius.units)
	else:
		return

def area_of_circle_radius():
	'''
A = πr²
	'''
	radius=0
	while True:
		try:
			diameter=Control(func=FormBuilderMkText,ptext="radius unit[2 cm]? ",helpText="radius with unit",data="string")
			if diameter is None:
				return
			elif diameter in ['d',]:
				diameter="2 cm"
			x=unit_registry.Quantity(diameter)
			radius=pint.Quantity(decc(x.magnitude),x.units)
			break
		except Exception as e:
			print(e)
	if isinstance(radius,pint.registry.Quantity):
		result=decc(math.pi)*decc(radius.magnitude**2)

		return pint.Quantity(result,radius.units)
	else:
		return

def lc_frequency():
	inductance=None
	capacitance=None
	while True:
		try:
			inductance=Control(func=FormBuilderMkText,ptext="inductance(356 microhenry): ",helpText="coil inductance",data="string")
			if inductance is None:
				return
			elif inductance in ['d',]:
				inductance="356 microhenry"
			x=unit_registry.Quantity(inductance)
			if x:
				x=x.to("henry")
			inductance=decc(x.magnitude,cf=20)
			break
		except Exception as e:
			print(e)
	while True:
		try:
			capacitance=Control(func=FormBuilderMkText,ptext="capacitance[365 picofarads]? ",helpText="capacitance in farads",data="string")
			if capacitance is None:
				return
			elif capacitance in ['d',]:
				capacitance="365 picofarads"
			x=unit_registry.Quantity(capacitance)
			if x:
				x=x.to("farads")
			farads=decc(x.magnitude,cf=20)
			break
		except Exception as e:
			print(e)
	frequency=1/(decc(2*math.pi)*decc(math.sqrt(farads*inductance),cf=20))
	return unit_registry.Quantity(frequency,"hertz")





def area_of_circle_diameter():
	'''
A = πr²
	'''
	radius=0
	while True:
		try:
			diameter=Control(func=FormBuilderMkText,ptext="diameter unit[4 cm]? ",helpText="diamater value with unit",data="string")
			if diameter is None:
				return
			elif diameter in ['d',]:
				diameter="4 cm"
			x=unit_registry.Quantity(diameter)
			radius=pint.Quantity(decc(x.magnitude/2),x.units)
			break
		except Exception as e:
			print(e)
	if isinstance(radius,pint.registry.Quantity):
		result=decc(math.pi)*decc(radius.magnitude**2)

		return pint.Quantity(result,radius.units)
	else:
		return


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
						'cmds':['area of a triangle',],
						'desc':f'A=BH/2',
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
}
