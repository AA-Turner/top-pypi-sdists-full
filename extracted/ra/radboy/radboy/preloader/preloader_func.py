from radboy.DB.db import *
from radboy.DB.RandomStringUtil import *
import radboy.Unified.Unified as unified
import radboy.possibleCode as pc
from radboy.DB.Prompt import *
from radboy.DB.Prompt import prefix_text
from radboy.TasksMode.ReFormula import *
from radboy.TasksMode.SetEntryNEU import *
from radboy.FB.FormBuilder import *
from radboy.FB.FBMTXT import *
from radboy.RNE.RNE import *
from radboy.Lookup2.Lookup2 import Lookup as Lookup2
from radboy.DayLog.DayLogger import *
from radboy.DB.masterLookup import *
from collections import namedtuple,OrderedDict
import nanoid,qrcode,io
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar,hashlib,haversine
from time import sleep
import itertools
import decimal
from decimal import localcontext,Decimal
unit_registry=pint.UnitRegistry()
import math

def volume():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		#print(f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow}")
		height=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} height?: ",helpText="height=1",data="dec.dec")
		if height is None:
			return
		elif height in ['d',]:
			height=Decimal('1')
		
		width=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} width?: ",helpText="width=1 ",data="dec.dec")
		if width is None:
			return
		elif width in ['d',]:
			width=Decimal('1')
	


		length=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} length?: ",helpText="length=1",data="dec.dec")
		if length is None:
			return
		elif length in ['d',]:
			length=Decimal('1')

		return length*width*height

def volume_pint():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		height=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} height?: ",helpText="height=1",data="string")
		if height is None:
			return
		elif height in ['d',]:
			height='1'
		
		width=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} width?: ",helpText="width=1 ",data="string")
		if width is None:
			return
		elif width in ['d',]:
			width='1'
		


		length=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} length?: ",helpText="length=1",data="string")
		if length is None:
			return
		elif length in ['d',]:
			length='1'

		return unit_registry.Quantity(length)*unit_registry.Quantity(width)*unit_registry.Quantity(height)

def inductance_pint():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		relative_permeability=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} relative_permeability?: ",helpText="relative_permeability(air)=1",data="string")
		if relative_permeability is None:
			return
		elif relative_permeability in ['d',]:
			relative_permeability='1'
		relative_permeability=float(relative_permeability)

		turns_of_wire_on_coil=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} turns_of_wire_on_coil?: ",helpText="turns_of_wire_on_coil=1",data="string")
		if turns_of_wire_on_coil is None:
			return
		elif turns_of_wire_on_coil in ['d',]:
			turns_of_wire_on_coil='1'
		turns_of_wire_on_coil=int(turns_of_wire_on_coil)

		#convert to meters
		core_cross_sectional_area_meters=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} core_cross_sectional_area_meters?: ",helpText="core_cross_sectional_area_meters=1",data="string")
		if core_cross_sectional_area_meters is None:
			return
		elif core_cross_sectional_area_meters in ['d',]:
			core_cross_sectional_area_meters='1m'
		try:
			core_cross_sectional_area_meters=unit_registry.Quantity(core_cross_sectional_area_meters).to("meters")
		except Exception as e:
			print(e,"defaulting to meters")
			core_cross_sectional_area_meters=unit_registry.Quantity(f"{core_cross_sectional_area_meters} meters")

		length_of_coil_meters=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} length_of_coil_meters?: ",helpText="length_of_coil_meters=1",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		hertz=1e9
		while True:
			try:
				hertz=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} frequency in hertz[530 kilohertz]? ",helpText="frequency in hertz",data="string")
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
				capacitance=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} capacitance[365 picofarads]? ",helpText="capacitance in farads",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''C = 1 / (4π²f²L)'''
		while True:
			try:
				frequency=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} frequency? ",helpText="frequency",data="string")
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
				inductance=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} inductance(356 microhenry): ",helpText="coil inductance",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
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
				diameter=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} diameter in cm [2 cm]? ",helpText="diamater of coil",data="string")
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
				length=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} length in cm [2 cm]? ",helpText="length of coil",data="string")
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
				turns=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} number of turns? ",helpText="turns of wire",data="integer")
				if turns is None:
					return
				elif turns in ['d',]:
					turns=1
				LTop=decc(0.394)*decc(radius**2)*decc(turns**2)
				LBottom=(decc(9)*radius)+decc(length*10)
				L=LTop/LBottom
				print(pint.Quantity(L,'microhenry'))
				different_turns=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} use a different number of turns?",helpText="yes or no",data="boolean")
				if different_turns is None:
					return
				elif different_turns in ['d',True]:
					continue
				break
			except Exception as e:
				print(e)

		
		return pint.Quantity(L,'microhenry')

