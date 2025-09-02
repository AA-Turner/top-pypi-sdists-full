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
unit_registry=pint.UnitRegistry()
def area_triangle():
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
		