def circumference_diameter():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		radius=0
		while True:
			try:
				diameter=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} diameter unit[4 cm]? ",helpText="diamater with unit",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		radius=0
		while True:
			try:
				diameter=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} radius unit[2 cm]? ",helpText="radius with unit",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
	A = πr²
		'''
		radius=0
		while True:
			try:
				diameter=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} radius unit[2 cm]? ",helpText="radius with unit",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		inductance=None
		capacitance=None
		while True:
			try:
				inductance=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} inductance(356 microhenry): ",helpText="coil inductance",data="string")
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
				capacitance=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} capacitance[365 picofarads]? ",helpText="capacitance in farads",data="string")
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
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
	A = πr²
		'''
		radius=0
		while True:
			try:
				diameter=Control(func=FormBuilderMkText,ptext=f"{Fore.light_green}Precision {ctx.prec}{Fore.light_yellow} diameter unit[4 cm]? ",helpText="diamater value with unit",data="string")
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


def area_triangle():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		height=None
		base=None
		'''
		A=hbb/2
		'''
		while True:
			try:
				base=Control(func=FormBuilderMkText,ptext="base",helpText="base width",data="string")
				if base is None:
					return
				elif base in ['d',]:
					base=unit_registry.Quantity('1')
				else:
					base=unit_registry.Quantity(base)
				break
			except Exception as e:
				print(e)
				try:
					base=Control(func=FormBuilderMkText,ptext="base no units",helpText="base width,do not include units",data="dec.dec")
					if base is None:
						return
					elif base in ['d',]:
						base=decc(1)
					break
				except Exception as e:
					continue

		while True:
			try:
				height=Control(func=FormBuilderMkText,ptext="height",helpText="height width",data="string")
				if height is None:
					return
				elif height in ['d',]:
					height=unit_registry.Quantity('1')
				else:
					height=unit_registry.Quantity(height)
				break
			except Exception as e:
				print(e)
				try:
					height=Control(func=FormBuilderMkText,ptext="height no units",helpText="height width, do not include units",data="dec.dec")
					if height is None:
						return
					elif height in ['d',]:
						height=decc(1)
					break
				except Exception as e:
					continue
		print(type(height),height,type(base))
		if isinstance(height,decimal.Decimal) and isinstance(base,decimal.Decimal):
			return decc((height*base)/decc(2))
		elif isinstance(height,pint.Quantity) and isinstance(base,pint.Quantity):
			return ((height.to(base)*base)/2)
		elif isinstance(height,pint.Quantity) and isinstance(base,decimal.Decimal):
			return ((height*unit_registry.Quantity(base,height.units))/2)
		elif isinstance(height,decimal.Decimal) and isinstance(base,pint.Quantity):
			return ((unit_registry.Quantity(height,base.units)*base)/2)

class Taxable:
	def general_taxable(self):
		taxables=[
"Alcoholic beverages",
"Books and publications",
"Cameras and film",
"Carbonated and effervescent water",
"Carbonated soft drinks and mixes",
"Clothing",
"Cosmetics",
"Dietary supplements",
"Drug sundries, toys, hardware, and household goods",
"Fixtures and equipment used in an activity requiring the holding of a seller’s permit, if sold at retail",
"Food sold for consumption on your premises (see Food service operations)",
"Hot prepared food products (see Hot prepared food products)",
"Ice",
"Kombucha tea (if alcohol content is 0.5 percent or greater by volume)",
"Medicated gum (for example, Nicorette and Aspergum)",
"Newspapers and periodicals",
"Nursery stock",
"Over-the-counter medicines (such as aspirin, cough syrup, cough drops, and throat lozenges)",
"Pet food and supplies",
"Soaps or detergents",
"Sporting goods",
"Tobacco products",
		]
		nontaxables=[
"Baby formulas (such as Isomil)",
"Cooking wine",
"Energy bars (such as PowerBars)",
"""Food products—This includes baby food, artificial sweeteners, candy, gum, ice cream, ice cream novelties,
popsicles, fruit and vegetable juices, olives, onions, and maraschino cherries. Food products also include
beverages and cocktail mixes that are neither alcoholic nor carbonated. The exemption applies whether sold in
liquid or frozen form.""",
"Granola bars",
"Kombucha tea (if less than 0.5 percent alcohol by volume and naturally effervescent)",
"Sparkling cider",
"Noncarbonated sports drinks (including Gatorade, Powerade, and All Sport)",
"Pedialyte",
"Telephone cards (see Prepaid telephone debit cards and prepaid wireless cards)",
"Water—Bottled noncarbonated, non-effervescent drinking water",
		]

		taxables_2=[
"Alcoholic beverages",
'''Carbonated beverages, including semi-frozen beverages
containing carbonation, such as slushies (see Carbonated fruit
juices)''',
"Coloring extracts",
"Dietary supplements",
"Ice",
"Over-the-counter medicines",
"Tobacco products",
"non-human food",
"Kombucha tea (if >= 0.5% alcohol by volume and/or is not naturally effervescent)",
		]
		for i in taxables_2:
			if i not in taxables:
				taxables.append(i)

		ttl=[]
		for i in taxables:
			ttl.append(i)
		for i in nontaxables:
			ttl.append(i)
		htext=[]
		cta=len(ttl)
		ttl=sorted(ttl,key=str)
		for num,i in enumerate(ttl):
			htext.append(std_colorize(i,num,cta))
		htext='\n'.join(htext)
		while True:
			print(htext)
			select=Control(func=FormBuilderMkText,ptext="Please select all indexes that apply to item?",helpText=htext,data="list")
			if select is None:
				return
			for i in select:
				try:
					index=int(i)
					if ttl[index] in taxables:
						return True
				except Exception as e:
					print(e)
			return False
	def kombucha(self):
		'''determine if kombucha is taxable'''
		fd={
			'Exceeds 0.5% ABV':{
			'default':False,
			'type':'boolean',
			},
			'Is it Naturally Effervescent?':{
			'default':False,
			'type':'boolean',
			},

		}
		data=FormBuilder(data=fd)
		if data is None:
			return
		else:
			if data['Exceeds 0.5% ABV']:
				return True

			if not data['Is it Naturally Effervescent?']:
				return True

			return False
		
#tax rate tools go here
def AddNewTaxRate(excludes=['txrt_id','DTOE']):
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		with Session(ENGINE) as session:
			'''AddNewTaxRate() -> None

			add a new taxrate to db.'''
			tr=TaxRate()
			session.add(tr)
			session.commit()
			session.refresh(tr)
			fields={i.name:{
			'default':getattr(tr,i.name),
			'type':str(i.type).lower()} for i in tr.__table__.columns if i.name not in excludes
			}

			fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
			if fd is None:
				session.delete(tr)
				return
			for k in fd:
				setattr(tr,k,fd[k])

		
			session.add(tr)
			session.commit()
			session.refresh(tr)
		print(tr)
		return tr.TaxRate

def GetTaxRate(excludes=['txrt_id','DTOE']):
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		with Session(ENGINE) as session:
			'''GetTaxRate() -> TaxRate:Decimal

			search for and return a Decimal/decc
			taxrate for use by prompt.
			'''
			tr=TaxRate()
			fields={i.name:{
			'default':getattr(tr,i.name),
			'type':str(i.type).lower()} for i in tr.__table__.columns if i.name not in excludes
			}

			fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec} ; GetTaxRate Search -> ")
			if fd is None:
				return
			for k in fd:
				setattr(tr,k,fd[k])
			#and_
			filte=[]
			for k in fd:
				if fd[k] is not None:
					if isinstance(fd[k],str):
						filte.append(getattr(TaxRate,k).icontains(fd[k]))
					else:
						filte.append(getattr(tr,k)==fd[k])
		
			results=session.query(TaxRate).filter(and_(*filte)).all()
			ct=len(results)
			htext=[]
			for num,i in enumerate(results):
				m=std_colorize(i,num,ct)
				print(m)
				htext.append(m)
			htext='\n'.join(htext)
			if ct < 1:
				print(f"{Fore.light_red}There is nothing to work on in TaxRates that match your criteria.{Style.reset}")
				return
			while True:
				select=Control(func=FormBuilderMkText,ptext="Which index to return for tax rate[NAN=0.0000]?",helpText=htext,data="integer")
				print(select)
				if select is None:
					return
				elif isinstance(select,str) and select.upper() in ['NAN',]:
					return 0
				elif select in ['d',]:
					return results[0].TaxRate
				else:
					if index_inList(select,results):
						return results[select].TaxRate
					else:
						continue

def price_by_tax(total=False):
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		fields={
		'price':{
			'default':0,
			'type':'dec.dec'
			},
		'rate':{
			'default':GetTaxRate(),
			'type':'dec.dec'
			}
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec} ; Tax on Price ->")
		if fd is None:
			return
		else:
			price=fd['price']
			rate=fd['rate']
			if price is None:
				price=0
			if fd['rate'] is None:
				rate=0
			if total == False:
				return decc(price,cf=4)*decc(rate,cf=4)
			else:
				return (decc(price,cf=4)*decc(rate,cf=4))+decc(price,cf=4)

def price_plus_crv_by_tax(total=False):
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		fields={
		'price':{
			'default':0,
			'type':'dec.dec'
			},
		'crv_total_for_pkg':{
			'default':0,
			'type':'dec.dec',
		},
		'rate':{
			'default':GetTaxRate(),
			'type':'dec.dec'
			}
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec};Tax on (Price+CRV)")
		if fd is None:
			return
		else:
			price=fd['price']
			rate=fd['rate']
			crv=fd['crv_total_for_pkg']
			if price is None:
				price=0
			if crv is None:
				crv=0
			if fd['rate'] is None:
				rate=0
			if total == False:
				return (decc(price,cf=4)+decc(crv,cf=4))*decc(rate,cf=4)
			else:
				return (price+crv)+((decc(price,cf=4)+decc(crv,cf=4))*decc(rate,cf=4))

def DeleteTaxRate(excludes=['txrt_id','DTOE']):
	with Session(ENGINE) as session:
		'''DeleteTaxRate() -> None

		search for and delete selected
		taxrate.
		'''
		'''AddNewTaxRate() -> None

		add a new taxrate to db.'''
		tr=TaxRate()
		fields={i.name:{
		'default':getattr(tr,i.name),
		'type':str(i.type).lower()} for i in tr.__table__.columns if i.name not in excludes
		}
		fd=FormBuilder(data=fields)
		if fd is None:
			return
		for k in fd:
			setattr(tr,k,fd[k])
		#and_
		filte=[]
		for k in fd:
			if fd[k] is not None:
				if isinstance(fd[k],str):
					filte.append(getattr(TaxRate,k).icontains(fd[k]))
				else:
					filte.append(getattr(tr,k)==fd[k])
		session.commit()
	
		results=session.query(TaxRate).filter(and_(*filte)).all()
		ct=len(results)
		htext=[]
		for num,i in enumerate(results):
			m=std_colorize(i,num,ct)
			print(m)
			htext.append(m)
		htext='\n'.join(htext)
		if ct < 1:
			print(f"{Fore.light_red}There is nothing to work on in TaxRates that match your criteria.{Style.reset}")
			return
		while True:
			select=Control(func=FormBuilderMkText,ptext="Which index to delete?",helpText=htext,data="integer")
			print(select)
			if select is None:
				print(f"{Fore.light_yellow}Nothing was deleted!{Style.reset}")
				return
			elif isinstance(select,str) and select.upper() in ['NAN',]:
				print(f"{Fore.light_yellow}Nothing was deleted!{Style.reset}")
				return 0
			elif select in ['d',]:
				print(f"{Fore.light_yellow}Nothing was deleted!{Style.reset}")
				return
			else:
				if index_inList(select,results):
					session.delete(results[select])
					session.commit()
					return
				else:
					continue

def EditTaxRate(excludes=['txrt_id','DTOE']):
	'''DeleteTaxRate() -> None

	search for and delete selected
	taxrate.
	'''
	tr=TaxRate()
	fields={i.name:{
	'default':getattr(tr,i.name),
	'type':str(i.type).lower()} for i in tr.__table__.columns if i.name not in excludes
	}
	fd=FormBuilder(data=fields)
	if fd is None:
		return
	for k in fd:
		setattr(tr,k,fd[k])
	#and_
	filte=[]
	for k in fd:
		if fd[k] is not None:
			if isinstance(fd[k],str):
				filte.append(getattr(TaxRate,k).icontains(fd[k]))
			else:
				filte.append(getattr(tr,k)==fd[k])
	with Session(ENGINE) as session:
		results=session.query(TaxRate).filter(and_(*filte)).all()
		ct=len(results)
		htext=[]
		for num,i in enumerate(results):
			m=std_colorize(i,num,ct)
			print(m)
			htext.append(m)
		htext='\n'.join(htext)
		if ct < 1:
			print(f"{Fore.light_red}There is nothing to work on in TaxRates that match your criteria.{Style.reset}")
			return
		while True:
			select=Control(func=FormBuilderMkText,ptext="Which index to edit?",helpText=htext,data="integer")
			print(select)
			if select is None:
				print(f"{Fore.light_yellow}Nothing was deleted!{Style.reset}")
				return
			elif isinstance(select,str) and select.upper() in ['NAN',]:
				print(f"{Fore.light_yellow}Nothing was deleted!{Style.reset}")
				return 0
			elif select in ['d',]:
				print(f"{Fore.light_yellow}Nothing was deleted!{Style.reset}")
				return
			else:
				if index_inList(select,results):
					fields={i.name:{
					'default':getattr(results[select],i.name),
					'type':str(i.type).lower()} for i in results[select].__table__.columns if i.name not in excludes
					}
					fd=FormBuilder(data=fields)
					for k in fd:
						setattr(results[select],k,fd[k])
					session.commit()
					session.refresh(results[select])
					print(results[select])
					return
				else:
					continue

def heronsFormula():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Calculate the semi-perimeter (s): Add the lengths of the three sides and divide by 2.
		s = (a + b + c) / 2
		'''
		fields={
			'side 1':{
			'default':1,
			'type':'dec.dec'
			},
			'side 2':{
			'default':1,
			'type':'dec.dec'
			},
			'side 3':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		s=(fd['side 1']+fd['side 2']+fd['side 3'])/2
		'''Apply Heron's formula: Substitute the semi-perimeter (s) and the side lengths (a, b, and c) into the formula:
		Area = √(s(s-a)(s-b)(s-c))'''
		Area=math.sqrt(s*(s-fd['side 1'])*(s-fd['side 2'])*(s-fd['side 3']))
		return Area

def volumeCylinderRadius():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a cylinder: Used for cylindrical storage bins, silos, or tanks.(V=pi r^{2}h)
		'''
		fields={
			'height':{
			'default':1,
			'type':'dec.dec'
			},
			'radius':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(math.pi)*(fd['radius']**2)*fd['height']
		return volume

def volumeCylinderDiameter():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a cylinder: Used for cylindrical storage bins, silos, or tanks.(V=pi r^{2}h)
		'''
		fields={
			'height':{
			'default':1,
			'type':'dec.dec'
			},
			'diameter':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(math.pi)*((fd['diameter']/2)**2)*fd['height']
		return volume

def volumeConeRadius():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a cylinder: Used for cylindrical storage bins, silos, or tanks.(V=pi r^{2}h)
		'''
		fields={
			'height':{
			'default':1,
			'type':'dec.dec'
			},
			'radius':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(1/3)*(Decimal(math.pi)*(fd['radius']**2)*fd['height'])
		return volume

def volumeConeDiameter():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a cylinder: Used for cylindrical storage bins, silos, or tanks.(V=pi r^{2}h)
		'''
		fields={
			'height':{
			'default':1,
			'type':'dec.dec'
			},
			'diameter':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(1/3)*(Decimal(math.pi)*((fd['diameter']/2)**2)*fd['height'])
		return volume

def volumeHemisphereRadius():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a hemisphere = (2/3) x 3.14 x r3
		'''
		fields={
			'radius':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(2/3)*Decimal(math.pi)*(fd['radius']**3)
		return volume

def volumeHemisphereDiameter():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a hemisphere = (2/3) x 3.14 x r3
		'''
		fields={
			'diameter':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(2/3)*Decimal(math.pi)*((fd['diameter']/2)**3)
		return volume

def areaCircleDiameter():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a hemisphere = (2/3) x 3.14 x r3
		'''
		fields={
			'diameter':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(math.pi)*((fd['diameter']/2)**2)
		return volume


def areaCircleRadius():
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		Volume of a hemisphere = (2/3) x 3.14 x r3
		'''
		fields={
			'radius':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		volume=Decimal(math.pi)*((fd['radius'])**2)
		return volume

###newest
def circumferenceCircleRadiu():
	#get the circumference of a circle using radius
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		2πr
		'''
		fields={
			'radius':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		circumference=2*Deimal(math.pi)*fd['radius']
		return circumference

def circumferenceCircleDiameter():
	#get the circumference of a circle using diameter
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		2π(d/2)
		'''
		fields={
			'diameter':{
			'default':1,
			'type':'dec.dec'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Precision {ctx.prec}")
		if fd is None:
			return

		circumference=2*Deimal(math.pi)*Decimal(fd['diameter']/2)
		return circumference

def sudokuCandidates():
	#get the circumference of a circle using diameter
	with localcontext() as ctx:
		ctx.prec=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=True))
		'''
		2π(d/2)
		'''
		fields={
			'Game Symbols':{
				'default':'123456789',
				'type':'string'
				},
			'Symbols for Row':{
			'default':'',
			'type':'string'
			},
			'Symbols for Column':{
			'default':'',
			'type':'string'
			},
			'Symbols for Cell':{
			'default':'',
			'type':'string'
			},
			'Symbols for Right-Diagnal':{
			'default':'',
			'type':'string'
			},
			'Symbols for Left-Diagnal':{
			'default':'',
			'type':'string'
			},
		}
		fd=FormBuilder(data=fields,passThruText=f"Sudoku Candidates? ")
		if fd is None:
			return
		symbols=fd['Game Symbols']
		sString=[]
		for i in fd:
			if i == 'Game Symbols':
				continue
			if isinstance(fd[i],str):
				sString.append(fd[i])
		sString=' '.join(sString)
		cd=[]
		for i in symbols:
			if i not in sString:
				cd.append(i)
		
		return cd
'''
Ellipse: area=πab
, where 2a
 and 2b
 are the lengths of the axes of the ellipse.

Sphere: vol=4πr3/3
, surface area=4πr2
.

Cylinder: vol=πr2h
, lateral area=2πrh
, total surface area=2πrh+2πr2
.


Cone: vol=πr2h/3
, lateral area=πrr2+h2−−−−−−√
, total surface area=πrr2+h2−−−−−−√+πr2
'''