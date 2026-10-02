from radboy.DB.db import *
import radboy.DB.db as db
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
from radboy.HowDoYouDefineMe.CoreEmotions import *
from radboy.DB.glossary_db import *
import plotext as plt
from pint import Quantity
plt.date_form('m/d/y-H:M:S')
import re
import time as TIME
from copy import deepcopy
from sqlalchemy import column,text
import radboy.TasksMode as TM
from datetime import datetime
import calendar
import random
from pyzipcode import ZipCodeDatabase
import string,nanoid
from collections import namedtuple
from copy import deepcopy
import sys

try:
    import pyperclip
except Exception as e:
    print(e)
import gc
from radboy.TasksMode.TasksUR import ureg
QTY=pint.Quantity
def modx(data):
    if data is None:
        return data
    else:
        try:
            return plt.datetime_to_string(data)
        except Exception as e:
            print(e)
            return data

def justValue(data):
    if data is None:
        return data
    print('x',data)
    if ' ' in data:
        x=data.split(' ')[0]
        try:
            return float(x)
        except Exception as e:
            print(e)
            return data
    else:
        return data

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
        gameSymbols=Control(func=FormBuilderMkText,ptext="Game symbols [123456789]",helpText="123456789",data="string")
        if gameSymbols in ['NaN',None,]:
            return
        elif gameSymbols in ['d',]:
            gameSymbols='123456789'

        fields={
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
        loop=True
        while loop:
            fd=FormBuilder(data=fields,passThruText=f"Sudoku Candidates? ")
            if fd is None:
                return
            
            sString=[]
            for i in fd:
                if isinstance(fd[i],str):
                    sString.append(fd[i])
            sString=' '.join(sString)
            cd=[]
            for i in gameSymbols:
                if i not in sString:
                    cd.append(i)
            print(cd)
            loop=Control(func=FormBuilderMkText,ptext="Again?",helpText="yes or no/boolean",data="boolean")
            if loop in ['NaN',None]:
                return
            elif loop in ['d',True]:
                loop=True
            else:
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

class candidates:
    def __new__(self,test=False):
        n=None
        symbols=[i for i in '123456789']
        none_symbol='0'

        if test:
            pzl={
            'l1':[1,n,9,n,n,3,7,n,8],
            'l2':[n,n,4,n,n,n,3,n,2],
            'l3':[3,n,5,n,6,8,1,9,4],
            'l4':[6,n,7,8,1,n,n,n,n],
            'l5':[9,3,1,n,n,n,5,8,n],
            'l6':[n,n,2,3,n,n,6,n,n],
            'l7':[n,n,8,n,n,5,n,3,n],
            'l8':[4,n,3,n,8,6,n,1,n],
            'l9':[n,9,6,n,n,n,n,n,7],
            }


        def mkpuzl():
            while True:
                done={}
                htext=[]
                symbols='123456789'
                ct=len(symbols)
                for num,i in enumerate(symbols):
                    htext.append(std_colorize(i,num,ct))
                    done[f'l{num+1}']={
                        'default':[],
                        'type':'list'
                    }
                finished=FormBuilder(data=done,passThruText=f"enter chars. of {symbols}, use 0 to represent an unfilled cell: Must be 9-Long")
                if finished is None:
                    return None
                else:
                    for i in finished:
                        if len(finished[i]) != 9:
                            continue
                        for num,ii in enumerate(finished[i]):
                            if ii == '0':
                                finished[i][num]=n
                    return finished


                #select a list of 9 symbols for ln#
                #symbol is 0, then symbol is None
                #append list to final list
                #for 9lines of 9elements per 1 line as a dict of 9 keys with 9 lists that are 9 elements long
        if not test:
            pzl=mkpuzl()

        while True:
            #print(pzl)
            if pzl is None:
                return
            mapped={
                'block1=':{
                    'rows':[0,1,2],
                    'columns':[0,1,2]
                },
                'block2':{
                    'rows':[0,1,2],
                    'columns':[3,4,5]
                },
                'block3':{
                    'rows':[0,1,2],
                    'columns':[4,5,6]
                },
                'block4':{
                    'rows':[3,4,5],
                    'columns':[0,1,2]
                },
                'block5':{
                    'rows':[3,4,5],
                    'columns':[3,4,5]
                },
                'block6':{
                    'rows':[3,4,5],
                    'columns':[6,7,8]
                },
                'block7':{
                    'rows':[6,7,8],
                    'columns':[0,1,2]
                },
                'block8':{
                    'rows':[6,7,8],
                    'columns':[3,4,5]
                },
                'block9':{
                    'rows':[6,7,8],
                    'columns':[6,7,8]
                },
            }

            def rx2idx(line,column,x_limit=9,y_limit=9):
                return ((x_limit*line)-(y_limit-column))

            def desired(block_x=[1,4],block_y=[1,4],num=''): 
                iblock_x=block_x
                iblock_x[-1]+=1

                iblock_y=block_y
                iblock_y[-1]+=1
                for i in range(*iblock_x):
                    for x in range(*iblock_y):
                        #print(f'block{num}',rx2idx(i,x))
                        yield rx2idx(i,x)
                        
            rgrid=[
            [[1,3],[1,3]],[[1,3],[4,6]],[[1,3],[7,9]],
            [[4,6],[1,3]],[[4,6],[4,6]],[[4,6],[7,9]],
            [[7,9],[1,3]],[[7,9],[4,6]],[[7,9],[7,9]],
            ]
            grid={}
            for num,y in enumerate(rgrid):
                grid[f'block{num+1}']=[i for i in desired(y[0],y[1],num+1)]

            #grid=mkgrid()
            def characters_row(row):
                tmp=''
                for i in row:
                    if i!=None:
                        tmp+=str(i)
                return tmp


            def characters_column(rows,column):
                tmp=''
                x=[]
                for r in rows:
                    c=rows[r][column]
                    if c is not None:
                        if not isinstance(c,list):
                            tmp+=str(c)
                return tmp

            def characters_block(pzl,mapped,ttl):
                tmp=''
                zz=[]
                for i in pzl:
                    zz.extend(pzl[i])
                ttl+=1
                #print(ttl,'ttl')
                for i in grid:
                    if ttl in grid[i]:
                        for x in grid[i]:
                            #print(x-1)
                            if zz[x-1] is not None:
                                tmp+=str(zz[x-1])
                            
                #back to the drawng board
                return tmp

            def display_candidates(pzl):
                ttl=0
                newStart=None
                while True:
                    ttl=0
                    for numRow in enumerate(pzl):
                        for COL in range(len(pzl[numRow[-1]])):
                            if ttl > 81:
                                ttl=0
                            filled=''
                            tmp=[]
                            ROW=[i for i in reversed(numRow)]
                            consumed=f"{characters_row(pzl[ROW[0]])}{characters_column(pzl,COL)}{characters_block(pzl,mapped,ttl)}"
                            tmpl=[]
                            for x in stre(consumed)/1:
                                if x not in tmpl:
                                    tmpl.append(x)
                            tmpl=sorted(tmpl)
                            fmsg=f'''Percent(({ttl}/80)*100)->{(ttl/80)*100:.2f} RowCol({Fore.orange_red_1}R={ROW[-1]},{Fore.light_steel_blue}C={COL})
    {Fore.light_green}Reduced("{consumed}")->"{''.join(tmpl)}"'''
                            symbol_string=f"""{fmsg}{Fore.light_yellow}
    NoneSymbol({none_symbol}){Fore.light_steel_blue}
    SYMBOL({pzl[numRow[-1]][COL]}) 
    ROWS({ROW[-1]}): {characters_row(pzl[ROW[0]])} 
    COLUMN({COL}): {characters_column(pzl,COL)} 
    BLOCK: '{characters_block(pzl,mapped,ttl)}' """
                            for char in symbols:
                                if char not in tmpl:
                                    tmp.append(char)
                            candidates=', '.join(tmp)
                            color=''
                            color_end=''
                            if len(candidates) == 1:
                                color=f"{Fore.light_green}"
                                color_end=f"{Style.reset}"
                                if pzl[numRow[-1]][COL] != candidates and pzl[numRow[-1]][COL] is not None:
                                    filled=f"{Fore.orange_red_1}AlreadyFilled({pzl[numRow[-1]][COL]}){Style.reset}"
                                    color_end=filled+color_end
                                    candidates=''
                            elif len(candidates) <= 0:
                                color=f"{Fore.light_red}"
                                if pzl[numRow[-1]][COL] is not None:
                                    filled=f"{Fore.orange_red_1}AlreadyFilled({pzl[numRow[-1]][COL]}){Style.reset}"
                                    color_end=filled+color_end
                                else:
                                    color_end=f"{filled} No candidates were found!{Style.reset}"
                            elif len(candidates) >= 1:
                                color=f"{Fore.light_cyan}"
                                color_end=f"{Style.reset}"
                                if pzl[numRow[-1]][COL] != candidates and pzl[numRow[-1]][COL] is not None:
                                    filled=f"{Fore.orange_red_1}AlreadyFilled({pzl[numRow[-1]][COL]}){Style.reset}"
                                    color_end=filled+color_end
                                    candidates=''
                            ttl+=1
                            if newStart is not None:
                                if ttl < newStart:
                                    continue
                                else:
                                    newStart=None
                            print(symbol_string)
                            print(f"{color}CANDIDATES: {color_end}",candidates)
                            
                            page=Control(func=lambda text,data:FormBuilderMkText(text,data,passThru=['goto',],PassThru=True),ptext="Next?",helpText="yes or no,",data="boolean")
                            if page in [None,'NaN']:
                                return
                            elif page in ['d',]:
                                pass
                            elif page in ['goto']:
                                breakMe=False
                                while True:
                                    stopAt=Control(func=FormBuilderMkText,ptext="Goto where?",helpText="0-81",data="integer")
                                    if stopAt in ['NaN',None]:
                                        return
                                    elif stopAt in [i for i in range(0,82)]:
                                        newStart=stopAt
                                        breakMe=True
                                        break
                                    else:
                                        print("between 0 and 81")
                                        continue
                                if breakMe:
                                    break

                            

                print('ROW and COL/COLUM are 0/zero-indexed!')
            display_candidates(pzl)
            control=Control(func=FormBuilderMkText,ptext="new data/nd,re-run/rr[default]",helpText='',data="string")
            if control in [None,'NaN']:
                return
            elif control in ['d','rr','re-run','re run']:
                continue
            elif control in ['new data','new-data','nd']:
                pzl=mkpuzl()
                continue
            else:
                continue


def costToRun():
    fields={
    'wattage of device plugged in, turned on/off?':{
        'default':60,
        'type':'float'
    },
    'hours of use?':{
        'default':1,
        'type':'float'
    },
    'electrical providers cost per kWh':{
        'default':0.70  ,
        'type':'float'
    },
    }

    fd=FormBuilder(data=fields)
    if fd is None:
        return
   
    cost=((fd['wattage of device plugged in, turned on/off?']/1000)*fd['electrical providers cost per kWh'])
    total_cost_to=cost*fd['hours of use?']
    return total_cost_to

def FederalIncomeTaxWithholding():
    fields={
    'Gross for Period':{
        'default':decc('657.88'),
        'type':'dec.dec'
    },
    f'IRS Publication 15-T ({datetime.now().year}) To Be Withheld for Status':{
        'default':decc('8'),
        'type':'dec.dec'
    },
    f'IRS Publication 15-T ({datetime.now().year}) WithHolding Amount "At Least" for Period':{
        'default':decc('655' ) ,
        'type':'dec.dec'
    },
    f'IRS Publication 15-T ({datetime.now().year}) WithHolding Amount "But Less Than" for Period':{
        'default':decc('660' ) ,
        'type':'dec.dec'
    },
    "Margin For Error":{
        'default':decc('0.05'),
        'type':'dec.dec'
    }
    }

    fd=FormBuilder(data=fields)
    if fd is None:
        return
   
    m=fd[f'IRS Publication 15-T ({datetime.now().year}) To Be Withheld for Status']/fd[f'IRS Publication 15-T ({datetime.now().year}) WithHolding Amount "At Least" for Period']
    mm=fd[f'IRS Publication 15-T ({datetime.now().year}) To Be Withheld for Status']/fd[f'IRS Publication 15-T ({datetime.now().year}) WithHolding Amount "But Less Than" for Period']
    mx=fd[f'IRS Publication 15-T ({datetime.now().year}) To Be Withheld for Status']/fd['Gross for Period']
    mmm=(m+mm+mx)/3
    gross=mmm*fd['Gross for Period']
    federal_withholding=gross+(gross*fd["Margin For Error"])

    return federal_withholding


def VAStateIncomeTaxWithholding():
    fields={
    'Gross for Period':{
        'default':decc('657.88'),
        'type':'dec.dec'
    },
    f'VA State Withholding ({datetime.now().year}) To Be Withheld for Status':{
        'default':decc('11'),
        'type':'dec.dec'
    },
    f'VA State Withholding ({datetime.now().year}) WithHolding Amount "At Least" for Period':{
        'default':decc('650' ) ,
        'type':'dec.dec'
    },
    f'VA State Withholding ({datetime.now().year}) WithHolding Amount "But Less Than" for Period':{
        'default':decc('660' ) ,
        'type':'dec.dec'
    },
    "Margin For Error":{
        'default':decc('0.0101'),
        'type':'dec.dec'
    }

    }

    fd=FormBuilder(data=fields)
    if fd is None:
        return
   
    m=fd[f'VA State Withholding ({datetime.now().year}) To Be Withheld for Status']/fd[f'VA State Withholding ({datetime.now().year}) WithHolding Amount "At Least" for Period']
    mm=fd[f'VA State Withholding ({datetime.now().year}) To Be Withheld for Status']/fd[f'VA State Withholding ({datetime.now().year}) WithHolding Amount "But Less Than" for Period']
    mx=fd[f'VA State Withholding ({datetime.now().year}) To Be Withheld for Status']/fd['Gross for Period']
    mmm=(m+mm+mx)/3
    gross=mmm*fd['Gross for Period']
    gross=gross+(gross*fd["Margin For Error"])
    return gross


def generic_service_or_item():
    fields={
    'PerBaseUnit':{
        'default':'squirt',
        'type':'string',
        },
    'PerBaseUnit_is_EquivalentTo[Conversion]':{
        'default':'1 squirt == 2 grams',
        'type':'string',
        },
    'PricePer_1_EquivalentTo[Conversion]':{
        'default':0,
        'type':'float',
        },
    'Name or Description':{
        'default':'dawn power wash',
        'type':'string'
        },
    'Cost/Price/Expense Taxed @ %':{
        'default':'Item was purchased for 3.99 Taxed @ 6.3% (PRICE+(PRICE+TAX))',
        'type':'string'
        },
    'Where was the item purchased/sold[Location/Street Address, City, State ZIP]?':{
        'default':'walmart in gloucester va, 23061',
        'type':'string'
        },
    }
    fd=FormBuilder(data=fields)
    if fd is not None:
        textty=[]
        cta=len(fd)
        for num,k in enumerate(fd):
            msg=f"{k} = '{fd[k]}'"
            textty.append(strip_colors(std_colorize(msg,num,cta)))
        master=f'''
Non-Std Item/Non-Std Service
----------------------------
{' '+'\n '.join(textty)}
----------------------------
        '''
        return master

def reciept_book_entry():
    fields={
    'reciept number':{
        'default':'',
        'type':'string'
    },
    'reciept dtoe':{
        'default':datetime.now(),
        'type':'datetime'
    },
    'recieved from':{
        'default':'',
        'type':'string'
    },
    'address':{
        'default':'',
        'type':'string'
    },
    'Amount ($)':{
        'default':0,
        'type':'dec.dec',
    },
    'For':{
        'default':'',
        'type':'string'
    },
    'By':{
        'default':'',
        'type':'string'
    },
    'Amount of Account':{
        'default':0,
        'type':'dec.dec',
    },
    'Amount Paid':{
        'default':0,
        'type':'dec.dec',
    },
    'Balance Due':{
        'default':0,
        'type':'dec.dec',
    },
    'Cash':{
        'default':0,
        'type':'dec.dec',
    },
    'Check':{
        'default':0,
        'type':'dec.dec',
    },
    'Money Order':{
        'default':0,
        'type':'dec.dec',
    },
    'Line 1':{
        'default':'',
        'type':'string'
    },
    'Line 2':{
        'default':'',
        'type':'string'
    },
    'Notes':{
        'default':'',
        'type':'string'
    },
    'Filing Location Id':{
        'default':'',
        'type':'string'
    },
    }
    fd=FormBuilder(data=fields)
    if fd is not None:
        textty=[]
        cta=len(fd)
        for num,k in enumerate(fd):
            msg=f"{k} = '{fd[k]}'"
            textty.append(strip_colors(std_colorize(msg,num,cta)))
        master=f'''
Reciept {fd['reciept number']}
----------------------------
{' '+'\n '.join(textty)}
----------------------------
        '''
        return master

def nowToPercentTime(now=None):
    if not isinstance(now,datetime):
        now=datetime.now()
    today=datetime(now.year,now.month,now.day)
    diff=now-today
    a=round(diff.total_seconds()/60/60/24,6)
    a100=round(a*100,2)
    m=str(now.strftime(f'{now} | %mM/%dD/%YY @ %H(24H)/%I %p(12H):%M:%S | {a100} Percent of 24H has passed since {today} as {diff.total_seconds()} seconds passed/{(24*60*60)} total seconds in day={a}*100={a100} | Percent of Day Passed = {a100}%'))
    return m


def ndtp():
    msg=''
    while True:
        try:
            fields={
                'distance':{
                'type':'float',
                'default':25,
                },
                'speed':{
                'type':'float',
                'default':70
                },
                'total break time':{
                'type':'string',
                'default':'10 minutes'
                }
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
            
            mph=fd['speed']
            distance=fd['distance']
            try:
                breaks=pint.Quantity(fd['total break time']).to('seconds').magnitude
            except Exception as e:
                breaks=pint.Quantity(fd['total break time']+' minutes').to('seconds').magnitude
            duration=pint.Quantity(distance/mph,'hour').to('sec').magnitude
            #12 minutes 
            buffer=timedelta(minutes=15)
            original=timedelta(seconds=duration)+timedelta(seconds=breaks)
            duration=timedelta(seconds=original.total_seconds()+buffer.total_seconds())
            now=datetime.now()
            then=now+duration
            msg=[]
            msg.append(f'Rate of Travel: {str(mph)}')
            msg.append(f'Distance To Travel: {distance}')
            msg.append(f"Now: {now}")
            msg.append(f'Non-Buffered Duration {original}')
            msg.append(f'Buffered: {duration} (+{buffer})')
            msg.append(f"Then: {then}")
            msg.append(f'Total Break Time: {timedelta(seconds=breaks)}')
            msg.append(f"From: {nowToPercentTime(now)}")
            msg.append(f"To: {nowToPercentTime(then)}")
            msg='\n\n'.join(msg)
            return msg
        except Exception as e:
            print(e)

def drug_text():
    while True:
        try:
            drug_names=[
            'thc flower',
            'thc vape',

            'thca flower',
            'thca vape',

            'caffiene',
            'caffiene+taurine',
            'caffiene+beta_alanine',

            'alcohol',
            'alcohol+thc flower',
            'alcohol+thca flower',
            
            'caffiene+thca flower+menthol',
            'caffiene+thc flower+menthol',
            ]
            extra_drugs=detectGetOrSet("extra_drugs","extra_drugs.csv",setValue=False,literal=True)
            if extra_drugs:
                extra_drugs=Path(extra_drugs)


                if extra_drugs.exists():
                    with extra_drugs.open("r") as fileio:
                        reader=csv.reader(fileio,delimiter=',')
                        for line in reader:
                            for sub in line:
                                if sub not in ['',]:
                                    sub0=f"{sub} {Fore.light_green}[{Fore.cyan}{extra_drugs}{Fore.light_green}]{Fore.dark_goldenrod}"
                                    if sub not in drug_names:
                                        drug_names.append(sub)
                                    if sub0 not in drug_names:
                                        drug_names.append(sub0)

                                    
            excludes_drn=['',' ',None,'\n','\r\n','\t',]
            rdr_state=db.detectGetOrSet('list maker lookup order',False,setValue=False,literal=False)
            if rdr_state:
                drug_names=list(sorted(set([i for i in drug_names if i not in excludes_drn]),key=str))
            else:
                drug_names=list(reversed(sorted(set([i for i in drug_names if i not in excludes_drn]),key=str)))
            htext=[]
            cta=len(drug_names)
            for num,i in enumerate(drug_names):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            
            which=Control(func=FormBuilderMkText,ptext=f"{htext}\n{Fore.yellow}which index?",helpText=htext,data="integer")
            if which in [None,'NaN']:
                return
            return strip_colors(drug_names[which])
        except Exception as e:
            print(e)
            continue

def TotalCurrencyFromMass():
    msg=''
    while True:
        try:
            fields={
                '1 Unit Mass(Grams)':{
                'type':'dec.dec',
                'default':2.50,
                },
                '1 Unit Value($)':{
                'type':'dec.dec',
                'default':0.01
                },
                'Total Unit Mass (Total Coin/Bill Mass)':{
                'type':'dec.dec',
                'default':0.0
                }
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
            value=(decc(1/fd['1 Unit Mass(Grams)'])*decc(fd['1 Unit Value($)']))*decc(fd['Total Unit Mass (Total Coin/Bill Mass)'])
            return value
        except Exception as e:
            print(e)

def BaseCurrencyValueFromMass():
    msg=''
    while True:
        try:
            fields={
                '1 Unit Mass(Grams)':{
                'type':'dec.dec',
                'default':2.50,
                },
                '1 Unit Value($)':{
                'type':'dec.dec',
                'default':0.01
                }
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
            value=(decc(1/fd['1 Unit Mass(Grams)'])*decc(fd['1 Unit Value($)']))
            return value
        except Exception as e:
            print(e)

def transport_trip_name():
    msg=''
    while True:
        try:
            transportName=db.detectGetOrSet("transport_trip_name transportName","ub",setValue=False,literal=True)
            tripNumber=db.detectGetOrSet("transport_trip_name tripNumber",0,setValue=False,literal=False)
            employeeName=db.detectGetOrSet("transport_trip_name employeeName","",setValue=False,literal=True)
            fields={
                "transport name":{
                    'default':transportName,
                    'type':'string',
                },
                'trip number':{
                    'default':tripNumber+1,
                    'type':'integer'
                },
                'dtoe':{
                    'default':datetime.now(),
                    'type':'datetime'
                },
                'employee name':{
                    'type':'string',
                    'default':employeeName,
                }
            }
            fb=FormBuilder(data=fields,passThruText=msg)
            if fb is None:
                return
            if fb['transport name'] != transportName:
                db.detectGetOrSet('transport_trip_name transportName',fb['transport name'],setValue=True,literal=True)
            if fb['trip number'] != tripNumber:
                db.detectGetOrSet('transport_trip_name tripNumber',fb['trip number'],setValue=True,literal=False)
            if fb['employee name'] != employeeName:
                db.detectGetOrSet('transport_trip_name employeeName',fb['employee name'],setValue=True,literal=True)


            value=f"""{fb['transport name']}.{fb['trip number']}-{fb['employee name']}@{fb['dtoe']}"""
            return value
        except Exception as e:
            print(e)


def USCurrencyMassValues():
    while True:
        try:
            drug_names={
            'Mass(Grams) - 1 Dollar Coin/1.0':decc(8.1),
            'Mass(Grams) - Half Dollar/0.50':decc(11.340),
            'Mass(Grams) - Quarter/0.25':decc(5.670),
            'Mass(Grams) - Nickel/0.05':decc(5.0),
            'Mass(Grams) - Dime/0.10':decc(2.268),
            'Mass(Grams) - Penny/0.01':decc(2.5),
            'Mass(Grams) - Bill($1/$2/$5/$10/$20/$50/$100':decc(1),

            'Value for Mass(Grams) - 1 Dollar Coin/8.1 Grams':1.00,
            'Value for Mass(Grams) - Half Dollar/11.340 Grams':0.50,
            'Value for Mass(Grams) - Quarter/5.670 Grams':0.25,
            'Value for Mass(Grams) - Nickel/5 Grams':0.05,
            'Value for Mass(Grams) - Dime/2.268 Grams':0.10,
            'Value for Mass(Grams) - Penny/2.5 Grams':0.01,
            'Value for Mass(Grams) - 1$ Bill/1 Grams':1,
            'Value for Mass(Grams) - 2$ Bill/1 Grams':2,
            'Value for Mass(Grams) - 5$ Bill/1 Grams':5,
            'Value for Mass(Grams) - 10$ Bill/1 Grams':10,
            'Value for Mass(Grams) - 20$ Bill/1 Grams':20,
            'Value for Mass(Grams) - 50$ Bill/1 Grams':50,
            'Value for Mass(Grams) - 100$ Bill/1 Grams':100,
            }
            

            keys=[]
            htext=[]
            cta=len(drug_names)
            for num,i in enumerate(drug_names):
                msg=f'{i} -> {drug_names[i]}'
                htext.append(std_colorize(msg,num,cta))
                keys.append(i)
            htext='\n'.join(htext)
            print(htext)
            which=Control(func=FormBuilderMkText,ptext="which index?",helpText=htext,data="integer")
            if which in [None,'NaN']:
                return
            return drug_names[keys[which]]
            
        except Exception as e:
            print(e)
            continue


def currency_conversion():
    cvt_registry=pint.UnitRegistry()
    
    definition=f'''
    USD = [currency]
Argentine_Peso  =    nan usd
Australian_Dollar   =    nan usd
Bahraini_Dinar  =    nan usd
Botswana_Pula   =    nan usd
Brazilian_Real  =    nan usd
British_Pound   =    nan usd
Bruneian_Dollar =    nan usd
Bulgarian_Lev   =    nan usd
Canadian_Dollar =    nan usd
Chilean_Peso    =    nan usd
Chinese_Yuan_Renminbi   =    nan usd
Colombian_Peso  =    nan usd
Czech_Koruna    =    nan usd
Danish_Krone    =    nan usd
Emirati_Dirham  =    nan usd
Euro    =    nan usd
Hong_Kong_Dollar    =    nan usd
Hungarian_Forint    =    nan usd
Icelandic_Krona =    nan usd
Indian_Rupee    =    nan usd
Indonesian_Rupiah   =    nan usd
Iranian_Rial    =    nan usd
Israeli_Shekel  =    nan usd
Japanese_Yen    =    nan usd
Kazakhstani_Tenge   =    nan usd
Kuwaiti_Dinar   =    nan usd
Libyan_Dinar    =    nan usd
Malaysian_Ringgit   =    nan usd
Mauritian_Rupee =    nan usd
Mexican_Peso    =    nan usd
Nepalese_Rupee  =    nan usd
New_Zealand_Dollar  =    nan usd
Norwegian_Krone =    nan usd
Omani_Rial  =    nan usd
Pakistani_Rupee =    nan usd
Philippine_Peso =    nan usd
Polish_Zloty    =    nan usd
Qatari_Riyal    =    nan usd
Romanian_New_Leu    =    nan usd
Russian_Ruble   =    nan usd
Saudi_Arabian_Riyal =    nan usd
Singapore_Dollar    =    nan usd
South_African_Rand  =    nan usd
South_Korean_Won    =    nan usd
Sri_Lankan_Rupee    =    nan usd
Swedish_Krona   =    nan usd
Swiss_Franc =    nan usd
Taiwan_New_Dollar   =    nan usd
Thai_Baht   =    nan usd
Trinidadian_Dollar  =    nan usd
Turkish_Lira    =    nan usd

@context FX
Argentine_Peso  =    0.000671    usd
Australian_Dollar   =    0.651104    usd
Bahraini_Dinar  =    2.659574    usd
Botswana_Pula   =    0.070042    usd
Brazilian_Real  =    0.185537    usd
British_Pound   =    1.330948    usd
Bruneian_Dollar =    0.769854    usd
Bulgarian_Lev   =    0.594475    usd
Canadian_Dollar =    0.714527    usd
Chilean_Peso    =    0.001062    usd
Chinese_Yuan_Renminbi   =    0.140424    usd
Colombian_Peso  =    0.000259    usd
Czech_Koruna    =    0.047793    usd
Danish_Krone    =    0.155642    usd
Emirati_Dirham  =    0.272294    usd
Euro    =    1.162692    usd
Hong_Kong_Dollar    =    0.128701    usd
Hungarian_Forint    =    0.002981    usd
Icelandic_Krona =    0.008119    usd
Indian_Rupee    =    0.011384    usd
Indonesian_Rupiah   =    0.00006 usd
Iranian_Rial    =    0.000024    usd
Israeli_Shekel  =    0.304734    usd
Japanese_Yen    =    0.006545    usd
Kazakhstani_Tenge   =    0.00186 usd
Kuwaiti_Dinar   =    3.261214    usd
Libyan_Dinar    =    0.183824    usd
Malaysian_Ringgit   =    0.236753    usd
Mauritian_Rupee =    0.02197 usd
Mexican_Peso    =    0.054181    usd
Nepalese_Rupee  =    0.007112    usd
New_Zealand_Dollar  =    0.575051    usd
Norwegian_Krone =    0.099905    usd
Omani_Rial  =    2.603489    usd
Pakistani_Rupee =    0.003531    usd
Philippine_Peso =    0.017016    usd
Polish_Zloty    =    0.274017    usd
Qatari_Riyal    =    0.274725    usd
Romanian_New_Leu    =    0.228593    usd
Russian_Ruble   =    0.012559    usd
Saudi_Arabian_Riyal =    0.266667    usd
Singapore_Dollar    =    0.769854    usd
South_African_Rand  =    0.057932    usd
South_Korean_Won    =    0.000695    usd
Sri_Lankan_Rupee    =    0.003293    usd
Swedish_Krona   =    0.106347    usd
Swiss_Franc =    1.256685    usd
Taiwan_New_Dollar   =    0.032417    usd
Thai_Baht   =    0.030604    usd
Trinidadian_Dollar  =    0.147095    usd
Turkish_Lira    =    0.023829    usd
@end'''.lower()
    defFile=db.detectGetOrSet("currency_definitions_file","currency_definitions.txt",setValue=False,literal=True)
    if defFile is None:
        return
    defFile=Path(defFile)
    with open(defFile,"w") as out:
        out.write(definition)
    cvt_registry.load_definitions(defFile)
    with cvt_registry.context("fx") as cvtr:  
        while True:  
            try:
                htext=[]
                definition=definition.split("@context FX")[-1].replace('\n@end','')
                cta=len(definition.split("\n"))
                formats='\n'.join([std_colorize(i,num,cta) for num,i in enumerate(definition.split("\n"))])
                
                formats=f'''Conversion Formats are:\n{formats}\n'''
                fields={
                'value':{
                    'default':1,
                    'type':'float',
                },
                'FromString':{
                    'default':'USD',
                    'type':'string',
                },
                'ToString':{
                    'default':'Euro',
                    'type':'string'
                },
                }
                fb=FormBuilder(data=fields,passThruText=formats)
                if fb is None:
                    return

                return_string=fb['ToString'].lower()
                value_string=f"{fb['value']} {fb['FromString']}".lower()
                resultant=cvtr.Quantity(value_string).to(return_string)

                #if it gets here return None
                return resultant
            except Exception as e:
                print(e)

def bible_try():
    try:
        os.system("sonofman")
        return None
    except Exception as e:
        print(e)

DELCHAR=db.detectGetOrSet("DELCHAR preloader func","|",setValue=False,literal=True)
if not DELCHAR:
    DELCHAR='|'

def SalesFloorLocationString():
    fields=OrderedDict({

        'Aisle[s]':{
            'default':'',
            'type':'string',
        },
        'Bay[s]/AisleDepth':{
            'default':'',
            'type':'string',
        },
        'Shel[f,ves]':{
            'default':'',
            'type':'string',
        }
    })
    passThruText=f"""
{Fore.orange_red_1}Valid Aisle[s]:{Fore.grey_85}
    this is the aisle on which the product resides
    if the product belongs on an end cap use the endcap here as
    well. endcaps are numbered 0+=1 from left to right of the store
    front. the same is true for aisle. if the product resides on an 
    end cap, append FEC (0FEC) to signify front end cap 0, or 0REC for 
    rear end cap 0.
    0 -> on aisle 0
    0,1 -> on aisle 0 and  1
    0-2 -> from aisle 0 to aisle 2

    encaps on the front side of the aisle will have an FEC Appended to its number
     The same is true for rear of the aisle(REC). if a encap range is used, the character
     will identify its side of the store. if two encaps on opposite sides of the store
     are specified, then use 2 separate ranges; one for front and one for the rear.
    0FEC -> on front endcap 0
    0FEC,1REC -> on front endcap 0 and on rear endcap 1.
    0-2FEC -> from front endcap 0 to front endcap 2
    0-2REC -> from rear endcap 0 to rear endcap 2
    0-2FEC,0-2REC -> from front endcap 0 to front endcap 2 && from rear endcap 0 to rear endcap 2

    if No number is provided, but a common NAME is used, use that here for this section of the location.
{Fore.orange_red_1}Valid 'Bay[s]/AisleDepth':{Fore.grey_85}
    This is How many shelf bays deep from the front of the store
     to the back, where 0 is the first bay from the endcap at the 
     front of the store and increments upwards to the rear end cap.
     Bays on the right side of the aisle will have an R Appended to its number
     The same is true for left of the aisle. if a bay range is used, the character
     will identify its side of the aisle. if two bays on opposite sides of the aisle
     are specified, then use 2 separate ranges; one for left and one for right.
    0 -> on bay 0
    0,1 -> on bay 0 and  1
    0-2R -> from bay 0 to bay 2 on the right side of the aisle
    0-2L -> from bay 0 to bay 2 on the left side of the aisle
    0-2R,0-2L -> from bay 0 to bay 2 on the right side of the aisle && from bay 0 to bay 2 on the left side of the aisle.

    if No number is provided, but a common NAME is used, use that here for this section of the location.    
{Fore.orange_red_1}Valid Shel[f,ves]:{Fore.grey_85}
    this is the height where the product is on the shelf
    shelves are number 0 to their highest from bottom to top
    where the very bottom shelf is 0, and the next following shelf upwards is 
    1, and so on.
    0 -> on shelf 0
    0,1 -> on shelf 0 and  1
    0-2 -> from shelf 0 to shelf 2

    if No number is provided, but a common NAME is used, use that here for this section of the location.    
{Fore.light_green}Aisle or EndCap{Fore.light_red}/{Fore.light_yellow}Depth or Bay in Aisle{Fore.light_red}/{Fore.light_steel_blue}Shelf or Location Number(s) Where Item Resides [optional]{Style.reset}
{Fore.light_green}A completely Valid Example is Aisle 0|Household Chemicals|Kitchen Care, which is where Dawn Dish Detergent is normally located.
{Fore.light_red}{os.get_terminal_size().columns*'/'}
"""
    fb=FormBuilder(data=fields,passThruText=passThruText)
    if fb is None:
        return
    if fb['Shel[f,ves]'] not in ['',]:
        fb['Shel[f,ves]']=f"{DELCHAR}{fb['Shel[f,ves]']}"
    locationString=f"{fb['Aisle[s]']}{DELCHAR}{fb['Bay[s]/AisleDepth']}{fb['Shel[f,ves]']}"
    return locationString

def BackroomLocation():
    fields=OrderedDict({
        'moduleType':{
            'default':'',
            'type':'string',
            },
        'moduleNumberRange':{
            'default':'',
            'type':'string',
        },
        'caseID':{
            'default':'',
            'type':'string',
        },

    })
    passThruText=f'''
{Fore.orange_red_1}Valid ModuleTypes:{Fore.grey_85}
    this what to look on for where the product is stored
    s or S -> For Pallet/Platform [General]/Skid
    u or U -> For U-Boat/Size Wheeler
    rc or rC or Rc or RC ->  for RotaCart
    sc or sC or Sc or SC -> Shopping Cart
    if a name is used, or common identifier is used, use that here in this segment of the location.

{Fore.orange_red_1}Valid ModuleNumberRange:{Fore.grey_85}
    This which of the what's contains said item.
    0 -> on which 0
    0,1 -> on which 0 and which 1
    0-2 -> from which 0 to which 2 on the left side of the aisle
    if a name is used, or common identifier is used, use that here in this segment of the location.
{Fore.orange_red_1}Valid caseID:{Fore.grey_85}
    This is the case where the item is stored in which is the which found on the what.
    anything that you want as long as it is unique to the module in which it is stored.
     try using the following cmds for something on the fly.
     nanoid - nanoid
     crbc - checked random barcode
     dsur - generate a datestring
     urid - generate reciept id with a log
     cruid - checked uuid
     if a name is used, or common identifier is used, use that here in this segment of the location.
{Fore.light_red}{os.get_terminal_size().columns*'/'}

    '''
    fb=FormBuilder(data=fields,passThruText=passThruText)
    if fb is None:
        return
    if fb['caseID'] not in ['',]:
        fb['caseID']=f"{DELCHAR}{fb['caseID']}"
    locationString=f"{fb['moduleType']}{DELCHAR}{fb['moduleNumberRange']}{' '.join(db.stre(fb['caseID'])/3)}"
    return locationString

def TaxMuleFraud():
    msg=''
    while True:
        try:
            fields={
                'Price':{
                'type':'dec.dec',
                'default':decc(2.50,)
                },
                'Legally Applied Tax':{
                'type':'dec.dec',
                'default':decc(0.01)
                },
                'Mule Tax Rate (Charged as Despite being legally the other)':{
                'type':'dec.dec',
                'default':decc(0.063)
                }
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            prc=fd['Price']
            ltx=fd['Legally Applied Tax']
            iltx=fd['Mule Tax Rate (Charged as Despite being legally the other)']
            print(BooleanAnswers.FraudAlert)
            totals={
            f'legally_taxed_tax[(Price({prc})*legal_tax({ltx})]':fd['Price']*fd['Legally Applied Tax'],
            f'legally_taxed_price[Price({prc})+(Price({prc})*legal_tax({ltx})]':(fd['Price']*fd['Legally Applied Tax'])+fd['Price'],

            f'illegally_taxed_tax[Price({prc})*Illegal Tax({iltx})]':fd['Price']*fd['Mule Tax Rate (Charged as Despite being legally the other)'],
            f'illegally_taxed_price(What was charged to the customer)[Price({prc})+(Price({prc})*Illegal_tax({iltx}))]':(fd['Price']*fd['Mule Tax Rate (Charged as Despite being legally the other)'])+fd['Price'],

            f'fraud_profit_tax_only[Price({prc})*(illegal_tax({iltx})-legal_tax({ltx})]':fd['Price']*(fd['Mule Tax Rate (Charged as Despite being legally the other)']-fd['Legally Applied Tax']),
            f'fraud_profit_as_price[Price({prc})+(Price({prc})*(illegal_tax({iltx})-legal_tax({ltx}))]':(fd['Price']*(fd['Mule Tax Rate (Charged as Despite being legally the other)']-fd['Legally Applied Tax']))+fd['Price'],
            }
            cta=len(totals)
            htext='\n'.join([std_colorize(f'{i} = {Fore.light_green}{totals[i]}',num,cta) for num,i in enumerate(totals)])
            while True:
                which=Control(func=FormBuilderMkText,ptext=f"{htext}\nwhich index to return?",helpText=htext,data="integer")
                if which in [None,'NaN']:
                    return 
                elif which in range(0,len(totals)):
                    return totals[[i for i in totals.keys()][which]]
                else:
                    continue

            value=None

            return value
        except Exception as e:
            print(e)

def abstract_filter(model):
    #still needs <=,>=,!=,<,>,
    #use +-10~=$VAL for around 10+- the value $VAL
    prototype=model()
    try:
        setattr(prototype,'photoSerialNo',None)
    except Exception as e:
        print(e)
    fields={i.name:{'default':getattr(prototype,i.name),'type':str(i.type).lower()} for i in prototype.__table__.columns}
    try:
        fields.pop('dtoe')
    except Exception as e:
        print(e,"please ignore")

    try:
        fields.pop('datetime')
    except Exception as e:
        print(e,"please ignore")

    try:
        fields.pop('time')
    except Exception as e:
        print(e,"please ignore")

    try:
        fields.pop('date')
    except Exception as e:
        print(e,"please ignore")

    fb=FormBuilder(data=fields)
    if not fb:
        return []
    xfilter=[]
    print(xfilter)

    for k in fb:
        data=fb[k]
        print(data,k)
        if data is not None:
            if isinstance(data,datetime):
                xfilter.append(getattr(model,k)==data)
            elif isinstance(data,str):
                xfilter.append(getattr(model,k).icontains(data))
            elif isinstance(data,int):
                xfilter.append(getattr(model,k)==data)
            elif isinstance(data,float):
                xfilter.append(getattr(model,k)==data)
    if len(xfilter) < 1:
        return None
    return or_(and_(*xfilter),or_(*xfilter))

class BTemplate:
    def __str__(self):
        return f"{Fore.light_yellow}{self.__class__.__name__}(){Fore.light_green} exited {Fore.orange_red_1}@{Fore.dark_goldenrod} {datetime.now()}{Fore.orange_red_1}!"

    def __repr__(self):
        return self.__str__()

class Templogger(BTemplate):
    def fix_table(self):
        TemplLog.__table__.drop(ENGINE)
        TemplLog.metadata.create_all(ENGINE)
        print("Done!")


    def newLog(self,temp=None):
        if temp:
            arg=True
        else:
            arg=False
        with Session(ENGINE) as session:
            excludes=['templogid',]
            provided=False
            print(temp)
            if temp is None:
                temp=TemplLog()
            else:
                provided=True

            if not provided:
                session.add(temp)
                session.commit()
                session.refresh(temp)
            else:
                temp=session.query(TemplLog).filter(TemplLog.templogid==temp.templogid).first()
            print(temp)

            fields={str(i.name):{'default':getattr(temp,i.name),'type':str(i.type).lower()} for i in temp.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(temp)
                session.commit()
                return
            for k in fb:
                setattr(temp,k,fb[k])
            temp.dtoe=datetime.now()
            session.commit()
            session.refresh(temp)
            print(temp)
            return temp

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            try:
                processed_templerature_string=pint.Quantity(i.templerature_value,i.templerature_unit)
                msg=f"""TemplLog ->\n {ii}    
    {Fore.light_red}[{Fore.cyan}templogid{Fore.light_red}] {Fore.light_green}{i.templogid}
    {Fore.light_red}[{Fore.cyan}dtoe{Fore.light_red}] {Fore.light_green}{i.dtoe}
    {Fore.light_red}[{Fore.cyan}Logged{Fore.light_yellow} Temperature{Fore.light_red}] {Fore.light_green}{processed_templerature_string.to('degC')} {Fore.green_yellow}or {processed_templerature_string.to('degF')} {Fore.light_magenta}or {processed_templerature_string.to('degK')}
    {Fore.light_red}[{Fore.cyan}Location{Fore.light_red}] {Fore.light_green}{i.Location}
    {Fore.light_red}[{Fore.cyan}EmployeeIDorNAME{Fore.light_red}] {Fore.light_green}{i.EmployeeIDorNAME}
    {Fore.light_red}[{Fore.cyan}note{Fore.light_red}] {Fore.light_green}{i.note}{Style.reset}
                """
                if not num:
                    m=std_colorize(msg,xnum,ct)
                else:
                    m=std_colorize(msg,num,ct)
                xtext.append(m)
                if printToScreen:            
                    print(m)
            except Exception as e:
                msg=f"""TemplLog ->\n {ii}    
    {Fore.light_red}[{Fore.cyan}templogid{Fore.light_red}] {Fore.light_green}{i.templogid}
    {Fore.light_red}[{Fore.cyan}dtoe{Fore.light_red}] {Fore.light_green}{i.dtoe}
    {Fore.light_red}[{Fore.cyan}Logged{Fore.light_yellow} Temperature{Fore.light_red}] {Fore.light_green}{i.templerature_value} {i.templerature_unit} 
    {Fore.light_red}[{Fore.cyan}Location{Fore.light_red}] {Fore.light_green}{i.Location}
    {Fore.light_red}[{Fore.cyan}EmployeeIDorNAME{Fore.light_red}] {Fore.light_green}{i.EmployeeIDorNAME}
    {Fore.light_red}[{Fore.cyan}note{Fore.light_red}] {Fore.light_green}{i.note}
    {Fore.light_red}A Value was not processed correctly, please review tmplogid={Fore.light_steel_blue}{i.templogid}
    {Style.reset}"""
                if not num:
                    m=std_colorize(msg,xnum,ct)
                else:
                    m=std_colorize(msg,num,ct)
                xtext.append(m)
                if printToScreen:            
                    print(m)

        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
        if printToScreen:
            print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(TemplLog).filter(TemplLog.templogid==item.templogid).first()
                return self.newLog(temp=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(TemplLog).filter(TemplLog.templogid==item.templogid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            
            filt=abstract_filter(TemplLog)
            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                return
            if filt is not None:
                query=session.query(TemplLog).filter(filt)
            else:
                query=session.query(TemplLog)
            
            
            orderedQuery=orderQuery(query,TemplLog.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()

            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)



    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}Templogger {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")


class MPGLogger(BTemplate):
    def fix_table(self):
        MPGL.__table__.drop(ENGINE)
        MPGL.metadata.create_all(ENGINE)
        print("Done!")


    def newLog(self,mpgl=None):
        if mpgl:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['mpglid',]
            provided=False
            #print(mpgl,"#0")
            if mpgl is None:
                mpgl=MPGL()
            else:
                provided=True

            if not provided:
                session.add(mpgl)
                session.commit()
                session.refresh(mpgl)
            else:
                mpgl=session.query(MPGL).filter(MPGL.mpglid==mpgl.mpglid).first()
            #print(mpgl,'#1')

            fields={str(i.name):{'default':getattr(mpgl,i.name),'type':str(i.type).lower()} for i in mpgl.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(mpgl)
                session.commit()
                return
            for k in fb:
                setattr(mpgl,k,fb[k])
            mpgl.dtoe=datetime.now()
            session.commit()
            session.refresh(mpgl)
            #print(mpgl,'#2')
            return mpgl

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            dist=0
            mpg=0
            fuelused=0
            if i.Starting_Odometer_Reading is not None and i.Ending_Odometer_Reading is not None:
                dist=unit_registry.Quantity(i.Ending_Odometer_Reading,i.Odometer_Unit_Of_Distance)-unit_registry.Quantity(i.Starting_Odometer_Reading,i.Odometer_Unit_Of_Distance)
                if i.FuelUsed:
                    fuelused=unit_registry.Quantity(i.FuelUsed,i.FuelUsedUnit)
                    mpg=dist/fuelused
                    
            
            msg=f"""{Back.black}MPG Log {i.LicensePlateOrVehicleIdentifier}[dtoe={i.dtoe}/comment='{i.comment}']->
{Fore.light_steel_blue}LicensePlateOrVehicleIdentifier{Fore.light_red}: {Fore.dark_goldenrod}{i.LicensePlateOrVehicleIdentifier}{Style.reset}
{Fore.light_green}Starting Odometer Reading{Fore.light_yellow}:{Fore.light_red} {i.Starting_Odometer_Reading}{Style.reset}
{Fore.light_green}Ending Odometer Reading{Fore.light_yellow}:{Fore.light_red} {i.Ending_Odometer_Reading}{Style.reset}
{Fore.light_green}Distance Travelled({Fore.light_cyan}End-Start{Fore.light_yellow}){Fore.light_yellow}:{Fore.light_red} {dist}{Style.reset}
{Fore.light_green}Unit Of Distance{Fore.light_yellow}:{Fore.light_red} {i.Odometer_Unit_Of_Distance}{Style.reset}
{Fore.light_green}Fuel-Used({Fore.light_cyan}What you refueled at the pump{Fore.light_yellow}){Fore.light_yellow}:{Fore.light_red} {fuelused}{Style.reset}
{Fore.light_green}Unit of Volume for Fuel Used{Fore.light_yellow}:{Fore.light_red} {i.FuelUsedUnit}{Style.reset}
{Fore.light_green}{i.Odometer_Unit_Of_Distance}-Per-{i.FuelUsedUnit}({Fore.light_cyan}Distance/FuelUsed{Fore.light_yellow}){Fore.light_yellow}:{Fore.light_red} {mpg}{Style.reset}
            """
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            #if printToScreen:            
            #    print(m)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(MPGL).filter(MPGL.mpglid==item.mpglid).first()
                return self.newLog(mpgl=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(MPGL).filter(MPGL.mpglid==item.mpglid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(MPGL)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                return
            if filt is not None:
                query=session.query(MPGL).filter(filt)
            else:
                query=session.query(MPGL)
            
           
            orderedQuery=orderQuery(query,MPGL.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            '''
            orderedQuery=orderQuery(query,FuelPrice.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            '''

            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)



    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}MPGL/Miles Per Gallon Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")


class GasLogger(BTemplate):
    

    def fix_table(self):
        FuelPrice.__table__.drop(ENGINE)
        FuelPrice.metadata.create_all(ENGINE)
        print("Done!")


    def newLog(self,fuel=None):
        if fuel:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['fuelid',]
            provided=False
            #print(fuel,"#0")
            if fuel is None:
                fuel=FuelPrice()
            else:
                provided=True

            if not provided:
                session.add(fuel)
                session.commit()
                session.refresh(fuel)
            else:
                fuel=session.query(FuelPrice).filter(FuelPrice.fuelid==fuel.fuelid).first()
            #print(fuel,'#1')

            fields={str(i.name):{'default':getattr(fuel,i.name),'type':str(i.type).lower()} for i in fuel.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(fuel)
                session.commit()
                return
            for k in fb:
                setattr(fuel,k,fb[k])
            fuel.dtoe=datetime.now()
            session.commit()
            session.refresh(fuel)
            #print(fuel,'#2')
            return fuel

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            dist=0
            mpg=0
            fuelused=0
            msg=f"""
            {Fore.orange_red_1}Location: {Fore.light_yellow}{i.location}
            {Fore.orange_red_1}Address[{Fore.light_steel_blue}not applicable if location is different or otherwise specified{Fore.orange_red_1}]:{Fore.grey_85}{i.street_address}, {i.city_county_of}, {i.state} {i.zipcode}, {i.country}
            {Fore.light_steel_blue}DTOE: {i.dtoe}
            {Fore.light_cyan}Comment:{i.comment}
            {Fore.light_green}{i.fuel_name}{Fore.light_red} @ {Fore.light_yellow}{i.fuel_price} {Fore.light_green}{i.fuel_price_unit}{Style.reset}
            """
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(FuelPrice).filter(FuelPrice.fuelid==item.fuelid).first()
                return self.newLog(fuel=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(FuelPrice).filter(FuelPrice.fuelid==item.fuelid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(FuelPrice)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                return
            if filt is not None:
                query=session.query(FuelPrice).filter(filt)
            else:
                query=session.query(FuelPrice)

            orderedQuery=orderQuery(query,FuelPrice.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)



    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}Fuel Price Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")

def QtyString():
    msg=''
    while True:
        try:
            fields={
                'Barcode':{
                'type':'string',
                'default':'',
                },
                'qty':{
                'type':'dec.dec',
                'default':decc('0001.0000')
                },
                'qtyUnit':{
                'type':'string',
                'default':'Unit/Each'
                },
                'dtoe':{
                'type':'datetime',
                'default':datetime.now()
                },
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            

            value=f"{fd['Barcode']}|{fd['qty']}|{fd['qtyUnit']}|{fd['dtoe']}"

            return value
        except Exception as e:
            print(e)
'''
class DoorSealRegistryLogger(BTemplate):
    def __new__(self):
        return "Not Yet Ready!"

'''


class DoorSealRegistryLogger(BTemplate):
    

    def fix_table(self):
        DoorSealRegistry.__table__.drop(ENGINE)
        DoorSealRegistry.metadata.create_all(ENGINE)
        print("Done!")

    def batchNewLog(self):
        with Session(ENGINE) as session:
            excludes=['dsrid','SealId']
            provided=False
            #print(doorSealRegistry,"#0")

            doorSealRegistry=DoorSealRegistry()
            session.add(doorSealRegistry)
            session.commit()
            session.refresh(doorSealRegistry)

            fields={str(i.name):{'default':getattr(doorSealRegistry,i.name),'type':str(i.type).lower()} for i in doorSealRegistry.__table__.columns if i.name not in excludes}
            fields['StartRange']={'default':25406521,'type':'integer'}
            fields['EndRange']={'default':25406530,'type':'integer'}
            fields['IdLength']={'default':8,'type':'integer'}

            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                session.delete(doorSealRegistry)
                session.commit()
                return
            StartRange=fb['StartRange']
            EndRange=fb['EndRange']
            IdLength=fb['IdLength']
            fb.pop('StartRange')
            fb.pop('EndRange')
            fb.pop('IdLength')

            for i in range(StartRange,EndRange+1):
                ndsl=DoorSealRegistry()
                session.add(ndsl)
                session.commit()

                seal=str(i).zfill(IdLength)
                for k in fb:
                    setattr(ndsl,k,fb[k])
                setattr(ndsl,'SealId',seal)
                ndsl.dtoe=datetime.now()
                
                session.commit()
                session.refresh(ndsl)
                print(ndsl)
            session.delete(doorSealRegistry)
            session.commit()

    def newLog(self,doorSealRegistry=None):
        if doorSealRegistry:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['dsrid',]
            provided=False
            #print(doorSealRegistry,"#0")
            if doorSealRegistry is None:
                doorSealRegistry=DoorSealRegistry()
            else:
                provided=True

            if not provided:
                session.add(doorSealRegistry)
                session.commit()
                session.refresh(doorSealRegistry)
            else:
                doorSealRegistry=session.query(doorSealRegistry).filter(doorSealRegistry.dsrid==doorSealRegistry.dsrid).first()
            #print(doorSealRegistry,'#1')

            fields={str(i.name):{'default':getattr(doorSealRegistry,i.name),'type':str(i.type).lower()} for i in doorSealRegistry.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(doorSealRegistry)
                session.commit()
                return
            for k in fb:
                setattr(doorSealRegistry,k,fb[k])
            doorSealRegistry.dtoe=datetime.now()
            session.commit()
            session.refresh(doorSealRegistry)
            #print(doorSealRegistry,'#2')
            return doorSealRegistry


    def newLog(self,door_seal_log_registry=None):
        if door_seal_log_registry:
            arg=True
        else:
            arg=False
        with Session(ENGINE) as session:
            excludes=['dsrid',]
            provided=False
            print(door_seal_log_registry)
            if door_seal_log_registry is None:
                door_seal_log_registry=DoorSealRegistry()
            else:
                provided=True

            if not provided:
                session.add(door_seal_log_registry)
                session.commit()
                session.refresh(door_seal_log_registry)
            else:
                door_seal_log_registry=session.query(DoorSealRegistry).filter(DoorSealRegistry.dsrid==door_seal_log_registry.dsrid).first()
            print(door_seal_log_registry)

            fields={str(i.name):{'default':getattr(door_seal_log_registry,i.name),'type':str(i.type).lower()} for i in door_seal_log_registry.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(door_seal_log_registry)
                session.commit()
                return
            for k in fb:
                setattr(door_seal_log_registry,k,fb[k])
            door_seal_log_registry.dtoe=datetime.now()
            session.commit()
            session.refresh(door_seal_log_registry)
            print(door_seal_log_registry)
            return door_seal_log_registry

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f"""
{Fore.light_green}{'-'*os.get_terminal_size().columns}{Style.reset}
{Fore.orange_red_1}dsrid={Fore.light_green}"{i.dsrid}"{Style.reset}
{Fore.light_yellow}SealId={Fore.light_green}"{i.SealId}"{Style.reset}
{Fore.light_red}RegisteredBy={Fore.light_green}"{i.RegisteredBy}"{Style.reset}
{Fore.light_blue}dtoe={Fore.light_green}"{i.dtoe}"{Style.reset}
{Fore.light_cyan}comment={Fore.light_green}"{i.comment}"{Style.reset}
{Fore.cyan}photoSerialNo={Fore.light_green}"{i.photoSerialNo}"{Style.reset}
{Fore.light_red}{'*'*os.get_terminal_size().columns}{Style.reset}
            """
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(DoorSealRegistry).filter(DoorSealRegistry.dsrid==item.dsrid).first()
                return self.newLog(door_seal_log_registry=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(DoorSealRegistry).filter(DoorSealRegistry.dsrid==item.dsrid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(DoorSealRegistry)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(DoorSealRegistry).filter(filt)
            else:
                query=session.query(DoorSealRegistry)
            
            
            orderedQuery=orderQuery(query,DoorSealRegistry.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)



    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            },
            str(uuid1()):{
            'cmds':['new batch','newbl','new batch temp log','nbtl'],
            'exec':self.batchNewLog,
            'desc':"create a new log in range batches"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}Door Seal Registry Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")

#'''
class DoorSealLogLogger(BTemplate):
    def currentSealMatchesLastNewSeal(self):
        with Session(ENGINE) as session:
            log=session.query(DoorSealLog).order_by(DoorSealLog.dtoe.desc()).first()
            if log is None:
                print(f"{Fore.orange_red_1}There are no logs present!{Style.reset}")
                return
            newSeal=session.query(DoorSealRegistry).filter(or_(DoorSealRegistry.SealId.icontains(log.NewSealId),DoorSealRegistry.SealId==log.NewSealId)).first()
            oldSeal=session.query(DoorSealRegistry).filter(or_(DoorSealRegistry.SealId.icontains(log.OldSealId),DoorSealRegistry.SealId==log.OldSealId)).first()
            if newSeal is None:
                log.doorSealMismatch=True
                if '\nNew Seal is not in Registry\n' not in log.doorSealMisMatchComment:
                    log.doorSealMisMatchComment+="\nNew Seal is not in Registry\n"
            if oldSeal is None:
                log.doorSealMismatch=True
                if '\nOld Seal Is Not in Registry\n' not in log.doorSealMisMatchComment:
                    log.doorSealMisMatchComment+="\nOld Seal Is Not in Registry\n"

            fields={
            'Current Door SealId|SealNo':{
                'default':'INVALID',
                'type':'string',
            },
            }
            msg=f"""
{'-'*os.get_terminal_size().columns}
NewSealId={log.NewSealId}
NewSealDate={log.NewSealDate}
NewSealEmployeeIdOrName={log.NewSealEmployeeIdOrName}
OldSealId={log.OldSealId}
OldSealDate={log.OldSealDate}
OldSealEmplyeeIdOrName={log.OldSealEmplyeeIdOrName}
dtoe={log.dtoe}
comment={log.comment}
doorSealMisMatch="{log.doorSealMisMatch}"   
doorSealMisMatchComment="{log.doorSealMisMatchComment}"
doorSealMisMatchPermitted="{log.doorSealMisMatchPermitted}"
doorSealMisMatchPermittedBy="{log.doorSealMisMatchPermittedBy}"
photoSerialNo={log.photoSerialNo}
{'*'*os.get_terminal_size().columns}
            """
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
            else:
                current_seal_id=fd['Current Door SealId|SealNo']
                if log.NewSealId != current_seal_id:
                    errMsg=f'''The Current Door Seal does not match the latest log's NewSealId: {log.NewSealId}'''
                    if errMsg not in log.doorSealMisMatchComment:
                        log.doorSealMisMatchComment+=f"\n{errMsg}\n"
                        session.commit()
                        session.refresh(log)
                        print(log)
                else:
                    print(f"{Fore.green_yellow}Verified! {Fore.light_green}Your are GTG ({Fore.orange_red_1}Good-To-Go{Fore.light_green})!{Style.reset}")

    def isSealValid(self):
        with Session(ENGINE) as session:
            logs=session.query(DoorSealLog).all()
            cta=len(logs)
            for num,log in enumerate(logs):
                newSeal=session.query(DoorSealRegistry).filter(DoorSealRegistry.SealId==log.NewSealId).first()
                oldSeal=session.query(DoorSealRegistry).filter(DoorSealRegistry.SealId==log.OldSealId).first()
                #print('seals','old',oldSeal,'new',newSeal,log)
                if not newSeal:
                    log.doorSealMisMatch=True
                    session.commit()
                    session.refresh(log)
                    if log.doorSealMisMatchComment is None:
                        log.doorSealMisMatchComment=''
                        session.commit()
                        session.refresh(log)
                    if '\nNew Seal is not in Registry\n' not in log.doorSealMisMatchComment:
                        log.doorSealMisMatchComment+="\nNew Seal is not in Registry\n"
                if not oldSeal:
                    log.doorSealMisMatch=True
                    session.commit()
                    session.refresh(log)
                    if log.doorSealMisMatchComment is None:
                        log.doorSealMisMatchComment=''
                        session.commit()
                        session.refresh(log)
                    if '\nOld Seal Is Not in Registry\n' not in log.doorSealMisMatchComment:
                        log.doorSealMisMatchComment+="\nOld Seal Is Not in Registry\n"
                
                fields={
                'doorSealMisMatchComment':{
                    'default':'',
                    'type':'string',
                },
                'doorSealMisMatchPermitted':{
                    'default':False,
                    'type':'boolean',
                },
                'doorSealMisMatchPermittedBy':{
                    'default':'string',
                    'type':'',
                },
                'photoSerialNo':{
                    'default':'',
                    'type':'string',
                },

                }
                msg=f"""
{'-'*os.get_terminal_size().columns}
NewSealId={log.NewSealId}
NewSealDate={log.NewSealDate}
NewSealEmployeeIdOrName={log.NewSealEmployeeIdOrName}
OldSealId={log.OldSealId}
OldSealDate={log.OldSealDate}
OldSealEmplyeeIdOrName={log.OldSealEmplyeeIdOrName}
dtoe={log.dtoe}
comment={log.comment}
doorSealMisMatch="{log.doorSealMisMatch}"   
doorSealMisMatchComment="{log.doorSealMisMatchComment}"
doorSealMisMatchPermitted="{log.doorSealMisMatchPermitted}"
doorSealMisMatchPermittedBy="{log.doorSealMisMatchPermittedBy}"
photoSerialNo={log.photoSerialNo}
{'*'*os.get_terminal_size().columns}
                """
                if log.doorSealMisMatch:
                    fd=FormBuilder(data=fields,passThruText=msg)
                    if fd is None:
                        return
                    else:
                        for k in fd:
                            if isinstance(fd[k],str):
                                if fd[k] is not None:
                                    if getattr(log,k) is not None:
                                        if fd[k] not in getattr(log,k):
                                            setattr(log,k,getattr(log,k,)+fd[k])
                                    else:
                                        setattr(log,k,fd[k])

                            else:
                                setattr(log,k,fd[k])

                    session.commit()
                    session.refresh(log)
                    print(log)
    

    def fix_table(self):
        DoorSealLog.__table__.drop(ENGINE)
        DoorSealLog.metadata.create_all(ENGINE)
        print("Done!")



    def newLog(self,door_seal_log=None):
        if door_seal_log:
            arg=True
        else:
            arg=False
        with Session(ENGINE) as session:
            excludes=['dslid',]
            provided=False
            print(door_seal_log)
            if door_seal_log is None:
                door_seal_log=DoorSealLog()
            else:
                provided=True

            if not provided:
                session.add(door_seal_log)
                session.commit()
                session.refresh(door_seal_log)
            else:
                door_seal_log=session.query(DoorSealLog).filter(DoorSealLog.dslid==door_seal_log.dslid).first()
            print(door_seal_log)

            fields={str(i.name):{'default':getattr(door_seal_log,i.name),'type':str(i.type).lower()} for i in door_seal_log.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(door_seal_log)
                session.commit()
                return
            for k in fb:
                setattr(door_seal_log,k,fb[k])
            door_seal_log.dtoe=datetime.now()
            session.commit()
            session.refresh(door_seal_log)
            print(door_seal_log)
            return door_seal_log
    '''
    def newLog(self,doorSealLogObj=None):
        if doorSealLogObj:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['dslid',]
            provided=False
            #print(doorSealLog,"#0")
            if doorSealLogObj is None:
                doorSealLog=DoorSealLog()
            else:
                doorSealLog=doorSealLogObj
                provided=True

            if not provided:
                session.add(doorSealLog)
                session.commit()
                session.refresh(doorSealLog)
            else:
                doorSealLog=session.query(doorSealLog).filter(doorSealLog.dslid==doorSealLogObj.dslid).first()
            #print(doorSealLog,'#1')

            fields={str(i.name):{'default':getattr(doorSealLog,i.name),'type':str(i.type).lower()} for i in doorSealLog.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(doorSealLog)
                session.commit()
                return
            for k in fb:
                setattr(doorSealLog,k,fb[k])
            doorSealLog.dtoe=datetime.now()
            session.commit()
            session.refresh(doorSealLog)
            #print(doorSealLog,'#2')
            return doorSealLog
    '''
    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f"""
{Fore.light_green}{'-'*os.get_terminal_size().columns}{Style.reset}
{Fore.light_green}NewSealId{Fore.light_yellow}="{i.NewSealId}"{Style.reset}
{Fore.light_green}NewSealDate{Fore.light_yellow}="{i.NewSealDate}"{Style.reset}
{Fore.light_green}NewSealEmployeeIdOrName{Fore.light_yellow}="{i.NewSealEmployeeIdOrName}"{Style.reset}
{Fore.orange_red_1}OldSealId{Fore.dark_goldenrod}="{i.OldSealId}"{Style.reset}
{Fore.orange_red_1}OldSealDate{Fore.dark_goldenrod}="{i.OldSealDate}"{Style.reset}
{Fore.orange_red_1}OldSealEmplyeeIdOrName{Fore.dark_goldenrod}="{i.OldSealEmplyeeIdOrName}"{Style.reset}
{Fore.light_cyan}dtoe{Fore.cyan}="{i.dtoe}{Style.reset}"
{Fore.light_cyan}comment{Fore.cyan}="{i.comment}{Style.reset}"
{Fore.light_red}doorSealMisMatch={Fore.grey_85}"{i.doorSealMisMatch}"   {Style.reset}
{Fore.light_red}doorSealMisMatchComment={Fore.grey_85}"{i.doorSealMisMatchComment}"{Style.reset}
{Fore.light_red}doorSealMisMatchPermitted={Fore.grey_85}"{i.doorSealMisMatchPermitted}"{Style.reset}
{Fore.light_red}doorSealMisMatchPermittedBy={Fore.grey_85}"{i.doorSealMisMatchPermittedBy}"{Style.reset}
{Fore.light_steel_blue}photoSerialNo={Fore.light_red}"{i.photoSerialNo}"{Style.reset}
{Fore.light_red}{'*'*os.get_terminal_size().columns}{Style.reset}
            """
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(DoorSealLog).filter(DoorSealLog.dslid==item.dslid).first()
                return self.newLog(door_seal_log=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(DoorSealLog).filter(DoorSealLog.dslid==item.dslid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(DoorSealLog)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(DoorSealLog).filter(filt)
            else:
                query=session.query(DoorSealLog)
            
            
            orderedQuery=orderQuery(query,DoorSealLog.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)



    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            },
            str(uuid1()):{
            'cmds':['validate','verify','v/v','vfy','vldt'],
            'exec':self.isSealValid,
            'desc':"Validate Seals"
            },
            str(uuid1()):{
            'cmds':['check seal','chk sl','chksl',],
            'exec':self.currentSealMatchesLastNewSeal,
            'desc':"check to see if current door seal is the last door seal logged."
            },
            
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}Door Seal Log Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")
def depreciation(): 
    manufacture_date=datetime(2024,11,23)
    expiration_date=datetime(2025,12,5)
    today=datetime.now()
    retail_price=2.99
    getRidOfPrice=0.25
    fields={
    'manufacture_date':{
    'default':manufacture_date,
    'type':'datetime',
    },
    'expiration_date':{
    'default':expiration_date,
    'type':'datetime'
    },
    'today':{
    'default':today,
    'type':'datetime'
    },
    'retail_price':{
    'default':retail_price,
    'type':'float'
    },
    'getRidOfPrice':{
    'default':getRidOfPrice,
    'type':'float'
    },
    }
    fd=FormBuilder(data=fields,passThruText="Product Details")
    if fd is None:
        return
    getRidOfPrice=fd['getRidOfPrice']
    manufacture_date=fd['manufacture_date']
    expiration_date=fd['expiration_date']
    today=fd['today']
    retail_price=fd['retail_price']

    timeLeft=expiration_date-today
    atMostTime=expiration_date-manufacture_date
    
    depreciationValue=1-(timeLeft/atMostTime)
    lostValue=retail_price*depreciationValue
    
    endZone=(timedelta(days=(timeLeft/lostValue).days/getRidOfPrice))
    toPriceAtAQuarter=expiration_date-endZone
    fireSale=retail_price-lostValue
    msg=f'''
{Fore.light_red}Depreciated By{Fore.grey_85}: {depreciationValue}{Style.reset}
{Fore.light_red}Lost Value{Fore.grey_85}: {lostValue}{Style.reset}

{Fore.light_yellow}FireSale{Fore.grey_85}: {fireSale}{Style.reset}
{Fore.light_green}Retail Price{Fore.grey_85}: {retail_price}{Style.reset}
{Fore.orange_red_1}GetRidOfPrice{Fore.grey_85}: {getRidOfPrice}{Style.reset}

{Fore.light_magenta}Expiration/Throw Out Date{Fore.grey_85}: {expiration_date}{Style.reset}
{Fore.light_cyan}Manufacture Or RX Date {Fore.grey_85}: {manufacture_date}{Style.reset}

{Fore.light_yellow}Time Left{Fore.grey_85}: {timeLeft}{Style.reset}
{Fore.light_steel_blue}Total Time{Fore.grey_85}: {atMostTime}{Style.reset}

{Fore.magenta}ToPriceAtAQuarter{Fore.grey_85}: {toPriceAtAQuarter}{Style.reset}
{Fore.cyan}TimeFromQuarterDollarPriceToExpiry{Fore.grey_85}: {endZone}{Style.reset}
    '''
    return msg
    


def TotalToComplete():
    msg='BareMinimumToComplete*DaysToComplete=TotalToComplete'
    while True:
        try:
            fields={
                'Bare Minimum To Complete':{
                'type':'float',
                'default':3.8333,
                },
                'Days To Complete':{
                'type':'float',
                'default':3
                },
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            

            value=fd['Bare Minimum To Complete']*timedelta(days=fd['Days To Complete']).days

            return value
        except Exception as e:
            print(e)


def DaysToComplete():
    msg='TotalToComplete/BareMinimumToComplete=DaysToComplete'
    while True:
        try:
            fields={
                'TotalToComplete':{
                'type':'float',
                'default':11.5,
                },
                'Bare Minimum To Complete':{
                'type':'float',
                'default':3
                },
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            

            value=timedelta(days=fd['TotalToComplete']/fd['Bare Minimum To Complete'])

            return value
        except Exception as e:
            print(e)

def BareMinimumToComplete():
    msg='TotalToComplete/DaysToComplete=BareMinimumToComplete'
    while True:
        try:
            fields={
                'TotalToComplete':{
                'type':'float',
                'default':11.5,
                },
                'Days To Complete':{
                'type':'float',
                'default':3
                },
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            

            value=fd['TotalToComplete']/fd['Days To Complete']

            return value
        except Exception as e:
            print(e)

def CheckInOut():
    msg='CheckIn/Store||CheckOut/Taken'
    while True:
        try:
            fields={
                'Pallet ID':{
                'type':'float',
                'default':11.5,
                },
                'Case ID':{
                'type':'float',
                'default':3
                },
                'stored||taken':{
                'default':'unspecified',
                'type':'string'
                }
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            

            value=f"Pallet Id:{fd['Pallet ID']} CaseId:{fd['Case ID']} stored||taken:{fd['stored||taken']}"

            return value
        except Exception as e:
            print(e)

def SpecificVolume():
    msg='Volume/Mass=SpecificVolume'
    while True:
        try:
            fields={
                'Volume':{
                'type':'string',
                'default':'0.5 oz',
                },
                'Mass':{
                'type':'string',
                'default':'1 gram'
                },
            }
            fd=FormBuilder(data=fields,passThruText=msg)
            if fd is None:
                return
                
            

            value=pint.Quantity(fd['Volume'])/pint.Quantity(fd['Mass'])
            print(f"{Fore.orange_red_1}{value}{Style.reset}")
            selector=[
            value,str(value),value.magnitude,value.units
            ]
            htext=[]
            cta=len(selector)
            for num,i in enumerate(selector):
                htext.append(std_colorize(f'{i} - {type(i)}',num,cta))
            htext='\n'.join(htext)
            which=Control(func=FormBuilderMkText,ptext=f"{htext}\nwhich index to use for return",helpText=htext,data="integer")
            if which is None:
                return
            check=[num for num,i in enumerate(selector)]
            if which not in check:
                return selector[-2]
            elif which in ['d',]:
                return selector[-2]
            else:
                return selector[which]

        except Exception as e:
            print(e)

class HeightWeightWaistLogger(BTemplate):
    

    def fix_table(self):
        HeightWeightWaist.__table__.drop(ENGINE)
        HeightWeightWaist.metadata.create_all(ENGINE)
        print("Done!")


    def newLog(self,HeightWeightWaistObj=None):
        if HeightWeightWaist:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['hwwid',]
            provided=False
            #print(HeightWeightWaist,"#0")
            if HeightWeightWaistObj is None:
                HeightWeightWaistObj=HeightWeightWaist()
            else:
                provided=True

            if not provided:
                session.add(HeightWeightWaistObj)
                session.commit()
                session.refresh(HeightWeightWaistObj)
            else:
                HeightWeightWaistObj=session.query(HeightWeightWaist).filter(HeightWeightWaist.hwwid==HeightWeightWaistObj.hwwid).first()
            #print(HeightWeightWaist,'#1')

            fields={str(i.name):{'default':getattr(HeightWeightWaistObj,i.name),'type':str(i.type).lower()} for i in HeightWeightWaistObj.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(HeightWeightWaistObj)
                session.commit()
                return
            for k in fb:
                setattr(HeightWeightWaistObj,k,fb[k])
            HeightWeightWaistObj.dtoe=datetime.now()
            session.commit()
            session.refresh(HeightWeightWaistObj)
            #print(HeightWeightWaist,'#2')
            return HeightWeightWaistObj

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            height=None
            try:
                height=pint.Quantity(i.Height,i.HeightUnit)
            except Exception as e:
                height=f"{i.Height} {i.HeightUnit}"
                print(e)

            weight=None
            try:
                weight=pint.Quantity(i.Weight,i.WeightUnit)
            except Exception as e:
                weight=f"{i.Weight} {i.WeightUnit}"
                print(e)

            waist=None
            try:
                waist=pint.Quantity(i.Waist,i.WaistUnit)
            except Exception as e:
                waist=f"{i.Waist} {i.WaistUnit}"
                print(e)

            msg=f"""
{Fore.light_green}{'*'*os.get_terminal_size().columns}{Style.reset}
{Fore.orange_red_1}Name:{Fore.medium_violet_red}"{i.Name}"
{Fore.light_green}Height:{Fore.light_cyan}"{height}"
{Fore.light_steel_blue}Weight:{Fore.light_yellow}"{weight}"
{Fore.light_red}Waist:{Fore.dark_goldenrod}"{waist}"
{Fore.orange_red_1}hwwid={Fore.light_green}"{i.hwwid}"
{Fore.cyan}dtoe={Fore.grey_85}"{i.dtoe}"
{Fore.cyan}comment={Fore.grey_85}"{i.comment}"
{Fore.magenta}{'-'*os.get_terminal_size().columns}{Style.reset}

            """
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(HeightWeightWaist).filter(HeightWeightWaist.hwwid==item.hwwid).first()
                return self.newLog(HeightWeightWaistObj=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(HeightWeightWaist).filter(HeightWeightWaist.hwwid==item.hwwid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(HeightWeightWaist)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(HeightWeightWaist).filter(filt)
            else:
                query=session.query(HeightWeightWaist)
            
            
            orderedQuery=orderQuery(query,HeightWeightWaist.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)
    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}Height Weight Waist Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")


class PieceCountLogger(BTemplate):
    

    def fix_table(self):
        PieceCount.__table__.drop(ENGINE)
        PieceCount.metadata.create_all(ENGINE)
        print("Done!")


    def newLog(self,PieceCountObj=None):
        if PieceCount:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['pcid',]
            provided=False
            #print(PieceCount,"#0")
            if PieceCountObj is None:
                PieceCountObj=PieceCount()
            else:
                provided=True

            if not provided:
                session.add(PieceCountObj)
                session.commit()
                session.refresh(PieceCountObj)
            else:
                PieceCountObj=session.query(PieceCount).filter(PieceCount.pcid==PieceCountObj.pcid).first()
            #print(PieceCount,'#1')

            fields={str(i.name):{'default':getattr(PieceCountObj,i.name),'type':str(i.type).lower()} for i in PieceCountObj.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(PieceCountObj)
                session.commit()
                return
            for k in fb:
                setattr(PieceCountObj,k,fb[k])
            PieceCountObj.dtoe=datetime.now()
            session.commit()
            session.refresh(PieceCountObj)
            #print(PieceCount,'#2')
            return PieceCountObj

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f"""
{Fore.light_green}{'*'*os.get_terminal_size().columns}{Style.reset}
{Fore.orange_red_1}Carts:{Fore.medium_violet_red}"{i.Carts}"
{Fore.light_green}Uboats:{Fore.light_cyan}"{i.Uboats}"
{Fore.light_steel_blue}Pallets:{Fore.light_yellow}"{i.Pallets}"
{Fore.light_magenta}Pallets:{Fore.light_red}"{i.Pallets}"
{Fore.orange_red_1}pcid={Fore.light_green}"{i.pcid}"
{Fore.cyan}dtoe={Fore.grey_85}"{i.dtoe}"
{Fore.cyan}comment={Fore.grey_85}"{i.comment}"
{Fore.magenta}{'-'*os.get_terminal_size().columns}{Style.reset}

            """
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(PieceCount).filter(PieceCount.pcid==item.pcid).first()
                return self.newLog(PieceCountObj=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(PieceCount).filter(PieceCount.pcid==item.pcid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(PieceCount)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(PieceCount).filter(filt)
            else:
                query=session.query(PieceCount)
            
            
            orderedQuery=orderQuery(query,PieceCount.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)
    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}PieceCount Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")


class LocalWeatherPatternLogger(BTemplate):
    def fix_table(self):
        LocalWeatherPattern.__table__.drop(ENGINE)
        LocalWeatherPattern.metadata.create_all(ENGINE)
        print("Done!")


    def newLog(self,LocalWeatherPatternObj=None):
        if LocalWeatherPattern:
            arg=True
        else:
            arg=False

        with Session(ENGINE) as session:
            excludes=['lwpid',]
            provided=False
            #print(LocalWeatherPattern,"#0")
            if LocalWeatherPatternObj is None:
                LocalWeatherPatternObj=LocalWeatherPattern()
            else:
                provided=True

            if not provided:
                session.add(LocalWeatherPatternObj)
                session.commit()
                session.refresh(LocalWeatherPatternObj)
            else:
                LocalWeatherPatternObj=session.query(LocalWeatherPattern).filter(LocalWeatherPattern.lwpid==LocalWeatherPatternObj.lwpid).first()
            #print(LocalWeatherPattern,'#1')

            fields={str(i.name):{'default':getattr(LocalWeatherPatternObj,i.name),'type':str(i.type).lower()} for i in LocalWeatherPatternObj.__table__.columns if i.name not in excludes}
            fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
            if fb in [None,]:
                if not arg:
                    session.delete(LocalWeatherPatternObj)
                session.commit()
                return
            for k in fb:
                setattr(LocalWeatherPatternObj,k,fb[k])
            LocalWeatherPatternObj.dtoe=datetime.now()
            session.commit()
            session.refresh(LocalWeatherPatternObj)
            #print(LocalWeatherPattern,'#2')
            return LocalWeatherPatternObj

    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''

        def tryComfort(value,unit):
            try:
                dp=pint.Quantity(value,unit)
                if dp <= pint.Quantity(54,"degF"):
                    return "Dry and comfortable (pleasant)"
                if dp >= pint.Quantity(55,"degF") and pint.Quantity <= pint.Quantity(65,"degF"):
                    return "Becoming 'sticky' or muggy"
                if dp > pint.Quantity(65,"degF"):
                    return "Humid, oppressive, and uncomfortable"
            except Exception as e:
                return str(e)

        def tryor(value,unit):
            try:
                return pint.Quantity(value,unit)
            except Exception as e:
                return f"{value} {unit}"

        for xnum,i in enumerate(data):
            fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
        %A(%d) of %B, 
        week[Business] %V of year %Y, 
        week[Sunday First] %U of year %Y, 
        week[Monday First] %W of year %Y) 
        @[12H] {Fore.light_cyan}%I:%M %p
        @[24H] {Fore.medium_violet_red}%H:%M""")

            msg=f"""
{Fore.light_green}{'*'*os.get_terminal_size().columns}{Style.reset}
    {Fore.green}location={Fore.grey_85}"{i.location}"{Style.reset}
    {Fore.green}geolocation={Fore.grey_85}"{i.geolocation}"{Style.reset}
    {Fore.green}elevation={Fore.grey_85}"{tryor(i.elevation,i.elevation_unit)}"{Style.reset}
    {Fore.green}elevation_reference={Fore.grey_85}"{i.elevation_reference}"{Style.reset}
    {Fore.dark_green}lwpid={Fore.grey_85}"{i.lwpid}"{Style.reset}
    {Fore.light_steel_blue}precip={Fore.grey_85}"{tryor(i.precip,i.precip_unit)}"{Style.reset}
    {Fore.orange_red_1}current_temp={Fore.grey_85}"{tryor(i.current_temp,i.current_temp_unit)}"{Style.reset}
    {Fore.orange_red_1}high_temp={Fore.grey_85}"{tryor(i.high_temp,i.high_temp_unit)}"{Style.reset}
    {Fore.light_cyan}low_temp={Fore.grey_85}"{tryor(i.low_temp,i.low_temp_unit)}"{Style.reset}
    {Fore.sky_blue_1}atmo_pressure={Fore.grey_85}"{tryor(i.atmo_pressure,i.atmo_pressure_unit)}"{Style.reset}
    {Fore.magenta}wind_speed={Fore.grey_85}"{tryor(i.wind_speed,i.wind_speed_unit)}"{Style.reset}
    {Fore.magenta}wind_direction={Fore.grey_85}{i.wind_direction}"{Style.reset}
    {Fore.light_yellow}humidity={Fore.grey_85}"{i.humidity}"{Style.reset}
    {Fore.light_yellow}dew_point={Fore.grey_85}"{tryor(i.dew_point,i.dew_point_unit)}"{Style.reset}
    {Fore.light_yellow}General Comfort="{Fore.grey_85}{tryComfort(i.dew_point,i.dew_point_unit)}"{Style.reset}
    {Fore.light_yellow}dawn_dtoe={Fore.grey_85}"{i.dawn_dtoe}"{Style.reset}
    {Fore.light_red}dusk_dtoe={Fore.grey_85}"{i.dusk_dtoe}"{Style.reset}
    {Fore.light_green}sunrise_dtoe={Fore.grey_85}"{i.sunrise_dtoe}"{Style.reset}
    {Fore.red}sunset_dtoe={Fore.grey_85}"{i.sunset_dtoe}"{Style.reset}
    {Fore.dark_goldenrod}UV_Index={Fore.grey_85}"{i.UV_Index}"{Style.reset}
    {Fore.green_yellow}dtoe={Fore.grey_85}"{i.dtoe}"{Style.reset}
    {Fore.cyan}DTOE_PROCESSED="{fmtd}"
    {Fore.tan}comment={Fore.grey_85}"{i.comment}"{Style.reset}
{Fore.magenta}{'-'*os.get_terminal_size().columns}{Style.reset}"""
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)


    def edit_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(LocalWeatherPattern).filter(LocalWeatherPattern.lwpid==item.lwpid).first()
                return self.newLog(LocalWeatherPatternObj=log)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(LocalWeatherPattern).filter(LocalWeatherPattern.lwpid==item.lwpid).first()
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def search_and_menu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(LocalWeatherPattern)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(LocalWeatherPattern).filter(filt)
            else:
                query=session.query(LocalWeatherPattern)
            
            
            orderedQuery=orderQuery(query,LocalWeatherPattern.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(results,False)
            else:
                htext=self.long_view(results,False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove']
                        try:
                            if short:
                                l=self.short_view([log,],False,num)
                            else:
                                l=self.long_view([log,],False,num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)

    def graphSunrise2Dawn(self):
        with Session(ENGINE) as session:
            query=session.query(LocalWeatherPattern)
            ordered=orderQuery(query,LocalWeatherPattern.dtoe)
            q=ordered
            results=ordered.all()
            cta=len(results)
            selector=['Dawn2SunRise','SunSet2Dusk','SunRise2SunSet','Dawn2Dusk']
            helpText=[]
            ct=len(selector)
            for num,i in enumerate(selector):
                helpText.append(std_colorize(f"{i}",num,ct))
            helpText='\n'.join(helpText)
            l1=True
            l2=True
            l3=True
            l4=True
            which=Control(func=FormBuilderMkText,ptext=f"{helpText}\n| Which indexes",helpText=f"a list of indexes {helpText}",data="list")
            if which in [None,'NAN']:
                return
            elif which in ['d','',[]]:
                l1=True
                l2=True
                l3=True
                l4=True
            else:
                which=tuple(set(which))
                if '0' not in which:
                    l1=False
                if '1' not in which:
                    l2=False
                if '2' not in which:
                    l3=False
                if '3' not in which:
                    l4=False

            tool=[]
            for num,i in enumerate(results):
                if num % 2 == 0 and num > 0:
                    s=' * '
                    p=' /'
                else:
                    s=' - '
                    p=' + '
                if i.sunrise_dtoe is not None and i.dawn_dtoe is not None and l1:
                    tool.append(f"{p}{i.dtoe} Dawn2SunRise: {i.sunrise_dtoe-i.dawn_dtoe}{s}")
                if i.sunset_dtoe is not None and i.dusk_dtoe is not None and l2:
                    tool.append(f"{p}{i.dtoe} SunSet2Dusk: {i.dusk_dtoe-i.sunset_dtoe}{s}")
                if i.sunset_dtoe is not None and i.sunrise_dtoe is not None and l3:
                    tool.append(f"{p}{i.dtoe} SunRise2SunSet: {i.sunset_dtoe-i.sunrise_dtoe}{s}")
                if i.dawn_dtoe is not None and i.dusk_dtoe is not None and l4:
                    tool.append(f"{p}{i.dtoe} Dawn2Dusk: {i.dusk_dtoe-i.dawn_dtoe}{s} Night Length: {timedelta(hours=24)-(i.dusk_dtoe-i.dawn_dtoe)}")

            for num,i in enumerate(tool):
                print(std_colorize(i,num,cta))

    def __init__(self):
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['sunrise2dawn','sr2dwn'],
            'exec':self.graphSunrise2Dawn,
            'desc':"review sunrise to dawn timedelta!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':self.search_and_menu,
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            
            str(uuid1()):{
            'cmds':['new log','new','new temp log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            }
        }
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))
        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}LocalWeatherPattern Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")


def RandomPrice(base=0,top=75,envelope_max=0.1,decimals=6):
    with localcontext() as ctx:
        ctx.prec=decimals
        rfloat=random.uniform(base,top)
        envelop=random.uniform(rfloat,rfloat+(rfloat*envelope_max))
        return Decimal(rfloat)*1

def RandomCustomerPayment(base=0,top=75,envelope_max=0.1,decimals=6,price=RandomPrice()):
    with localcontext() as ctx:
        ctx.prec=decimals
        if price is None:
            rfloat=random.uniform(base,top)
        else:
            rfloat=float(price)
        envelop=random.uniform(rfloat,rfloat+(rfloat*envelope_max))
        print(f"""Price was: {price}!
Customer Paid: {Decimal(envelop)*1}
Their Change is: {(Decimal(envelop)*1)-(Decimal(rfloat)*1)}
            """)
        return Decimal(envelop)*1

def RandomChange(base=0,top=75,envelope_max=0.1,decimals=6,price=RandomPrice()):
    with localcontext() as ctx:
        ctx.prec=decimals
        if price is None:
            rfloat=random.uniform(base,top)
        else:
            rfloat=float(price)
        envelop=random.uniform(rfloat,rfloat+(rfloat*envelope_max))
        print(f"""Price was: {price}!
Customer Paid: {Decimal(envelop)*1}
Their Change is: {(Decimal(envelop)*1)-(Decimal(rfloat)*1)}
            """)
        return (Decimal(envelop))-(Decimal(rfloat))



class ModelLogger(BTemplate):
    def fix_table(self):
        last_log_fix_dtoe=detectGetOrSet(f"{self.__class__.__name__}.{self.Model} fixed_table_date",datetime.now(),setValue=False,literal=True)
        p=protect(self,pt=f"{Fore.light_red}Really {Fore.light_steel_blue} Factory RESET{Fore.light_yellow} the table[LastFactoryReset={last_log_fix_dtoe}]?{Style.reset}")
        if p:
            print(f"{Fore.light_red}User {Fore.light_steel_blue}was-using/{Fore.cyan}is-using/{Fore.light_yellow}used{Fore.light_magenta} protection!{Style.reset}")
            return
        last_log_fix_dtoe=detectGetOrSet(f"{self.__class__.__name__}.{self.Model} fixed_table_date",datetime.now(),setValue=True,literal=True)
        print(f"{Fore.orange_red_1}Last Factory RESET = '{Fore.light_steel_blue}{last_log_fix_dtoe}{Style.reset}'")
        self.Model.__table__.drop(ENGINE)
        self.Model.metadata.create_all(ENGINE)
        dotdot='....'
        sleepers=[f"{Fore.light_green}",f"{Fore.light_yellow}",f"{Fore.orange_red_1}",f"{Fore.light_red}"]
        sleeper=''
        msg=''
        for num,i in enumerate(dotdot):
            TIME.sleep(0.3)
            sleeper=sleepers[num]
            msg=f"{sleeper}Checking for stragglers{'.'*num}"
            print(msg)
        if num >= (len(dotdot)-1):
            print(f"{Fore.light_cyan}")
        with Session(ENGINE) as session:
            print(session.query(self.Model).count(),"Logs Found!")
        print("Done!")

    def random_result(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for random result :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            results=session.query(self.Model).order_by(func.random()).first()
            msg=std_colorize(results,0,1)
            print(msg)
    
    def listUniq(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for unique values list :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            results=session.query(self.Model).group_by(getattr(self.Model,fields[xaxis][0])).all()
            cta=len(results)
            for num,i in enumerate(results):
                msg=std_colorize(i,num,cta)
                print(msg)

    def histograph_log(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for x axis :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            '''
            print(htext)
            yaxis=Control(func=FormBuilderMkText,ptext="index for y axis :",helpText=f"{htext}\nan integer",data="integer")
            if yaxis in [None,'NAN','NaN','nan']:
                return
            elif yaxis in ['d','']:
                return
            if yaxis not in indexs:
                return
            '''

            bins=Control(func=FormBuilderMkText,ptext="bins:",helpText=f"{htext}\nan integer",data="integer")
            if bins in [None,'NAN','NaN','nan']:
                return
            elif bins in ['d','']:
                return

            query=self.search_and_menu(menu=False,short=True,returnQuery=True)

            df=pd.read_sql_query(sql=query.statement,con=session.bind)
            df=df.fillna(0)
            if not isinstance(df,pd.DataFrame):
                print(f"df was '{df}:{type(df)}'")
                return
            if len(df) > 0:
                for col_name, dtype in df.dtypes.items():
                    try:
                        if pd.api.types.is_datetime64_any_dtype(dtype):
                            # Create a new column with '_ts' suffix
                            df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                            # Optionally, replace the original column
                            #df[col_name] = df[col_name].astype(np.int64) // 10**9
                            #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                            df[col_name]=df[col_name].apply(modx) #here
                        elif pd.api.types.is_string_dtype(dtype):
                            df[col_name]=df[col_name].apply(justValue)
                    except Exception as e:
                        print(e)
                data=df[[fields[xaxis][0]]]
                #,fields[yaxis][0],]]

                x=df[fields[xaxis][0]].tolist()
                #y=df[fields[yaxis][0]].tolist()

                plt.hist(x,bins=bins,label=f"{fields[xaxis][0]} / {bins}")
                plt.show()
                plt.clf()
            else:
                print("no results!")


    def bar_log(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for x axis :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            
            print(htext)
            yaxis=Control(func=FormBuilderMkText,ptext="index for y axis :",helpText=f"{htext}\nan integer",data="integer")
            if yaxis in [None,'NAN','NaN','nan']:
                return
            elif yaxis in ['d','']:
                return
            if yaxis not in indexs:
                return
            '''

            bins=Control(func=FormBuilderMkText,ptext="bins:",helpText=f"{htext}\nan integer",data="integer")
            if bins in [None,'NAN','NaN','nan']:
                return
            elif bins in ['d','']:
                return
            '''
            query=self.search_and_menu(menu=False,short=True,returnQuery=True)

            df=pd.read_sql_query(sql=query.statement,con=session.bind)
            df=df.fillna(0)
            if not isinstance(df,pd.DataFrame):
                print(f"df was '{df}:{type(df)}'")
                return
            if len(df) > 0:
                for col_name, dtype in df.dtypes.items():
                    try:
                        if pd.api.types.is_datetime64_any_dtype(dtype):
                            # Create a new column with '_ts' suffix
                            df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                            # Optionally, replace the original column
                            #df[col_name] = df[col_name].astype(np.int64) // 10**9
                            #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                            df[col_name]=df[col_name].apply(modx) #here
                        elif pd.api.types.is_string_dtype(dtype):
                            df[col_name]=df[col_name].apply(justValue)
                    except Exception as e:
                        print(e)

                data=df[[fields[xaxis][0],fields[yaxis][0]]]

                x=df[fields[xaxis][0]].tolist()
                y=df[fields[yaxis][0]].tolist()

                plt.bar(x,y,label=f"{fields[xaxis][0]} / {fields[yaxis][0]}")
                plt.show()
                plt.clf()
            else:
                print("no results!")

    def avg_field(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for x axis :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            '''

            bins=Control(func=FormBuilderMkText,ptext="bins:",helpText=f"{htext}\nan integer",data="integer")
            if bins in [None,'NAN','NaN','nan']:
                return
            elif bins in ['d','']:
                return
            '''
            query=self.search_and_menu(menu=False,short=True,returnQuery=True)

            df=pd.read_sql_query(sql=query.statement,con=session.bind)
            df=df.fillna(0)
            if not isinstance(df,pd.DataFrame):
                print(f"df was '{df}:{type(df)}'")
                return
            try:
                adf=df.copy()
                span=adf['dtoe'].max()-adf['dtoe'].min()
            except Exception as e:
                print(e)
                span=None
            if len(df) > 0:
                for col_name, dtype in df.dtypes.items():
                    try:
                        if pd.api.types.is_datetime64_any_dtype(dtype):
                            # Create a new column with '_ts' suffix
                            df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                            # Optionally, replace the original column
                            #df[col_name] = df[col_name].astype(np.int64) // 10**9
                            #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                            df[col_name]=df[col_name].apply(modx) #here
                        elif pd.api.types.is_string_dtype(dtype):
                            df[col_name]=df[col_name].apply(justValue)
                    except Exception as e:
                        print(e)

                

                x=df[fields[xaxis][0]]
                msg=f"""
Span of Data:
Span: {span}
pandas.DataFrame[.mean(),.min(),.max()]:
MEAN: {x.mean()}
MAX: {x.max()}
MIN: {x.min()}
numpy.average()[.mean(),.min(),.max()]:
AVG:  {np.average(x.tolist())}
MAX:  {np.max(x.tolist())}
MIN:  {np.min(x.tolist())}

                """
                #.tolist()
                print(msg)
                
            else:
                print("no results!")

    def forecasting_naive(self):
        def select_column_dtoe(df,self=self):
            try:
                df['dtoe'] = pd.to_datetime(df['dtoe'])
                df.set_index('dtoe', inplace=True)
                return df
            except KeyError as e:
                names=[]
                htext=[]
                ct=len(df.columns)
                for num,c in enumerate(df.columns):
                    names.append(c)
                    htext.append(std_colorize(f"{c}:{df[c].dtype.name}",num,ct))
                htext='\n'.join(htext)
                while True:
                    which=Control(ptext=f"{htext}\nWhich Column would you like to substitue with for 'dtoe'?",helpText="select an integer index",data="integer")
                    if which in BooleanAnswers.NONE:
                        return
                    if which in range(0,len(names)):
                        df[names[which]]=pd.to_datetime(df[names[which]])
                        df['dtoe']=df[names[which]].copy()
                        df.set_index('dtoe', inplace=True)
                    else:
                        continue
                        
                    return df

                    #df['datetime']=pd.to_datetime(df['dtoe'])
            except:
                print("No Valid DateTime Column Found")
                return

        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for x axis :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            '''

            bins=Control(func=FormBuilderMkText,ptext="bins:",helpText=f"{htext}\nan integer",data="integer")
            if bins in [None,'NAN','NaN','nan']:
                return
            elif bins in ['d','']:
                return
            '''
            query=self.search_and_menu(menu=False,short=True,returnQuery=True)
            if query in BooleanAnswers.NONE:
                print(f"df was '{df}:{type(df)}'")
                return
            df=pd.read_sql_query(sql=query.statement,con=session.bind)
            df=df.fillna(0)
            df=select_column_dtoe(df)
            if not isinstance(df,pd.DataFrame):
                print(f"df was '{df}:{type(df)}'")
                return
            try:
                adf=df.copy()
                span=adf['dtoe'].max()-adf['dtoe'].min()
            except Exception as e:
                print(e)
                span=None
            if len(df) > 0:
                for col_name, dtype in df.dtypes.items():
                    try:
                        if pd.api.types.is_datetime64_any_dtype(dtype):
                            # Create a new column with '_ts' suffix
                            df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                            # Optionally, replace the original column
                            #df[col_name] = df[col_name].astype(np.int64) // 10**9
                            #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                            df[col_name]=df[col_name].apply(modx) #here
                        elif pd.api.types.is_string_dtype(dtype):
                            df[col_name]=df[col_name].apply(justValue)
                    except Exception as e:
                        print(e)

                

                MovingAveragePrice = df[fields[xaxis][0]].tail(3).mean()
                try:
                    fieldName=fields[xaxis][0]
                except Exception as e:
                    print(e)
                    return
                def linear_regression(df,key,self=self,fieldName=fieldName):
                    try:
                        span=Control(ptext="Span N-Days [24-hours updates 5-3,default=3]",helpText="N-day moving average",data="integer")
                        if span in BooleanAnswers.NONE or span in ['d','']:
                            span=3


                        df['Day'] = range(len(df))

                        # Compute the trend slope and intercept using pure pandas
                        slope = df['Day'].cov(df[key]) / df['Day'].var()
                        intercept = df[key].mean() - slope * df['Day'].mean()

                        # Predict the next day's price
                        next_day_index = len(df)
                        predicted_price = (slope * next_day_index) + intercept

                        print(f"")
                        
                        ewma_series = df[key].ewm(span=span, adjust=False).mean()

                        # The last value in the EWMA series serves as the prediction for the next period
                        predicted_ewma_price = ewma_series.iloc[-1]


                        return f"""
Linear Regression (EWM Price)[{fieldName}]:
    slope = {slope:.3f}
    intercept = {intercept:.3f}
    Predicted Trend Price/Value[{fieldName}] for Day {next_day_index}: {predicted_price:.3f}
    Predicted EWMA Price/Value[{fieldName}]: {predicted_ewma_price:.3f}"""
                    except Exception as e:
                        return str(e),repr(e)
                    
                def seasonal_lag_regression(df,key,self=self,fieldName=fieldName):
                    try:
                        #df=select_column_dtoe(df)

                        # 2. Extract day of the week (0=Monday, 6=Sunday)
                        df['Day_of_Week'] = df.index.dayofweek

                        # 3. Create the 24-hour lag feature (yesterday's price)
                        df[f'Yesterday_{key}'] = df[key].shift(1)
                        df_clean = df.dropna()
                        prediction_standard_error = df_clean[key].std()

                        # 4. Calculate the base mathematical trend (Autoregression)
                        slope = df_clean[f'Yesterday_{key}'].cov(df_clean[key]) / df_clean[f'Yesterday_{key}'].var()
                        intercept = df_clean[key].mean() - slope * df_clean[f'Yesterday_{key}'].mean()

                        # 5. Calculate day-of-week adjustment factors using pure pandas grouping
                        # This finds how much each specific day typically deviates from the general average
                        global_mean = df_clean[key].mean()
                        day_averages = df_clean.groupby('Day_of_Week')[key].mean()
                        day_adjustments = day_averages - global_mean

                        # 6. Predict tomorrow's price
                        latest_date = df.index[-1]
                        next_date = latest_date + pd.Timedelta(days=1)
                        next_day_of_week = next_date.dayofweek
                        latest_price = df[key].iloc[-1]

                        # Base prediction from yesterday + seasonal adjustment for tomorrow's day of the week
                        base_pred = (slope * latest_price) + intercept
                        seasonal_adjustment = day_adjustments.get(next_day_of_week,0.0)

                        # 6. Generate the ranges
                        # Standard range (68% confident the price falls here)
                        low_68 = base_pred - prediction_standard_error
                        high_68 = base_pred + prediction_standard_error

                        # Wider range (95% confident the price falls here)
                        low_95 = base_pred - (2 * prediction_standard_error)
                        high_95 = base_pred + (2 * prediction_standard_error)
                        #.loc[next_day_of_week]
                        predicted_price = base_pred + seasonal_adjustment

                        msg=f"""
Seasonal Lag Regression[{fieldName}]:
    slope = {slope:.3f}
    std error = {prediction_standard_error:.3f}
    Latest Date ({latest_date.strftime('%Y-%m-%d')}): {latest_price:.3f}
    Predicted Price/Value[{fieldName}] for Tomorrow ({next_date.strftime('%Y-%m-%d')}, Day {next_day_of_week}): {predicted_price:.3f}
    Ranged:
        low_68[{fieldName}] = {low_68:.3f}
        high_68[{fieldName}] = {high_68:.3f}

        low_95[{fieldName}] = {low_95:.3f}
        high_95[{fieldName}] = {high_95:.3f}
                        """
                        return msg
                    except Exception as e:
                        return str(e),repr(e)

                msg=f"""
Predicted Moving Average Price|Value/Naive Forecast [{fieldName}]:
    {MovingAveragePrice}
    {linear_regression(df,fields[xaxis][0])}
    {seasonal_lag_regression(df,fields[xaxis][0])}
    """
                #.tolist()
                print(msg)
                
            else:
                print("no results!")

    def scatter_log(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for x axis :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            
            print(htext)
            yaxis=Control(func=FormBuilderMkText,ptext="index for y axis :",helpText=f"{htext}\nan integer",data="integer")
            if yaxis in [None,'NAN','NaN','nan']:
                return
            elif yaxis in ['d','']:
                return
            if yaxis not in indexs:
                return
            '''

            bins=Control(func=FormBuilderMkText,ptext="bins:",helpText=f"{htext}\nan integer",data="integer")
            if bins in [None,'NAN','NaN','nan']:
                return
            elif bins in ['d','']:
                return
            '''
            query=self.search_and_menu(menu=False,short=True,returnQuery=True)

            df=pd.read_sql_query(sql=query.statement,con=session.bind)
            df=df.fillna(0)
            if not isinstance(df,pd.DataFrame):
                print(f"df was '{df}:{type(df)}'")
                return
            if len(df) > 0:
                for col_name, dtype in df.dtypes.items():
                    try:
                        if pd.api.types.is_datetime64_any_dtype(dtype):
                            # Create a new column with '_ts' suffix
                            df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                            # Optionally, replace the original column
                            #df[col_name] = df[col_name].astype(np.int64) // 10**9
                            #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                            df[col_name]=df[col_name].apply(modx) #here
                        elif pd.api.types.is_string_dtype(dtype):
                            df[col_name]=df[col_name].apply(justValue)
                    except Exception as e:
                        print(e,str(e),repr(e))

                data=df[[fields[xaxis][0],fields[yaxis][0]]]

                x=df[fields[xaxis][0]].tolist()
                y=df[fields[yaxis][0]].tolist()

                plt.scatter(x,y,label=f"{fields[xaxis][0]} / {fields[yaxis][0]}")
                plt.show()
                plt.clf()
            else:
                print("no results!")

    def line_log(self):
        with Session(ENGINE) as session:
            #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
            excludes=[]
            fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
            indexs=[num[0] for num in enumerate(fields)]
            print(fields,excludes)
            htext=[]
            cta=len(fields)
            for num,i in enumerate(fields):
                htext.append(std_colorize(i,num,cta))
            htext='\n'.join(htext)
            print(htext)

            xaxis=Control(func=FormBuilderMkText,ptext="index for x axis :",helpText=f"{htext}\nan integer",data="integer")
            if xaxis in [None,'NAN','NaN','nan']:
                return
            elif xaxis in ['d','']:
                return
            if xaxis not in indexs:
                return

            
            print(htext)
            yaxis=Control(func=FormBuilderMkText,ptext="index for y axis :",helpText=f"{htext}\nan integer",data="integer")
            if yaxis in [None,'NAN','NaN','nan']:
                return
            elif yaxis in ['d','']:
                return
            if yaxis not in indexs:
                return
            '''

            bins=Control(func=FormBuilderMkText,ptext="bins:",helpText=f"{htext}\nan integer",data="integer")
            if bins in [None,'NAN','NaN','nan']:
                return
            elif bins in ['d','']:
                return
            '''
            query=self.search_and_menu(menu=False,short=True,returnQuery=True)

            df=pd.read_sql_query(sql=query.statement,con=session.bind)
            df=df.fillna(0)
            if not isinstance(df,pd.DataFrame):
                print(f"df was '{df}:{type(df)}'")
                return
            if len(df) > 0:
                print("results are in...")
                for col_name, dtype in df.dtypes.items():
                    try:
                        if pd.api.types.is_datetime64_any_dtype(dtype):
                            # Create a new column with '_ts' suffix
                            df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                            # Optionally, replace the original column
                            #df[col_name] = df[col_name].astype(np.int64) // 10**9
                            #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                            df[col_name]=df[col_name].apply(modx) #here
                        elif pd.api.types.is_string_dtype(dtype):
                            df[col_name]=df[col_name].apply(justValue)
                    except Exception as e:
                        print(e,str(e),repr(e))
                        print(col_name)
                
                x=df[fields[xaxis][0]].tolist()
                y=df[fields[yaxis][0]].tolist()

                plt.plot(x,y,label=f"{fields[xaxis][0]} / {fields[yaxis][0]}")
                plt.show()
                plt.clf()
            else:
                print("No Results!")

    def within_dtoes(self):
        try:
            while True:
                try:
                    now=datetime.now()
                    fields={
                    "start dtoe":{
                        'type':'datetime',
                        'default':now-timedelta(days=14)
                    },
                    "end dtoe":{
                        'type':'datetime',
                        'default':now
                    }
                    }
                    fb=FormBuilder(data=fields)
                    if fb in [None,]:
                        return

                    with Session(ENGINE) as session:
                        query=session.query(self.Model).filter(
                            self.Model.dtoe >= fb['start dtoe'],
                            self.Model.dtoe <= fb['end dtoe']
                            )
                        query=orderQuery(query,self.Model.dtoe)
                        results=query.all()
                        cta=len(results)
                        if cta < 1:
                            print(f"{Fore.orange_red_1}No Results!{Style.reset}")
                            return
                        for num, i in enumerate(results):
                            msg=std_colorize(i,num,cta)
                            print(msg)
                        return
                except Exception as ee:
                    print(ee)

        except Exception as e:
            print(e)
            return


    def newLog(self,ModelObj=None):
        original=deepcopy(ModelObj)
        provided=None
        batch=None
        defaults={}
        while True:
            if self.Model:
                arg=True
            else:
                arg=False

            with Session(ENGINE) as session:
                idtext=[i for i in dir(self.Model) if 'primary_key' in [x for x in dir(getattr(self.Model,i))] and getattr(getattr(self.Model,i),'primary_key') and not i.startswith('__')][0]
                print(idtext)
                excludes=[idtext,]
                provided=False
                #print(Model,"#0")
                if ModelObj is None:
                    ModelObj=self.Model()
                else:
                    provided=True

                if not provided:
                    session.add(ModelObj)
                    session.commit()
                    session.refresh(ModelObj)
                else:
                    ModelObj=session.query(self.Model).filter(getattr(self.Model,idtext)==getattr(ModelObj,idtext)).first()
                #print(Model,'#1')

                if defaults == {}:
                    fields={str(i.name):{'default':getattr(ModelObj,i.name),'type':str(i.type).lower()} for i in ModelObj.__table__.columns if i.name not in excludes}
                else:
                    fields=defaults
                fb=FormBuilder(data=fields,passThruText="if you see #UNUS, then only state that info if it is needed!")
                if fb in [None,]:
                    #if not arg:
                    if original in [None,]:
                        session.delete(ModelObj)
                        session.commit()
                    return
                for k in fb:
                    setattr(ModelObj,k,fb[k])
                    defaults[k]={'type':fields[k]['type'],'default':fb[k]}
                if ModelObj.dtoe in BooleanAnswers.NONE:               
                    ModelObj.dtoe=datetime.now()
                if 'dtoe' in set(fb.keys()):
                    if (ModelObj.dtoe != fb['dtoe']) and (fb['dtoe'] not in BooleanAnswers.NONE):
                        ModelObj.dtoe=fb['dtoe']
                
                session.commit()
                session.refresh(ModelObj)
                print('='*os.get_terminal_size().columns,original,ModelObj)
                print("Short View |"+'.'*(os.get_terminal_size().columns-len("Short View |")))
                a=self.short_view(self,data=[ModelObj,],printToScreen=True)
                #print(Model,'#2')
                another=Control(func=FormBuilderMkText,ptext="another line/log?",helpText="yes/no",data="boolean")
                if not provided:
                    if another in ['NAN','NaN',None,False]:
                        return ModelObj
                    else:
                        ModelObj=None
                        provided=False

                        continue
                else:
                    return ModelObj


    def short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''

        

        for xnum,i in enumerate(data):
            fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
        %A(%d) of %B, 
        week[Business] %V of year %Y, 
        week[Sunday First] %U of year %Y, 
        week[Monday First] %W of year %Y) 
        @[12H] {Fore.light_cyan}%I:%M %p
        @[24H] {Fore.medium_violet_red}%H:%M""")

            msg=f"""
            Short View Not Ready - {i}
"""
            if not num:
                m=std_colorize(msg,xnum,ct)
            else:
                m=std_colorize(msg,num,ct)
            xtext.append(m)
            if printToScreen:            
                print(m)
        return '\n'.join(xtext)

    def long_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        for numx,i in enumerate(data):
            if not num:
                m=std_colorize(i,numx,ct)
            else:
                m=std_colorize(i,num,ct)
            xtext.append(m)
            if printToScreen:
                print(m)
        return '\n'.join(xtext)

    def primaryKey(self,item):
        v=inspect(item).mapper.primary_key
        return v

    def edit_id(self,item):
        try:
            protection=db.protect(self,pt=f"{Fore.light_green}Un-{Fore.light_yellow}Protect from {Fore.orange_red_1}Editing?{Fore.light_yellow}")
            if protection:
                return item
            with Session(ENGINE) as session:
                #log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
                return self.newLog(ModelObj=item)
        except Exception as e:
            print(e)
            return item
        pass

    def delete_id(self,item):
        try:
            protection=db.protect(self,pt=f"{Fore.light_green}Un-{Fore.light_yellow}Protect from {Fore.orange_red_1}Deletion?{Fore.light_yellow}")
            if protection:
                return item
            with Session(ENGINE) as session:
                log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
                print(log)
                session.delete(log)
                session.commit()
        except Exception as e:
            print(e)
            return item
        pass

    def delete_by_id(self):
        #return 'Not User Ready yet'
        try:
            idx=Control(FormBuilderMkText,ptext="Delete what ID?",helpText="an integer id to delete",data="integer")
            if idx in [None,'NAN','NaN','','d']:
                return
            else:
                with Session(ENGINE) as session:
                    print(self.primaryKey(self.Model))
                    query=session.query(self.Model).filter(getattr(self.Model,str(self.primaryKey(self.Model)[0]).split(".")[-1])==int(idx))

                    log=query.first()
                    print(log,idx)
                    protection=db.protect(self,pt=f"{Fore.light_green}Un-{Fore.light_yellow}Protect from {Fore.orange_red_1}Deletion?{Fore.light_yellow}")
                    if protection:
                        return
                    session.delete(log)
                    session.commit()
                    session.flush()
        except Exception as e:
            print(e)

    def edit_by_id(self):
        #return 'Not User Ready yet'
        try:
            idx=Control(FormBuilderMkText,ptext="Edit what ID?",helpText="an integer id to delete",data="integer")
            if idx in [None,'NAN','NaN','','d']:
                return
            else:
                with Session(ENGINE) as session:
                    
                    query=session.query(self.Model).filter(getattr(self.Model,str(self.primaryKey(self.Model)[0]).split(".")[-1])==int(idx))

                    log=query.first()
                    if log:
                        print(f"{self.primaryKey(self.Model)[0]} = '{getattr(log,str(self.primaryKey(self.Model)[0]).split(".")[-1])}'")
                    self.edit_id(log)
                    session.commit()
                    session.refresh(log)
                    print(log)
                    session.flush()
        except Exception as e:
            print(e)

    def search_and_menu(self,menu=False,short=True,returnQuery=False):
        fbd=None
        with Session(ENGINE) as session:
            between=Control(ptext="between two dates?",helpText="a boolean value[default is YES]",data="boolean")
            if between in BooleanAnswers.NONE:
                return
            elif between in BooleanAnswers.YES_defaulted:
                fields={
                        'start':{
                        'type':'datetime',
                        'default':today()
                        },
                        'end':{
                        'type':'datetime',
                        'default':datetime.now()
                        }
                    }
                fbd=FormBuilder(data=fields)
                if fbd in [None,]:
                    return
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            if fbd != None:
                query=query.filter(self.Model.dtoe.between(fbd['start'],fbd['end']))
            try:
                orderedQuery=orderQuery(query,self.Model.dtoe)
            except Exception as e:
                print(e,"try 1")

            print("OrderQuery Passed!")
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            print('QueryLimit Passed!')
            if returnQuery:
                print(limited,type(limited))
                return limited
            
            while True:
                results=limited.all()
                if len(results) < 1:
                    create_new=Control(func=FormBuilderMkText,ptext="No results were found! Create New? [Y/N]",helpText=f"{BooleanAnswers.no} or {BooleanAnswers.yes}",data="boolean")
                    if create_new in [None,'NaN','NAN',False]:
                        return
                    if create_new in ['',True]:
                        self.newLog()
                        continue
                if short:
                    htext=self.short_view(self=self,data=results,printToScreen=False)
                else:
                    htext=self.long_view(data=results,printToScreen=False)

                if menu:
                    #next update
                    cta=len(results)
                    gotoNext=None
                    for num,log in enumerate(results):
                        if log == None:
                            continue
                        while True:
                            if log is None:
                                gotoNext=True
                                break
                            
                            cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo','refresh and print=rfshp/refresh and print/pcont/pcntu/print continue']
                            try:
                                if short:
                                    l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                                else:
                                    l=self.long_view(data=[log,],printToScreen=False,num=num)
                                doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}(save='s2f','save2file','save to file','save','sv')(clipboard='2cb','2clipboard')][ID={getattr(log,self.primaryKey(self.Model)[0].name)}]?",helpText=f"{l}\n{cmds}",data="string")
                                print(f"{Fore.light_green}CMD Executed: '{Fore.light_yellow}{doWhat}{Fore.light_green}'{Style.reset}")
                                if doWhat in ['NaN',None]:
                                    return
                                elif doWhat.lower() in ['d','']:
                                    gotoNext=True
                                    break
                                elif doWhat.lower() in [i.lower() for i in 'refresh and print=rfshp/refresh and print/pcont/pcntu/print continue'.split('=')[-1].split("/")]:
                                    session.refresh(log)
                                    print(log)
                                    continue
                                elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:            
                                    log=self.edit_id(log)
                                    continue
                                elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                    log=self.StoreForCDP(log)
                                    continue
                                elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                    log=self.delete_id(log)
                                    continue
                                elif doWhat.lower() in ['s2f','save2file','save to file','save','sv']:
                                    outfile=Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))
                                    with open(outfile,'w') as x:
                                        otext=self.short_view(self,data=[log,],printToScreen=False,num=num)
                                        otext=strip_colors(otext)
                                        x.write(otext)
                                        print(f"wrote '{otext}' to '{outfile}'")
                                elif doWhat.lower() in ['2cb','2clipboard']:
                                    with db.Session(db.ENGINE) as session:
                                        otext=self.short_view(self,data=[log,],printToScreen=False,num=num)
                                        otext=strip_colors(otext)
                                        cb=db.ClipBoord(cbValue=otext,doe=datetime.now(),ageLimit=db.ClipBoordEditor.ageLimit,defaultPaste=True)
                                        results=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).all()
                                        ct=len(results)
                                        if ct > 0:
                                            for num,r in enumerate(results):
                                                r.defaultPaste=False
                                                if num % 100:
                                                    session.commit()
                                            session.commit()
                                        session.add(cb)
                                        session.commit()
                                else:
                                    gotoNext=True
                                    break
                                if gotoNext:
                                    gotoNext=False
                                    break
                            except Exception as e:
                                print(e)
                                gotoNext=True
                                break
                else:
                    print(htext)
                break

    def StoreInCB(self,ncb_text=''):
        with Session(ENGINE) as session:
            cb=ClipBoord(cbValue=ncb_text,doe=datetime.now(),ageLimit=ClipBoordEditor.ageLimit,defaultPaste=True)
            results=session.query(ClipBoord).filter(ClipBoord.defaultPaste==True).all()
            ct=len(results)
            if ct > 0:
                for num,r in enumerate(results):
                    r.defaultPaste=False
                    if num % 100:
                        session.commit()
                session.commit()
            session.add(cb)
            session.commit()

    def StoreForCDP(self,item):
        try:
            with Session(ENGINE) as session:
                log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
                keys={i.name:getattr(log,i.name) for i in log.__table__.columns}
                htext=[]
                cta=len(keys)
                for num,k in enumerate(keys):
                    htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
                htext='\n'.join(htext)
                while True:
                    try:
                        print(htext)
                        which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                        if which is None:
                            return
                        elif which in ['NAN','NaN',None,'None','d','']:
                            return
                        else:
                            self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                        return
                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)
            return item
        pass

    def __init__(self,Model,short_view=None,menu={}):
        self.Model=Model
        if short_view is not None and callable(short_view):
            self.short_view=short_view
        cmds={
            str(uuid1()):{
            'cmds':['fixtable','fx tbl'],
            'exec':self.fix_table,
            'desc':"regenerate tables; a complete clear!!!"
            },
            str(uuid1()):{
            'cmds':['within dtoes','between dates','between dtoes','between','btwn'],
            'exec':self.within_dtoes,
            'desc':"print data within dates"
            },
            str(uuid1()):{
            'cmds':['search','sch 1'],
            'exec':lambda self=self: self.search_and_menu(short=False),
            'desc':"search and print - Long!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 2'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=False),
            'desc':"search and use menu - LONG!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 3'],
            'exec':lambda self=self: self.search_and_menu(short=True),
            'desc':"search and print - Short!!!"
            },
            str(uuid1()):{
            'cmds':['search','sch 4'],
            'exec':lambda self=self: self.search_and_menu(menu=True,short=True),
            'desc':"search and use menu - Short!!!"
            },
            str(uuid1()):{
            'cmds':['new log','new','new log','ntl'],
            'exec':self.newLog,
            'desc':"create a new log"
            },
            str(uuid1()):{
            'cmds':['del log','rmid','del by id',],
            'exec':self.delete_by_id,
            'desc':"delete a log by its id"
            },
            str(uuid1()):{
            'cmds':['ed log','edid','edit by id',],
            'exec':self.edit_by_id,
            'desc':"edit a log by its id"
            },
            str(uuid1()):{
            'cmds':['r r','random result','rdm rslt'],
            'exec':self.random_result,
            'desc':"provide a random result"
            },
            str(uuid1()):{
            'cmds':['histograph log','hg lg',],
            'exec':self.histograph_log,
            'desc':"histograph log data"
            },
            str(uuid1()):{
            'cmds':['bargraph log','bg lg',],
            'exec':self.bar_log,
            'desc':"bargraph log data"
            },
            str(uuid1()):{
            'cmds':['scattergraph log','sg lg',],
            'exec':self.scatter_log,
            'desc':"scattergraph log data"
            },
            str(uuid1()):{
            'cmds':['linegraph log','lg lg',],
            'exec':self.line_log,
            'desc':"linegraph log data"
            },
            str(uuid1()):{
            'cmds':['listUniq','lsu','uniq','unique','distinct','group_by','groupBy','gb'],
            'exec':self.listUniq,
            'desc':"list only unique values for a column"
            },
            str(uuid1()):{
            'cmds':['avg max min field','average maximum minium field','avgmaxminfld','ammf',],
            'exec':self.avg_field,
            'desc':"average, min, max the data in a column"
            },
            str(uuid1()):{
            'cmds':['3 day moving average price','3dmap','forecasting naive','fornaiv'],
            'exec':self.forecasting_naive,
            'desc':"average, min, max the data in a column"
            }

            
        }
        cmds.update(menu)
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))

        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}{self.Model.__name__} Logger: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            try:
                                cmds[c]['exec'](self)
                                continue
                            except Exception as ee:
                                print(ee)
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")
def sibdsd_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    

    for xnum,i in enumerate(data):
        fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
    %A(%d) of %B, 
    week[Business] %V of year %Y, 
    week[Sunday First] %U of year %Y, 
    week[Monday First] %W of year %Y) 
    @[12H] {Fore.light_cyan}%I:%M %p
    @[24H] {Fore.medium_violet_red}%H:%M""")

        msg=f"""
        Short View Not Ready - {i}
"""
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)


def DC_Delivery_Preparation_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    

    for xnum,i in enumerate(data):
        fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
    %A(%d) of %B, 
    week[Business] %V of year %Y, 
    week[Sunday First] %U of year %Y, 
    week[Monday First] %W of year %Y) 
    @[12H] {Fore.light_cyan}%I:%M %p
    @[24H] {Fore.medium_violet_red}%H:%M""")

        msg=f"""
        Short View Not Ready - {i}
"""
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def ApprovedStoreUse_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    

    for xnum,i in enumerate(data):
        fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
    %A(%d) of %B, 
    week[Business] %V of year %Y, 
    week[Sunday First] %U of year %Y, 
    week[Monday First] %W of year %Y) 
    @[12H] {Fore.light_cyan}%I:%M %p
    @[24H] {Fore.medium_violet_red}%H:%M""")

        msg=f"""
{Fore.light_green}Name: "{Fore.light_yellow}{i.name}{Fore.light_green}" comment:"{Fore.light_yellow}{i.comment}{Fore.light_green}" asuid:"{Fore.light_yellow}{i.asuid}{Fore.light_green}" dtoe:"{Fore.light_yellow}{i.dtoe}{Fore.light_green}"{Style.reset}
"""
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def DC_Delivery_Preparation_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    

    for xnum,i in enumerate(data):
        fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
    %A(%d) of %B, 
    week[Business] %V of year %Y, 
    week[Sunday First] %U of year %Y, 
    week[Monday First] %W of year %Y) 
    @[12H] {Fore.light_cyan}%I:%M %p
    @[24H] {Fore.medium_violet_red}%H:%M""")

        msg=f"""
        Short View Not Ready - {i}
"""
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def MarkDownsAndExpireds_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x='''group_id=gid
name=nm
NameOrBarcode=bcd
ManufactureDate=Rxd/Mnfctr DTOE
ExpirationDate=BB
Markdown_050Time=50 Cent
Markdown_025Time=25 Cent
ProductLifeSpanTime=LifeSpan
ProductType=ptype
Description=desc
dtoe=dtoe
comment=cmnt
Remaining Shelf Life = Expiration - Now []
CalculatedLifeSpan = Expiration Date - Manufacture Date'''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        lifespan=None
        if i.ManufactureDate is not None:
            if i.ExpirationDate is not None:
                lifespan=i.ExpirationDate-i.ManufactureDate

        tttSellBy=None
        if i.ExpirationDate != None:
            tttSellBy=i.ExpirationDate-datetime.now()
            if timedelta(hours=0,minutes=0,seconds=0)>tttSellBy:
                tttSellBy=f"{Fore.green_yellow}Expired it had a total life of {Fore.light_yellow}{lifespan} and is {tttSellBy} past-due."

        

        fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
    %A(%d) of %B, 
    week[Business] %V of year %Y, 
    week[Sunday First] %U of year %Y, 
    week[Monday First] %W of year %Y) 
    @[12H] {Fore.light_cyan}%I:%M %p
    @[24H] {Fore.medium_violet_red}%H:%M""")

        msg=f"""
{Fore.orange_red_1}gid:{Fore.light_yellow}{i.group_id} {Fore.orange_red_1}nm:{Fore.light_yellow}{i.name} {Fore.orange_red_1}bcd:{Fore.light_yellow}{i.NameOrBarcode} {Fore.orange_red_1}Rxd/Mnfctr DTOE:{Fore.light_yellow}{i.ManufactureDate} {Fore.orange_red_1}BB:{Fore.light_yellow}{i.ExpirationDate} {Fore.orange_red_1}remainingShelfLife:{Fore.light_yellow}{tttSellBy}
{Fore.orange_red_1}50Cent:{Fore.light_yellow}{i.Markdown_050Time} {Fore.orange_red_1}25Cent:{Fore.light_yellow}{i.Markdown_025Time} {Fore.orange_red_1}LifeSpan:{Fore.light_yellow}{i.ProductLifeSpanTime} {Fore.orange_red_1}CalculatedLifeSpan:{Fore.light_yellow}{lifespan}
{Fore.orange_red_1}ptype:{Fore.light_yellow}{i.ProductType} {Fore.orange_red_1}desc:{Fore.light_yellow}{i.Description} {Fore.orange_red_1}dtoe:{Fore.light_yellow}{i.dtoe} {Fore.orange_red_1}cmnt:{Fore.light_yellow}{i.comment} {Fore.orange_red_1}asuid:{Fore.light_yellow}{i.asuid}{Style.reset}
"""
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def mlee_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    

    for xnum,i in enumerate(data):
        fmtd=i.dtoe.strftime(f"""{Fore.light_green}%m/%d/%Y 
    %A(%d) of %B, 
    week[Business] %V of year %Y, 
    week[Sunday First] %U of year %Y, 
    week[Monday First] %W of year %Y) 
    @[12H] {Fore.light_cyan}%I:%M %p
    @[24H] {Fore.medium_violet_red}%H:%M""")

        msg=f"""
        Short View Not Ready - {i}
"""
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def mleeLogger(Model=Entry,short_view=mlee_short_view):
    return ModelLogger(Model=Entry,short_view=mlee_short_view)

def ShippingInvoice_By_Dept_SubDeptLogger(Model=ShippingInvoice_By_Dept_SubDept,short_view=sibdsd_short_view):
    return ModelLogger(Model=ShippingInvoice_By_Dept_SubDept,short_view=sibdsd_short_view)

def DC_Delivery_PreparationLogger(Model=DC_Delivery_Preparation,short_view=DC_Delivery_Preparation_short_view):
    return ModelLogger(Model=DC_Delivery_Preparation,short_view=DC_Delivery_Preparation_short_view)

def ApprovedStoreUseLogger(Model=ApprovedStoreUse,short_view=ApprovedStoreUse_short_view):
    return ModelLogger(Model=ApprovedStoreUse,short_view=ApprovedStoreUse_short_view)

def MarkDownsAndExpiredsLogger(Model=MarkDownsAndExpireds,short_view=MarkDownsAndExpireds_short_view):
    return ModelLogger(Model=MarkDownsAndExpireds,short_view=MarkDownsAndExpireds_short_view)


def bodyStats_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        msg=f'''{Fore.orange_red_1}patient_name={Fore.salmon_1}{i.patient_name}
{Fore.orange_red_1}dtoe={Fore.salmon_1}{i.dtoe}
{Fore.magenta}body_temp={Fore.salmon_1}{i.body_temp} {i.body_temp_unit}
{Fore.cyan}blood_pressure_systolic={Fore.salmon_1}{i.blood_pressure_systolic} {i.blood_pressure_unit}
{Fore.light_cyan}blodd_pressure_diastolic={Fore.salmon_1}{i.blodd_pressure_diastolic} {i.blood_pressure_unit}
{Fore.grey_50}group_id={Fore.salmon_1}{i.group_id}
{Fore.grey_50}asuid={Fore.salmon_1}{i.asuid}
{Fore.pale_green_1a}comment={Fore.salmon_1}{i.comment}
        '''
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def bdsts_StoreInCB(self,ncb_text=''):
    with Session(ENGINE) as session:
        cb=ClipBoord(cbValue=ncb_text,doe=datetime.now(),ageLimit=ClipBoordEditor.ageLimit,defaultPaste=True)
        results=session.query(ClipBoord).filter(ClipBoord.defaultPaste==True).all()
        ct=len(results)
        if ct > 0:
            for num,r in enumerate(results):
                r.defaultPaste=False
                if num % 100:
                    session.commit()
            session.commit()
        session.add(cb)
        session.commit()

def bdsts_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
            'blood_pressure_systolic':f'{log.blood_pressure_systolic} {log.blood_pressure_unit}',
            'blodd_pressure_diastolic':f'{log.blodd_pressure_diastolic} {log.blood_pressure_unit}',
            f'blodd_pressure_diastolic {log.blood_pressure_unit}/blood_pressure_systolic {log.blood_pressure_unit}':f"{log.blood_pressure_systolic} {log.blood_pressure_unit}/{log.blodd_pressure_diastolic} {log.blood_pressure_unit}",
            'body_temp':f'{log.body_temp} {log.body_temp_unit}',
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass


def s2cb_w_u(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=bdsts_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    



bdsts_menu={
    str(uuid1()):{
    "cmds":['s2cb w/u',],
    "exec":lambda self:s2cb_w_u(self,menu=True,short=True),
    "desc":"Save to Clipboard with unit",
    }
}
def bodyStatsLogger(Model=BodyStats,short_view=bodyStats_short_view,menu=bdsts_menu):
    return ModelLogger(Model=BodyStats,short_view=bodyStats_short_view,menu=bdsts_menu)

def drugs_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        msg=f'''-{Back.grey_15}{Fore.light_green}dtoe={Fore.pale_green_1a}{i.dtoe}
-{Fore.light_steel_blue}patient_name={Fore.light_blue}{i.patient_name}
-{Fore.light_steel_blue}patient_address={Fore.light_blue}{i.patient_address}
-{Fore.orange_red_1}drug_name={Fore.light_red}{i.drug_name} {i.drug_strength_with_unit}
-{Fore.orange_red_1}drug_qty={Fore.light_red}{i.drug_qty}
-{Fore.cyan}Instructions_for_use={Fore.light_cyan}{i.Instructions_for_use}
-{Fore.light_yellow}Prescription_RX_number={Fore.dark_goldenrod}{i.Prescription_RX_number}
-{Fore.grey_85}Refills_Remaining={Fore.grey_50}{i.Refills_Remaining}
-{Fore.spring_green_1}IssueDTOE={Fore.sea_green_1a}{i.IssueDTOE}
-{Fore.magenta}FillDTOE={Fore.light_magenta}{i.FillDTOE}
-{Fore.medium_violet_red}Pharmacy_Information={Fore.light_magenta}{i.Pharmacy_Information}
-{Fore.grey_85}comment={Fore.grey_50}{i.comment}
-{Fore.grey_85}did={Fore.grey_50}{i.did}
-{Fore.grey_85}group_id={Fore.grey_50}{i.group_id}{Style.reset}'''
        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def drgs_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           'drug drug_strength':f"{log.drug_name} {log.drug_strength_with_unit}",
           'refills byDTOE':f"{log.Refills_Remaining} by {log.Refills_By}",
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass


def s2cb_drugs(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=drgs_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    



drgs_menu={
    str(uuid1()):{
    "cmds":['s2cb custom',],
    "exec":lambda self:s2cb_drugs(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

def medicationsLogger(Model=Drugs,short_view=drugs_short_view,menu=drgs_menu):
    return ModelLogger(Model=Drugs,short_view=drugs_short_view,menu=drgs_menu)

def per_serving():
    while True:
        try:
            fd={
            'serving size':{
             'type':'string',
             'default':'8 floz'
            },
            'amount served/consumed':{
            'type':'string',
            'default':'16.9 floz'
            },
            'per serving':{
            'type':'string',
            'default':'5 calories'
            }
            }
            fb=FormBuilder(data=fd)
            if fb is None:
                return
                
            fmla=(pint.Quantity(fb['per serving'])/pint.Quantity(fb['serving size']))*pint.Quantity(fb['amount served/consumed'])
            return fmla
        except Exception as e:
             print(e)

def fcl_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
    {Fore.orange_red_1}DTOE = {Fore.light_steel_blue} {i.dtoe}
    {Fore.light_yellow}Consumer(s) is/are What = {Fore.medium_violet_red}{i.consumer_s_is_what}
    {Fore.orange_red_1}Feed Name = {Fore.light_steel_blue}{i.feed_name}
    {Fore.orange_red_1}Feed BCD = {Fore.light_steel_blue}{i.feed_barcode}
    {Fore.orange_red_1}Feed Initial Qty = {Fore.light_steel_blue}{pint.Quantity(i.feed_initial_qty)}
    {Fore.orange_red_1}Old({pint.Quantity(i.old_feed)})+{Fore.light_green}New({pint.Quantity(i.new_feed)}) = {Fore.light_steel_blue}{pint.Quantity(i.new_feed)+pint.Quantity(i.old_feed)}
    {Fore.orange_red_1}Desired Feed Amount = {Fore.light_steel_blue}{pint.Quantity(i.desired_feed_qty)}
    {Fore.orange_red_1}fclid = {Fore.light_steel_blue}{i.fclid}
    {Fore.orange_red_1}Initial Feed Qty = {Fore.light_steel_blue}{i.feed_initial_qty}
    {Fore.orange_red_1}Last Purchase DTOE = {Fore.light_steel_blue} {i.last_feed_purchase_dtoe}{Style.reset}'''
        except Exception as e:
            print(e)
            try:
                msg=f'''
    {Fore.orange_red_1}DTOE = {Fore.light_steel_blue} {i.dtoe}
    {Fore.light_yellow}Consumer(s) is/are What = {Fore.medium_violet_red}{i.consumer_s_is_what}
    {Fore.orange_red_1}Feed Name = {Fore.light_steel_blue}{i.feed_name}
    {Fore.orange_red_1}Feed BCD = {Fore.light_steel_blue}{i.feed_barcode}
    {Fore.orange_red_1}Feed Initial Qty = {Fore.light_steel_blue}{i.feed_initial_qty}
    {Fore.orange_red_1}Old({i.old_feed})+{Fore.light_green}New({i.new_feed}) = {Fore.light_steel_blue}{i.new_feed+i.old_feed}
    {Fore.orange_red_1}Desired Feed Amount = {Fore.light_steel_blue}{i.desired_feed_qty}
    {Fore.orange_red_1}fclid = {Fore.light_steel_blue}{i.fclid}
    {Fore.orange_red_1}Initial Feed Qty = {Fore.light_steel_blue}{i.feed_initial_qty}
    {Fore.orange_red_1}Last Purchase DTOE = {Fore.light_steel_blue} {i.last_feed_purchase_dtoe}{Style.reset}'''
            except Exception as ee:
                print(ee)
                msg=f'''
    {Fore.orange_red_1}DTOE = {Fore.light_steel_blue} {i.dtoe}
    {Fore.light_yellow}Consumer(s) is/are What = {Fore.medium_violet_red}{i.consumer_s_is_what}
    {Fore.orange_red_1}Feed Name = {Fore.light_steel_blue}{i.feed_name}
    {Fore.orange_red_1}Feed BCD = {Fore.light_steel_blue}{i.feed_barcode}
    {Fore.orange_red_1}Feed Initial Qty = {Fore.light_steel_blue}{i.feed_initial_qty}
    {Fore.orange_red_1}Old({i.old_feed})+{Fore.light_green}New({i.new_feed})
    {Fore.orange_red_1}Desired Feed Amount = {Fore.light_steel_blue}{i.desired_feed_qty}
    {Fore.orange_red_1}fclid = {Fore.light_steel_blue}{i.fclid}
    {Fore.orange_red_1}Initial Feed Qty = {Fore.light_steel_blue}{i.feed_initial_qty}
    {Fore.orange_red_1}Last Purchase DTOE = {Fore.light_steel_blue} {i.last_feed_purchase_dtoe}{Style.reset}'''

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def fcl_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_fcl(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=fcl_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    



fcl_menu={
    str(uuid1()):{
    "cmds":['s2cb custom',],
    "exec":lambda self:s2cb_fcl(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

def fclLogger(Model=FeedConsumptionLog,short_view=fcl_short_view,menu=fcl_menu):
    return ModelLogger(Model=FeedConsumptionLog,short_view=fcl_short_view,menu=fcl_menu)


def ttw_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
    {Fore.orange_red_1}DTOE = {Fore.light_steel_blue} {i.dtoe}
    {Fore.light_yellow}Tried_To_Wake_Whom = {Fore.medium_violet_red}{i.Tried_To_Wake_Whom}
    {Fore.orange_red_1}Tried_To_Wake_DTOE = {Fore.medium_violet_red}{i.Tried_To_Wake_DTOE}
    {Fore.orange_red_1}Success = {Fore.medium_violet_red}{i.Success}
    {Fore.orange_red_1}ttwid = {Fore.medium_violet_red}{i.ttwid}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def ttw_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_ttw(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=ttw_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    



ttw_menu={
    str(uuid1()):{
    "cmds":['ttw custom',],
    "exec":lambda self:s2cb_ttw(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def ttwLogger(Model=TriedToWake,short_view=ttw_short_view,menu=ttw_menu):
    return ModelLogger(Model=TriedToWake,short_view=ttw_short_view,menu=ttw_menu)


def tpoc_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
    {Fore.orange_red_1}DTOE = {Fore.light_steel_blue}{i.dtoe}
    {Fore.light_yellow}tpocid = {Fore.medium_violet_red}{i.tpocid}
    {Fore.orange_red_1}Name={Fore.medium_violet_red}{i.Name}
    {Fore.orange_red_1}Complete={Fore.medium_violet_red}{i.Complete}
    {Fore.orange_red_1}Completed_by_Whom={Fore.medium_violet_red}{i.Completed_by_Whom}
    {Fore.orange_red_1}Completed_DTOE={Fore.medium_violet_red}{i.Completed_DTOE}

    {Fore.orange_red_1}comment={Fore.medium_violet_red}{i.comment}
    {Fore.orange_red_1}group_id={Fore.medium_violet_red}{i.group_id}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def tpoc_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_tpoc(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=tpoc_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    



tpoc_menu={
    str(uuid1()):{
    "cmds":['tpoc custom',],
    "exec":lambda self:s2cb_tpoc(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def tpocLogger(Model=TasksPendingOrComplete,short_view=tpoc_short_view,menu=tpoc_menu):
    return ModelLogger(Model=TasksPendingOrComplete,short_view=tpoc_short_view,menu=tpoc_menu)

def gas2_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_gas2(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=gas2_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    
def gas2_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

gas2_menu={
    str(uuid1()):{
    "cmds":['gas2 custom',],
    "exec":lambda self:s2cb_gas2(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def gas2Logger(Model=FuelPrice,short_view=gas2_short_view,menu=gas2_menu):
    return ModelLogger(Model=FuelPrice,short_view=gas2_short_view,menu=gas2_menu)

def lwpl2_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_lwpl2(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=lwpl2_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    
def lwpl2_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}lwpid={Fore.light_steel_blue}{i.lwpid}
    {Fore.orange_red_1}location={Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}geolocation={Fore.light_steel_blue}{i.geolocation}
    {Fore.orange_red_1}elevation={Fore.light_steel_blue}{i.elevation}
    {Fore.orange_red_1}elevation_unit={Fore.light_steel_blue}{i.elevation_unit}
    {Fore.orange_red_1}elevation_reference={Fore.light_steel_blue}{i.elevation_reference}
    {Fore.orange_red_1}precip={Fore.light_steel_blue}{i.precip}
    {Fore.orange_red_1}precip_unit={Fore.light_steel_blue}{i.precip_unit}
    {Fore.orange_red_1}current_temp={Fore.light_steel_blue}{i.current_temp}
    {Fore.orange_red_1}current_temp_unit={Fore.light_steel_blue}{i.current_temp_unit}
    {Fore.orange_red_1}high_temp={Fore.light_steel_blue}{i.high_temp}
    {Fore.orange_red_1}high_temp_unit={Fore.light_steel_blue}{i.high_temp_unit}
    {Fore.orange_red_1}low_temp={Fore.light_steel_blue}{i.low_temp}
    {Fore.orange_red_1}low_temp_unit={Fore.light_steel_blue}{i.low_temp_unit}
    {Fore.orange_red_1}atmo_pressure={Fore.light_steel_blue}{i.atmo_pressure}
    {Fore.orange_red_1}atmo_pressure_unit={Fore.light_steel_blue}{i.atmo_pressure_unit}
    {Fore.orange_red_1}wind_speed={Fore.light_steel_blue}{i.wind_speed}
    {Fore.orange_red_1}wind_speed_unit={Fore.light_steel_blue}{i.wind_speed_unit}
    {Fore.orange_red_1}wind_direction={Fore.light_steel_blue}{i.wind_direction}
    {Fore.orange_red_1}humidity={Fore.light_steel_blue}{i.humidity}
    {Fore.orange_red_1}dew_point={Fore.light_steel_blue}{i.dew_point}
    {Fore.orange_red_1}dew_point_unit={Fore.light_steel_blue}{i.dew_point_unit}
    {Fore.orange_red_1}dawn_dtoe={Fore.light_steel_blue}{i.dawn_dtoe}
    {Fore.orange_red_1}dusk_dtoe={Fore.light_steel_blue}{i.dusk_dtoe}
    {Fore.orange_red_1}sunrise_dtoe={Fore.light_steel_blue}{i.sunrise_dtoe}
    {Fore.orange_red_1}sunset_dtoe={Fore.light_steel_blue}{i.sunset_dtoe}
    {Fore.orange_red_1}UV_Index={Fore.light_steel_blue}{i.UV_Index}
    {Fore.orange_red_1}dtoe={Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment={Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)

def hlcg(self):
    with Session(ENGINE) as session:
        localtemp=detectGetOrSet('local_temperature_unit','degF',setValue=False,literal=True)
        local_atmo=detectGetOrSet('local_atmo_unit','inHg',setValue=False,literal=True)
        #excludes=[str(self.primaryKey(self.Model)[0]).split('.')[-1],]
        excludes=[]
        fields=[(i.name,i.type) for i in self.Model.__table__.columns if i.name not in excludes]
        indexs=[num[0] for num in enumerate(fields)]
        #print(fields,excludes)
        htext=[]
        cta=len(fields)
        for num,i in enumerate(fields):
            htext.append(std_colorize(i,num,cta))
        htext='\n'.join(htext)
        print(htext)
        print(f"{Fore.orange_red_1}fields related to {Fore.light_steel_blue}{self.Model}{Fore.orange_red_1} are listed above.{Style.reset}")

        query=self.search_and_menu(menu=False,short=True,returnQuery=True)
        if query == None:
            return
        df=pd.read_sql_query(sql=query.statement,con=session.bind)

        for col_name, dtype in df.dtypes.items():
            try:
                if pd.api.types.is_datetime64_any_dtype(dtype):
                    # Create a new column with '_ts' suffix
                    df[f"{col_name}_ts"] = df[col_name].astype(np.int64) // 10**9
                    # Optionally, replace the original column
                    #df[col_name] = df[col_name].astype(np.int64) // 10**9
                    #df[col_name]=df[col_name].dt.strftime("%m/%d/%Y-%H:%M:%S")
                    df[col_name]=df[col_name].apply(modx) #here
                elif pd.api.types.is_string_dtype(dtype):
                    df[col_name]=df[col_name].apply(justValue)
            except Exception as es:
                print(es,repr(es),type(es))

        dtoe=df['dtoe'].tolist()
        
        hitemp=df['high_temp'].tolist()
        hitemp_unit=df['high_temp_unit'].tolist()
        
        lotemp=df['low_temp'].tolist()
        lotemp_unit=df['low_temp_unit'].tolist()

        current_temp=df['current_temp'].tolist()
        current_temp_unit=df['current_temp_unit'].tolist()
        try:
            hitemp_proc=[]
            lotemp_proc=[]
            current_temp_proc=[]
            for num,i in enumerate(dtoe):
                try:

                    qchi=pint.Quantity(hitemp[num],hitemp_unit[num])
                    hitemp_proc.append(qchi.to(localtemp).magnitude)

                    qclo=pint.Quantity(lotemp[num],lotemp_unit[num])
                    lotemp_proc.append(qclo.to(localtemp).magnitude)

                    qccur=pint.Quantity(current_temp[num],current_temp_unit[num])
                    current_temp_proc.append(qccur.to(localtemp).magnitude)
                except Exception as e:
                    print(e)
                    print("until this is issue is resolved with this log entry, this log will be excluded!")


            plt.plot(dtoe,hitemp_proc,color="red")
            plt.plot(dtoe,lotemp_proc,color="blue")
            plt.plot(dtoe,current_temp_proc,color="green")
            plt.show()
            plt.clf()
            print(f"{Fore.light_red}temperature is expressed in {localtemp}{Fore.light_yellow} the high temp {Fore.red}red{Fore.light_yellow},the low temp is {Fore.blue}blue{Fore.light_yellow},the current temp is {Fore.green}green{Style.reset}")
        except Exception as es:
            print(es)
            print('temp fail!')
        try:
            humidity_percent=df['humidity'].tolist()
            humidity_dewpoint=df['dew_point'].tolist()
            humidity_dewpoint_unit=df['dew_point_unit'].tolist()

            humidity_proc=[]
            dew_point_proc=[]
            for num,i in enumerate(dtoe):
                try:
                    humidity=pint.Quantity(humidity_percent[num],"percent")
                    humidity_proc.append(humidity.magnitude)

                    dew_point=pint.Quantity(humidity_dewpoint[num],humidity_dewpoint_unit[num])
                    dew_point_proc.append(dew_point.to(localtemp).magnitude)
                except Exception as e:
                    print(e)
                    print("until this is issue is resolved with this log entry, this log will be excluded!")
            plt.date_form('m/d/y-H:M:S')
            plt.plot(dtoe,humidity_proc,color="red")
            plt.plot(dtoe,dew_point_proc,color="blue")
            plt.show()
            plt.clf()
            print(f"{Fore.light_red}dewpoint temperature is expressed in {localtemp}{Fore.light_yellow} humidity is{Fore.red}red{Fore.light_yellow},dew_point is{Fore.blue}blue{Fore.light_yellow}.{Style.reset}")
        except Exception as ex:
            print(ex)
            print("Humidity and Dewpoint fail!")
        try:
            atmo_proc=[]
            atmo_values=df['atmo_pressure'].tolist()
            atmo_units=df['atmo_pressure_unit'].tolist()

            for num,i in enumerate(dtoe):
                try:
                    atmo=pint.Quantity(atmo_values[num],atmo_units[num])
                    atmo_proc.append(atmo.to(local_atmo).magnitude)

                except Exception as e:
                    print(e)
                    print("until this is issue is resolved with this log entry, this log will be excluded!")

            plt.date_form('m/d/y-H:M:S')
            plt.plot(dtoe,atmo_proc,color="red")

            plt.show()
            plt.clf()
            print(f"{Fore.light_red}atmo pressure is expressed in {local_atmo}{Fore.light_yellow} atmo is {Fore.red}red{Fore.light_yellow}.{Style.reset}")
        except Exception as es:
            print(es)
            print("atmo-pressure fail!")

        try:
            local_wind=detectGetOrSet('local_wind_unit','mph',setValue=False,literal=True)
            wind_proc=[]
            wind_values=df['wind_speed'].tolist()
            wind_units=df['wind_speed_unit'].tolist()

            for num,i in enumerate(dtoe):
                try:
                    wind=pint.Quantity(wind_values[num],wind_units[num])
                    wind_proc.append(wind.to(local_wind).magnitude)

                except Exception as e:
                    print(e)
                    print("until this is issue is resolved with this log entry, this log will be excluded!")

            plt.date_form('m/d/y-H:M:S')
            plt.plot(dtoe,wind_proc,color="red")

            plt.show()
            plt.clf()
            print(f"{Fore.light_red}wind speed is expressed in {local_wind}{Fore.light_yellow} wind is {Fore.red}red{Fore.light_yellow}.{Style.reset}")
        except Exception as es:
            print(es)
            print("wind fail!")
        try:    
            local_precip=detectGetOrSet('local_precip_unit','inches',setValue=False,literal=True)
            precip_proc=[]
            precip_values=df['precip'].tolist()
            precip_units=df['precip_unit'].tolist()

            for num,i in enumerate(dtoe):
                try:
                    precip=pint.Quantity(precip_values[num],precip_units[num])
                    precip_proc.append(precip.to(local_precip).magnitude)

                except Exception as e:
                    print(e)
                    print("until this is issue is resolved with this log entry, this log will be excluded!")

            plt.date_form('m/d/y-H:M:S')
            plt.plot(dtoe,precip_proc,color="red")

            plt.show()
            plt.clf()
            print(f"{Fore.light_red}precip is expressed in {local_precip}{Fore.light_yellow} precip is {Fore.red}red{Fore.light_yellow}.{Style.reset}")
        except Exception as es:
            print(es)
            print('precip fail! ')

lwpl2_menu={
    str(uuid1()):{
    "cmds":['lwpl2 custom',],
    "exec":lambda self:s2cb_lwpl2(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['graph data','gd'],
    "exec":lambda self:hlcg(self=self),
    "desc":"graph data",
    }
}

#TriedToWake
def lwpl2Logger(Model=LocalWeatherPattern,short_view=lwpl2_short_view,menu=lwpl2_menu):
    return ModelLogger(Model=LocalWeatherPattern,short_view=lwpl2_short_view,menu=lwpl2_menu)

def rented_rental_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_rented_rental(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=rented_rental_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    
def rented_rental_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            tankSize=pint.Quantity(i.fuel_tank_size)
            odometerStart=pint.Quantity(i.odometer_at_start)
            odometerAtRefuel=pint.Quantity(i.odometer_at_refuel)
            odometerAtReturn=pint.Quantity(i.odometer_at_return)
            requiredFuelLevelToReturnWith=fractions.Fraction(i.required_fuel_level_to_return_with)
            fuelLevelAtPump=fractions.Fraction(i.fuel_level_at_pump)
            fuelToPurchase=(requiredFuelLevelToReturnWith*tankSize)-(fuelLevelAtPump*tankSize)
            ftp=pint.Quantity(Decimal(eval(str(fuelToPurchase.magnitude))),fuelToPurchase.units)
            
            distance_traveled_to_return=odometerAtReturn-odometerStart

            msg=f'''
{'-'*20}
{Fore.orange_red_1}rrid={Fore.light_steel_blue}{i.rrid }
{Fore.orange_red_1}for_whom={Fore.light_steel_blue}{i.for_whom }
{Fore.orange_red_1}vehicle_plate={Fore.light_steel_blue}{i.vehicle_plate }
{Fore.orange_red_1}vehicle_name={Fore.light_steel_blue}{i.vehicle_name }
{Fore.orange_red_1}vehicle_model={Fore.light_steel_blue}{i.vehicle_model }
{Fore.orange_red_1}vehicle_description={Fore.light_steel_blue}{i.vehicle_description }
{Fore.orange_red_1}renting_from_address={Fore.light_steel_blue}{i.renting_from_address }
{Fore.orange_red_1}renting_from_name={Fore.light_steel_blue}{i.renting_from_name }

{Fore.orange_red_1}fuel_tank_size={Fore.light_steel_blue}{i.fuel_tank_size }
{Fore.orange_red_1}odometer_at_start={Fore.light_steel_blue}{i.odometer_at_start }
{Fore.orange_red_1}odometer_at_refuel={Fore.light_steel_blue}{i.odometer_at_refuel }
{Fore.orange_red_1}odometer_at_return={Fore.light_steel_blue}{i.odometer_at_return }
{Fore.orange_red_1}required_fuel_level_to_return_with={Fore.light_steel_blue}{i.required_fuel_level_to_return_with }
{Fore.orange_red_1}fuel_level_at_pump={Fore.light_steel_blue}{i.fuel_level_at_pump }
{Fore.orange_red_1}comment={Fore.light_steel_blue}{i.comment }
{Fore.orange_red_1}group_id={Fore.light_steel_blue}{i.group_id }
{Fore.orange_red_1}dtoe={Fore.light_steel_blue}{i.dtoe }

{Fore.light_magenta}Calculated{Style.reset}
    {Fore.light_red}tankSize={Fore.light_yellow}{tankSize}
    {Fore.light_red}odometerStart={Fore.light_yellow}{odometerStart}
    {Fore.light_red}odometerAtRefuel={Fore.light_yellow}{odometerAtRefuel}
    {Fore.light_red}odometerAtReturn={Fore.light_yellow}{odometerAtReturn}
    {Fore.light_red}requiredFuelLevelToReturnWith={Fore.light_yellow}{requiredFuelLevelToReturnWith}
    {Fore.light_red}fuelLevelAtPump={Fore.light_yellow}{fuelLevelAtPump}
    {Fore.light_red}fuelToPurchase={Fore.light_yellow}{fuelToPurchase}
    {Fore.light_red}fuel_to_purchase_decimal={Fore.light_yellow}{ftp}
    {Fore.light_red}distance_traveled_to_return={Fore.light_steel_blue}{distance_traveled_to_return}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)


rented_rental_menu={
    str(uuid1()):{
    "cmds":['rented_rental custom',],
    "exec":lambda self:s2cb_rented_rental(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}

#TriedToWake
def rented_rentalLogger(Model=RentedRental,short_view=rented_rental_short_view,menu=rented_rental_menu):
    return ModelLogger(Model=RentedRental,short_view=rented_rental_short_view,menu=rented_rental_menu)

def employer_info_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_employer_info(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=employer_info_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    
def employer_info_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{Fore.orange_red_1}eiid={Fore.light_steel_blue}{i.eiid }
{Fore.orange_red_1}info_text={Fore.light_steel_blue}{i.info_text }
{Fore.orange_red_1}info_title={Fore.light_steel_blue}{i.info_title }
{Fore.orange_red_1}info_group_name={Fore.light_steel_blue}{i.info_group_name }
{Fore.orange_red_1}info_personnel_name={Fore.light_steel_blue}{i.info_personnel_name }
{Fore.orange_red_1}info_priority={Fore.light_steel_blue}{i.info_priority }
{Fore.orange_red_1}info_source={Fore.light_steel_blue}{i.info_source }
{Fore.orange_red_1}info_value={Fore.light_steel_blue}{i.info_value }
{Fore.orange_red_1}comment={Fore.light_steel_blue}{i.comment }
{Fore.orange_red_1}group_id={Fore.light_steel_blue}{i.group_id }
{Fore.orange_red_1}dtoe={Fore.light_steel_blue}{i.dtoe }
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)


employer_info_menu={
    str(uuid1()):{
    "cmds":['employer_info custom',],
    "exec":lambda self:s2cb_employer_info(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}

#TriedToWake
def employer_infoLogger(Model=EmployerInfo,short_view=employer_info_short_view,menu=employer_info_menu):
    return ModelLogger(Model=EmployerInfo,short_view=employer_info_short_view,menu=employer_info_menu)

def daily_budget(value=None,dtToPayCheck=None,cost=None):
    while True:
        try:
            if isinstance(value,float) or isinstance(value,Decimal):
                total_value=float(value)
            else:
                total_value=Control(func=FormBuilderMkText,ptext='total to spread',helpText='amount to derive daily budget from',data='float')
                if total_value in [None,'nan','NAN','NaN']:
                    return
                if total_value in ['d','']:
                    print("this value has no default... please try again.")
                    continue
            if not isinstance(total_value,float):
                continue

            try:
                old=datetime.strptime(detectGetOrSet("daily budget last_paycheck_date",None,setValue=False,literal=True),"%m/%d/%Y %H:%M:%S")
            except Exception as e:
                old=None
                print(e)

            last_paycheck_date=Control(func=FormBuilderMkText,ptext=f'last payday[d={old}]',helpText='last date you were paid',data='datetime')
            if last_paycheck_date in [None,'nan','NAN','NaN']:
                return
            if last_paycheck_date in ['d','']:
                if old is None:
                    last_paycheck_date=datetime.now()
                else:
                    last_paycheck_date=old
            if not isinstance(last_paycheck_date,datetime):
                continue

            old=detectGetOrSet("daily budget last_paycheck_date",last_paycheck_date.strftime("%m/%d/%Y %H:%M:%S"),setValue=True,literal=True)

            tmp=int(detectGetOrSet('days until next paycheck',14,setValue=False,literal=False))
            days_to_next_paycheck=Control(func=FormBuilderMkText,ptext=f'days to next payday[d={tmp}]',helpText='how many days until you are paid again',data='integer')
            if days_to_next_paycheck in [None,'nan','NAN','NaN']:
                return
            if days_to_next_paycheck in ['d','']:
                days_to_next_paycheck=tmp
            if not isinstance(days_to_next_paycheck,int):
                continue
            if not isinstance(dtToPayCheck,datetime):
                TDY=datetime.today()
            else:
                TDY=dtToPayCheck

            roundTo=int(db.detectGetOrSet("lsbld ROUNDTO default",4,setValue=False,literal=False))
            dailyBudget=total_value/math.ceil((((((last_paycheck_date+timedelta(days=days_to_next_paycheck))-TDY).total_seconds())/60)/60)/24)
            expnse=''
            if cost != None:
                xcolor=''
                if cost > 0:
                    xcolor=f"{Fore.light_red}-"
                    taken=f"{Fore.light_steel_blue}Taken From "
                elif cost < 0:
                    taken=f"{Fore.light_magenta}Paid To "
                    xcolor=f"{Fore.light_green}+"
                expnse=f"{Fore.orange_red_1}[Expense {taken}{Fore.light_green}${decc(cost,cf=roundTo)+decc(value,cf=roundTo)}{Fore.orange_red_1}] {Fore.grey_50}:{Fore.green_yellow}${Fore.cyan}({xcolor}{abs(cost)}{Fore.cyan}){Style.reset}\n"
            msg=f'''{expnse}{Fore.grey_50}For {Fore.light_green}${decc(total_value,cf=roundTo)}{Fore.grey_50}
to be spread across {Fore.light_steel_blue}{math.ceil((((((last_paycheck_date+timedelta(days=days_to_next_paycheck))-TDY).total_seconds())/60)/60)/24)}{Fore.grey_50} days
(today is {Fore.light_steel_blue}{TDY}{Fore.grey_50})
before the {Fore.light_red}next payday{Fore.light_cyan} the daily budget is {Fore.cyan}${decc(dailyBudget,cf=roundTo)}{Fore.grey_50} for
{Fore.green_yellow}from the last paycheck date, {last_paycheck_date},
{Fore.light_red} to the next payday {last_paycheck_date+timedelta(days=days_to_next_paycheck)}{Style.reset}.'''
            print(msg)
            while True:
                simulateWithExpense=Control(func=FormBuilderMkText,ptext="simulate with expense? [y/n]",helpText="simulate with expense",data="boolean")
                if simulateWithExpense in [None,'NaN','NAN','nan']:
                    break
                if simulateWithExpense in BooleanAnswers.YES_defaulted:
                    expense=Control(func=FormBuilderMkText,ptext="how much is the expense?",helpText="a float value",data="float")
                    if expense in [None,'NaN','NAN','nan']:
                        break
                    elif expense in ['d','']:
                        expense=0
                    dtToPayCheck=Control(func=FormBuilderMkText,ptext="what is the desired today date?",helpText="a datetime value",data="datetime")
                    if dtToPayCheck in [None,'NaN','NAN','nan']:
                        break
                    elif dtToPayCheck in ['d','']:
                        dtToPayCheck=datetime.now()
                    return daily_budget(value=decc(total_value,cf=roundTo)-decc(expense,cf=roundTo),dtToPayCheck=dtToPayCheck,cost=expense)

                else:
                    break
            again=Control(func=FormBuilderMkText,ptext="run again? [y/n]",helpText="make another calculation",data="boolean")
            if again in [None,'NaN','NAN','nan']:
                break
            elif again in BooleanAnswers.YES_defaulted:
                continue
            return_msg_text=Control(func=FormBuilderMkText,ptext="Return the daily budget value[False,all else], or the msg text[True]?",helpText="a boolean yes or no",data="boolean")
            if return_msg_text in [None,'NAN','nan','NaN']:
                return
            elif return_msg_text in ['d','','D']:
                return decc(dailyBudget,cf=roundTo)
            if return_msg_text:
                return strip_colors(msg)
            else:
                return decc(dailyBudget,cf=roundTo)
        except Exception as e:
            print(e)


def billing_text_gen():
    fields={
            'Client Name':{
            'default':'',
            'type':'string'
            },
            'Job(s)':{
            'default':'',
            'type':'string',
            },
            'Rate':{
            'default':'$10 per 1 Hour',
            'type':'string'
            },
            'From':{
            'default':datetime.now()-timedelta(hours=1),
            'type':'datetime'
            },
            'To':{
            'default':datetime.now(),
            'type':'datetime'
            }
            }
    while True:
        try:
            
            fb=FormBuilder(data=fields,passThruText="billing text fields")
            if fb in [None,'None','NaN','nan']:
                return
            for k in fb:
                fields[k]['default']=fb[k]
            
            msg=f'''
I provided the following service(s), on {fb['From'].strftime("%m/%d/%Y")}, from {fb['From']} to {fb['To']}, for the client {fb['Client Name']}, for a total duration of {fb['To']-fb['From']} at a rate of {fb['Rate']}:  {fb['Job(s)']}.
            '''
            print(msg)
            useMessage=Control(func=FormBuilderMkText,ptext="Use this message?",helpText="yes or no",data="boolean")
            if useMessage in [None,'NAN','nan']:
                return
            elif useMessage in ['d','',True]:
                return msg
            else:
                continue
        except Exception as e:
            print(e)
default_bank_app=db.detectGetOrSet("default bank app","American 1st Advantage",setValue=False,literal=True)
def bank_transfer_text():
    fields={
             'My name is?':{
            'default':db.detectGetOrSet("xfer My name is?",'',setValue=False,literal=True),
            'type':'string'
            },
            'For Whom?':{
            'default':db.detectGetOrSet("xfer For Whom?",'',setValue=False,literal=True),
            'type':'string'
            },
            'For What?':{
            'default':db.detectGetOrSet("xfer For What?",'',setValue=False,literal=True),
            'type':'string'
            },
            'From What/Which Account?':{
            'default':db.detectGetOrSet('xfer from what/which accnt dflt',"checking",setValue=False,literal=True),
            'type':'string',
            },
            'To What/Which Account?':{
            'default':db.detectGetOrSet("xfer to what/which accnt dflt?","savings",setValue=False,literal=True),
            'type':'string'
            },
            "How Much was transfered?":{
                'type':'float',
                'default':float(db.detectGetOrSet("xfer How Much was transfered?",0,setValue=False,literal=False)),
            },
            "Today's DTOE?":{
                'type':'string',
                'default':datetime.now(),
            },
            "For When (Due Date)?":{
                'type':'datetime',
                'default':datetime.now()
            },
            "Was this an 'internal', 'external', or 'something else' transfer":{
                'type':'string',
                'default':db.detectGetOrSet("xfer Was this an 'internal', 'external', or 'something else' transfer?","internal",setValue=False,literal=True),
            },
            "about how long will the transfer take in days?":{
                'type':'float',
                'default':float(db.detectGetOrSet("xfer about how long will the transfer take in days?",0,setValue=False,literal=False)),
            },
            "What was used to perform the transfer?":{
                'type':'string',
                'default':db.detectGetOrSet("xfer What was used to perform the transfer?",f"the '{default_bank_app}' app installed on my mobile cellular device",setValue=False,literal=True),
            },
            "Message Serial No.":{
                'type':'string',
                'default':str(nanoid.generate(alphabet=string.ascii_letters+string.digits+"/-",size=8)),
            },
            }
    while True:
        try:
            fb=FormBuilder(data=fields,passThruText="Bank Transfer Text")
            if fb in [None,'None','NaN','nan']:
                return
            for k in fb:
                fields[k]['default']=fb[k]

            
            msg=f'''I, {fb['My name is?']},
made an {fb["Was this an 'internal', 'external', or 'something else' transfer"]}
transfer of ${fb["How Much was transfered?"]}
from {fb['From What/Which Account?']} 
to {fb['To What/Which Account?']} 
for {fb['For Whom?']}, 
for {fb['For What?']}, 
due on {fb["For When (Due Date)?"].strftime("%m/%d/%Y")}, 
with today being {fb["Today's DTOE?"].strftime("%m/%d/%Y")},
which may take {fb["about how long will the transfer take in days?"]} days for the transfer to complete, 
using {fb["What was used to perform the transfer?"]} 
Msg.Serial No:'{fb["Message Serial No."]}'.
'''
            print(msg)
            useMessage=Control(func=FormBuilderMkText,ptext="Use this message?",helpText="yes or no",data="boolean")
            if useMessage in [None,'NAN','nan']:
                return
            elif useMessage in ['d','',True]:
                return msg
            else:
                continue
        except Exception as e:
            print(e,str(e),repr(e))

#----------------------------
def tmplg2_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            try:
                processed_templerature_string=pint.Quantity(i.templerature_value,i.templerature_unit)
                msg=f"""TemplLog ->\n {ii}    
    {Fore.light_red}[{Fore.cyan}templogid{Fore.light_red}] {Fore.light_green}{i.templogid}
    {Fore.light_red}[{Fore.cyan}dtoe{Fore.light_red}] {Fore.light_green}{i.dtoe}
    {Fore.light_red}[{Fore.cyan}Logged{Fore.light_yellow} Temperature{Fore.light_red}] {Fore.light_green}{processed_templerature_string.to('degC')} {Fore.green_yellow}or {processed_templerature_string.to('degF')} {Fore.light_magenta}or {processed_templerature_string.to('degK')}
    {Fore.light_red}[{Fore.cyan}Location{Fore.light_red}] {Fore.light_green}{i.Location}
    {Fore.light_red}[{Fore.cyan}EmployeeIDorNAME{Fore.light_red}] {Fore.light_green}{i.EmployeeIDorNAME}
    {Fore.light_red}[{Fore.cyan}note{Fore.light_red}] {Fore.light_green}{i.note}{Style.reset}
                """
                if not num:
                    m=std_colorize(msg,xnum,ct)
                else:
                    m=std_colorize(msg,num,ct)
                xtext.append(m)
                if printToScreen:            
                    print(m)
            except Exception as e:
                msg=f"""TemplLog ->\n {ii}    
    {Fore.light_red}[{Fore.cyan}templogid{Fore.light_red}] {Fore.light_green}{i.templogid}
    {Fore.light_red}[{Fore.cyan}dtoe{Fore.light_red}] {Fore.light_green}{i.dtoe}
    {Fore.light_red}[{Fore.cyan}Logged{Fore.light_yellow} Temperature{Fore.light_red}] {Fore.light_green}{i.templerature_value} {i.templerature_unit} 
    {Fore.light_red}[{Fore.cyan}Location{Fore.light_red}] {Fore.light_green}{i.Location}
    {Fore.light_red}[{Fore.cyan}EmployeeIDorNAME{Fore.light_red}] {Fore.light_green}{i.EmployeeIDorNAME}
    {Fore.light_red}[{Fore.cyan}note{Fore.light_red}] {Fore.light_green}{i.note}
    {Fore.light_red}A Value was not processed correctly, please review tmplogid={Fore.light_steel_blue}{i.templogid}
    {Style.reset}"""
                if not num:
                    m=std_colorize(msg,xnum,ct)
                else:
                    m=std_colorize(msg,num,ct)
                xtext.append(m)
                if printToScreen:            
                    print(m)

        return '\n'.join(xtext)
def tmplg2_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_tmplg2(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=tmplg2_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def tmplg2_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
tmplg2_menu={
    str(uuid1()):{
    "cmds":['tmplg2 custom',],
    "exec":lambda self:s2cb_tmplg2(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def tmplg2Logger(Model=TemplLog,short_view=tmplg2_short_view,menu=tmplg2_menu):
    return ModelLogger(Model=TemplLog,short_view=tmplg2_short_view,menu=tmplg2_menu)

def closeOut_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            penny= decc(( Quantity(i.Penny_Total_Mass,i.MassUnit) / Quantity(i.Penny_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Penny_Unit_Value,cf=8)
            #exit(str(penny))
            nickel= decc(( Quantity(i.Nickel_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Unit_Value,cf=8)
            #exit(str(nickel))
            dime= decc(( Quantity(i.Dime_Total_Mass,i.MassUnit) / Quantity(i.Dime_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dime_Unit_Value,cf=8)
            #exit(str(dime))
            quarter= decc(( Quantity(i.Quarter_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Quarter_Unit_Value,cf=8)
            #exit(str(quarter))
            halfdollar= decc(( Quantity(i.HalfDollar_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.HalfDollar_Unit_Value,cf=8)
            #exit(str(halfdollar))
            edollar=decc(( Quantity(i.EDollar_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Unit_Value,cf=8)
            #exit(str(edollar))
            edollar_collectors=decc(( Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Unit_Value_collectors,cf=8)
            #exit(str(edollar_collectors))
            pdollar=decc(( Quantity(i.PDollar_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.PDollar_Unit_Value,cf=8)
            #exit(str(pdollar))
            
            dollar1=decc(( Quantity(i.Dollar1_Total_Mass,i.MassUnit) / Quantity(i.Dollar1_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar1_Unit_Value,cf=8)
            #exit(str(dollar1))
            dollar2=decc(( Quantity(i.Dollar2_Total_Mass,i.MassUnit) / Quantity(i.Dollar2_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar2_Unit_Value,cf=8)
            #exit(str(dollar2))
            dollar5=decc(( Quantity(i.Dollar5_Total_Mass,i.MassUnit) / Quantity(i.Dollar5_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar5_Unit_Value,cf=8)
            #exit(str(dollar5))
            dollar10=decc(( Quantity(i.Dollar10_Total_Mass,i.MassUnit) / Quantity(i.Dollar10_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar10_Unit_Value,cf=8)
            #exit(str(dollar10))
            dollar20=decc(( Quantity(i.Dollar20_Total_Mass,i.MassUnit) / Quantity(i.Dollar20_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar20_Unit_Value,cf=8)
            #exit(str(dollar20))
            dollar50=decc(( Quantity(i.Dollar50_Total_Mass,i.MassUnit) / Quantity(i.Dollar50_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar50_Unit_Value,cf=8)
            #exit(str(dollar50))
            dollar100=decc(( Quantity(i.Dollar100_Total_Mass,i.MassUnit) / Quantity(i.Dollar100_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar100_Unit_Value,cf=8)
            #exit(str(dollar100))

            penny_roll=decc(( Quantity(i.Penny_Roll_Total_Mass,i.MassUnit) / Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Penny_Roll_Unit_Value,cf=8)
            #exit(str(penny_roll))
            nickel_roll=decc(( Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Roll_Unit_Value,cf=8)
            #exit(str(nickel_roll))
            dime_roll=decc(( Quantity(i.Dime_Roll_Total_Mass,i.MassUnit) / Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dime_Roll_Unit_Value,cf=8)
            #exit(str(dime_roll))
            quarter_roll=decc(( Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Quarter_Roll_Unit_Value,cf=8)
            #exit(str(quarter_roll))
            halfDollar_roll=decc(( Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.HalfDollar_Roll_Unit_Value,cf=8)
            #exit(str(halfDollar_roll))
            edollar_roll=decc(( Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Roll_Unit_Value)
            #exit(str(edollar_roll))
            edollar_roll_collectors=decc(( Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Roll_Unit_Value_collectors,cf=8)
            #exit(str(edollar_roll_collectors))
            pdollar_roll=decc(( Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.PDollar_Roll_Unit_Value,cf=8)
            total=penny+nickel+dime+quarter+halfdollar+edollar+edollar_collectors+pdollar+dollar1+dollar2+dollar5+dollar10+dollar20+dollar50+dollar100+penny_roll+nickel_roll+dime_roll+quarter_roll+halfDollar_roll+edollar_roll+edollar_roll_collectors+pdollar_roll


            take=''
            state=decc(i.register_ready_total,cf=8)-total
            if state > 0:
                take="You need to Add(+$)"
            elif state < 0:
                take="You need to Remove(-$)"
            msg=f'''CloseOut COID: {i.coid} DTOE:{i.dtoe}
Comment: {i.comment}
Group: {i.group_id}
Register No: {i.register_number}
whom: {i.whom}
{Fore.cyan}Penny( {Fore.light_green}Total Value  = ${penny} = {Fore.light_yellow}Total Mass( {Quantity(i.Penny_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Penny_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Penny_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Penny_Total_Mass,i.MassUnit) / Quantity(i.Penny_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Nickel( {Fore.light_green}Total Value  = ${nickel} = {Fore.light_yellow}Total Mass( {Quantity(i.Nickel_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Nickel_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Nickel_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Nickel_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dime( {Fore.light_green}Total Value  = ${dime} = {Fore.light_yellow}Total Mass( {Quantity(i.Dime_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dime_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dime_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dime_Total_Mass,i.MassUnit) / Quantity(i.Dime_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Quarter( {Fore.light_green}Total Value  = ${quarter} = {Fore.light_yellow}Total Mass( {Quantity(i.Quarter_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Quarter_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Quarter_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Quarter_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Half Dollar( {Fore.light_green}Total Value  = ${halfdollar} = {Fore.light_yellow}Total Mass( {Quantity(i.HalfDollar_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.HalfDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.HalfDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.HalfDollar_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar( {Fore.light_green}Total Value  = ${edollar} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar( Collectors {Fore.light_green}Total Value  = ${edollar_collectors} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Unit_Value_collectors,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}P Dollar( {Fore.light_green}Total Value  = ${pdollar} = {Fore.light_yellow}Total Mass( {Quantity(i.PDollar_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.PDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.PDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.PDollar_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Penny Roll( {Fore.light_green}Total Value  = ${penny_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Penny_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Penny_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Penny_Roll_Total_Mass,i.MassUnit) / Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Nickel Roll( {Fore.light_green}Total Value  = ${nickel_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Nickel_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Roll_Unit_Value,cf=8)})
{Fore.cyan}Dime Roll( {Fore.light_green}Total Value  = ${dime_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Dime_Roll_Total_Mass,i.MassUnit)}) * Mass Unit({Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dime_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dime_Roll_Total_Mass,i.MassUnit) / Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Quarter Roll( {Fore.light_green}Total Value  = ${quarter_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Quarter_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Half Dollar Roll( {Fore.light_green}Total Value  = ${halfDollar_roll} = {Fore.light_yellow}Total Mass( { Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.HalfDollar_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar Roll( {Fore.light_green}Total Value  = ${edollar_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Roll_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar Roll( Collectors {Fore.light_green}Total Value  = ${edollar_roll_collectors} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Roll_Unit_Value_collectors,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}P Dollar Roll( {Fore.light_green}Total Value  = ${pdollar_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.PDollar_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 1( {Fore.light_green}Total Value  = ${dollar1} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar1_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar1_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar1_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar1_Total_Mass,i.MassUnit) / Quantity(i.Dollar1_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 2( {Fore.light_green}Total Value  = ${dollar2} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar2_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar2_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar2_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar2_Total_Mass,i.MassUnit) / Quantity(i.Dollar2_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 5( {Fore.light_green}Total Value  = ${dollar5} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar5_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar5_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar5_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar5_Total_Mass,i.MassUnit) / Quantity(i.Dollar5_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 10( {Fore.light_green}Total Value  = ${dollar10} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar10_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar10_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar10_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar10_Total_Mass,i.MassUnit) / Quantity(i.Dollar10_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 20( {Fore.light_green}Total Value  = ${dollar20} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar20_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar20_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar20_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar20_Total_Mass,i.MassUnit) / Quantity(i.Dollar20_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 50( {Fore.light_green}Total Value  = ${dollar50} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar50_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar50_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar50_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar50_Total_Mass,i.MassUnit) / Quantity(i.Dollar50_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 100( {Fore.light_green}Total Value  = ${dollar100} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar100_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar100_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar100_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar100_Total_Mass,i.MassUnit) / Quantity(i.Dollar100_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
Register Ready Total({Fore.dark_goldenrod}${decc(i.register_ready_total,cf=8)}) - {Fore.orange_red_1}What Is In The Till({total}) = {take}({decc(i.register_ready_total,cf=8)-total}){Style.reset}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def closeOut_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_closeOut(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=closeOut_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def closeOut_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
closeOut_menu={
    str(uuid1()):{
    "cmds":['closeOut custom',],
    "exec":lambda self:s2cb_closeOut(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def closeOutLogger(Model=CloseOut,short_view=closeOut_short_view,menu=closeOut_menu):
    return ModelLogger(Model=CloseOut,short_view=closeOut_short_view,menu=closeOut_menu)

def deposit_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            penny= decc(( Quantity(i.Penny_Total_Mass,i.MassUnit) / Quantity(i.Penny_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Penny_Unit_Value,cf=8)
            #exit(str(penny))
            nickel= decc(( Quantity(i.Nickel_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Unit_Value,cf=8)
            #exit(str(nickel))
            dime= decc(( Quantity(i.Dime_Total_Mass,i.MassUnit) / Quantity(i.Dime_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dime_Unit_Value,cf=8)
            #exit(str(dime))
            quarter= decc(( Quantity(i.Quarter_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Quarter_Unit_Value,cf=8)
            #exit(str(quarter))
            halfdollar= decc(( Quantity(i.HalfDollar_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.HalfDollar_Unit_Value,cf=8)
            #exit(str(halfdollar))
            edollar=decc(( Quantity(i.EDollar_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Unit_Value,cf=8)
            #exit(str(edollar))
            edollar_collectors=decc(( Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Unit_Value_collectors,cf=8)
            #exit(str(edollar_collectors))
            pdollar=decc(( Quantity(i.PDollar_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.PDollar_Unit_Value,cf=8)
            #exit(str(pdollar))
            
            dollar1=decc(( Quantity(i.Dollar1_Total_Mass,i.MassUnit) / Quantity(i.Dollar1_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar1_Unit_Value,cf=8)
            #exit(str(dollar1))
            dollar2=decc(( Quantity(i.Dollar2_Total_Mass,i.MassUnit) / Quantity(i.Dollar2_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar2_Unit_Value,cf=8)
            #exit(str(dollar2))
            dollar5=decc(( Quantity(i.Dollar5_Total_Mass,i.MassUnit) / Quantity(i.Dollar5_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar5_Unit_Value,cf=8)
            #exit(str(dollar5))
            dollar10=decc(( Quantity(i.Dollar10_Total_Mass,i.MassUnit) / Quantity(i.Dollar10_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar10_Unit_Value,cf=8)
            #exit(str(dollar10))
            dollar20=decc(( Quantity(i.Dollar20_Total_Mass,i.MassUnit) / Quantity(i.Dollar20_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar20_Unit_Value,cf=8)
            #exit(str(dollar20))
            dollar50=decc(( Quantity(i.Dollar50_Total_Mass,i.MassUnit) / Quantity(i.Dollar50_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar50_Unit_Value,cf=8)
            #exit(str(dollar50))
            dollar100=decc(( Quantity(i.Dollar100_Total_Mass,i.MassUnit) / Quantity(i.Dollar100_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar100_Unit_Value,cf=8)
            #exit(str(dollar100))

            penny_roll=decc(( Quantity(i.Penny_Roll_Total_Mass,i.MassUnit) / Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Penny_Roll_Unit_Value,cf=8)
            #exit(str(penny_roll))
            nickel_roll=decc(( Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Roll_Unit_Value,cf=8)
            #exit(str(nickel_roll))
            dime_roll=decc(( Quantity(i.Dime_Roll_Total_Mass,i.MassUnit) / Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dime_Roll_Unit_Value,cf=8)
            #exit(str(dime_roll))
            quarter_roll=decc(( Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Quarter_Roll_Unit_Value,cf=8)
            #exit(str(quarter_roll))
            halfDollar_roll=decc(( Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.HalfDollar_Roll_Unit_Value,cf=8)
            #exit(str(halfDollar_roll))
            edollar_roll=decc(( Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Roll_Unit_Value)
            #exit(str(edollar_roll))
            edollar_roll_collectors=decc(( Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Roll_Unit_Value_collectors,cf=8)
            #exit(str(edollar_roll_collectors))
            pdollar_roll=decc(( Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.PDollar_Roll_Unit_Value,cf=8)
            total=penny+nickel+dime+quarter+halfdollar+edollar+edollar_collectors+pdollar+dollar1+dollar2+dollar5+dollar10+dollar20+dollar50+dollar100+penny_roll+nickel_roll+dime_roll+quarter_roll+halfDollar_roll+edollar_roll+edollar_roll_collectors+pdollar_roll


            
            msg=f'''Deposit: {i.did} DTOE:{i.dtoe}
Comment: {i.comment}
Group: {i.group_id}
{Fore.cyan}Penny( {Fore.light_green}Total Value  = ${penny} = {Fore.light_yellow}Total Mass( {Quantity(i.Penny_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Penny_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Penny_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Penny_Total_Mass,i.MassUnit) / Quantity(i.Penny_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Nickel( {Fore.light_green}Total Value  = ${nickel} = {Fore.light_yellow}Total Mass( {Quantity(i.Nickel_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Nickel_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Nickel_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Nickel_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dime( {Fore.light_green}Total Value  = ${dime} = {Fore.light_yellow}Total Mass( {Quantity(i.Dime_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dime_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dime_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dime_Total_Mass,i.MassUnit) / Quantity(i.Dime_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Quarter( {Fore.light_green}Total Value  = ${quarter} = {Fore.light_yellow}Total Mass( {Quantity(i.Quarter_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Quarter_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Quarter_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Quarter_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Half Dollar( {Fore.light_green}Total Value  = ${halfdollar} = {Fore.light_yellow}Total Mass( {Quantity(i.HalfDollar_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.HalfDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.HalfDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.HalfDollar_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar( {Fore.light_green}Total Value  = ${edollar} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar( Collectors {Fore.light_green}Total Value  = ${edollar_collectors} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Unit_Value_collectors,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}P Dollar( {Fore.light_green}Total Value  = ${pdollar} = {Fore.light_yellow}Total Mass( {Quantity(i.PDollar_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.PDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.PDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.PDollar_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Penny Roll( {Fore.light_green}Total Value  = ${penny_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Penny_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Penny_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Penny_Roll_Total_Mass,i.MassUnit) / Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Nickel Roll( {Fore.light_green}Total Value  = ${nickel_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Nickel_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Roll_Unit_Value,cf=8)})
{Fore.cyan}Dime Roll( {Fore.light_green}Total Value  = ${dime_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Dime_Roll_Total_Mass,i.MassUnit)}) * Mass Unit({Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dime_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dime_Roll_Total_Mass,i.MassUnit) / Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Quarter Roll( {Fore.light_green}Total Value  = ${quarter_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Quarter_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Half Dollar Roll( {Fore.light_green}Total Value  = ${halfDollar_roll} = {Fore.light_yellow}Total Mass( { Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.HalfDollar_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar Roll( {Fore.light_green}Total Value  = ${edollar_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Roll_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar Roll( Collectors {Fore.light_green}Total Value  = ${edollar_roll_collectors} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Roll_Unit_Value_collectors,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}P Dollar Roll( {Fore.light_green}Total Value  = ${pdollar_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.PDollar_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 1( {Fore.light_green}Total Value  = ${dollar1} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar1_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar1_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar1_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar1_Total_Mass,i.MassUnit) / Quantity(i.Dollar1_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 2( {Fore.light_green}Total Value  = ${dollar2} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar2_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar2_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar2_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar2_Total_Mass,i.MassUnit) / Quantity(i.Dollar2_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 5( {Fore.light_green}Total Value  = ${dollar5} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar5_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar5_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar5_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar5_Total_Mass,i.MassUnit) / Quantity(i.Dollar5_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 10( {Fore.light_green}Total Value  = ${dollar10} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar10_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar10_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar10_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar10_Total_Mass,i.MassUnit) / Quantity(i.Dollar10_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 20( {Fore.light_green}Total Value  = ${dollar20} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar20_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar20_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar20_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar20_Total_Mass,i.MassUnit) / Quantity(i.Dollar20_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 50( {Fore.light_green}Total Value  = ${dollar50} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar50_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar50_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar50_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar50_Total_Mass,i.MassUnit) / Quantity(i.Dollar50_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 100( {Fore.light_green}Total Value  = ${dollar100} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar100_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar100_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar100_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar100_Total_Mass,i.MassUnit) / Quantity(i.Dollar100_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.orange_red_1}Deposit Total({Fore.light_yellow}${Fore.light_green}{total}){Style.reset}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def deposit_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_deposit(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=deposit_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def deposit_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
deposit_menu={
    str(uuid1()):{
    "cmds":['deposit custom',],
    "exec":lambda self:s2cb_deposit(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def depositLogger(Model=Deposit,short_view=deposit_short_view,menu=deposit_menu):
    return ModelLogger(Model=Deposit,short_view=deposit_short_view,menu=deposit_menu)

def safe_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            penny= decc(( Quantity(i.Penny_Total_Mass,i.MassUnit) / Quantity(i.Penny_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Penny_Unit_Value,cf=8)
            #exit(str(penny))
            nickel= decc(( Quantity(i.Nickel_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Unit_Value,cf=8)
            #exit(str(nickel))
            dime= decc(( Quantity(i.Dime_Total_Mass,i.MassUnit) / Quantity(i.Dime_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dime_Unit_Value,cf=8)
            #exit(str(dime))
            quarter= decc(( Quantity(i.Quarter_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Quarter_Unit_Value,cf=8)
            #exit(str(quarter))
            halfdollar= decc(( Quantity(i.HalfDollar_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.HalfDollar_Unit_Value,cf=8)
            #exit(str(halfdollar))
            edollar=decc(( Quantity(i.EDollar_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Unit_Value,cf=8)
            #exit(str(edollar))
            edollar_collectors=decc(( Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Unit_Value_collectors,cf=8)
            #exit(str(edollar_collectors))
            pdollar=decc(( Quantity(i.PDollar_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.PDollar_Unit_Value,cf=8)
            #exit(str(pdollar))
            
            dollar1=decc(( Quantity(i.Dollar1_Total_Mass,i.MassUnit) / Quantity(i.Dollar1_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar1_Unit_Value,cf=8)
            #exit(str(dollar1))
            dollar2=decc(( Quantity(i.Dollar2_Total_Mass,i.MassUnit) / Quantity(i.Dollar2_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar2_Unit_Value,cf=8)
            #exit(str(dollar2))
            dollar5=decc(( Quantity(i.Dollar5_Total_Mass,i.MassUnit) / Quantity(i.Dollar5_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar5_Unit_Value,cf=8)
            #exit(str(dollar5))
            dollar10=decc(( Quantity(i.Dollar10_Total_Mass,i.MassUnit) / Quantity(i.Dollar10_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar10_Unit_Value,cf=8)
            #exit(str(dollar10))
            dollar20=decc(( Quantity(i.Dollar20_Total_Mass,i.MassUnit) / Quantity(i.Dollar20_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar20_Unit_Value,cf=8)
            #exit(str(dollar20))
            dollar50=decc(( Quantity(i.Dollar50_Total_Mass,i.MassUnit) / Quantity(i.Dollar50_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar50_Unit_Value,cf=8)
            #exit(str(dollar50))
            dollar100=decc(( Quantity(i.Dollar100_Total_Mass,i.MassUnit) / Quantity(i.Dollar100_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dollar100_Unit_Value,cf=8)
            #exit(str(dollar100))

            penny_roll=decc(( Quantity(i.Penny_Roll_Total_Mass,i.MassUnit) / Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Penny_Roll_Unit_Value,cf=8)
            #exit(str(penny_roll))
            nickel_roll=decc(( Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Roll_Unit_Value,cf=8)
            #exit(str(nickel_roll))
            dime_roll=decc(( Quantity(i.Dime_Roll_Total_Mass,i.MassUnit) / Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Dime_Roll_Unit_Value,cf=8)
            #exit(str(dime_roll))
            quarter_roll=decc(( Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Quarter_Roll_Unit_Value,cf=8)
            #exit(str(quarter_roll))
            halfDollar_roll=decc(( Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.HalfDollar_Roll_Unit_Value,cf=8)
            #exit(str(halfDollar_roll))
            edollar_roll=decc(( Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Roll_Unit_Value)
            #exit(str(edollar_roll))
            edollar_roll_collectors=decc(( Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8) * decc(i.EDollar_Roll_Unit_Value_collectors,cf=8)
            #exit(str(edollar_roll_collectors))
            pdollar_roll=decc(( Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.PDollar_Roll_Unit_Value,cf=8)
            total=penny+nickel+dime+quarter+halfdollar+edollar+edollar_collectors+pdollar+dollar1+dollar2+dollar5+dollar10+dollar20+dollar50+dollar100+penny_roll+nickel_roll+dime_roll+quarter_roll+halfDollar_roll+edollar_roll+edollar_roll_collectors+pdollar_roll


            
            msg=f'''Safe: {i.sid} DTOE:{i.dtoe}
Comment: {i.comment}
Group: {i.group_id}
Whom: {i.whom}
{Fore.cyan}Penny( {Fore.light_green}Total Value  = ${penny} = {Fore.light_yellow}Total Mass( {Quantity(i.Penny_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Penny_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Penny_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Penny_Total_Mass,i.MassUnit) / Quantity(i.Penny_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Nickel( {Fore.light_green}Total Value  = ${nickel} = {Fore.light_yellow}Total Mass( {Quantity(i.Nickel_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Nickel_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Nickel_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Nickel_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dime( {Fore.light_green}Total Value  = ${dime} = {Fore.light_yellow}Total Mass( {Quantity(i.Dime_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dime_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dime_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dime_Total_Mass,i.MassUnit) / Quantity(i.Dime_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Quarter( {Fore.light_green}Total Value  = ${quarter} = {Fore.light_yellow}Total Mass( {Quantity(i.Quarter_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Quarter_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Quarter_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Quarter_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Half Dollar( {Fore.light_green}Total Value  = ${halfdollar} = {Fore.light_yellow}Total Mass( {Quantity(i.HalfDollar_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.HalfDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.HalfDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.HalfDollar_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar( {Fore.light_green}Total Value  = ${edollar} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar( Collectors {Fore.light_green}Total Value  = ${edollar_collectors} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Unit_Value_collectors,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}P Dollar( {Fore.light_green}Total Value  = ${pdollar} = {Fore.light_yellow}Total Mass( {Quantity(i.PDollar_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.PDollar_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.PDollar_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.PDollar_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Penny Roll( {Fore.light_green}Total Value  = ${penny_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Penny_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Penny_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Penny_Roll_Total_Mass,i.MassUnit) / Quantity(i.Penny_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Nickel Roll( {Fore.light_green}Total Value  = ${nickel_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Nickel_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Nickel_Roll_Total_Mass,i.MassUnit) / Quantity(i.Nickel_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8) * decc(i.Nickel_Roll_Unit_Value,cf=8)})
{Fore.cyan}Dime Roll( {Fore.light_green}Total Value  = ${dime_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Dime_Roll_Total_Mass,i.MassUnit)}) * Mass Unit({Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dime_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dime_Roll_Total_Mass,i.MassUnit) / Quantity(i.Dime_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Quarter Roll( {Fore.light_green}Total Value  = ${quarter_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Quarter_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Quarter_Roll_Total_Mass,i.MassUnit) / Quantity(i.Quarter_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Half Dollar Roll( {Fore.light_green}Total Value  = ${halfDollar_roll} = {Fore.light_yellow}Total Mass( { Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.HalfDollar_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.HalfDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.HalfDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar Roll( {Fore.light_green}Total Value  = ${edollar_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Roll_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}E Dollar Roll( Collectors {Fore.light_green}Total Value  = ${edollar_roll_collectors} = {Fore.light_yellow}Total Mass( {Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.EDollar_Roll_Unit_Value_collectors,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.EDollar_Roll_Total_Mass_collectors,i.MassUnit) / Quantity(i.EDollar_Roll_Unit_Mass_collectors,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}P Dollar Roll( {Fore.light_green}Total Value  = ${pdollar_roll} = {Fore.light_yellow}Total Mass( {Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.PDollar_Roll_Unit_Value,cf=8)},{Fore.medium_violet_red} Units={decc(( Quantity(i.PDollar_Roll_Total_Mass,i.MassUnit) / Quantity(i.PDollar_Roll_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 1( {Fore.light_green}Total Value  = ${dollar1} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar1_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar1_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar1_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar1_Total_Mass,i.MassUnit) / Quantity(i.Dollar1_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 2( {Fore.light_green}Total Value  = ${dollar2} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar2_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar2_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar2_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar2_Total_Mass,i.MassUnit) / Quantity(i.Dollar2_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 5( {Fore.light_green}Total Value  = ${dollar5} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar5_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar5_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar5_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar5_Total_Mass,i.MassUnit) / Quantity(i.Dollar5_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 10( {Fore.light_green}Total Value  = ${dollar10} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar10_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar10_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar10_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar10_Total_Mass,i.MassUnit) / Quantity(i.Dollar10_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 20( {Fore.light_green}Total Value  = ${dollar20} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar20_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar20_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar20_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar20_Total_Mass,i.MassUnit) / Quantity(i.Dollar20_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 50( {Fore.light_green}Total Value  = ${dollar50} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar50_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar50_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar50_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar50_Total_Mass,i.MassUnit) / Quantity(i.Dollar50_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.cyan}Dollar Bill 100( {Fore.light_green}Total Value  = ${dollar100} = {Fore.light_yellow}Total Mass( {Quantity(i.Dollar100_Total_Mass,i.MassUnit)}) / {Fore.light_steel_blue}Unit Mass({Quantity(i.Dollar100_Unit_Mass,i.MassUnit)} * {Fore.light_magenta}Unit Value=${decc(i.Dollar100_Unit_Value)},{Fore.medium_violet_red} Units={decc(( Quantity(i.Dollar100_Total_Mass,i.MassUnit) / Quantity(i.Dollar100_Unit_Mass,i.MassUnit) ).magnitude,cf=8)})
{Fore.orange_red_1}Safe Total({Fore.light_yellow}${Fore.light_green}{total}){Style.reset}
{"*"*os.get_terminal_size().columns}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def safe_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_safe(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=safe_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def safe_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
safe_menu={
    str(uuid1()):{
    "cmds":['safe custom',],
    "exec":lambda self:s2cb_safe(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}


#TriedToWake
def safeLogger(Model=Safe,short_view=safe_short_view,menu=safe_menu):
    return ModelLogger(Model=Safe,short_view=safe_short_view,menu=safe_menu)

def ExpenseText():
    while True:
        try:
            fields={
            'Expense.Name':{
                'default':'gasoline.regular',
                'type':'string',
            },
            'Expense.Cost':{
                'default':4.469384,
                'type':'float'
            },
            'Location/Address':{
                'default':'7Eleven',
                'type':'string',
            },
            'Qty purchased':{
                'type':'string',
                'default':'1.016 gal',
            },
            'Rate.How Much of Qty?':{
                'type':'string',
                'default':'1 gal',
            },
            'Rate.For What Cost, or Price?':{
                'default':4.399,
                'type':'float'
            },
            'DTOE':{
                'default':datetime.now(),
                'type':'datetime', 
            },
            'nID':{
                'default':nanoid.generate(alphabet=string.ascii_letters+string.digits+"./- ",size=8),
                'type':'string'
            },
            }
            fb=FormBuilder(data=fields,passThruText="generate expense text on the go")
            if fb in [None,'None','NaN']:
                return
            else:
                return str(fb)
        except Exception as e:
            print(e)
            continue

class GarbageCollection:
    def __init__(self,menu={}):
        cmds={
        str(uuid1()):{
            "cmds":['collect','clean','clct','cln'],
            "exec":lambda: gc.collect(),
            "desc":"collect garbage",
            },
        str(uuid1()):{
            "cmds":['freeze','frz','frez',],
            "exec":lambda: gc.freeze(),
            "desc":"freeze all objects tracked",
            },
        str(uuid1()):{
            "cmds":['get freeze count','gtfrzcnt','gt frez cnt',],
            "exec":lambda: gc.get_freeze_count(),
            "desc":"get freeze count",
            },
        str(uuid1()):{
            "cmds":['unfreeze','ufrz','ufrez',],
            "exec":lambda: gc.unfreeze(),
            "desc":"unfreeze all objects tracked",
            },
        str(uuid1()):{
            "cmds":['is enabled','isenable','enabled',],
            "exec":lambda: print(gc.isenabled()),
            "desc":"is garbage collection enabled?",
            },
        str(uuid1()):{
            "cmds":['get stats','gtstts','gtsts',],
            "exec":lambda: print(gc.get_stats()),
            "desc":"get stats",
            },
        }

        cmds.update(menu)
        htext=[]
        cta=len(cmds.keys())
        for num,i in enumerate(cmds):
            if str(num) not in cmds[i]['cmds']:
                cmds[i]['cmds'].append(str(num))
            msg=f"{cmds[i]['cmds']} - {Fore.light_green}{cmds[i]['desc']}"
            htext.append(std_colorize(msg,num,cta))

        htext='\n'.join(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}{self.__class__.__name__}: {Fore.light_green}Exec:",helpText=htext,data="string")
            if doWhat in [None,"NaN"]:
                return None
            elif doWhat in ['d','']:
                print(htext)
                continue
            for c in cmds:
                if doWhat.lower() in [i.lower() for i in cmds[c]['cmds']]:
                    if callable(cmds[c]['exec']):
                        try:
                            cmds[c]['exec']()
                        except Exception as e:
                            try:
                                cmds[c]['exec'](self)
                                continue
                            except Exception as ee:
                                print(ee)
                            print(e)
                            break
                    else:
                        print(cmds[c],"!Callable()")



def count_per_mil():
    while True:
        try:
            fields={
            'total width':{
                'type':'float',
                'default':float(detectGetOrSet('cpm total width',0.0,setValue=False,literal=False)),
            },
            'total width unit':{
                'type':'string',
                'default':detectGetOrSet('cpm total width unit','inch',setValue=False,literal=True)
            },
            'unit width':{
                'type':'float',
                'default':float(detectGetOrSet('cpm unit width',0.35,setValue=False,literal=False)),
            },
            'unit width unit':{
                'type':'string',
                'default':detectGetOrSet('cpm unit width unit','mm',setValue=False,literal=True)
            },
            }

            fb=FormBuilder(data=fields,passThruText="Total Count for Width (Count Per Mil)")
            if fb in [None,]:
                return
            rate=pint.Quantity(f"{fb['unit width']} {fb['unit width unit']}").to('mm')
            total=pint.Quantity(f"{fb['total width']} {fb['total width unit']}").to('mm')
            count=total*(1/rate)
            print(f"{Fore.light_red}Result :{Fore.light_cyan}{decc(count.magnitude)}{Style.reset}")
            return decc(count.magnitude)

        except Exception as e:
            print(e)

def deweyDecimalSystem_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            
            
            msg=f'''
{Fore.orange_red_1}ddsid {Fore.light_blue}={Fore.light_yellow}{i.ddsid}{Style.reset}

{Fore.orange_red_1}Number {Fore.light_blue}={Fore.light_yellow}{i.Number}{Style.reset}
{Fore.orange_red_1}CallNumber {Fore.light_blue}={Fore.light_yellow}{i.CallNumber}{Style.reset}
{Fore.orange_red_1}Discipline {Fore.light_blue}={Fore.light_yellow}{i.Discipline}{Style.reset}
{Fore.orange_red_1}Common_Topics {Fore.light_blue}={Fore.light_yellow}{i.Common_Topics}{Style.reset}

{Fore.orange_red_1}comment {Fore.light_blue}={Fore.light_yellow}{i.comment}{Style.reset}
{Fore.orange_red_1}group_id {Fore.light_blue}={Fore.light_yellow}{i.group_id}{Style.reset}
{Fore.orange_red_1}dtoe {Fore.light_blue}={Fore.light_yellow}{i.dtoe}{Style.reset}
{"*"*os.get_terminal_size().columns}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def deweyDecimalSystem_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_deweyDecimalSystem(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=deweyDecimalSystem_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def deweyDecimalSystem_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
def import_dds_ff(self):
    with Session(ENGINE) as session:
        #query=session.query(self.Model)
        importFile=detectGetOrSet("dds ifile","dds.csv",setValue=False,literal=True)
        with Path(importFile).open('r') as ifile:
            x=csv.reader(ifile,delimiter='#')
            for i in x:
                model=self.Model(Number=float(i[0]),Discipline=str(i[1]))
                session.add(model)
                session.commit()


deweyDecimalSystem_menu={
    str(uuid1()):{
    "cmds":['deweyDecimalSystem custom',],
    "exec":lambda self:s2cb_deweyDecimalSystem(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['import from file','iff'],
    "exec":lambda self:import_dds_ff(self),
    "desc":"import dewey decimal data from csv with fields: Number,Discipline only",
    }
}

#TriedToWake
def deweyDecimalSystemLogger(Model=DeweyDecimalSystem,short_view=deweyDecimalSystem_short_view,menu=deweyDecimalSystem_menu):
    return ModelLogger(Model=DeweyDecimalSystem,short_view=deweyDecimalSystem_short_view,menu=deweyDecimalSystem_menu)

def dmu_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''
    {Fore.grey_50}dmid{Fore.light_red}={Fore.light_steel_blue}{i.dmid}{Style.reset}
    {Fore.light_magenta}date{Fore.light_red}={Fore.light_green}{i.date}{Style.reset}
    {Fore.light_magenta}time{Fore.light_red}={Fore.light_green}{i.time}{Style.reset}
    {Fore.light_magenta}datetime{Fore.light_red}={Fore.light_green}{i.datetime}{Style.reset}

    {Fore.grey_85}#notes about weather events/space/trade/government reg. that is not numerically quanifiable but could be a contributing factor to demand{Style.reset}
    {Fore.grey_85}#events internal to city/county/region on only{Style.reset}
    {Fore.orange_red_1}local_events{Fore.light_yellow}={Fore.dark_goldenrod}{i.local_events}
    {Fore.grey_85}#events internal to the state only{Style.reset}
    {Fore.orange_red_1}state_events{Fore.light_yellow}={Fore.dark_goldenrod}{i.state_events}
    {Fore.grey_85}#events internal to the us only{Style.reset}
    {Fore.orange_red_1}national_events{Fore.light_yellow}={Fore.dark_goldenrod}{i.national_events}
    {Fore.grey_85}#between multiple nations{Style.reset}
    {Fore.orange_red_1}international_events{Fore.light_yellow}={Fore.dark_goldenrod}{i.international_events}
    {Fore.grey_85}#involves everyone on the globe{Style.reset}
    {Fore.orange_red_1}global_events{Fore.light_yellow}={Fore.dark_goldenrod}{i.global_events}

    {Fore.grey_85}#weather metric for forecast_weather{Style.reset}
    {Fore.light_cyan}name{Fore.light_red}={Fore.light_green}{i.name}{Style.reset}
    {Fore.light_cyan}condition{Fore.light_red}={Fore.light_green}{i.condition}{Style.reset}
    {Fore.light_cyan}temp_c{Fore.light_red}={Fore.light_green}{i.temp_c}{Style.reset}
    {Fore.light_cyan}temp_f{Fore.light_red}={Fore.light_green}{i.temp_f}{Style.reset}
    {Fore.light_cyan}wind_mph{Fore.light_red}={Fore.light_green}{i.wind_mph}{Style.reset}
    {Fore.light_cyan}pressure_mb{Fore.light_red}={Fore.light_green}{i.pressure_mb}{Style.reset}
    {Fore.light_cyan}precip_in{Fore.light_red}={Fore.light_green}{i.precip_in}{Style.reset}
    {Fore.light_cyan}humidity{Fore.light_red}={Fore.light_green}{i.humidity}{Style.reset}
    {Fore.light_cyan}cloud{Fore.light_red}={Fore.light_green}{i.cloud}{Style.reset}
    {Fore.light_cyan}uv{Fore.light_red}={Fore.light_green}{i.uv}{Style.reset}
    {Fore.light_cyan}location{Fore.light_red}={Fore.light_green}{i.location}{Style.reset}
'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def dmu_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_dmu(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=dmu_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def dmu_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
dmu_menu={
    str(uuid1()):{
    "cmds":['dmu custom',],
    "exec":lambda self:s2cb_dmu(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}


#TriedToWake
def dmuLogger(Model=DateMetricsManual,short_view=dmu_short_view,menu=dmu_menu):
    return ModelLogger(Model=DateMetricsManual,short_view=dmu_short_view,menu=dmu_menu)


def symptom_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            
            
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def symptom_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_symptom(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=symptom_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def symptom_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
symptom_menu={
    str(uuid1()):{
    "cmds":['symptom custom',],
    "exec":lambda self:s2cb_symptom(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}
#bptxt - bill paid text

#TriedToWake
def symptomLogger(Model=Symptom,short_view=symptom_short_view,menu=symptom_menu):
    return ModelLogger(Model=Symptom,short_view=symptom_short_view,menu=symptom_menu)


default_bptxt_bank_app=db.detectGetOrSet("default bptxt bank app","CashApp",setValue=False,literal=True)
def bill_paid_text():
    fields={
            "For Whom is the Billed Owed (debtor)":{
                'type':'String',
                'default':db.detectGetOrSet("bptxt debtor?",f"Carl Joseph Hirner III",setValue=False,literal=True),
            },
            "Who Am I?":{
                'type':'String',
                'default':db.detectGetOrSet("bptxt who am i?",f"Carl Joseph Hirner III",setValue=False,literal=True),
            },
            "What was the Bill for?":{
                'type':"string",
                'default':db.detectGetOrSet("bptxt What was the Bill for?",f"rent",setValue=False,literal=True),
            },
            "How Much was the Bill?":{
                'type':"float",
                'default':float(db.detectGetOrSet("bptxt How Much was the Bill?",300,setValue=False,literal=False)),
            },
            "To Whom the bill is owed/paid/(payee)?":{
                'type':'String',
                'default':db.detectGetOrSet("bptxt payee?",f"Charles & Linda Rickman",setValue=False,literal=True),
            },
            "What was used to perform the transfer?":{
                'type':'string',
                'default':db.detectGetOrSet("bptxt What was used to perform the transfer?",f"the '{default_bptxt_bank_app}' app installed on my mobile cellular device",setValue=False,literal=True),
            },
            "reciept transaction number/ID (If Any)":{
                'type':'String',
                'default':db.detectGetOrSet("bptxt reciept transaction number/ID (If Any)",'',setValue=False,literal=True),
            },
             "dtoe":{
                'type':'datetime',
                'default':datetime.now()
            },
            "Message Serial No.":{
                'type':'string',
                'default':str(nanoid.generate(alphabet=string.ascii_letters+string.digits+"/-",size=8)),
            },
            }
    while True:
        try:
            fb=FormBuilder(data=fields,passThruText="Bill Paid Text")
            if fb in [None,'None','NaN','nan']:
                return
            for k in fb:
                fields[k]['default']=fb[k]

            
            msg=f'''I ({fb['Who Am I?']}), paid the debtor's ({fb['For Whom is the Billed Owed (debtor)']}) bill for '{fb['What was the Bill for?']}'.
A payment of ${fb['How Much was the Bill?']} was paid to '{fb['To Whom the bill is owed/paid/(payee)?']}
via the '{fb['What was used to perform the transfer?']}'.
The Transaction Number/ID is '{fb['reciept transaction number/ID (If Any)']}'.
The Message Serial Number is '{fb['Message Serial No.']}'.
This was done on '{fb['dtoe']}'.'''
            print(msg)
            useMessage=Control(func=FormBuilderMkText,ptext="Use this message?",helpText="yes or no",data="boolean")
            if useMessage in [None,'NAN','nan']:
                return
            elif useMessage in ['d','',True]:
                return msg
            else:
                continue
        except Exception as e:
            print(e,str(e),repr(e))


def moveShift():
    fields={
            "shift start":{
                'type':'datetime',
                'default':datetime.now()
            },
            'shift end':{
            'type':'datetime',
            'default':datetime.now()+timedelta(hours=8)
            },
            'hours to change shift by':{
            'type':'float',
            'default':7.5
            }
            }
    while True:
        try:
            fb=FormBuilder(data=fields,passThruText="Old To New Shift")
            if fb in [None,'None','NaN','nan']:
                return
            for k in fb:
                fields[k]['default']=fb[k]

            new_shift_end=fb['shift end']+timedelta(hours=fb['hours to change shift by'])
            new_shift_start=fb['shift start']+timedelta(hours=fb['hours to change shift by'])
            msg=f'''
{Fore.light_green}Shift Start = {Fore.light_steel_blue}{fb['shift start']}{Style.reset}
{Fore.light_red}Shift End = {Fore.light_steel_blue}{fb['shift end']}{Style.reset}
{Fore.cyan}Shifted By = {Fore.light_magenta}{timedelta(hours=fb['hours to change shift by'])}{Style.reset}
{Fore.light_yellow}New Shift Start = {Fore.light_magenta}{new_shift_start}{Style.reset}
{Fore.light_yellow}New Shift End = {Fore.light_magenta}{new_shift_end}{Style.reset}
            '''
            print(msg)
            useMessage=Control(func=FormBuilderMkText,ptext="Use this message?",helpText="yes or no",data="boolean")
            if useMessage in [None,'NAN','nan']:
                return
            elif useMessage in ['d','',True]:
                return msg
            else:
                continue
        except Exception as e:
            print(e,str(e),repr(e))


def offsetClock_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            
            
            msg=f'''{Fore.light_red}[{Fore.light_magenta}{i.ClockName}{Fore.light_red}] {Fore.light_steel_blue}There{Fore.orange_red_1}: {datetime.now()+timedelta(hours=i.Offset_from_network_time_hours,minutes=i.Offset_from_network_time_minutes,seconds=i.Offset_from_network_time_seconds,days=i.Offset_from_network_time_days)}{Fore.cyan} Now{Fore.light_cyan}: {datetime.now()}
{Fore.light_steel_blue}ocid={i.ocid} dtoe='{i.dtoe}' comment='{i.comment}' group_id='{i.group_id}'{Style.reset}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def offsetClock_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_offsetClock(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=offsetClock_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def offsetClock_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
offsetClock_menu={
    str(uuid1()):{
    "cmds":['offsetClock custom',],
    "exec":lambda self:s2cb_offsetClock(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}
#bptxt - bill paid text

#TriedToWake
def offsetClockLogger(Model=OffsetClock,short_view=offsetClock_short_view,menu=offsetClock_menu):
    return ModelLogger(Model=OffsetClock,short_view=offsetClock_short_view,menu=offsetClock_menu)


def FormatEntryInsertScript():
    fields={
            'sku':{
            'default':'',
            'type':'string'
            },
            'name':{
            'default':'',
            'type':'string',
            },
            'price':{
            'default':1.25,
            'type':'float'
            },
            }
    while True:
        try:
            
            fb=FormBuilder(data=fields,passThruText="gnerate insert script")
            if fb in [None,'None','NaN','nan']:
                return
            for k in fb:
                fields[k]['default']=fb[k]
            
            msg=f'''{fb['sku']}
1
{fb['name']}
{fb['price']}
t
0
f'''
            print(msg)
            useMessage=Control(func=FormBuilderMkText,ptext="Use this message?",helpText="yes or no",data="boolean")
            if useMessage in [None,'NAN','nan']:
                return
            elif useMessage in ['d','',True]:
                try:
                    pyperclip.copy(msg)
                except Exception as e:
                    return msg
            else:
                continue
        except Exception as e:
            print(e)


def Accronym():
    fields={
            'name':{
            'default':'',
            'type':'string'
            },
            }
    while True:
        try:
            
            fb=FormBuilder(data=fields,passThruText="generate accronym from name")
            if fb in [None,'None','NaN','nan']:
                return
            for k in fb:
                fields[k]['default']=fb[k]
            def accronym(x):
                line=[]
                numCounter=0
                for num,sub in enumerate(x.split(" ")):
                    try:
                        z=f"{str(int(sub))}"
                    except Exception as e:
                        z=sub[0].lower()
                    line.append(z)
                line='-'.join(re.findall(r'\d+|\D+',''.join(line)))
                print(line)
                return line

            msg=accronym(fb['name'])

            print(msg)
            useMessage=Control(func=FormBuilderMkText,ptext="Use this message?",helpText="yes or no",data="boolean")
            if useMessage in [None,'NAN','nan']:
                return
            elif useMessage in ['d','',True]:
                try:
                    pyperclip.copy(msg)
                    useMessage=Control(func=FormBuilderMkText,ptext="Return this message?",helpText="yes or no",data="boolean")
                    if useMessage in [None,'NAN','nan']:
                        return
                    elif useMessage in ['d','',True]:
                        return msg
                    else:
                        continue
                except Exception as e:
                    return msg
            else:
                continue
        except Exception as e:
            print(e)


def ClockToDecimal():
    def datetime2decimal(now_hr=datetime.now().hour,now_minute=datetime.now().minute,now_second=datetime.now().second):
        return now_hr+(now_minute/60)+((now_second/60)/60)
    fields={
    'Time':{
        'type':'time',
        'default':None
        },
    }
    fb=FormBuilder(data=fields)
    if fb in [None,]:
        return
    f=fb['Time']
    return datetime2decimal(f.hour,f.minute,f.second)



def HourOfTheYear():
    def datetime2decimal(now_hr=datetime.now().hour,now_minute=datetime.now().minute,now_second=datetime.now().second):
        return now_hr+(now_minute/60)+((now_second/60)/60)
    fields={
    'datetime':{
        'type':'datetime',
        'default':None
        },
    }
    fb=FormBuilder(data=fields)
    if fb in [None,]:
        return
    f=fb['datetime']
    if not f:
        f=datetime.now()
    yearStart=datetime(datetime.now().year,1,1,0,0,0)
    secondsOfTheYear=(f-yearStart).total_seconds()
    minutesOfTheYear=secondsOfTheYear/60
    hoursOfTheYear=minutesOfTheYear/60
    daysOfTheYear=hoursOfTheYear/24

    msg=f"""
{Fore.light_red}Year Start {Fore.orange_red_1}= {Fore.grey_85}'{yearStart}'{Style.reset}
{Fore.green_yellow}DateTime Entered {Fore.orange_red_1}= {Fore.grey_85}'{f}'{Style.reset}
{Fore.light_magenta}Seconds of The Year Elapsed {Fore.orange_red_1}= {Fore.light_steel_blue}'{secondsOfTheYear}'{Style.reset}
{Fore.light_green}Minutes of The Year Elapsed {Fore.orange_red_1}= {Fore.light_steel_blue}'{minutesOfTheYear}'{Style.reset}
{Fore.light_magenta}Hours of The Year Elapsed {Fore.orange_red_1}= {Fore.light_steel_blue}'{hoursOfTheYear}'{Style.reset}
{Fore.light_green}Days of The Year Elapsed {Fore.orange_red_1}= {Fore.light_steel_blue}'{daysOfTheYear}'{Style.reset}
{Fore.cyan}Hours of the Day Decimal(BASE10) {Fore.orange_red_1}= {Fore.medium_violet_red}'{datetime2decimal(f.hour,f.minute,f.second)}'{Style.reset}
    """
    return msg


def NewEntryName():
    try:
        fields={
            'Brand Name':{
                'type':'string',
                'default':'',
            },
            'Product Name':{
                'type':'string',
                'default':'',
            },
            'Product Version':{
                'type':'string',
                'default':'',
            },
            'Product Style/Quality/Concentration':{
                'type':'string',
                'default':'',
            },
            'Net Weight':{
                'type':'string',
                'default':'',
            },
        }
        m=f"""'Net Weight'~='24 Oz(1 lb 8 Oz) 680g'
'Product Style/Quality/Concentration'~='Medium-Dark Roast'
'Product Version'~='Columbian'
'Product Name'~='Ground Coffee'
'Brand Name'~='McCafe'
        """
        fb=FormBuilder(data=fields,passThruText=m)
        if fb in [None,]:
            return

        msg=f"{fb['Brand Name']} {fb['Product Name']} {fb['Product Version']} {fb['Product Style/Quality/Concentration']} {fb['Net Weight']}"
        print(f"{Fore.orange_red_1}{msg}{Style.reset}")
        return msg

    except Exception as e:
        print(e)
        return None

def emotion_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            
            
            msg=f'''{'*'*os.get_terminal_size().columns}
{Fore.orange_red_1}emoid={Fore.light_green}{i.emoid}{Style.reset}
{Fore.orange_red_1}NameDesc={Fore.light_green}{i.NameDesc}{Style.reset}
{Fore.orange_red_1}TimeSpentComment={Fore.light_green}{i.TimeSpentComment}{Style.reset}
{Fore.orange_red_1}comment={Fore.light_green}{i.comment}{Style.reset}
{Fore.orange_red_1}group_id={Fore.light_green}{i.group_id}{Style.reset}
{Fore.orange_red_1}name={Fore.light_green}{i.name}{Style.reset}
{Fore.orange_red_1}dtoe={Fore.light_green}{i.dtoe}{Style.reset}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def emotion_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_emotion(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=emotion_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def emotion_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
emotion_menu={
    str(uuid1()):{
    "cmds":['emotion custom',],
    "exec":lambda self:s2cb_emotion(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}
#bptxt - bill paid text

#TriedToWake
def emotionLogger(Model=Emotion,short_view=emotion_short_view,menu=emotion_menu):
    return ModelLogger(Model=Emotion,short_view=emotion_short_view,menu=emotion_menu)

def Convert():
    try:
        fields={
            'From Value':{
                'type':'float',
                'default':(20+(5/12))/18.98,
            },
            'From Unit':{
                'type':'string',
                'default':'feet per second',
            },
            'To Unit':{
                'type':'string',
                'default':'feet per hour',
            },

        }
        m=f"""'
        Estimate Walking Distance"""
        fb=FormBuilder(data=fields,passThruText=m)
        if fb in [None,]:
            return
        print(Quantity(fb['From Value'],fb['From Unit']).to(fb['To Unit']))
        return Quantity(fb['From Value'],fb['From Unit']).to(fb['To Unit']).magnitude

    except Exception as e:
        print(e)
        return None

def FuelOverArea():
    try:
        fields={
            'Fuel Value':{
                'type':'float',
                'default':16,
            },
            'Fuel Unit':{
                'type':'string',
                'default':'floz',
            },
            'Area Value':{
                'type':'float',
                'default':1922.3,
            },
            'Area Unit':{
                'type':'string',
                'default':'square feet',
            },

        }
        m=f"""'
        Estimate Walking Distance"""
        fb=FormBuilder(data=fields,passThruText=m)
        if fb in [None,]:
            return
        fmula=Quantity(fb['Fuel Value'],fb['Fuel Unit'])/Quantity(fb['Area Value'],fb['Area Unit'])
        print(fmula)
        return fmula.magnitude

    except Exception as e:
        print(e)
        return None

def cooling_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            walls_load = i.walls_u_factor * i.walls_area * i.delta_t
            window_load = i.window_area * i.shgf * i.sc
            total_btu = walls_load + window_load + i.people_load + i.equipment_load
            total_tons = total_btu / 12000
            msg=f'''
{'$'*12}{i.name}|{i.emoid}|{i.dtoe}{'@'*12}
# --- 1. Transmission Load (Walls, Roof, Floor) ---
# Formula: Q = U * Area * Delta_T
# Example values for a standard insulated shed
walls_area = {i.walls_area} # sq ft
walls_u_factor = {i.walls_u_factor} # Example for R-13 insulation
delta_t = {i.delta_t}  # Temp difference between outside and inside (F)

walls_load = walls_u_factor * walls_area * delta_t
walls_load = {walls_load}
# --- 2. Solar Gain (Windows) ---
# Formula: Area * SC * SHGF (Simplified)
window_area = {i.window_area}  # sq ft
shgf = {i.shgf}  # Solar Heat Gain Factor for summer sun (BTU/hr-sq ft)
sc = {i.sc}  # Shading coefficient

window_load = window_area * shgf * sc   
window_load = {window_load}         
# --- 3. Occupancy & Equipment ---
# Baseline defaults
people_load = {i.people_load}  # total BTU/hr per person for estimated level of activity
equipment_load = {i.equipment_load}  # BTU/hr for lights/tools

# --- 4. Total Load ---
total_btu = walls_load + window_load + people_load + equipment_load
total_btu = {walls_load} + {window_load} + {i.people_load} + {i.equipment_load}
total_btu = {total_btu}
# Convert to Tons of AC (1 Ton = 12,000 BTU/hr)
total_tons = total_btu / 12000
total_tons = {total_tons}
--- Cooling Load Results ---
Transmission Load: {walls_load:.2f} BTU/hr
Window Solar Load: {window_load:.2f} BTU/hr
Occupancy/Gear: {i.people_load + i.equipment_load:.2f} BTU/hr

Total Cooling Load: {total_btu:.2f} BTU/hr
Recommended AC Size: {total_tons:.2f} Tons
            '''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def cooling_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_cooling(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=cooling_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    
def average_btus(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                wallsLoad=[]
                windowLoad=[]
                peopleLoad=[]
                equipmentLoad=[]
                totalBtu=[]
                totalTons=[]
                for num,i in enumerate(results):
                    walls_load = i.walls_u_factor * i.walls_area * i.delta_t
                    window_load = i.window_area * i.shgf * i.sc
                    total_btu = walls_load + window_load + i.people_load + i.equipment_load
                    total_tons = total_btu / 12000
                    wallsLoad.append(walls_load)
                    windowLoad.append(window_load)
                    peopleLoad.append(i.people_load)
                    equipmentLoad.append(i.equipment_load)
                    totalBtu.append(total_btu)
                    totalTons.append(total_tons)
                #print(np.mean(total_btu),"AVG BTU/Hr")
                #print(np.mean(),"")
                avg_total_btu=np.mean(wallsLoad) + np.mean(windowLoad) + np.mean(peopleLoad) + np.mean(equipmentLoad)
                print(f"{Fore.orange_red_1}",np.mean(wallsLoad),f"{Fore.light_steel_blue} = {Fore.medium_violet_red}AVG Walls Load{Style.reset}")
                print(f"{Fore.orange_red_1}",np.mean(windowLoad),f"{Fore.light_steel_blue} = {Fore.medium_violet_red}AVG Window Load{Style.reset}")
                print(f"{Fore.orange_red_1}",np.mean(peopleLoad),f"{Fore.light_steel_blue} = {Fore.medium_violet_red}AVG People Load{Style.reset}")
                print(f"{Fore.orange_red_1}",np.mean(equipmentLoad),f"{Fore.light_steel_blue} = {Fore.medium_violet_red}AVG Equipment Load{Style.reset}")
                print(f"{Fore.orange_red_1}",np.mean(avg_total_btu),f"{Fore.light_steel_blue} = {Fore.medium_violet_red}AVG Total BTU from Above Values{Style.reset}")
                print(f"{Fore.light_yellow}Below was calculated from the above individually and avged at the end.{Style.reset}")
                print(f"{Fore.orange_red_1}",np.mean(totalBtu),f"{Fore.light_steel_blue} = {Fore.light_red}AVG Total Btu{Style.reset}")
                print(f"{Fore.orange_red_1}",np.mean(totalTons),f"{Fore.light_steel_blue} = {Fore.light_red}AVG Total Tons{Style.reset}")
            else:
                print(htext) 
"""               
def cooling_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
cooling_menu={
    str(uuid1()):{
    "cmds":['cooling custom',],
    "exec":lambda self:s2cb_cooling(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['avg btus',],
    "exec":lambda self:average_btus(self,menu=True,short=True),
    "desc":"give an average btu summary",
    }
}
#bptxt - bill paid text

#TriedToWake
def coolingLogger(Model=Cooling,short_view=cooling_short_view,menu=cooling_menu):
    return ModelLogger(Model=Cooling,short_view=cooling_short_view,menu=cooling_menu)


def wtfday_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''
{Fore.green_yellow}{'*'*(os.get_terminal_size().columns-int((os.get_terminal_size().columns*0.4)))}{Style.reset}
{Fore.cyan}Whom{Fore.light_steel_blue} ={Fore.light_green} {i.person_identifier}{Style.reset}
{Fore.cyan}Something Bad Happen? {Fore.light_steel_blue} ={Fore.light_green} {i.bad_event_occurance}{Style.reset}
{Fore.cyan}ID{Fore.light_steel_blue} ={Fore.light_green} {i.emoid}{Style.reset}
{Fore.cyan}Comment{Fore.light_steel_blue} ={Fore.light_green} {i.comment}{Style.reset}
{Fore.cyan}GID{Fore.light_steel_blue} ={Fore.light_green} {i.group_id}{Style.reset}
{Fore.cyan}DTOE{Fore.light_steel_blue} ={Fore.light_green} {i.dtoe}{Style.reset}
{Fore.orange_red_1}{'*'*(os.get_terminal_size().columns-int((os.get_terminal_size().columns*0.4)))}{Style.reset}
            '''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def wtfday_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_wtfday(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=wtfday_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

wtfday_menu={
    str(uuid1()):{
    "cmds":['wtfday custom',],
    "exec":lambda self:s2cb_wtfday(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def wtfdayLogger(Model=WTFDay,short_view=wtfday_short_view,menu=wtfday_menu):
    return ModelLogger(Model=WTFDay,short_view=wtfday_short_view,menu=wtfday_menu)

def schedule_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            start_end_duration=timedelta()
            meal_0_duration=timedelta()
            meal_1_duration=timedelta()
            break_0_duration=timedelta()
            break_1_duration=timedelta()
            if isinstance(i.start,datetime) and isinstance(i.end,datetime):
                start_end_duration=i.end-i.start
            if isinstance(i.lunch_end_0,datetime) and isinstance(i.lunch_start_0,datetime):
                meal_0_duration=i.lunch_end_0-i.lunch_start_0
            if isinstance(i.lunch_end_1,datetime) and isinstance(i.lunch_start_1,datetime):
                meal_1_duration=i.lunch_end_1-i.lunch_start_1
            if isinstance(i.break_end_0,datetime) and isinstance(i.break_start_0,datetime):
                break_0_duration=i.break_end_0-i.break_start_0
            if isinstance(i.break_end_1,datetime) and isinstance(i.break_start_1,datetime):
                break_1_duration=i.break_end_1-i.break_start_1
            msg=f'''
{Fore.cyan}name{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.name}'{Style.reset}
{Fore.cyan}start{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.start}'{Style.reset}
{Fore.cyan}end{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.end}'{Style.reset}
{Fore.cyan}complete{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.complete}'{Style.reset}
{Fore.cyan}lunch_start_0{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.lunch_start_0}'{Style.reset}
{Fore.cyan}lunch_end_0{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.lunch_end_0}'{Style.reset}
{Fore.cyan}lunch_start_1{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.lunch_start_1}'{Style.reset}
{Fore.cyan}lunch_end_1{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.lunch_end_1}'{Style.reset}
{Fore.cyan}break_start_0{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.break_start_0}'{Style.reset}
{Fore.cyan}break_end_0{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.break_end_0}'{Style.reset}
{Fore.cyan}break_start_1{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.break_start_1}'{Style.reset}
{Fore.cyan}break_end_1{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.break_end_1}'{Style.reset}
{Fore.cyan}comment{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.comment}'{Style.reset}
{Fore.cyan}group_id{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.group_id}'{Style.reset}
{Fore.cyan}dtoe{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.dtoe}'{Style.reset}   
{Fore.orange_red_1}Shift {i.dtoe} Break Down{Style.reset}
{Fore.cyan}start_end_duration{Fore.light_steel_blue} ={Fore.sea_green_1a}'{start_end_duration}{Style.reset} 
{Fore.cyan}meal_0_duration{Fore.light_steel_blue} ={Fore.sea_green_1a}'{meal_0_duration}{Style.reset} 
{Fore.cyan}meal_1_duration{Fore.light_steel_blue} ={Fore.sea_green_1a}'{meal_1_duration}{Style.reset}
{Fore.cyan}break_0_duration{Fore.light_steel_blue} ={Fore.sea_green_1a}'{break_0_duration}{Style.reset} 
{Fore.cyan}break_1_duration{Fore.light_steel_blue} ={Fore.sea_green_1a}'{break_1_duration}{Style.reset}
{Fore.cyan}Total Hours{Fore.light_steel_blue} ={Fore.sea_green_1a}'{start_end_duration-(meal_0_duration+meal_1_duration)}'{Style.reset}            
            '''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def schedule_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_schedule(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=schedule_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

schedule_menu={
    str(uuid1()):{
    "cmds":['schedule custom',],
    "exec":lambda self:s2cb_schedule(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def scheduleLogger(Model=Schedule,short_view=schedule_short_view,menu=schedule_menu):
    return ModelLogger(Model=Schedule,short_view=schedule_short_view,menu=schedule_menu)

def lawnjob_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            break_duration=i.break_duration
            if break_duration != None:
                try:
                    break_duration=pd.to_pytimedelta(i.break_duration)
                except Exception as e:
                    break_duration=timedelta(minutes=0)
            else:
                break_duration=timedelta(minutes=0)

            start_end_duration=timedelta()
            meal_0_duration=timedelta()
            meal_1_duration=timedelta()
            break_0_duration=timedelta()
            break_1_duration=timedelta()
            if isinstance(i.start,datetime) and isinstance(i.end,datetime):
                start_end_duration=i.end-i.start
            if isinstance(i.lunch_end_0,datetime) and isinstance(i.lunch_start_0,datetime):
                meal_0_duration=i.lunch_end_0-i.lunch_start_0
            if isinstance(i.lunch_end_1,datetime) and isinstance(i.lunch_start_1,datetime):
                meal_1_duration=i.lunch_end_1-i.lunch_start_1

            if i.lunch_end_1 == None:
                meal_1_duration=timedelta(minutes=0)
            if i.lunch_start_1 == None:
                meal_1_duration=timedelta(minutes=0)
            if i.lunch_start_0 == None:
                meal_0_duration=timedelta(minutes=0)
            if i.lunch_end_0 == None:
                meal_0_duration=timedelta(minutes=0)

            try:
                grass_height=Quantity(i.mean_grass_height_value,i.mean_grass_height_unit)
            except Exception as e:
                print(e)
                track=f"{i.track_length_value} {i.track_length_unit}"
            try:
                track=Quantity(i.track_length_value,i.track_length_unit)
            except Exception as e:
                print(e)
                track=f"{i.track_length_value} {i.track_length_unit}"

            try:
                deck=Quantity(i.deck_width_value,i.deck_width_unit)
            except Exception as e:
                print(e)
                deck=f"{i.deck_width_value} {i.deck_width_unit}"

            try:
                MaxSpeed=Quantity(i.MaxSpeedValue,i.MaxSpeedUnit)
            except Exception as e:
                print(e)
                MaxSpeed=f"{i.MaxSpeedValue} {i.MaxSpeedUnit}"

            try:
                AverageSpeed=Quantity(i.AverageSpeedValue,i.AverageSpeedUnit)
            except Exception as e:
                print(e)
                AverageSpeed=f"{i.AverageSpeedValue} {i.AverageSpeedUnit}"

            try:
                AverageSpeedMoving=Quantity(i.AverageSpeedMovingValue,i.AverageSpeedMovingUnit)
            except Exception as e:
                print(e)
                AverageSpeedMoving=f"{i.AverageSpeedMovingValue} {i.AverageSpeedMovingUnit}"

            try:
                record_dur=pd.to_timedelta(i.RecordDuration).to_pytimedelta()
            except Exception as e:
                print(e)
                record_dur=f"{i.RecordDuration}"

            try:
                moving_dur=pd.to_timedelta(i.MovementDuration).to_pytimedelta()
            except Exception as e:
                print(e)
                moving_dur=f"{i.MovementDuration}"

            try:
                AltitudeDifference=Quantity(i.AltitudeDifferenceValue,i.AltitudeDifferenceUnit)
            except Exception as e:
                print(e)
                AltitudeDifference=f"{i.AltitudeDifferenceValue} {i.AltitudeDifferenceUnit}"

            try:
                MaxAltitude=Quantity(i.MaxAltitudeValue,i.MaxAltitudeUnit)
            except Exception as e:
                print(e)
                MaxAltitude=f"{i.MaxAltitudeValue} {i.MaxAltitudeUnit}"

            try:
                MinAltitude=Quantity(i.MinAltitudeValue,i.MinAltitudeUnit)
            except Exception as e:
                print(e)
                MinAltitude=f"{i.MinAltitudeValue} {i.MinAltitudeUnit}"

            try:
                VerticalSpeed=Quantity(i.VerticalSpeed_Value,i.VerticalSpeed_Unit)
            except Exception as e:
                print(e)
                VerticalSpeed=f"{i.VerticalSpeed_Value} {i.VerticalSpeed_Unit}"

            try:
                VerticalDistance=Quantity(i.VerticalDistanceValue,i.VerticalDistanceUnit)
            except Exception as e:
                print(e)
                VerticalDistance=f"{i.VerticalDistanceValue} {i.VerticalDistanceUnit}"
            try:
                VerticalAscent=Quantity(i.VerticalAscentValue,i.VerticalDistanceUnit)
            except Exception as e:
                print(e)
                VerticalAscent=f"{i.VerticalAscentValue} {i.VerticalDistanceUnit}"
            try:
                total_duration_minus_lunch=start_end_duration-(meal_0_duration+meal_1_duration+break_duration)
            except Exception as e:
                print(e)
                total_duration_minus_lunch=0
            try:
                sfm=(deck.to(track.units)*track).to('feet ** 2')
            except Exception as e:
                print(e)
                sfm=0
            try:
                cfgc=deck.to(track.units)*track*grass_height.to(track.units)
            except Exception as e:
                print(e)
                cfgc=0
            
            try:
                ep=(total_duration_minus_lunch.total_seconds()/(60*60))*i.per_hour_wage
            except Exception as e:
                print(e)
                ep=0

            msg=f'''
{Fore.orange_red_1}[You provide these]{Style.reset}
JobName='{i.JobName}'
JobDesc='{i.JobDesc}'
JobRequirements='{i.JobRequirements}'
JobNotes='{i.JobNotes}'

post_comments='{i.post_comments}'
prep_comments='{i.prep_comments}'
wage_per_hour='{i.per_hour_wage}'
{Fore.orange_red_1}[Your Client's Info]{Style.reset}
client_name='{i.client_name}'
client_address='{i.client_address}'
client_phone='{i.client_phone}'
client_email='{i.client_email}'

{Fore.orange_red_1}[GeoTracker]{Style.reset}
geolocation='{i.geolocation}'

{Fore.orange_red_1}[Time Squared]{Style.reset}
start='{i.start}' 
end='{i.end}' 
start_end_duration={start_end_duration}

lunch_start_0='{i.lunch_start_0}'
lunch_end_0='{i.lunch_end_0}'
lse0 duration='{meal_0_duration}'

lunch_start_1='{i.lunch_start_1}'
lunch_end_1='{i.lunch_end_1}'
lse1 duration='{meal_1_duration}'

break_duration='{break_duration}'
{Fore.orange_red_1}[Your Lawn in Multiple Areas w/ Measuring Tape]{Style.reset}
mean_grass_height='{grass_height}'

{Fore.orange_red_1}[GeoTracker]{Style.reset}
track_length='{track}'

{Fore.orange_red_1}[Your Mower Deck Width]{Style.reset}
deck_width='{deck}'

{Fore.orange_red_1}[GeoTracker]{Style.reset}
MaxSpeed='{MaxSpeed}'
AverageSpeed='{AverageSpeed}'
AverageSpeedMoving='{AverageSpeedMoving}'
RecordDuration='{record_dur}'
MovementDuration='{moving_dur}'
AltitudeDifference='{AltitudeDifference}'
MaxAltitude='{MaxAltitude}
MinAltitudeValue='{MinAltitude}
VerticalSpeed='{VerticalSpeed}'
VerticalDistanceValue='{VerticalDistance}'
VerticalAscentValue='{VerticalAscent}'

{Fore.orange_red_1}[From Data Collected]{Style.reset}
Square Footage Mowed='{sfm}'
~ Cubic Feet Grass Cut='{cfgc}'
Shift Duration='{total_duration_minus_lunch}'
Expected Pay='{ep}'

complete={i.complete}
comment='{i.comment}'
group_id='{i.group_id}'
dtoe='{i.dtoe}'
emoid={i.emoid}

photograph_links='{i.photograph_links}'
photograph_links_post='{i.photograph_links_post}'
photograph_links_pre='{i.photograph_links_pre}'
            '''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def lawnjob_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_lawnjob(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=lawnjob_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

lawnjob_menu={
    str(uuid1()):{
    "cmds":['lawnjob custom',],
    "exec":lambda self:s2cb_lawnjob(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def lawnjobLogger(Model=LawnJob,short_view=lawnjob_short_view,menu=lawnjob_menu):
    return ModelLogger(Model=LawnJob,short_view=lawnjob_short_view,menu=lawnjob_menu)



class get_from_child_db():
    def lsboot(self):
        boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)

        htext=[]
        ct=len(bootable_dirs)
        for num,i in enumerate(bootable_dirs):
            msg=f"{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {Fore.dark_goldenrod}{i}{Style.reset}"
            htext.append(msg)
        htext='\n'.join(htext)
        print(htext)
        return bootable_dirs


    def load_dbs(self,code=None):
        for d in self.lsboot():
            path=d/Path('codesAndBarcodes.db')
            print(path)
            if path.exists():
                try:
                    dbfile=f"sqlite:///{str(path)}"
                    engine=create_engine(dbfile)
                    with Session(engine) as session:
                        results_query=session.query(Entry)
                        if code in [None,]:
                            code=Control(ptext="Barcode|Code|Name",helpText="anthing helps",data="string")
                            if code in ['NAN','NaN','nan',None,'','d']:
                                return
                        results_query=results_query.filter(
                        or_(
                            Entry.Code==code,
                            Entry.Barcode==code,
                            Entry.Barcode.icontains(code),
                            Entry.Code.icontains(code),
                            Entry.Name.icontains(code)
                            )
                        ) 
                        results=orderQuery(results_query,Entry.Name.asc())
                        results=results_query.all()
                        ct=len(results)
                        if ct < 1:
                            msg=f"{Fore.light_steel_blue}Nothing in {Fore.slate_blue_1}Bld{Fore.light_red}LS!{Style.reset}"
                            logInput(msg,user=False,filter_colors=True,maxed_hfl=False,ofile=Prompt.bld_file)
                            print(msg)
                            continue
                        else:
                            for num, i in enumerate(results):
                                try:
                                    print(std_colorize(i,num,ct),f"{Fore.light_steel_blue}From {dbfile}{Style.reset}",sep="\n")
                                    importit=Control(func=lambda text,data:FormBuilderMkText(text=text,data=data,passThru=["next db","ndb","next"],PassThru=True),ptext="Import to Current DB?",helpText="yes or no",data="boolean")
                                    if importit in ['NAN','NaN','nan',None]:
                                        return
                                    elif importit in ["next db","ndb","next"]:
                                        break
                                    elif importit in ['','d',False]:
                                        continue
                                    elif importit == True:
                                        with Session(ENGINE) as s:
                                            data={}
                                            for k in Entry.__table__.columns:
                                                name=str(k.name)
                                                if name in ['EntryId',]:
                                                    continue
                                                data[name]=getattr(i,name)
                                            if not self.checkForExistance(data):
                                                nE=Entry(**data)

                                                s.add(nE)
                                                s.commit()
                                                s.refresh(nE)
                                                self.EntryId=nE.EntryId
                                                print(nE.seeShort)
                                            else:
                                                print(f"{Fore.orange_red_1}That Already Exists!{Style.reset}")
                                except Exception as e:
                                    print(e)
                except Exception as e:
                    print(e)
                    continue

    def checkForExistance(self,data):
        with Session(ENGINE) as session:
            query=session.query(Entry)
            filt=[]
            for k in data:
                filt.append(getattr(Entry,k)==data[k])
            query=query.filter(and_(*filt))
            result=query.first()
            if result:
                return True
            else:
                return False

    def __init__(self,code=None):
        self.boot_dirs=Path("RadBoy_Boot_Directory")
        self.EntryId=None
        self.load_dbs(code=code)

def tilldrawerloadout_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            if i.total_drawer() != None:
                if i.total_drawer()[1] == False:
                    give_take='take'
                    if i.total_drawer()[0] > i.target_till_value:
                        give_take="give"
                    msg=f'''{i.total_drawer()[-1]} Target({i.target_till_value}) - Total({i.total_drawer()[0]}) = {give_take}({decc(abs(i.target_till_value-i.total_drawer()[0]),cf=2)})'''
                    msg=std_colorize(msg,xnum,ct)
                    zt=[]
                    cta=len(msg.split("\n"))
                    for znum,ii in enumerate(msg.split("\n")):
                        zt.append(std_colorize(ii,znum,cta))
                    xtext.append('\n'.join(zt))
                else:
                    print(f"{Fore.light_red}TillDrawerLoadOut({Fore.light_yellow}Total={Fore.light_steel_blue}{i.total_drawer()[0]},{Fore.light_yellow}Under Target={Fore.light_steel_blue}{i.total_drawer()[1]},{Fore.light_yellow}emoid={Fore.light_steel_blue}{i.emoid}{Fore.light_red}){Style.reset}")
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def tilldrawerloadout_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_tilldrawerloadout(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=tilldrawerloadout_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

tilldrawerloadout_menu={
    str(uuid1()):{
    "cmds":['tilldrawerloadout custom',],
    "exec":lambda self:s2cb_tilldrawerloadout(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def tilldrawerloadoutLogger(Model=TillDrawerLoadOut,short_view=tilldrawerloadout_short_view,menu=tilldrawerloadout_menu):
    return ModelLogger(Model=TillDrawerLoadOut,short_view=tilldrawerloadout_short_view,menu=tilldrawerloadout_menu)

#------------

def customUnit_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            useable=None
            try:
                ureg.define(i.definition)
                useable=True
            except Exception as e:
                useable=False
                print(e,i)
            if useable in [None,False]:
                useable=f"{Fore.orange_red_1}Un-Useable"
            else:
                useable=f"{Fore.green_yellow}Useable"
            msg=f"""{useable} {Fore.light_green}emoid{Fore.light_steel_blue}={Fore.light_yellow}'{i.emoid}' {Fore.light_green}definition{Fore.light_steel_blue}={Fore.light_yellow}'{i.definition}' {Fore.light_green}comment{Fore.light_steel_blue}={Fore.light_yellow}'{i.comment}' {Fore.light_green}group_id{Fore.light_steel_blue}={Fore.light_yellow}'{i.group_id}' {Fore.light_green}dtoe{Fore.light_steel_blue}={Fore.light_yellow}'{i.dtoe}{Style.reset}'"""
            xtext.append(std_colorize(msg,xnum,ct))
            
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def customUnit_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_customUnit(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=customUnit_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

customUnit_menu={
    str(uuid1()):{
    "cmds":['customUnit custom',],
    "exec":lambda self:s2cb_customUnit(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def customUnitLogger(Model=CustomUnit,short_view=customUnit_short_view,menu=customUnit_menu):
    return ModelLogger(Model=CustomUnit,short_view=customUnit_short_view,menu=customUnit_menu)


def storagePaths_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""path='{i.path}' | comment='{i.comment}' | dtoe='{i.dtoe}' | emoid='{i.emoid}' group_id='{i.group_id}'"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def storagePaths_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_storagePaths(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=storagePaths_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

storagePaths_menu={
    str(uuid1()):{
    "cmds":['storagePaths custom',],
    "exec":lambda self:s2cb_storagePaths(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def storagePathsLogger(Model=StoragePaths,short_view=storagePaths_short_view,menu=storagePaths_menu):
    return ModelLogger(Model=StoragePaths,short_view=storagePaths_short_view,menu=storagePaths_menu)

def i_InteractedWith_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def i_InteractedWith_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_i_InteractedWith(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=i_InteractedWith_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

i_InteractedWith_menu={
    str(uuid1()):{
    "cmds":['i_InteractedWith custom',],
    "exec":lambda self:s2cb_i_InteractedWith(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def i_InteractedWithLogger(Model=iInteractedWith,short_view=i_InteractedWith_short_view,menu=i_InteractedWith_menu):
    return ModelLogger(Model=iInteractedWith,short_view=i_InteractedWith_short_view,menu=i_InteractedWith_menu)

def foodlabel_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def foodlabel_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_foodlabel(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=foodlabel_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

foodlabel_menu={
    str(uuid1()):{
    "cmds":['foodlabel custom',],
    "exec":lambda self:s2cb_foodlabel(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def foodlabelLogger(Model=FoodLabel,short_view=foodlabel_short_view,menu=foodlabel_menu):
    return ModelLogger(Model=FoodLabel,short_view=foodlabel_short_view,menu=foodlabel_menu)


def mark_all_in_list_unpaid():
    pass

def unmark_all_in_list_unpaid():
    pass

def All_UnMarkUnPaid():
        try:
            with Session(ENGINE) as session:
                query=session.query(Entry).filter(Entry.InList==True)
                results=query.all()
                ct=len(results)
                if ct == 0:
                    print("Nothing Found; the list may be empty!")
                
                for num,selected in enumerate(results):
                    if BooleanAnswers.DontLog in selected.Note:
                        selected.Note=selected.Note.replace(f"\n{BooleanAnswers.DontLog}\n",'')
                
                    session.commit()
                    session.refresh(selected)
                    print(selected)
        except Exception as e:
            print(e)

def All_MarkUnPaid():
    try:
        with Session(ENGINE) as session:
            query=session.query(Entry).filter(Entry.InList==True)
            results=query.all()
            ct=len(results)
            if ct == 0:
                print("Nothing Found; the list may be empty")
            for num,selected in enumerate(results):
                if BooleanAnswers.DontLog not in selected.Note:
                    selected.Note+=f"\n{BooleanAnswers.DontLog}\n"

                session.commit()
                session.refresh(selected)
                print(selected)
    except Exception as e:
        print(e)

def CostReport():
    fields={
        'start':{
        'type':'datetime',
        'default':datetime.now()-timedelta(days=30)
        },
        'end':{
        'type':'datetime',
        'default':datetime.now()
        }
    }
    fb=FormBuilder(data=fields)
    if fb in [None,]:
        return
    '''
    Distress=Column(Integer,default=0)
    Price=Column(Float,default=0.0)
    CRV=Column(Float,default=0.0)
    Tax=Column(Float,default=0.0)
Shelf=Column(Integer,default=0)
    BackRoom=Column(Integer,default=0)
    Display_1=Column(Integer,default=0)
    Display_2=Column(Integer,default=0)
    Display_3=Column(Integer,default=0)
    Display_4=Column(Integer,default=0)
    Display_5=Column(Integer,default=0)
    Display_6=Column(Integer,default=0)
ListQty=Column(Float,default=0)
SBX_WTR_DSPLY=Column(Integer,default=0)
    SBX_CHP_DSPLY=Column(Integer,default=0)
    SBX_WTR_KLR=Column(Integer,default=0)
    FLRL_CHP_DSPLY=Column(Integer,default=0)
    FLRL_WTR_DSPLY=Column(Integer,default=0)
    WD_DSPLY=Column(Integer,default=0)
    CHKSTND_SPLY=Column(Integer,default=0)
    '''
    with Session(ENGINE) as session:
        total_qty=((-(DayLog.Distress))+(
            DayLog.Shelf+
            DayLog.BackRoom+
            DayLog.Display_1+
            DayLog.Display_2+
            DayLog.Display_3+
            DayLog.Display_4+
            DayLog.Display_5+
            DayLog.Display_6+
            DayLog.ListQty+
            DayLog.SBX_WTR_DSPLY+
            DayLog.SBX_CHP_DSPLY+
            DayLog.SBX_WTR_KLR+
            DayLog.FLRL_CHP_DSPLY+
            DayLog.FLRL_WTR_DSPLY+
            DayLog.WD_DSPLY+
            DayLog.CHKSTND_SPLY
        ))
        total_crv=total_qty*DayLog.CRV
        total_price=(total_qty*DayLog.Price)
        total_tax=(total_qty*DayLog.Tax)
        total_expense=(total_crv+total_price+total_tax)
        

        rankables=[    
        ]
        for i in DayLog.__table__.columns:
            if i.type in [VARCHAR]:
                rankables.append(text(i.name))
            else:
                rankables.append(column(i.name))
        rankables.append(func.rank().over(order_by=desc(total_expense)).label("total_expense desc"))
        rankables.append(func.rank().over(order_by=asc(total_expense)).label("total_expense asc"))
        htext=[]
        hct=len(rankables)
        for num,i in enumerate(rankables):
            htext.append(std_colorize(f"{i.name}",num,hct))
        htext='\n'.join(htext)

        while True:
            which=Control(ptext=f"{htext}\nRank by Which index",helpText=f"{htext}; select an integer",data="integer")
            if which in [None,'NAN','nan','NaN','nAn']:
                return
            elif which in ['d',]:
                rankSpec=column('Name')
                break
            else:
                if which >= 0 and which < len(rankables):
                    rankSpec=rankables[which]
                else:
                    continue
                break

        orders=["ascending","descending" ]
        htext=[]
        Oct=len(orders)
        for num,i in enumerate(orders):
            htext.append(std_colorize(f"{i}",num,Oct))
        htext='\n'.join(htext)

        if isinstance(rankSpec,sqlalchemy.sql.elements.Label):
            rank=rankSpec
        else:
            direction='ascending'
            while True:
                which=Control(ptext=f"{htext}\nWhich Order index",helpText=f"{htext}; select an integer",data="integer")
                if which in [None,'NAN','nan','NaN','nAn']:
                    return
                elif which in ['d',]:
                    direction=orders[0]
                    break
                else:
                    print(which,len(orders),which < len(orders))
                    if which >= 0 and which < len(orders):
                        direction=orders[which]
                    else:
                        continue
                    break

            if direction == "descending":
                rank=func.rank().over(order_by=rankSpec.desc())
            elif direction == 'ascending':
                rank=func.rank().over(order_by=rankSpec.asc())
            else:
                rank=func.rank().over(order_by=rankSpec.asc())


        code=Control(ptext="Text in Code/BarCode/Name/Desc/Note?",helpText="Text in Code/BarCode/Name/Desc/Note?",data="string")
        if code in [None,'NAN','nan','NaN','nAn']:
            return
        elif code in ['d',]:
            code=''
        else:
            pass
        code=code.split(",")
        exclude_code=Prompt.__init2__(None,func=FormBuilderMkText,ptext="exclude this code from results:",helpText="yes or no",data="boolean")
        if exclude_code in [None,]:
            return
        elif exclude_code in ['d',]:
            exclude_code=False
        #--------------
        excludes=['',None]
        if not exclude_code:
            filt=[]
            for q in code:
                if code in excludes:
                    continue
                filt.extend([
                DayLog.Barcode.icontains(q),
                DayLog.Code.icontains(q),
                DayLog.Name.icontains(q),
                DayLog.Description.icontains(q),
                DayLog.Note.icontains(q),
                ])

            fff=or_(*filt)        
        else:
            filt=[]
            for q in code:
                if code in excludes:
                    continue
                filt.extend([or_(
                    not_(DayLog.Barcode.icontains(q)),
                    not_(DayLog.Code.icontains(q)),
                    not_(DayLog.Name.icontains(q)),
                    not_(DayLog.Description.icontains(q)),
                    not_(DayLog.Note.icontains(q))),
                not_(DayLog.Barcode.icontains(q)),
                not_(DayLog.Code.icontains(q)),
                not_(DayLog.Name.icontains(q)),
                not_(DayLog.Description.icontains(q)),
                not_(DayLog.Note.icontains(q)),
                and_(
                    not_(DayLog.Barcode.icontains(q)),
                    not_(DayLog.Code.icontains(q)),
                    not_(DayLog.Name.icontains(q)),
                    not_(DayLog.Description.icontains(q)),
                    not_(DayLog.Note.icontains(q))),
                ])
            fff=and_(*filt)


        roundTo=int(detectGetOrSet("TotalSpent ROUNDTO default",3,setValue=False,literal=True))
        total_e=decc(0,cf=roundTo)
        total_q=decc(0,cf=roundTo)
        total_c=decc(0,cf=roundTo)
        total_t=decc(0,cf=roundTo)
        total_p=decc(0,cf=roundTo)
        statement=select(DayLog,total_qty.label('total_qty'),
        total_crv.label("total_crv"),total_price.label("total_price"),total_tax.label("total_tax"),total_expense.label("total_expense"),rank
        ).where(DayLog.DayLogDate.between(fb['start'],fb['end']),fff)
        results=session.execute(statement)
        cta=len(results.all())
        results=session.execute(statement)
        for num,i in enumerate(results):
            msg=std_colorize(f"{Fore.light_red}DLiD({i[0].DayLogId}){Fore.light_green}{i[0].Name} - {Fore.light_yellow}Price({i[0].Price}) {Fore.light_steel_blue}CRV({i[0].CRV}) {Fore.light_red}Tax({i[0].Tax}) {Fore.cyan}for Qty({i.total_qty}) {Fore.cyan}TotalExpense({i.total_expense})",num,cta)
            print(msg)
            total_e+=decc(i.total_expense,cf=roundTo)
            total_q+=decc(i.total_qty,cf=roundTo)
            total_c+=decc(i.total_crv,cf=roundTo)
            total_t+=decc(i.total_tax,cf=roundTo)
            total_p+=decc(i.total_price,cf=roundTo)
        x={'total_expense':total_e,
        'total qty':total_q,
        'total crv':total_c,
        'total tax':total_t,
        'total price':total_p,'start date':fb['start'].ctime(),'end date':fb['end'].ctime()}
        ct=len(x)
        for num,k in enumerate(x):
            print(std_colorize(f"{k}: {x[k]}",num,ct))

        #save_reciept

        #(((qty*crv)+(qty*price))*tax)
'''        
Price
CRV
Tax
'''
def ListBuild():
    launch=0
    launch+=1
    wantedState=None
    bldls_print_code=db.detectGetOrSet("list maker dont print barcode code",False,setValue=False,literal=False)
    if bldls_print_code in [True,None]:
        wantedState=db.BooleanAnswers.YES_defaulted
        wantedStateVal=True
    elif bldls_print_code == False:
        wantedState=db.BooleanAnswers.NO_defaulted
        wantedStateVal=False

    dontPrintCodeBarcode=Control(func=FormBuilderMkText,ptext=f"Stage: {launch}\nDo not print Barcode and Code.",helpText='Do not print Barcode or Barcode',data="boolean")
    if dontPrintCodeBarcode in db.BooleanAnswers.NONE:
        return

    if dontPrintCodeBarcode != bldls_print_code and dontPrintCodeBarcode not in ['d','']:
        print(dontPrintCodeBarcode)
        if dontPrintCodeBarcode in db.BooleanAnswers.NO_defaulted:
            dontPrintCodeBarcode=False
        elif dontPrintCodeBarcode in db.BooleanAnswers.YES_defaulted:
            dontPrintCodeBarcode=True
        bldls_print_code=db.detectGetOrSet("list maker dont print barcode code",dontPrintCodeBarcode,setValue=True,literal=False)
    
    if dontPrintCodeBarcode in wantedState:
        dontPrintCodeBarcode=bldls_print_code

    try:
        reciept_dir=Path(detectGetOrSet("reciept directory","reciepts",setValue=False,literal=True))
        reciept_name=Path(f"reciept_{datetime.now().strftime('%m-%d-%Y_%H_%M_%Y')}.txt")
    except Exception as e:
        print(e)
        reciept_dir=Path("reciepts_hc")
        reciept_name=Path(f"reciept_hc_{datetime.now().strftime('%m-%d-%Y_%H_%M_%Y')}.txt")

    try:
        if not reciept_dir.exists():
            reciept_dir.mkdir()
        store_file=(reciept_dir/reciept_name).open("w")
    except Exception as e:
        print(e)
        store_file=None


    page=Control(ptext=f"Stage: {launch}\npage w/ menu?",helpText="go through list 1 at a time; yes or no",data="boolean")
    if page in BooleanAnswers.NONE:
        return
    elif page in BooleanAnswers.NO_defaulted:
        page=False
    '''
    Distress=Column(Integer,default=0)
    Price=Column(Float,default=0.0)
    CRV=Column(Float,default=0.0)
    Tax=Column(Float,default=0.0)
Shelf=Column(Integer,default=0)
    BackRoom=Column(Integer,default=0)
    Display_1=Column(Integer,default=0)
    Display_2=Column(Integer,default=0)
    Display_3=Column(Integer,default=0)
    Display_4=Column(Integer,default=0)
    Display_5=Column(Integer,default=0)
    Display_6=Column(Integer,default=0)
ListQty=Column(Float,default=0)
SBX_WTR_DSPLY=Column(Integer,default=0)
    SBX_CHP_DSPLY=Column(Integer,default=0)
    SBX_WTR_KLR=Column(Integer,default=0)
    FLRL_CHP_DSPLY=Column(Integer,default=0)
    FLRL_WTR_DSPLY=Column(Integer,default=0)
    WD_DSPLY=Column(Integer,default=0)
    CHKSTND_SPLY=Column(Integer,default=0)
    '''
    with Session(ENGINE) as session:
        total_qty=((-(Entry.Distress))+(
            Entry.Shelf+
            Entry.BackRoom+
            Entry.Display_1+
            Entry.Display_2+
            Entry.Display_3+
            Entry.Display_4+
            Entry.Display_5+
            Entry.Display_6+
            Entry.ListQty+
            Entry.SBX_WTR_DSPLY+
            Entry.SBX_CHP_DSPLY+
            Entry.SBX_WTR_KLR+
            Entry.FLRL_CHP_DSPLY+
            Entry.FLRL_WTR_DSPLY+
            Entry.WD_DSPLY+
            Entry.CHKSTND_SPLY
        ))
        total_crv=total_qty*Entry.CRV
        total_price=(total_qty*Entry.Price)
        total_tax=(total_qty*Entry.Tax)
        total_expense=(total_crv+total_price+total_tax)
        taxRate=((total_tax/(total_price+total_crv))*100)

        rankables=[    
        ]
        for i in Entry.__table__.columns:
            if i.type in [VARCHAR]:
                rankables.append(text(i.name))
            else:
                rankables.append(column(i.name))
        rankables.append(func.rank().over(order_by=desc(total_expense)).label("total_expense desc"))
        rankables.append(func.rank().over(order_by=asc(total_expense)).label("total_expense asc"))

        rankables.append(func.rank().over(order_by=[
            desc(total_expense),
            getattr(Entry.__table__.columns,'Size').desc()
            ]).label("total_expense & size desc"))
        rankables.append(func.rank().over(order_by=[
            asc(total_expense),
            getattr(Entry.__table__.columns,'Size').asc()
            ]).label("total_expense & size asc"))
        
        htext=[]
        hct=len(rankables)
        for num,i in enumerate(rankables):
            htext.append(std_colorize(f"{i.name}",num,hct))
        htext='\n'.join(htext)
        launch+=1
        while True:
            which=Control(ptext=f"Stage: {launch}\n{htext}\nRank Which index",helpText=f"{htext}; select an integer",data="integer")
            if which in [None,'NAN','nan','NaN','nAn']:
                return
            elif which in ['d',]:
                rankSpec=column('Name')
                break
            else:
                if which >= 0 and which < len(rankables):
                    rankSpec=rankables[which]
                else:
                    continue
                break

        orders=["ascending","descending" ]
        htext=[]
        Oct=len(orders)
        for num,i in enumerate(orders):
            htext.append(std_colorize(f"{i}",num,Oct))
        htext='\n'.join(htext)

        direction='ascending'
        launch+=1
        while True:
            which=Control(ptext=f"Stage: {launch}\n{htext}\nWhich Order index",helpText=f"{htext}; select an integer",data="integer")
            if which in [None,'NAN','nan','NaN','nAn']:
                return
            elif which in ['d',]:
                direction=orders[0]
                break
            else:
                print(which,len(orders),which < len(orders))
                if which >= 0 and which < len(orders):
                    direction=orders[which]
                else:
                    continue
                break
        if isinstance(rankSpec,sqlalchemy.sql.elements.Label):
            rank=rankSpec
        else:
            if direction == "descending":
                rank=func.rank().over(order_by=rankSpec.desc())
            elif direction == 'ascending':
                rank=func.rank().over(order_by=rankSpec.asc())
            else:
                rank=func.rank().over(order_by=rankSpec.asc())

        abv=0
        launch+=1
        total_qty_abv_or_equal=Control(ptext=f"Stage: {launch}\ntotal qty above or equal to[d={abv}]?",helpText="an integer",data="integer")
        if total_qty_abv_or_equal in BooleanAnswers.NONE:
            return
        elif total_qty_abv_or_equal in ['d','']:
            pass
        else:
            abv=total_qty_abv_or_equal

        blo=sys.maxsize
        launch+=1
        total_qty_blo_or_equal=Control(ptext=f"Stage: {launch}\ntotal qty below or equal to[d={blo}]?",helpText="an integer",data="integer")
        if total_qty_blo_or_equal in BooleanAnswers.NONE:
            return
        elif total_qty_blo_or_equal in ['d','']:
            pass
        else:
            blo=total_qty_blo_or_equal
            
        launch+=1
        code=Control(ptext=f"Stage: {launch}\nText in Code/BarCode/Name/Desc/Note?",helpText="Text in Code/BarCode/Name/Desc/Note?",data="string")
        if code in [None,'NAN','nan','NaN','nAn']:
            return
        elif code in ['d',]:
            code=''
        else:
            pass
        code=code.split(",")
        launch+=1
        exclude_code=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Stage: {launch}\nexclude this code from results:",helpText="yes or no",data="boolean")
        if exclude_code in [None,]:
            return
        elif exclude_code in ['d',]:
            exclude_code=False
        launch+=1
        retailer=Control(func=FormBuilderMkText,ptext=f"Stage: {launch}\nRetailer for Gift Card Maxes:",helpText="retailer where purchases are made",data="string")
        if retailer is None:
            return
        elif retailer in ['d',]:
            retailer=detectGetOrSet('list maker default retailer','home depot',setValue=False,literal=True)

        #--------------
        excludes=['',None]
        if not exclude_code:
            filt=[]
            for q in code:
                if code in excludes:
                    continue
                filt.extend([
                Entry.Barcode.icontains(q),
                Entry.Code.icontains(q),
                Entry.Name.icontains(q),
                Entry.Description.icontains(q),
                Entry.Note.icontains(q),
                ])

            fff=or_(*filt)        
        else:
            filt=[]
            for q in code:
                if code in excludes:
                    continue
                filt.extend([or_(
                    not_(Entry.Barcode.icontains(q)),
                    not_(Entry.Code.icontains(q)),
                    not_(Entry.Name.icontains(q)),
                    not_(Entry.Description.icontains(q)),
                    not_(Entry.Note.icontains(q))),
                not_(Entry.Barcode.icontains(q)),
                not_(Entry.Code.icontains(q)),
                not_(Entry.Name.icontains(q)),
                not_(Entry.Description.icontains(q)),
                not_(Entry.Note.icontains(q)),
                and_(
                    not_(Entry.Barcode.icontains(q)),
                    not_(Entry.Code.icontains(q)),
                    not_(Entry.Name.icontains(q)),
                    not_(Entry.Description.icontains(q)),
                    not_(Entry.Note.icontains(q)))
                ])
            fff=and_(*filt)

        roundTo=int(detectGetOrSet("TotalSpent ROUNDTO default",3,setValue=False,literal=True))
        total_e=decc(0,cf=roundTo)
        total_q=decc(0,cf=roundTo)
        total_c=decc(0,cf=roundTo)
        total_t=decc(0,cf=roundTo)
        total_p=decc(0,cf=roundTo)
        statement=select(Entry,total_qty.label('total_qty'),
        total_crv.label("total_crv"),total_price.label("total_price"),total_tax.label("total_tax"),total_expense.label("total_expense"),taxRate.label("tr"),rank.label('rank')
        ).where(Entry.InList==True,fff,total_qty<=blo,total_qty>=abv)
        results=session.execute(statement)
        cta=len(results.all())
        results=session.execute(statement)
        msgd=''
        colormapped=[
        Fore.deep_sky_blue_4c,
        Fore.spring_green_4,
        Fore.turquoise_4,
        Fore.dark_cyan,
        Fore.deep_sky_blue_2,
        Fore.spring_green_2a,
        Fore.medium_spring_green,
        Fore.steel_blue,
        Fore.cadet_blue_1,
        Fore.aquamarine_3,
        Fore.purple_1a,
        Fore.medium_purple_3a,
        Fore.slate_blue_1,
        Fore.light_slate_grey,
        Fore.dark_olive_green_3a,
        Fore.deep_pink_4c,
        Fore.orange_3,
        ]
        location_fields=["Shelf","BackRoom","Display_1","Display_2","Display_3","Display_4","Display_5","Display_6","ListQty","SBX_WTR_DSPLY","SBX_CHP_DSPLY","SBX_WTR_KLR","FLRL_CHP_DSPLY","FLRL_WTR_DSPLY","WD_DSPLY","CHKSTND_SPLY","Distress"]
        reRunRequired=False

        xults=session.execute(statement).scalars().all()
        breakTransaction=False
        gcmsgs=[]
        for i in xults:
            for gc in BooleanAnswers.gift_cards:
                msg=''
                if gc in i.Name.lower():
                    msg=checkForWarningsGC_per_card(i,retailer)
                elif gc in i.Note.lower():
                    msg=checkForWarningsGC_per_card(i,retailer)
                elif gc in i.Description.lower():
                    msg=checkForWarningsGC_per_card(i,retailer)
                elif gc in i.Barcode.lower():
                    msg=checkForWarningsGC_per_card(i,retailer)
                elif gc in i.Code.lower():
                    msg=checkForWarningsGC_per_card(i,retailer)
                if msg != '':
                    store_file.write(strip_colors(msg))
                    print(msg)
                    breakTransaction=True
                    gcmsgs.append(msg)
        msgXces=checkForWarningsGC_per_transaction(xults,retailer)
        if msgXces != '':
            store_file.write(strip_colors(msgXces))
            print(msgXces)
            breakTransaction=True
            gcmsgs.append(msgXces)

        l=len(gcmsgs)
        gftmsg=[]
        for x in gcmsgs:
            gftmsg.append(x)
        gftmsg='\t\n'.join(gftmsg)

        for num,i in enumerate(results):
            refresh=False
            if i[0].Description == None:
                i[0].Description=''
                refresh=True
                session.commit()
                session.refresh(i[0])

            if i[0].Note == None:
                i[0].Note=''
                refresh=True
                session.commit()
                session.refresh(i[0])

            if reRunRequired:
                print(f"{Fore.orange_red_1}Your total {Fore.light_yellow}MAY{Fore.orange_red_1} may be off; a re-run is required{Style.reset}")
            try:
                if 'DoNotTotal' in i[0].Description:
                    continue
            except Exception as e:
                print(e)
            try:
                txr=decc(i.tr,cf=roundTo)
            except Exception as e:
                txr=0
            msgd=''
            for n2,f in enumerate(location_fields):
                if getattr(i[0],f) not in [0,None]:
                    msg2=f'{colormapped[n2]}{f} = {decc(getattr(i[0],f),cf=3)}{Style.reset}'
                    if n2 < len(location_fields):
                        msg2+=","
                    msgd+=msg2
            if i.total_qty == 0:
                m=f"{Fore.magenta}EiD({i[0].EntryId}) {Fore.light_green}Name({i[0].Name}) {Fore.light_magenta}BCD({i[0].rebar(i[0].Barcode)}{Fore.light_magenta}) {Fore.orange_red_1}CD({i[0].cfmt(i[0].Code)}{Fore.orange_red_1}) {Fore.light_blue}->> {Fore.light_red}Not Counted{Style.reset}"
                print(std_colorize(m,num,cta))
                if page:
                    clear=Control(ptext="Reset to default values and clear from list?",helpText="yes or no",data="boolean")
                    if clear in BooleanAnswers.NONE:
                        return
                    elif clear in BooleanAnswers.YES_defaulted:
                        session.execute(update(Entry).where(Entry.EntryId==i[0].EntryId).values({'InList':False,
                'ListQty':0,
                'Shelf':0,
                'Note':'',
                'BackRoom':0,
                'Distress':0,
                'Display_1':0,
                'Display_2':0,
                'Display_3':0,
                'Display_4':0,
                'Display_5':0,
                'Display_6':0,
                'Stock_Total':0,
                'CaseID_BR':'',
                'CaseID_LD':'',
                'CaseID_6W':'',
                'SBX_WTR_DSPLY':0,
                'SBX_CHP_DSPLY':0,
                'SBX_WTR_KLR':0,
                'FLRL_CHP_DSPLY':0,
                'FLRL_WTR_DSPLY':0,
                'WD_DSPLY':0,
                'CHKSTND_SPLY':0,
                'Expiry':None,
                'BestBy':None,
                'AquisitionDate':None,
                }))
                        session.commit()
                        session.refresh(i[0])
                        print(i[0].seeShort())
                continue
            if dontPrintCodeBarcode:
                msg=std_colorize(f"""{Fore.light_green}Name({i[0].Name}) {Fore.grey_50}EiD({i[0].EntryId})
    {Fore.light_steel_blue}TotalExpense({Fore.light_magenta}{i.total_expense}{Fore.light_steel_blue}) {Fore.light_yellow}Price({i[0].Price}) {Fore.light_steel_blue}CRV({i[0].CRV}) {Fore.light_red}Tax({i[0].Tax}) {Fore.light_cyan}TaxRate({txr}%) {Fore.cyan}for Qty({i.total_qty})
    {Fore.light_cyan}Location({Fore.light_steel_blue}{i[0].Location}){Style.reset}
    {Fore.grey_70}Note({Fore.grey_50}\n{'\n'.join(["\t"+z for num,z in enumerate(i[0].Note.split("\n"))])}{Fore.grey_70}\n\t){Style.reset}
    {Fore.grey_70}Desc({Fore.light_slate_grey}\n{'\n'.join(["\t"+z for num,z in enumerate(i[0].Description.split("\n"))])}{Fore.grey_70}\n\t){Style.reset}
    {Fore.light_steel_blue}Where({msgd})
    """,num,cta)
            else:
                msg=std_colorize(f"""{Fore.light_green}Name({i[0].Name}) {Fore.grey_50}EiD({i[0].EntryId}) {Fore.light_yellow}BcD({Fore.light_cyan}FMTD={i[0].rebar(i[0].Barcode)}, {Fore.orange_red_1}RAW={i[0].Barcode}{Fore.light_yellow}) {Fore.sea_green_1a}Code({Fore.light_cyan}FMTD={i[0].cfmt(i[0].Code)}, {Fore.orange_red_1}RAW={i[0].Code}{Fore.sea_green_1a})
    {Fore.light_steel_blue}TotalExpense({Fore.light_magenta}{i.total_expense}{Fore.light_steel_blue}) {Fore.light_yellow}Price({i[0].Price}) {Fore.light_steel_blue}CRV({i[0].CRV}) {Fore.light_red}Tax({i[0].Tax}) {Fore.light_cyan}TaxRate({txr}%) {Fore.cyan}for Qty({i.total_qty})
    {Fore.light_cyan}Location({Fore.light_steel_blue}{i[0].Location}){Style.reset}
    {Fore.grey_70}Note({Fore.grey_50}\n{'\n'.join(["\t"+z for num,z in enumerate(i[0].Note.split("\n"))])}{Fore.grey_70}\n\t){Style.reset}
    {Fore.grey_70}Desc({Fore.light_slate_grey}\n{'\n'.join(["\t"+z for num,z in enumerate(i[0].Description.split("\n"))])}{Fore.grey_70}\n\t){Style.reset}
    {Fore.light_steel_blue}Where({msgd})
    """,num,cta)
            print(msg)
            if store_file:
                store_file.write(f"{strip_colors(msg)}\n")
            if page:
                menus=f"edit={['edit','ed','e','ee']} clear={['reset','clear','zero','0','zro','rst','clr']}"
                menu=Control(ptext=f"{menus}: Do What?",helpText="Do What to this object.",data="string")
                if menu in BooleanAnswers.NONE:
                    return
                elif menu.lower() in ['edit','ed','e','ee']:
                    reRunRequired=True
                    TM.Tasks.TasksMode(parent=None,engine=db.ENGINE,init_only=True).NewEntryMenu(code=i[0].Barcode)
                elif menu.lower() in ['reset','clear','zero','0','zro','rst','clr']:
                    reRunRequired=True
                    session.execute(update(Entry).where(Entry.EntryId==i[0].EntryId).values({'InList':False,
                'ListQty':0,
                'Shelf':0,
                'Note':'',
                'BackRoom':0,
                'Distress':0,
                'Display_1':0,
                'Display_2':0,
                'Display_3':0,
                'Display_4':0,
                'Display_5':0,
                'Display_6':0,
                'Stock_Total':0,
                'CaseID_BR':'',
                'CaseID_LD':'',
                'CaseID_6W':'',
                'SBX_WTR_DSPLY':0,
                'SBX_CHP_DSPLY':0,
                'SBX_WTR_KLR':0,
                'FLRL_CHP_DSPLY':0,
                'FLRL_WTR_DSPLY':0,
                'WD_DSPLY':0,
                'CHKSTND_SPLY':0,
                'Expiry':None,
                'BestBy':None,
                'AquisitionDate':None,
                }))
                    session.commit()
                    session.refresh(i[0])
                    print(f"{Fore.orange_red_1}cleared!{Style.reset}")
                    continue
            total_e+=decc(i.total_expense,cf=roundTo)
            total_q+=decc(i.total_qty,cf=roundTo)
            total_c+=decc(i.total_crv,cf=roundTo)
            total_t+=decc(i.total_tax,cf=roundTo)
            total_p+=decc(i.total_price,cf=roundTo)
        x={'total_expense':total_e,
        'total qty':total_q,
        'total crv':total_c,
        'total tax':total_t,
        'total price':total_p,}
        ct=len(x)
        
        for num,k in enumerate(x):
            msg=std_colorize(f"{k}: {x[k]}",num,ct)
            print(msg)
            store_file.write(strip_colors(msg)+"\n")
        if breakTransaction:
            msg=f"{Fore.orange_red_1}Do Not Accept this Transaction unless offending warnings regarding gift cards have been quelled! That includes this one!{Style.reset}"
            store_file.write("\n"+strip_colors(msg)+"\n")
            store_file.write("\n"+strip_colors(gftmsg)+"\n")
        with db.Session(db.ENGINE) as session:
            r=session.query(TransactionID).order_by(TransactionID.emoid.desc()).first()
            if r is None:
                transactionID=TransactionID(
                transactionId=str(uuid1()),
                transactionTotalExpense=x['total_expense'],
                transactionTotalPrice=x['total price'],
                TransactionTax=x['total tax'],
                TransactionCRV=x['total crv'],
                TransactionQTY=x['total qty'],
                dtoe=datetime.now()
                )
                session.add(transactionID)
                session.commit()
                session.refresh(transactionID)
                r=transactionID
            else:
                #r.transactionId=str(uuid1())
                r.transactionTotalExpense=x['total_expense']
                r.transactionTotalPrice=x['total price']
                r.TransactionTax=x['total tax']
                r.TransactionCRV=x['total crv']
                r.TransactionQTY=x['total qty']
                r.dtoe=datetime.now()
                session.commit()
                session.refresh(r)
            store_file.write("\n"+strip_colors(f"transactionID:{r.transactionId}")+"\n")
            print("\n"+strip_colors(f"transactionID:{r.transactionId}"))

        print(gftmsg)
        nmsg=toRounded(x['total_expense'],False)
        store_file.write(nmsg+'\n')
        store_file.close()

        #(((qty*crv)+(qty*price))*tax)
'''        
Price
CRV
Tax
'''

def oillog_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def oillog_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_oillog(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=oillog_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

oillog_menu={
    str(uuid1()):{
    "cmds":['oillog custom',],
    "exec":lambda self:s2cb_oillog(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def oillogLogger(Model=OilLog,short_view=oillog_short_view,menu=oillog_menu):
    return ModelLogger(Model=OilLog,short_view=oillog_short_view,menu=oillog_menu)


def tpoc2_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def tpoc2_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_tpoc2(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=tpoc2_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

tpoc2_menu={
    str(uuid1()):{
    "cmds":['tpoc2 custom',],
    "exec":lambda self:s2cb_tpoc2(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def tpoc2Logger(Model=TasksCompleted,short_view=tpoc2_short_view,menu=tpoc2_menu):
    return ModelLogger(Model=TasksCompleted,short_view=tpoc2_short_view,menu=tpoc2_menu)

def Correspondence_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def Correspondence_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_Correspondence(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=Correspondence_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

Correspondence_menu={
    str(uuid1()):{
    "cmds":['Correspondence custom',],
    "exec":lambda self:s2cb_Correspondence(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def CorrespondenceLogger(Model=Correspondence,short_view=Correspondence_short_view,menu=Correspondence_menu):
    return ModelLogger(Model=Correspondence,short_view=Correspondence_short_view,menu=Correspondence_menu)


def Bills_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def Bills_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_Bills(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=Bills_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

Bills_menu={
    str(uuid1()):{
    "cmds":['Bills custom',],
    "exec":lambda self:s2cb_Bills(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def BillsLogger(Model=Bills,short_view=Bills_short_view,menu=Bills_menu):
    return ModelLogger(Model=Bills,short_view=Bills_short_view,menu=Bills_menu)


def HumanWaste_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def HumanWaste_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_HumanWaste(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=HumanWaste_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

HumanWaste_menu={
    str(uuid1()):{
    "cmds":['HumanWaste custom',],
    "exec":lambda self:s2cb_HumanWaste(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def HumanWasteLogger(Model=HumanWaste,short_view=HumanWaste_short_view,menu=HumanWaste_menu):
    return ModelLogger(Model=HumanWaste,short_view=HumanWaste_short_view,menu=HumanWaste_menu)

def RestroomBreak_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def RestroomBreak_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_RestroomBreak(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=RestroomBreak_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

RestroomBreak_menu={
    str(uuid1()):{
    "cmds":['RestroomBreak custom',],
    "exec":lambda self:s2cb_RestroomBreak(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def RestroomBreakLogger(Model=RestroomBreak,short_view=RestroomBreak_short_view,menu=RestroomBreak_menu):
    return ModelLogger(Model=RestroomBreak,short_view=RestroomBreak_short_view,menu=RestroomBreak_menu)

def FreightStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def FreightStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_FreightStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=FreightStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def truck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        whose_cases={}
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
                if str(p) not in whose_cases:
                    whose_cases[str(p)]=0
                if p.exists() and p.is_file():
                    dbfile=f"sqlite:///{str(p)}"
                    engine=create_engine(dbfile)
                    with Session(engine) as session1:
                        totalCount=FreightStartEnd.TransportStartCaseCount-FreightStartEnd.TransportEndCaseCount
                        statement_sub=select(FreightStartEnd,totalCount.label('total_completed')
                            ).where(FreightStartEnd.dtoe.between(fb['start'],fb['end']),FreightStartEnd.TransportEndCaseCount!=None)
                        orderedQuery=orderQuery(statement_sub,FreightStartEnd.dtoe,inverse=True)
                        results=session1.execute(orderedQuery)
                        cta=len(results.fetchall())
                        results=session1.execute(orderedQuery)
                        
                        for num,r in enumerate(results):
                            print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                            completed_cases+=r.total_completed
                            whose_cases[str(p)]+=r.total_completed


                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(FreightRecieved).where(FreightRecieved.dtoe.between(fb['start'],fb['end']),FreightRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            statement=select(SeasonalRecieved).where(SeasonalRecieved.dtoe.between(fb['start'],fb['end']),SeasonalRecieved.recieved_load_total!=None)
            #print('x x')
            results=session.execute(statement)
            #print('x x')
            rz=results.scalars().first()
            if rz == None:
                rz=0
            else:
                rz=rz.recieved_load_total
            print(f"{Fore.orange_red_1}Total Freight RedZone:{Fore.light_green} {rz}\n{Fore.orange_red_1}Total Freight Store:{Fore.light_green} {ft.recieved_load_total}\nfrom \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/(Decimal(ft.recieved_load_total)-Decimal(rz)))*100}%")
            cta=len(whose_cases)
            for num,i in enumerate(whose_cases):
                try:
                    print(
                        std_colorize(
                            f"{Fore.light_red}{i} :{Fore.orange_red_1} {whose_cases[i]} {Fore.light_yellow} of {(Decimal(ft.recieved_load_total)-Decimal(rz))}{Style.reset}",num,cta
                            )
                        )
                except Exception as e:
                    print(e)


def randomDate(start_year=1985,end_year=1999):
    if start_year in BooleanAnswers.NONE:
        return
    elif end_year in BooleanAnswers.NONE:
        return
    if isinstance(start_year,str):
        start_year=1985
    if isinstance(end_year,str):
        end_year=1985

    random_year=random.randint(start_year,end_year)
    random_month=random.randint(1,12)
    max_month_days=calendar.monthrange(random_year,random_month)[-1]
    random_day=random.randint(1,max_month_days)

    hours=random.randint(0,23)
    minutes=random.randint(0,59)
    seconds=random.randint(0,59)
    ms=random.randint(0,999)
    random_dtoe=datetime(random_year,random_month,random_day,int(hours),int(minutes),int(seconds),int(ms))

    print(random_dtoe)
    return random_dtoe


def get_case_minute(self=None):
    with Session(ENGINE) as session:
        daysUntilNextLoad=detectGetOrSet("get_case_minute daysUntilNextLoad",7,setValue=False,literal=False)
        if daysUntilNextLoad in BooleanAnswers.NONE:
            daysUntilNextLoad=7

        load_dates_statement=select(FreightRecieved).where(FreightRecieved.dtoe!=None)
        load_dates=session.execute(load_dates_statement).scalars().all()
        case_per_minute=[]
        dates=[f'{Fore.light_yellow}Your Average Speed For Load Dates: {Style.reset}']
        for ld in load_dates:
            start=ld.dtoe
            end=ld.dtoe+timedelta(days=daysUntilNextLoad)
            
            key1=f'hours alloted for {start} - {end}'
            fields={
                key1:{
                'default':40,
                'type':'float'
                }
            }
            fb=FormBuilder(data=fields)
            if fb in BooleanAnswers.NONE:
                continue
            if fb[key1] == 0:
                continue
            cases_completed_statement=select(FreightStartEnd).where(FreightStartEnd.dtoe.between(start,end))
            cases_completed=session.execute(cases_completed_statement).scalars().all()
            cases_for_period=0
            for day in cases_completed:
                try:
                    freight=(day.TransportStartCaseCount-day.TransportEndCaseCount)
                    cases_for_period+=freight
                except Exception as e:
                    print(e)
            if cases_for_period == 0:
                continue
            try:
                speed=cases_for_period/(fb[key1]*60)
                case_per_minute.append(speed)
            except Exception as e:
                print(e)
                continue
            dates.append(f"\t{Fore.light_green}{start}{Fore.cyan} - {Fore.light_red}{end}{Fore.light_steel_blue} {cases_for_period} cases/{fb[key1]*60} minutes(hours={fb[key1]}) = {speed} minute{Style.reset}")
        average_case_per_minute=float(np.average(case_per_minute))
        print('\n'.join(dates))
        print(f'Average Case Per Minute: {average_case_per_minute}')

def get_freight_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=FreightStartEnd.TransportStartCaseCount-FreightStartEnd.TransportEndCaseCount
        statement=select(FreightStartEnd,totalCount.label('total_completed')
            ).where(FreightStartEnd.dtoe.between(fb['start'],fb['end']),FreightStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,FreightStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

def get_truck_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        statement=select(SeasonalRecieved).where(SeasonalRecieved.dtoe.between(fb['start'],fb['end']))
        seasonal_result=session.execute(statement).scalars().first()
        if seasonal_result in [None,]:
            seasonal_load=0
        else:
            seasonal_load=seasonal_result.recieved_load_total

        statement=select(FreightRecieved).where(FreightRecieved.dtoe.between(fb['start'],fb['end']))
        load_result=session.execute(statement).scalars().first()
        if load_result in [None,]:
            load=0
        else:
            load=load_result.recieved_load_total
        store_load=decc(load)-decc(seasonal_load)
        if store_load < 0:
            store_load=f"{Fore.orange_3}No Load was Recorded under `fse`; check your records{Style.reset}"
        msg=[f"Seasonal Load: {seasonal_load}",f"Total Load Recieved: {load}",f"Store Load: {store_load}"]
        cta=len(msg)
        for num, i in enumerate(msg):
            print(std_colorize(i,num,cta))



FreightStartEnd_menu={
    str(uuid1()):{
    "cmds":['FreightStartEnd custom',],
    "exec":lambda self:s2cb_FreightStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_freight_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":truck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
    str(uuid1()):{
    "cmds":['get truck total','gtt'],
    "exec":get_truck_total,
    "desc":"get total truck to be recieved",
    },
    str(uuid1()):{
    "cmds":['get case per minute','gcpm'],
    "exec":get_case_minute,
    "desc":"get case per minute with allotted time from from schedule",
    },
    
}
#bptxt - bill paid text

#TriedToWake
def FreightStartEndLogger(Model=FreightStartEnd,short_view=FreightStartEnd_short_view,menu=FreightStartEnd_menu):
    return ModelLogger(Model=FreightStartEnd,short_view=FreightStartEnd_short_view,menu=FreightStartEnd_menu)

def FreightRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def FreightRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_FreightRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=FreightRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

FreightRecieved_menu={
    str(uuid1()):{
    "cmds":['FreightRecieved custom',],
    "exec":lambda self:s2cb_FreightRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def FreightRecievedLogger(Model=FreightRecieved,short_view=FreightRecieved_short_view,menu=FreightRecieved_menu):
    return ModelLogger(Model=FreightRecieved,short_view=FreightRecieved_short_view,menu=FreightRecieved_menu)

def FrozenStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def FrozenStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_FrozenStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=FrozenStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def ftruck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
        
                if p.exists() and p.is_file():
                    try:
                        dbfile=f"sqlite:///{str(p)}"
                        engine=create_engine(dbfile)
                        with Session(engine) as session1:
                            totalCount=FrozenStartEnd.TransportStartCaseCount-FrozenStartEnd.TransportEndCaseCount
                            statement_sub=select(FrozenStartEnd,totalCount.label('total_completed')
                                ).where(FrozenStartEnd.dtoe.between(fb['start'],fb['end']),FrozenStartEnd.TransportEndCaseCount!=None)
                            orderedQuery=orderQuery(statement_sub,FrozenStartEnd.dtoe,inverse=True)
                            results=session1.execute(orderedQuery)
                            cta=len(results.fetchall())
                            results=session1.execute(orderedQuery)
                            
                            for num,r in enumerate(results):
                                print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                                completed_cases+=r.total_completed
                    except Exception as e:
                        print(e)
                        print(f"{Fore.light_red}Please Boot this DB first! {dbfile}{Style.reset}")
                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(FrozenRecieved).where(FrozenRecieved.dtoe.between(fb['start'],fb['end']),FrozenRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            print(f" from \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/Decimal(ft.recieved_load_total))*100}%")
        

def get_frozen_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=FrozenStartEnd.TransportStartCaseCount-FrozenStartEnd.TransportEndCaseCount
        statement=select(FrozenStartEnd,totalCount.label('total_completed')
            ).where(FrozenStartEnd.dtoe.between(fb['start'],fb['end']),FrozenStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,FrozenStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

FrozenStartEnd_menu={
    str(uuid1()):{
    "cmds":['FrozenStartEnd custom',],
    "exec":lambda self:s2cb_FrozenStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_frozen_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":ftruck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
}
#bptxt - bill paid text

#TriedToWake
def FrozenStartEndLogger(Model=FrozenStartEnd,short_view=FrozenStartEnd_short_view,menu=FrozenStartEnd_menu):
    return ModelLogger(Model=FrozenStartEnd,short_view=FrozenStartEnd_short_view,menu=FrozenStartEnd_menu)

def FrozenRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def FrozenRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_FrozenRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=FrozenRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

FrozenRecieved_menu={
    str(uuid1()):{
    "cmds":['FrozenRecieved custom',],
    "exec":lambda self:s2cb_FrozenRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def FrozenRecievedLogger(Model=FrozenRecieved,short_view=FrozenRecieved_short_view,menu=FrozenRecieved_menu):
    return ModelLogger(Model=FrozenRecieved,short_view=FrozenRecieved_short_view,menu=FrozenRecieved_menu)

def BackroomStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def BackroomStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_BackroomStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=BackroomStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def btruck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
        
                if p.exists() and p.is_file():
                    try:
                        dbfile=f"sqlite:///{str(p)}"
                        engine=create_engine(dbfile)
                        with Session(engine) as session1:
                            totalCount=BackroomStartEnd.TransportStartCaseCount-BackroomStartEnd.TransportEndCaseCount
                            statement_sub=select(BackroomStartEnd,totalCount.label('total_completed')
                                ).where(BackroomStartEnd.dtoe.between(fb['start'],fb['end']),BackroomStartEnd.TransportEndCaseCount!=None)
                            orderedQuery=orderQuery(statement_sub,BackroomStartEnd.dtoe,inverse=True)
                            results=session1.execute(orderedQuery)
                            cta=len(results.fetchall())
                            results=session1.execute(orderedQuery)
                            
                            for num,r in enumerate(results):
                                print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                                completed_cases+=r.total_completed
                    except Exception as e:
                        print(e)
                        print(f"{Fore.light_red}Please Boot this DB first! {dbfile}{Style.reset}")
                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(BackroomRecieved).where(BackroomRecieved.dtoe.between(fb['start'],fb['end']),BackroomRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            print(f" from \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/Decimal(ft.recieved_load_total))*100}%")
        

def get_backroom_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=BackroomStartEnd.TransportStartCaseCount-BackroomStartEnd.TransportEndCaseCount
        statement=select(BackroomStartEnd,totalCount.label('total_completed')
            ).where(BackroomStartEnd.dtoe.between(fb['start'],fb['end']),BackroomStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,BackroomStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

BackroomStartEnd_menu={
    str(uuid1()):{
    "cmds":['BackroomStartEnd custom',],
    "exec":lambda self:s2cb_BackroomStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_backroom_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":btruck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
}
#bptxt - bill paid text

#TriedToWake
def BackroomStartEndLogger(Model=BackroomStartEnd,short_view=BackroomStartEnd_short_view,menu=BackroomStartEnd_menu):
    return ModelLogger(Model=BackroomStartEnd,short_view=BackroomStartEnd_short_view,menu=BackroomStartEnd_menu)

def BackroomRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def BackroomRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_BackroomRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=BackroomRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

BackroomRecieved_menu={
    str(uuid1()):{
    "cmds":['BackroomRecieved custom',],
    "exec":lambda self:s2cb_BackroomRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def BackroomRecievedLogger(Model=BackroomRecieved,short_view=BackroomRecieved_short_view,menu=BackroomRecieved_menu):
    return ModelLogger(Model=BackroomRecieved,short_view=BackroomRecieved_short_view,menu=BackroomRecieved_menu)

#frozen backroom
def FrozenBackroomStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def FrozenBackroomStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_FrozenBackroomStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=FrozenBackroomStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def fbtruck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
        
                if p.exists() and p.is_file():
                    try:
                        dbfile=f"sqlite:///{str(p)}"
                        engine=create_engine(dbfile)
                        with Session(engine) as session1:
                            totalCount=FrozenBackroomStartEnd.TransportStartCaseCount-FrozenBackroomStartEnd.TransportEndCaseCount
                            statement_sub=select(FrozenBackroomStartEnd,totalCount.label('total_completed')
                                ).where(FrozenBackroomStartEnd.dtoe.between(fb['start'],fb['end']),FrozenBackroomStartEnd.TransportEndCaseCount!=None)
                            orderedQuery=orderQuery(statement_sub,FrozenBackroomStartEnd.dtoe,inverse=True)
                            results=session1.execute(orderedQuery)
                            cta=len(results.fetchall())
                            results=session1.execute(orderedQuery)
                            
                            for num,r in enumerate(results):
                                print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                                completed_cases+=r.total_completed
                    except Exception as e:
                        print(e)
                        print(f"{Fore.light_red}Please Boot this DB first! {dbfile}{Style.reset}")
                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(FrozenBackroomRecieved).where(FrozenBackroomRecieved.dtoe.between(fb['start'],fb['end']),FrozenBackroomRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            print(f" from \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/Decimal(ft.recieved_load_total))*100}%")
        

def get_fbackroom_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=FrozenBackroomStartEnd.TransportStartCaseCount-FrozenBackroomStartEnd.TransportEndCaseCount
        statement=select(FrozenBackroomStartEnd,totalCount.label('total_completed')
            ).where(FrozenBackroomStartEnd.dtoe.between(fb['start'],fb['end']),FrozenBackroomStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,FrozenBackroomStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

FrozenBackroomStartEnd_menu={
    str(uuid1()):{
    "cmds":['FrozenBackroomStartEnd custom',],
    "exec":lambda self:s2cb_FrozenBackroomStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_fbackroom_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":fbtruck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
}
#bptxt - bill paid text

#TriedToWake
def FrozenBackroomStartEndLogger(Model=FrozenBackroomStartEnd,short_view=FrozenBackroomStartEnd_short_view,menu=FrozenBackroomStartEnd_menu):
    return ModelLogger(Model=FrozenBackroomStartEnd,short_view=FrozenBackroomStartEnd_short_view,menu=FrozenBackroomStartEnd_menu)

def FrozenBackroomRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def FrozenBackroomRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_FrozenBackroomRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=FrozenBackroomRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

FrozenBackroomRecieved_menu={
    str(uuid1()):{
    "cmds":['FrozenBackroomRecieved custom',],
    "exec":lambda self:s2cb_FrozenBackroomRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def FrozenBackroomRecievedLogger(Model=FrozenBackroomRecieved,short_view=FrozenBackroomRecieved_short_view,menu=FrozenBackroomRecieved_menu):
    return ModelLogger(Model=FrozenBackroomRecieved,short_view=FrozenBackroomRecieved_short_view,menu=FrozenBackroomRecieved_menu)

#cooler backroom
def DairyBackroomStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def DairyBackroomStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_DairyBackroomStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=DairyBackroomStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def dbr_truck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
        
                if p.exists() and p.is_file():
                    try:
                        dbfile=f"sqlite:///{str(p)}"
                        engine=create_engine(dbfile)
                        with Session(engine) as session1:
                            totalCount=DairyBackroomStartEnd.TransportStartCaseCount-DairyBackroomStartEnd.TransportEndCaseCount
                            statement_sub=select(DairyBackroomStartEnd,totalCount.label('total_completed')
                                ).where(DairyBackroomStartEnd.dtoe.between(fb['start'],fb['end']),DairyBackroomStartEnd.TransportEndCaseCount!=None)
                            orderedQuery=orderQuery(statement_sub,DairyBackroomStartEnd.dtoe,inverse=True)
                            results=session1.execute(orderedQuery)
                            cta=len(results.fetchall())
                            results=session1.execute(orderedQuery)
                            
                            for num,r in enumerate(results):
                                print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                                completed_cases+=r.total_completed
                    except Exception as e:
                        print(e)
                        print(f"{Fore.light_red}Please Boot this DB first! {dbfile}{Style.reset}")
                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(DairyBackroomRecieved).where(DairyBackroomRecieved.dtoe.between(fb['start'],fb['end']),DairyBackroomRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            print(f" from \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/Decimal(ft.recieved_load_total))*100}%")
        

def get_dbackroom_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=DairyBackroomStartEnd.TransportStartCaseCount-DairyBackroomStartEnd.TransportEndCaseCount
        statement=select(DairyBackroomStartEnd,totalCount.label('total_completed')
            ).where(DairyBackroomStartEnd.dtoe.between(fb['start'],fb['end']),DairyBackroomStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,DairyBackroomStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

DairyBackroomStartEnd_menu={
    str(uuid1()):{
    "cmds":['DairyBackroomStartEnd custom',],
    "exec":lambda self:s2cb_DairyBackroomStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_dbackroom_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":dbr_truck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
}
#bptxt - bill paid text

#TriedToWake
def DairyBackroomStartEndLogger(Model=DairyBackroomStartEnd,short_view=DairyBackroomStartEnd_short_view,menu=DairyBackroomStartEnd_menu):
    return ModelLogger(Model=DairyBackroomStartEnd,short_view=DairyBackroomStartEnd_short_view,menu=DairyBackroomStartEnd_menu)

def DairyBackroomRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def DairyBackroomRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_DairyBackroomRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=DairyBackroomRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

DairyBackroomRecieved_menu={
    str(uuid1()):{
    "cmds":['DairyBackroomRecieved custom',],
    "exec":lambda self:s2cb_DairyBackroomRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def DairyBackroomRecievedLogger(Model=DairyBackroomRecieved,short_view=DairyBackroomRecieved_short_view,menu=DairyBackroomRecieved_menu):
    return ModelLogger(Model=DairyBackroomRecieved,short_view=DairyBackroomRecieved_short_view,menu=DairyBackroomRecieved_menu)

def DairyStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def DairyStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_DairyStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=DairyStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def dtruck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
        
                if p.exists() and p.is_file():
                    try:
                        dbfile=f"sqlite:///{str(p)}"
                        engine=create_engine(dbfile)
                        with Session(engine) as session1:
                            totalCount=DairyStartEnd.TransportStartCaseCount-DairyStartEnd.TransportEndCaseCount
                            statement_sub=select(DairyStartEnd,totalCount.label('total_completed')
                                ).where(DairyStartEnd.dtoe.between(fb['start'],fb['end']),DairyStartEnd.TransportEndCaseCount!=None)
                            orderedQuery=orderQuery(statement_sub,DairyStartEnd.dtoe,inverse=True)
                            results=session1.execute(orderedQuery)
                            cta=len(results.fetchall())
                            results=session1.execute(orderedQuery)
                            
                            for num,r in enumerate(results):
                                print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                                completed_cases+=r.total_completed
                    except Exception as e:
                        print(e)
                        print(f"{Fore.light_red}Please Boot this DB first! {dbfile}{Style.reset}")
                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(DairyRecieved).where(DairyRecieved.dtoe.between(fb['start'],fb['end']),DairyRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            print(f" from \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/Decimal(ft.recieved_load_total))*100}%")
        

def get_dairy_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=DairyStartEnd.TransportStartCaseCount-DairyStartEnd.TransportEndCaseCount
        statement=select(DairyStartEnd,totalCount.label('total_completed')
            ).where(DairyStartEnd.dtoe.between(fb['start'],fb['end']),DairyStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,DairyStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

DairyStartEnd_menu={
    str(uuid1()):{
    "cmds":['DairyStartEnd custom',],
    "exec":lambda self:s2cb_DairyStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_dairy_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":dtruck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
}
#bptxt - bill paid text

#TriedToWake
def DairyStartEndLogger(Model=DairyStartEnd,short_view=DairyStartEnd_short_view,menu=DairyStartEnd_menu):
    return ModelLogger(Model=DairyStartEnd,short_view=DairyStartEnd_short_view,menu=DairyStartEnd_menu)

def DairyRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def DairyRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_DairyRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=DairyRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

DairyRecieved_menu={
    str(uuid1()):{
    "cmds":['DairyRecieved custom',],
    "exec":lambda self:s2cb_DairyRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def DairyRecievedLogger(Model=DairyRecieved,short_view=DairyRecieved_short_view,menu=DairyRecieved_menu):
    return ModelLogger(Model=DairyRecieved,short_view=DairyRecieved_short_view,menu=DairyRecieved_menu)


def DateString1(self=None):
    while True:
        try:
            fields={
            'month':{
            'type':'integer',
            'default':int(datetime.now().month)
            },
            'day':{
            'type':'integer',
            'default':int(datetime.now().day)
            },
            'year':{
            'type':'integer',
            'default':int(datetime.now().year)
            }
            }
            fb=FormBuilder(data=fields,passThruText="return mm/dd/yyyy")
            if fb in BooleanAnswers.NONE:
                return
            return datetime(fb['year'],fb['month'],fb['day']).strftime("%m/%d/%Y")

        except Exception as e:
            print(e,str(e),repr(e))

def DateString2(self=None):
    while True:
        try:
            fields={
            'dtoe':{
                'type':'datetime',
                'default':today()
            }
            }
            fb=FormBuilder(data=fields,passThruText="return mm/dd/yyyy from dtoe")
            if fb in BooleanAnswers.NONE:
                return
            return fb['dtoe'].strftime("%m/%d/%Y")

        except Exception as e:
            print(e,str(e),repr(e))

def PowerOutage_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def PowerOutage_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_PowerOutage(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=PowerOutage_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

PowerOutage_menu={
    str(uuid1()):{
    "cmds":['PowerOutage custom',],
    "exec":lambda self:s2cb_PowerOutage(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
def PowerOutageLogger(Model=PowerOutage,short_view=PowerOutage_short_view,menu=PowerOutage_menu):
    return ModelLogger(Model=PowerOutage,short_view=PowerOutage_short_view,menu=PowerOutage_menu)

#attendance
def Attendance_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def Attendance_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_Attendance(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=Attendance_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

Attendance_menu={
    str(uuid1()):{
    "cmds":['Attendance custom',],
    "exec":lambda self:s2cb_Attendance(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
def AttendanceLogger(Model=Attendance,short_view=Attendance_short_view,menu=Attendance_menu):
    return ModelLogger(Model=Attendance,short_view=Attendance_short_view,menu=Attendance_menu)

#redzone
#attendance
def RedZoneFreight_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def RedZoneFreight_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_RedZoneFreight(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=RedZoneFreight_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

RedZoneFreight_menu={
    str(uuid1()):{
    "cmds":['RedZoneFreight custom',],
    "exec":lambda self:s2cb_RedZoneFreight(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
def RedZoneFreightLogger(Model=RedZoneFreight,short_view=RedZoneFreight_short_view,menu=RedZoneFreight_menu):
    return ModelLogger(Model=RedZoneFreight,short_view=RedZoneFreight_short_view,menu=RedZoneFreight_menu)

def SeasonalStartEnd_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def SeasonalStartEnd_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_SeasonalStartEnd(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=SeasonalStartEnd_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)   
                
def struck_percent_complete(self=None):
    '''boot_dirs=self.boot_dirs
        if not boot_dirs.exists():
            boot_dirs.mkdir()
        bootable_dirs=[]
        bootable_dirs.append(str(Path(".").absolute()))
        with Session(ENGINE) as session:
            query=session.query(StoragePaths).filter(StoragePaths.group_id.icontains("active"))
            orderedQuery=orderQuery(query,StoragePaths.dtoe)
            
            results=orderedQuery.all()
            cta=len(results)
            for num, i in enumerate(results):
                print(std_colorize(f"{Path(i.path)} : Exists = {Fore.light_steel_blue}{Path(i.path).exists()}{Style.reset}",num,cta))
                if Path(i.path).exists():
                    bootable_dirs.append(Path(i.path))
        for root,dirs,files in boot_dirs.walk(top_down=True):
            for d in dirs:
                dsub=root/d
                if dsub not in bootable_dirs:
                    bootcfg=dsub/Path("__bootable__.py")
                    if bootcfg.exists():
                        bootable_dirs.append(dsub)


                        '''
    with Session(ENGINE) as session:
        statement=select(StoragePaths).where(StoragePaths.group_id.icontains('freight accounting'))
        rslts=session.execute(statement).fetchall()
        fields={
            'start':{
                'default':today(),
                'type':'datetime'
            },
            'end':{
                'default':datetime.now(),
                'type':'datetime'
            },
        }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        completed_cases=0
        whose_cases={}
        for i in rslts:
            if i[0].path != None:
                p=Path(i[0].path)
                print(p)
                if str(p) not in whose_cases:
                    whose_cases[str(p)]=0
                if p.exists() and p.is_file():
                    dbfile=f"sqlite:///{str(p)}"
                    engine=create_engine(dbfile)
                    with Session(engine) as session1:
                        totalCount=SeasonalStartEnd.TransportStartCaseCount-SeasonalStartEnd.TransportEndCaseCount
                        statement_sub=select(SeasonalStartEnd,totalCount.label('total_completed')
                            ).where(SeasonalStartEnd.dtoe.between(fb['start'],fb['end']),SeasonalStartEnd.TransportEndCaseCount!=None)
                        orderedQuery=orderQuery(statement_sub,SeasonalStartEnd.dtoe,inverse=True)
                        results=session1.execute(orderedQuery)
                        cta=len(results.fetchall())
                        results=session1.execute(orderedQuery)
                        
                        for num,r in enumerate(results):
                            print(std_colorize(f"Path: {p}\n{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
                            completed_cases+=r.total_completed
                            whose_cases[str(p)]+=r.total_completed


                print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))
            else:
                pass

        statement=select(SeasonalRecieved).where(SeasonalRecieved.dtoe.between(fb['start'],fb['end']),SeasonalRecieved.recieved_load_total!=None)
        #print('x x')
        results=session.execute(statement)
        #print('x x')
        ft=results.scalars().first()
        #print('ft',ft)
        if ft not in BooleanAnswers.NONE:
            statement=select(SeasonalRecieved).where(SeasonalRecieved.dtoe.between(fb['start'],fb['end']),SeasonalRecieved.recieved_load_total!=None)
            #print('x x')
            results=session.execute(statement)
            #print('x x')
            rz=results.scalars().first()
            if rz == None:
                rz=0
            else:
                rz=rz.recieved_load_total
            print(f"{Fore.orange_red_1}Total Seasonal:{Fore.light_green} {rz}\n{Fore.orange_red_1}\nfrom \n{ft}\n{Fore.orange_red_1}Truck Percent Completed: {Fore.light_green}{(Decimal(completed_cases)/(Decimal(ft.recieved_load_total)))*100}%")
            cta=len(whose_cases)
            for num,i in enumerate(whose_cases):
                try:
                    print(
                        std_colorize(
                            f"{Fore.light_red}{i} :{Fore.orange_red_1} {whose_cases[i]} {Fore.light_yellow} of {(Decimal(ft.recieved_load_total))}{Style.reset}",num,cta
                            )
                        )
                except Exception as e:
                    print(e)

def get_sfreight_total(self=None):
    with Session(ENGINE) as session:
        fields={
            'start':{
            'type':'datetime',
            'default':today()
            },
            'end':{
            'type':'datetime',
            'default':datetime.now()
            }
        }
        fb=FormBuilder(data=fields)
        if fb in [None,]:
            return

        totalCount=SeasonalStartEnd.TransportStartCaseCount-SeasonalStartEnd.TransportEndCaseCount
        statement=select(SeasonalStartEnd,totalCount.label('total_completed')
            ).where(SeasonalStartEnd.dtoe.between(fb['start'],fb['end']),SeasonalStartEnd.TransportEndCaseCount!=None)
        orderedQuery=orderQuery(statement,SeasonalStartEnd.dtoe,inverse=True)
        results=session.execute(orderedQuery)
        cta=len(results.fetchall())
        results=session.execute(orderedQuery)
        completed_cases=0
        for num,r in enumerate(results):
            print(std_colorize(f"{r[0]} {Fore.orange_red_1} Total Completed For Transport: {Fore.light_green}{r.total_completed}",num,cta))
            completed_cases+=r.total_completed
        print(std_colorize(f"Completed Cases/Cartons: {completed_cases}",0,1))

SeasonalStartEnd_menu={
    str(uuid1()):{
    "cmds":['SeasonalStartEnd custom',],
    "exec":lambda self:s2cb_SeasonalStartEnd(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['get freight total','gft'],
    "exec":get_sfreight_total,
    "desc":"get total freight completed",
    },
    str(uuid1()):{
    "cmds":['get total truck percent complete','gttpc'],
    "exec":struck_percent_complete,
    "desc":"get total truck percent complete; ensure db file is saved in StoragePaths with group_id 'freight accounting",
    },
}
#bptxt - bill paid text

#TriedToWake
def SeasonalStartEndLogger(Model=SeasonalStartEnd,short_view=SeasonalStartEnd_short_view,menu=SeasonalStartEnd_menu):
    return ModelLogger(Model=SeasonalStartEnd,short_view=SeasonalStartEnd_short_view,menu=SeasonalStartEnd_menu)

def SeasonalRecieved_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            msg=f"""{i}"""
            xtext.append(std_colorize(msg,xnum,ct))
            #xtext.append(msg)
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def SeasonalRecieved_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_SeasonalRecieved(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=SeasonalRecieved_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

SeasonalRecieved_menu={
    str(uuid1()):{
    "cmds":['SeasonalRecieved custom',],
    "exec":lambda self:s2cb_SeasonalRecieved(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def SeasonalRecievedLogger(Model=SeasonalRecieved,short_view=SeasonalRecieved_short_view,menu=SeasonalRecieved_menu):
    return ModelLogger(Model=SeasonalRecieved,short_view=SeasonalRecieved_short_view,menu=SeasonalRecieved_menu)


def notePod_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def notePod_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_notePod(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=notePod_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def notePod_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
notePod_menu={
    str(uuid1()):{
    "cmds":['notePod custom',],
    "exec":lambda self:s2cb_notePod(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def notePodLogger(Model=NotePod,short_view=notePod_short_view,menu=notePod_menu):
    return ModelLogger(Model=NotePod,short_view=notePod_short_view,menu=notePod_menu)

def oilGrade_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def oilGrade_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_oilGrade(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=oilGrade_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def oilGrade_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
oilGrade_menu={
    str(uuid1()):{
    "cmds":['oilGrade custom',],
    "exec":lambda self:s2cb_oilGrade(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def oilGradeLogger(Model=OilGrade,short_view=oilGrade_short_view,menu=oilGrade_menu):
    return ModelLogger(Model=OilGrade,short_view=oilGrade_short_view,menu=oilGrade_menu)

def vehicleRegistration_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def vehicleRegistration_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_vehicleRegistration(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=vehicleRegistration_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def vehicleRegistration_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
vehicleRegistration_menu={
    str(uuid1()):{
    "cmds":['vehicleRegistration custom',],
    "exec":lambda self:s2cb_vehicleRegistration(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def vehicleRegistrationLogger(Model=VehicleRegistration,short_view=vehicleRegistration_short_view,menu=vehicleRegistration_menu):
    return ModelLogger(Model=VehicleRegistration,short_view=vehicleRegistration_short_view,menu=vehicleRegistration_menu)

def driversLicense_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def driversLicense_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_driversLicense(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=driversLicense_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def driversLicense_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
driversLicense_menu={
    str(uuid1()):{
    "cmds":['driversLicense custom',],
    "exec":lambda self:s2cb_driversLicense(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def driversLicenseLogger(Model=DriversLicense,short_view=driversLicense_short_view,menu=driversLicense_menu):
    return ModelLogger(Model=DriversLicense,short_view=driversLicense_short_view,menu=driversLicense_menu)

def stateIdCard_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,i in enumerate(data):
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            zt=[]
            cta=len(msg.split("\n"))
            for znum,ii in enumerate(msg.split("\n")):
                zt.append(std_colorize(ii,znum,cta))
            xtext.append('\n'.join(zt))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def stateIdCard_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_stateIdCard(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=stateIdCard_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def stateIdCard_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
stateIdCard_menu={
    str(uuid1()):{
    "cmds":['stateIdCard custom',],
    "exec":lambda self:s2cb_stateIdCard(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def stateIdCardLogger(Model=StateIdCard,short_view=stateIdCard_short_view,menu=stateIdCard_menu):
    return ModelLogger(Model=StateIdCard,short_view=stateIdCard_short_view,menu=stateIdCard_menu)

def addLstQtyById():
    with Session(ENGINE) as session:
        while True:
            fields={
                'EntryId':{
                    'type':'integer',
                    'default':None,
                },
            }
            for k in reversed(BooleanAnswers.location_fields):
                fields[k]={
                    'type':'float',
                    'default':0,
                }
            fb=FormBuilder(data=fields)
            if fb in BooleanAnswers.NONE:
                return
            statement=select(Entry).where(Entry.EntryId==fb['EntryId'])
            result=session.execute(statement).scalars().first()
            if result is not None:
                for k in fb:
                    setattr(result,k,fb[k])
                result.InList=True
                session.commit()
                session.refresh(result)
                print(result)
            again=Control(ptext='Again?',helpText='yes or no',data='boolean')
            if again in BooleanAnswers.NONE or again in BooleanAnswers.NO_defaulted:
                return
            

def find_zip_code(self=None):
    zcdb=ZipCodeDatabase()
    fields={
        'city':{
        'type':'string',
        'default':None,
        },
        'state':{
        'type':'string',
        'default':None,
        }
    }
    fb=FormBuilder(data=fields)
    if fb in BooleanAnswers.NONE:
        return
    for k in fb:
        if fb[k] is None:
            fb.pop(k)
    if fb == {}:
        print("no data was provided to use.")
        return

    results=zcdb.find_zip(**fb)
    cta=len(results)
    helpText=[]
    for num, i in enumerate(results):
        msg=std_colorize(f'{i}',num,cta)
        helpText.append(msg)
    helpText='\n'.join(helpText)
    while True:
        which=Control(ptext=f"{helpText}\nWhich index? ",helpText="an integer",data="integer")
        if which in BooleanAnswers.NONE:
            return
        if which in range(0,cta):
            return results[which].zip
        else:
            continue

def calorieIntake_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        ttlCarb=[]
        

        carbs=QTY(0,"grams")
        fat=QTY(0,"grams")
        cholesterol=QTY(0,"grams")
        sodium=QTY(0,"mg")
        ttlSodiumConsumed=QTY(0,"mg")
        ss=QTY(0,"grams")
        ttlsugars=QTY(0,"grams")
        ttladdsugars=QTY(0,"grams")
        protien=QTY(0,"grams")
        cal=QTY(0,"kilocalorie")

        ttlCarbConsumed=QTY(0,"grams")
        ttlFatConsumed=QTY(0,"grams")
        ttlCholesterolConsumed=QTY(0,"mg")
        ttlSodiumConsumed=QTY(0,"mg")
        ttlDietaryFiberConsumed=QTY(0,"grams")
        ttlTTLSugarsConsumed=QTY(0,"grams")
        ttlTTLAddedSugarsConsumed=QTY(0,"grams")
        ttlProtienConsumed=QTY(0,"grams")
        ttlCalConsumed=QTY(0,"kilocalorie")

        for xnum,i in enumerate(data):
            if i.QtyConsumed is None:
                print(f'{Fore.light_yellow}emod={Fore.light_steel_blue}{i.emoid} {Fore.cyan}QtyConsumed={Fore.magenta}"{i.QtyConsumed}"')
            elif i.QtyConsumed < 1:
                print(f'{Fore.light_yellow}emod={Fore.light_steel_blue}{i.emoid} {Fore.cyan}QtyConsumed={Fore.magenta}"{i.QtyConsumed}"')
            if i.ServingSize is None:
                print(f'{Fore.light_yellow}emod={Fore.light_steel_blue}{i.emoid} {Fore.cyan}ServingSize={Fore.magenta}"{i.ServingSize}"')
            elif i.ServingSize < 1:
                print(f'{Fore.light_yellow}emod={Fore.light_steel_blue}{i.emoid} {Fore.cyan}ServingSize={Fore.magenta}"{i.ServingSize}"')

            try:
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                upperRange=(servingsize*i.ServingsPerContainer)
                asPercent=qtyConsumed/upperRange
            except Exception as e:
                print(e)
                asPercent=0

            try:
                carb_per_serving=QTY(i.TotalCarbs,i.TotalCarbsUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                #print(servingsize,qtyConsumed,carb_per_serving)
                carbs=(qtyConsumed/servingsize)*carb_per_serving

                ttlCarbConsumed=carbs
            except Exception as e:
                print(e)
                
            #exit(carbs)
            try:
                fat_per_serving=QTY(i.TotalFat,i.TotalFatUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                fat=(qtyConsumed/servingsize)*fat_per_serving
                ttlFatConsumed+=(qtyConsumed/servingsize)*fat_per_serving
            except Exception as e:
                print(e)
                

            try:
                cal_per_serving=QTY(i.Calories,'kilocalorie')
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                cal=(qtyConsumed/servingsize)*cal_per_serving
                ttlCalConsumed+=(qtyConsumed/servingsize)*cal_per_serving
            except Exception as e:
                print(e)

            try:
                cholesterol_per_serving=QTY(i.Cholesterol,i.CholesterolUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                cholesterol=(qtyConsumed/servingsize)*cholesterol_per_serving
                ttlCholesterolConsumed+=cholesterol
            except Exception as e:
                print(e)
                

            try:
                sodium_per_serving=QTY(i.Sodium,i.SodiumUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                sodium=(qtyConsumed/servingsize)*sodium_per_serving
                ttlSodiumConsumed+=sodium
            except Exception as e:
                print(e)
                

            try:
                dietaryFiber_per_serving=QTY(i.DietaryFiber,i.DietaryFiberUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                ss=(qtyConsumed/servingsize)*dietaryFiber_per_serving
                ttlDietaryFiberConsumed+=ss
            except Exception as e:
                print(e)
                

            try:
                TTLSugars_per_serving=QTY(i.TTLSugars,i.TTLSugarsUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                ttlsugars=(qtyConsumed/servingsize)*TTLSugars_per_serving
                ttlTTLSugarsConsumed+=ttlsugars
            except Exception as e:
                print(e)
                

            try:
                TTLAddedSugars_per_serving=QTY(i.TTLSugars,i.TTLAddedSugarsUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                ttladdsugars=(qtyConsumed/servingsize)*TTLAddedSugars_per_serving
                ttlTTLAddedSugarsConsumed+=ttladdsugars
            except Exception as e:
                print(e)
                

            try:
                Protien_per_serving=QTY(i.Protien,i.ProtienUnit)
                qtyConsumed=QTY(i.QtyConsumed,i.QtyConsumedUnit)
                servingsize=QTY(i.ServingSize,i.ServingSizeUnit)
                protien=(qtyConsumed/servingsize)*Protien_per_serving
                ttlProtienConsumed+=protien
            except Exception as e:
                print(e)
                

            ttlCarb.append(ttlCarbConsumed)
            msg=f'''
{Fore.cyan}emoid={Fore.light_yellow}{i.emoid}{Style.reset}
{Fore.light_steel_blue}group_id={Fore.light_yellow}{i.group_id}{Style.reset}
{Fore.orange_red_1}Barcode={i.Barcode}{Style.reset}
{Fore.orange_red_1}EntryName={i.EntryName}{Style.reset}
{Fore.orange_red_1}QtyConsumed={i.QtyConsumed:.2f} {i.QtyConsumedUnit}{Style.reset}
{Fore.orange_red_1}ServingSize={i.ServingSize:.2f} {i.ServingSizeUnit}{Style.reset}
{Fore.orange_red_1}ServingsPerContainer={i.ServingsPerContainer:.2f}{Style.reset}
{Fore.orange_red_1}Calories(Food Label Calorie==KiloCalorie)={i.Calories:.2f}{Style.reset}
{Fore.orange_red_1}TotalFat={i.TotalFat:.2f} {i.TotalFatUnit}{Style.reset}
{Fore.orange_red_1}Cholesterol={i.Cholesterol:.2f} {i.CholesterolUnit}{Style.reset}
{Fore.orange_red_1}Sodium={i.Sodium:.2f} {i.SodiumUnit}{Style.reset}
{Fore.orange_red_1}TotalCarbs={i.TotalCarbs:.2f} {i.TotalCarbsUnit}{Style.reset}
{Fore.orange_red_1}DietaryFiber={i.DietaryFiber:.2f} {i.DietaryFiberUnit}{Style.reset}
{Fore.orange_red_1}TTLSugars={i.TTLSugars:.2f} {i.TTLSugarsUnit}{Style.reset}
{Fore.orange_red_1}TTLAddedSugars={i.TTLAddedSugars:.2f} {i.TTLAddedSugarsUnit}{Style.reset}
{Fore.orange_red_1}Protien={i.Protien:.2f} {i.ProtienUnit}{Style.reset}
{Fore.orange_red_1}TTL Carb Consumed:{ttlCarbConsumed:.2f}{Style.reset}
{Fore.orange_red_1}TTL Cal(Food Label Calorie==KiloCalorie) Consumed:{i.Calories}{Style.reset}
{Fore.light_yellow}DTOE: {Fore.light_magenta}{i.dtoe}{Style.reset}
{Fore.light_cyan}Consumed carbs:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{carbs:.2f}{Style.reset}
{Fore.light_cyan}Consumed fat:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}%= {Fore.light_steel_blue}{fat:.2f}{Style.reset}
{Fore.light_cyan}Consumed cholesterol:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{cholesterol:.2f}{Style.reset}
{Fore.light_cyan}Consumed sodium:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{sodium:.2f}{Style.reset}
{Fore.light_cyan}Consumed fiber:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{ss:.2f}{Style.reset}
{Fore.light_cyan}Consumed ttlsugars:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{ttlsugars:.2f}{Style.reset}
{Fore.light_cyan}Consumed ttladdsugars:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{ttladdsugars:.2f}{Style.reset}
{Fore.light_cyan}Consumed protien:(Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{protien:.2f}{Style.reset}
{Fore.light_cyan}Consumed calorie(Food Label Calorie==KiloCalorie):Percent Of Pkg by ServingSize={asPercent.magnitude*100:.2f}% = {Fore.light_steel_blue}{cal:.2f}{Style.reset}'''
            msg=std_colorize(msg,xnum,ct)
            xtext.append(msg.replace("\n"," | "))
        consumedTTL=None
        for i in ttlCarb:
            try:
                if consumedTTL is None:
                    consumedTTL=i
                else:
                    consumedTTL+=i
            except Exception as e:
                print(e)
        x='\n'.join(xtext+[
f"{Fore.red}Totals For Retrieved Data Set{Style.reset}",
f"{Fore.light_green}TTL Carbs: {consumedTTL:.2f}{Style.reset}",
f"{Fore.light_green}TTL Fat: {ttlFatConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL Cholesterol: {ttlCholesterolConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL Sodium: {ttlSodiumConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL DietaryFiber: {ttlDietaryFiberConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL Sugars: {ttlTTLSugarsConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL Added Sugars: {ttlTTLAddedSugarsConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL Protien: {ttlProtienConsumed:.2f}{Style.reset}",
f"{Fore.light_green}TTL Calories(Food Label Calorie==KiloCalorie): {ttlCalConsumed:.2f}{Style.reset}",
            ])
        if printToScreen:
            print(x)
        return x

def calorieIntake_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_calorieIntake(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=calorieIntake_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def calorieIntake_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
calorieIntake_menu={
    str(uuid1()):{
    "cmds":['calorieIntake custom',],
    "exec":lambda self:s2cb_calorieIntake(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def calorieIntakeLogger(Model=CalorieIntake,short_view=calorieIntake_short_view,menu=calorieIntake_menu):
    return ModelLogger(Model=CalorieIntake,short_view=calorieIntake_short_view,menu=calorieIntake_menu)

def nameFromSearch(self=None):
    while True:
        try:
            with Session(ENGINE) as session:
                code=Control(ptext='Search Name/Barcode/Code: ',helpText='what are you looking for',data='string')
                if code in BooleanAnswers.NONE:
                    return
                results=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.Barcode.icontains(code),Entry.Code.icontains(code),Entry.ALT_Barcode==code,Entry.ALT_Barcode.icontains(code),Entry.DUP_Barcode==code,Entry.DUP_Barcode.icontains(code),Entry.Name.icontains(code))).all()
                cta=len(results)
                if cta < 0:
                    again=Control("no results were found; try again?",helpText="a yes or a no",data='boolean')
                    if again in BooleanAnswers.NONE:
                        return
                    elif again in BooleanAnswers.YES_defaulted:
                        continue
                    else:
                        return

                helpText=[]
                for num,i in enumerate(results):
                    msg=std_colorize(f'{i.seeShort()}',num,cta)
                    helpText.append(msg)
                helpText='\n'.join(helpText)
                while True:
                    index=Control(ptext=f'{helpText}\n{Fore.light_yellow}Which index? ',helpText=f'{helpText}\n{Fore.light_yellow}An integer index',data="integer")
                    if index in BooleanAnswers.NONE:
                        return
                    if index in range(0,cta):
                        return_fields=[i.name for i in Entry.__table__.columns]
                        htext=[]
                        while True:
                            for num,i in enumerate(return_fields):
                                msg=std_colorize(f'{i}',num,cta)
                                htext.append(msg)
                            htext='\n'.join(htext)
                            ctf=len(htext)
                            field_from_search=Control(ptext=f'{htext}\n{Fore.light_yellow}Which index? ',helpText=f'{htext}\n{Fore.light_yellow}An integer index',data="integer")
                            if field_from_search in BooleanAnswers.NONE:
                                return
                            if field_from_search in range(0,ctf):
                                return getattr(results[index],return_fields[field_from_search])
                            else:
                                continue
                        return results[index].Name
                    else:
                        continue
        except Exception as e:
            print(e)
            continue

def requiredMaterials_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        for xnum,ii in enumerate(data):

            msg=f"{Fore.light_green}Name{Fore.light_red}:{Fore.light_steel_blue} {ii.Name} {Fore.light_green}Barcode{Fore.light_red}:{Fore.light_steel_blue} {ii.Barcode} {Fore.light_green}Qty{Fore.light_red}:{Fore.light_steel_blue} {ii.Qty} {ii.QtyUnit} {Fore.light_green}EmoId{Fore.light_red}:{Fore.light_steel_blue} {ii.emoid} {Fore.light_green}DTOE{Fore.light_red}:{Fore.light_steel_blue} {ii.dtoe} {Fore.light_green}FromLocation{Fore.light_red}:{Fore.light_steel_blue} {ii.FromLocation} {Fore.light_green}Comment{Fore.light_red}:{Fore.light_steel_blue} {ii.comment} {Fore.light_green}group_id{Fore.light_red}:{Fore.light_steel_blue} {ii.group_id}{Style.reset}"
            xtext.append(std_colorize(msg,xnum,ct))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def requiredMaterials_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_requiredMaterials(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=requiredMaterials_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def requiredMaterials_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
requiredMaterials_menu={
    str(uuid1()):{
    "cmds":['requiredMaterials custom',],
    "exec":lambda self:s2cb_requiredMaterials(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def requiredMaterialsLogger(Model=RequiredMaterials,short_view=requiredMaterials_short_view,menu=requiredMaterials_menu):
    return ModelLogger(Model=RequiredMaterials,short_view=requiredMaterials_short_view,menu=requiredMaterials_menu)


def solvefor_triangle_hypotenuse():
    fields={
    'base':{
        'type':'float',
        'default':1,
        },
    'height':{
        'type':'float',
        'default':1
        }
    }
    fb=FormBuilder(data=fields,passThruText="((fb['base']**2)+(fb['height']**2))**0.5")
    if fb in BooleanAnswers.NONE:
        return
    formula=((fb['base']**2)+(fb['height']**2))**0.5
    return formula

def solvefor_triangle_base():
    fields={
    'hypotenuse':{
        'type':'float',
        'default':1,
        },
    'height':{
        'type':'float',
        'default':1
        }
    }
    fb=FormBuilder(data=fields,passThruText="((fb['hypotenus']**2)-(fb['height']**2))**0.5")
    if fb in BooleanAnswers.NONE:
        return
    formula=((fb['hypotenuse']**2)-(fb['height']**2))**0.5
    return formula

def solvefor_triangle_height():
    fields={
    'hypotenuse':{
        'type':'float',
        'default':1,
        },
    'base':{
        'type':'float',
        'default':1
        }
    }
    fb=FormBuilder(data=fields,passThruText="((fb['hypotnuse']**2)-(fb['base']**2))**0.5")
    if fb in BooleanAnswers.NONE:
        return
    formula=((fb['hypotenuse']**2)-(fb['base']**2))**0.5
    return formula

def soh_side_opposite_angle():
    fields={
    'hypotenuse':{
        'type':'float',
        'default':1,
        },
    'oppositeAngle':{
        'type':'float',
        'default':1
        }
    }
    fb=FormBuilder(data=fields,passThruText="[SOH]find Adj=sin(angle)*Opp the side opposite the angle")
    if fb in BooleanAnswers.NONE:
        return
    formula=math.sin(math.radians(fb['oppositeAngle']))*(fb['hypotenuse'])
    return formula

def cah_side_adjacent_angle():
    fields={
    'hypotenuse':{
        'type':'float',
        'default':1,
        },
    'adjacentAngle':{
        'type':'float',
        'default':1
        }
    }
    fb=FormBuilder(data=fields,passThruText="[CAH]find Opp=cos(angle)*hypotenuse the side adjacent the angle")
    if fb in BooleanAnswers.NONE:
        return
    formula=math.cos(math.radians(fb['adjacentAngle']))*(fb['hypotenuse'])
    return formula

def toa_side_oppOrAdj_when_you_have_opposite_or_adjacent():
    fields={
    'side_opposite_or_adjacent_to_angle':{
        'type':'float',
        'default':1,
        'help':'side opposite, or adjacent, of the side to find'
        },
    'opposite_or_adjacent_Angle':{
        'type':'float',
        'default':1,
        'help':'angle opposite, or adjacent, of the side to find'
        }
    }
    fb=FormBuilder(data=fields,passThruText="[TOA]find Opp=tan(angle)*Adj or Adj=tan(angle)*Opp")
    if fb in BooleanAnswers.NONE:
        return
    formula=math.tan(math.radians(fb['opposite_or_adjacent_Angle']))*(fb['side_opposite_or_adjacent_to_angle'])
    return formula

    ###

def asoh_side_opposite_angle():
    fields={
    'hypotenuse':{
        'type':'float',
        'default':1,
        'help':'hypotenuse'
        },
    'opposite of Angle to find':{
        'type':'float',
        'default':1,
        'help':'side opposite of the Angle to find'
        }
    }
    fb=FormBuilder(data=fields,passThruText="[aSOH]find math.degrees(math.asin(fb['opposite of Angle to find']/fb['hypotenuse']))")
    if fb in BooleanAnswers.NONE:
        return
    formula=math.degrees(math.asin(fb['opposite of Angle to find']/fb['hypotenuse']))
    return formula

def acah_side_adjacent_angle():
    fields={
    'hypotenuse':{
        'type':'float',
        'default':1,
        'help':'hypotenuse'
        },
    'adjacent of Angle to find':{
        'type':'float',
        'default':1,
        'help':'side adjacent of the Angle to find'
        }
    }
    fb=FormBuilder(data=fields,passThruText="[aCAH]find math.degrees(math.acos(fb['adjacent of Angle to find']/fb['hypotenuse']))")
    if fb in BooleanAnswers.NONE:
        return
    formula=math.degrees(math.acos(fb['adjacent of Angle to find']/fb['hypotenuse']))
    return formula

def atoa_side_oppOrAdj_when_you_have_opposite_or_adjacent():
    fields={
    'side adjacent of Angle to find':{
        'type':'float',
        'default':1,
        'help':'side adjacent of the Angle to find'
        },
    'side opposite of Angle to find':{
        'type':'float',
        'default':1,
        'help':'side opposite of the Angle to find'
        }
    }
    fb=FormBuilder(data=fields,passThruText="[aTOA]find math.degrees(math.acos(fb['side opposite of Angle to find']/fb['side adjacent of Angle to find']))")
    if fb in BooleanAnswers.NONE:
        return
    formula=math.degrees(math.atan(fb['side opposite of Angle to find']/fb['side adjacent of Angle to find']))
    return formula


def ohms_law_resistance():
    
    fields={
    'volts':{
        'type':'float',
        'default':1,
        'help':'voltage across the load',
        'ptext':"Voltage(V)"
        },
    'volts unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of voltage across the load',
        'ptext':"Voltage(V) Unit"
        },
    'amps':{
        'type':'float',
        'default':1,
        'help':'amperage through the load',
        'ptext':'Amperes(A)'
        },
    'amps unit':{
        'type':'string',
        'default':'amp',
        'help':'unit of amperage through the load',
        'ptext':'Amperes(A) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Ohms Law - Resistance")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['volts'],fb['volts unit'],"/")
    print(fb['amps'],fb['amps unit'])
    formula=QTY((Decimal(QTY(fb['volts'],fb['volts unit']).to('volts').magnitude)/Decimal(QTY(fb['amps'],fb['amps unit']).to('amp').magnitude)),'ohms')
    print("=",formula)
    return formula.magnitude

def ohms_law_current():
    
    fields={
    'volts':{
        'type':'float',
        'default':1,
        'help':'voltage across the load',
        'ptext':"Voltage(V)"
        },
    'volts unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of voltage across the load',
        'ptext':"Voltage(V) Unit"
        },
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(Ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(Ohm) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Ohms Law - Current")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['volts'],fb['volts unit'],"/")
    print(fb['ohm'],fb['ohm unit'])
    formula=QTY((Decimal(QTY(fb['volts'],fb['volts unit']).to('volts').magnitude)/Decimal(QTY(fb['ohm'],fb['ohm unit']).to('ohm').magnitude)),'amp')
    print("=",formula)
    return formula.magnitude

def ohms_law_voltage():
    
    fields={
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(Ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(Ohm) Unit'
        },
    'amps':{
        'type':'float',
        'default':1,
        'help':'amperage through the load',
        'ptext':'Amperes(A)'
        },
    'amps unit':{
        'type':'string',
        'default':'amp',
        'help':'unit of amperage through the load',
        'ptext':'Amperes(A) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Ohms Law - Voltage")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['ohm'],fb['ohm unit'],"*")
    print(fb['amps'],fb['amps unit'])
    formula=QTY((Decimal(QTY(fb['amps'],fb['amps unit']).to('amp').magnitude)*Decimal(QTY(fb['ohm'],fb['ohm unit']).to('ohm').magnitude)),'volts')
    print("=",formula)
    return formula.magnitude

def ohms_law_current():
    
    fields={
    'volts':{
        'type':'float',
        'default':1,
        'help':'voltage across the load',
        'ptext':"Voltage(V)"
        },
    'volts unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of voltage across the load',
        'ptext':"Voltage(V) Unit"
        },
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(Ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(Ohm) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Ohms Law - Current")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['volts'],fb['volts unit'],"/")
    print(fb['ohm'],fb['ohm unit'])
    formula=QTY((Decimal(QTY(fb['volts'],fb['volts unit']).to('volts').magnitude)/Decimal(QTY(fb['ohm'],fb['ohm unit']).to('ohm').magnitude)),'amp')
    print("=",formula)
    return formula.magnitude

def power_dissipation_watt():
    
    fields={
    'volts':{
        'type':'float',
        'default':1,
        'help':'voltage through the load',
        'ptext':'Voltage(Volt)'
        },
    'volts unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of voltage through the load',
        'ptext':'Voltage(Volt) Unit'
        },
    'amps':{
        'type':'float',
        'default':1,
        'help':'amperage through the load',
        'ptext':'Amperes(A)'
        },
    'amps unit':{
        'type':'string',
        'default':'amp',
        'help':'unit of amperage through the load',
        'ptext':'Amperes(A) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Power Dissipation - Watt")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['volts'],fb['volts unit'],"*")
    print(fb['amps'],fb['amps unit'])
    formula=QTY((Decimal(QTY(fb['amps'],fb['amps unit']).to('amp').magnitude)*Decimal(QTY(fb['volts'],fb['volts unit']).to('volt').magnitude)),'watt')
    print("=",formula)
    return formula.magnitude


def power_dissipation_volt():
    
    fields={
    'watts':{
        'type':'float',
        'default':1,
        'help':'wattage of the load',
        'ptext':'Power(Watt)'
        },
    'watts unit':{
        'type':'string',
        'default':'watt',
        'help':'unit of wattage of the load',
        'ptext':'Power(Watt) Unit'
        },
    'amps':{
        'type':'float',
        'default':1,
        'help':'amperage through the load',
        'ptext':'Amperes(A)'
        },
    'amps unit':{
        'type':'string',
        'default':'amp',
        'help':'unit of amperage through the load',
        'ptext':'Amperes(A) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Power Dissipation - Volt")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['watts'],fb['watts unit'],"*")
    print(fb['amps'],fb['amps unit'])
    formula=QTY((Decimal(QTY(fb['watts'],fb['watts unit']).to('watt').magnitude)/Decimal(QTY(fb['amps'],fb['amps unit']).to('amp').magnitude)),'volt')
    print("=",formula)
    return formula.magnitude

#turn to amp
def power_dissipation_amp():
    
    fields={
    'watts':{
        'type':'float',
        'default':1,
        'help':'wattage of the load',
        'ptext':'Power(Watt)'
        },
    'watts unit':{
        'type':'string',
        'default':'watt',
        'help':'unit of wattage of the load',
        'ptext':'Power(Watt) Unit'
        },
    'volts':{
        'type':'float',
        'default':1,
        'help':'voltage across the load',
        'ptext':'Voltage(Volts)'
        },
    'volts unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of voltage across the load',
        'ptext':'Voltage(Volts) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Power Dissipation - Watt")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['watts'],fb['watts unit'],"*")
    print(fb['volts'],fb['volts unit'])
    formula=QTY((Decimal(QTY(fb['watts'],fb['watts unit']).to('watt').magnitude)/Decimal(QTY(fb['volts'],fb['volts unit']).to('volt').magnitude)),'amp')
    print("=",formula)
    return formula.magnitude

def power_v2_over_r():
    
    fields={
    'volts':{
        'type':'float',
        'default':1,
        'help':'voltage across the load',
        'ptext':'Voltage(Volts)'
        },
    'volts unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of voltage across the load',
        'ptext':'Voltage(Volts) Unit'
        },
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(ohm) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Power Dissipation - Watt")
    if fb in BooleanAnswers.NONE:
        return
    resistance=QTY(Decimal(fb['ohm']),fb['ohm unit']).to('ohm')
    volt=QTY(fb['volts'],fb['volts unit']).to('volt')
    print(f"({volt} ** 2)",'/',resistance)
    volt=QTY(
        Decimal(
            volt.magnitude)
    ,'volt')
    formula=((volt**2)/resistance).to('watt')
    print("=",formula)
    return formula.magnitude

def amp_sqrt_power_over_r():
    
    fields={
    'power':{
        'type':'float',
        'default':1,
        'help':'Power dissipated in the load',
        'ptext':'Power(Watts)'
        },
    'power unit':{
        'type':'string',
        'default':'watt',
        'help':'unit of Power dissipated in the load',
        'ptext':'Power(Watts) Unit'
        },
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(ohm) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="I=Square_Root(P/R) || I=(P/2)**0.5")
    if fb in BooleanAnswers.NONE:
        return
    resistance=QTY(Decimal(fb['ohm']),fb['ohm unit']).to('ohm')
    power=QTY(fb['power'],fb['power unit']).to('watt')
    print(f"({power}/{resistance})**0.5")

    formula=QTY(
        Decimal(
            Decimal(power.magnitude)/Decimal(resistance.magnitude)
            )**Decimal(0.5)
        ,"amp"
    )
    print("=",formula)
    return formula.magnitude

def volt_sqrt_power_mult_resistance():
    
    fields={
    'power':{
        'type':'float',
        'default':1,
        'help':'Power dissipated in the load',
        'ptext':'Power(Watts)'
        },
    'power unit':{
        'type':'string',
        'default':'watt',
        'help':'unit of Power dissipated in the load',
        'ptext':'Power(Watts) Unit'
        },
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(ohm) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="V = SquareRoot(P*R) || V=(P*R)**0.5")
    if fb in BooleanAnswers.NONE:
        return
    resistance=QTY(Decimal(fb['ohm']),fb['ohm unit']).to('ohm')
    power=QTY(fb['power'],fb['power unit']).to('watt')
    print(f"({power}*{resistance})**0.5")

    formula=QTY(
        Decimal(
            Decimal(power.magnitude)*Decimal(resistance.magnitude)
            )**Decimal(0.5)
        ,"volt"
    )
    print("=",formula)
    return formula.magnitude

def ohm_power_over_i_squared():
    
    fields={
    'power':{
        'type':'float',
        'default':1,
        'help':'Power dissipated in the load',
        'ptext':'Power(Watts)'
        },
    'power unit':{
        'type':'string',
        'default':'watt',
        'help':'unit of Power dissipated in the load',
        'ptext':'Power(Watts) Unit'
        },
    'amp':{
        'type':'float',
        'default':1,
        'help':'Current through the load',
        'ptext':'Current(Amperes)'
        },
    'amp unit':{
        'type':'string',
        'default':'amp',
        'help':'unit of current through the load',
        'ptext':'Current(Amperes) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="R=P/(I**2)")
    if fb in BooleanAnswers.NONE:
        return
    current=QTY(Decimal(fb['amp']),fb['amp unit']).to('amp')
    power=QTY(fb['power'],fb['power unit']).to('watt')
    print(f"({power}/{current}**2)")

    formula=QTY(
        Decimal(power.magnitude)/Decimal(current.magnitude**2)
        ,'ohm')
    print("=",formula)
    return formula.magnitude

def ohm_v_squared_over_p():
    
    fields={
    'power':{
        'type':'float',
        'default':1,
        'help':'Power dissipated in the load',
        'ptext':'Power(Watts)'
        },
    'power unit':{
        'type':'string',
        'default':'watt',
        'help':'unit of Power dissipated in the load',
        'ptext':'Power(Watts) Unit'
        },
    'volt':{
        'type':'float',
        'default':1,
        'help':'Voltage across the load',
        'ptext':'Voltage(volts)'
        },
    'volt unit':{
        'type':'string',
        'default':'volt',
        'help':'unit of current through the load',
        'ptext':'Voltage(volts) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="R=(V**2)/P")
    if fb in BooleanAnswers.NONE:
        return
    voltage=QTY(Decimal(fb['volt']),fb['volt unit']).to('volt')
    power=QTY(fb['power'],fb['power unit']).to('watt')
    print(f"({voltage}**2)/({power})")

    formula=QTY(
        (Decimal(voltage.magnitude**2)/Decimal(power.magnitude))
        ,'ohm')
    print("=",formula)
    return formula.magnitude

def power_i2_times_r():
    
    fields={
    'current':{
        'type':'float',
        'default':1,
        'help':'current through the load',
        'ptext':'Current(Amperes)'
        },
    'current unit':{
        'type':'string',
        'default':'amp',
        'help':'unit of current through the load',
        'ptext':'Current(Amperes) Unit'
        },
    'ohm':{
        'type':'float',
        'default':1,
        'help':'resistance through the load',
        'ptext':'Resistance(ohm)'
        },
    'ohm unit':{
        'type':'string',
        'default':'ohm',
        'help':'unit of resistance through the load',
        'ptext':'Resistance(ohm) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="Power Dissipation - Watt")
    if fb in BooleanAnswers.NONE:
        return
    resistance=QTY(Decimal(fb['ohm']),fb['ohm unit']).to('ohm')
    amp=QTY(fb['current'],fb['current unit']).to('amp')
    print(f"({amp} ** 2)",'*',resistance)
    current=QTY(
        Decimal(
            amp.magnitude)
    ,'amp')
    formula=(resistance*(current**2)).to('watt')
    print("=",formula)
    return formula.magnitude

def cross_sectional_area_meters():
    
    fields={
    'radius':{
        'type':'float',
        'default':1,
        'help':'1/2 Diameter = Radius',
        'ptext':'Radius(meter)'
        },
    'radius unit':{
        'type':'string',
        'default':'meter',
        'help':'unit for radius',
        'ptext':'Radius(meter) Unit'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Cross Sectional Area - Meter ** 2")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['radius'],fb['radius unit'])
    formula=QTY(Decimal(math.pi)*(Decimal(QTY(fb['radius'],fb['radius unit']).to('meter').magnitude)**2),'meter ** 2')
    print("=",formula)
    return formula.magnitude

def resistance_csa_rstvty_lng():
    
    fields={
    'cross_sectional_area_meters':{
        'type':'float',
        'default':1,
        'help':'cross_sectional_area_meters of conductor',
        'ptext':'cross_sectional_area_meters(meter)'
        },
    'cross_sectional_area_meters unit':{
        'type':'string',
        'default':'meter ** 2',
        'help':'unit for cross_sectional_area_meters',
        'ptext':'cross_sectional_area_meters(meter) Unit'
        },
    'length':{
        'type':'float',
        'default':1,
        'help':'length of conductor',
        'ptext':'length(meter)'
        },
    'length unit':{
        'type':'string',
        'default':'meter',
        'help':'unit length',
        'ptext':'length(meter) Unit'
        },
    'resistivity':{
        'type':'float',
        'default':1,
        'help':'resistivity of conductor',
        'ptext':'resistivity(rho) (Ohm-meter)'
        },
    'resistivity unit':{
        'type':'string',
        'default':'ohm * meter',
        'help':'unit resistivity',
        'ptext':'resistivity(rho) (Ohm-meter) Unit'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Resistance rho*(l/csa)")
    if fb in BooleanAnswers.NONE:
        return
    print(fb['cross_sectional_area_meters'],fb['cross_sectional_area_meters unit'])
    print(fb['length'],fb['length unit'])
    print(fb['resistivity'],fb['resistivity unit'])
    formula=QTY(Decimal(QTY(fb['resistivity'],fb['resistivity unit']).to('ohm * meter').magnitude)*(
    Decimal(QTY(fb['length'],fb['length unit']).to('meter').magnitude)
        /
    Decimal(QTY(fb['cross_sectional_area_meters'],fb['cross_sectional_area_meters unit']).to('meter ** 2').magnitude)
        ),'ohm')
    print("=",formula)
    return formula.magnitude

def temperature_coefficient_of_resistivity():
    
    fields={
    'Resistivity at reference temperature':{
        'type':'float',
        'default':1.68e-8,
        'help':'Resistivity at reference temperature',
        'ptext':'Resistivity at reference temperature(ohm * meter)'
        },
    'Resistivity at reference temperature unit':{
        'type':'string',
        'default':'ohm * meter',
        'help':'unit for Resistivity at reference temperature',
        'ptext':'Resistivity at reference temperature Unit'
        },
    'Temperature coefficient of resistivity':{
        'type':'float',
        'default':0.00393,
        'help':'Temperature coefficient of resistivity of conductor',
        'ptext':'Temperature coefficient of resistivity(degC ** -1)'
        },
    'Temperature coefficient of resistivity unit':{
        'type':'string',
        'default':'degC ** -1',
        'help':'unit Temperature coefficient of resistivity',
        'ptext':'Temperature coefficient of resistivity(degC ** -1) Unit'
        },
    'Start Temperature':{
        'type':'float',
        'default':1,
        'help':'Start Temperature of conductor',
        'ptext':'Start Temperature(degC)'
        },
    'Start Temperature unit':{
        'type':'string',
        'default':'degC',
        'help':'unit Start Temperature',
        'ptext':'Start Temperature(degC) Unit'
        },
    'End Temperature':{
        'type':'float',
        'default':1,
        'help':'End Temperature of conductor',
        'ptext':'End Temperature(degC)'
        },
    'End Temperature unit':{
        'type':'string',
        'default':'degC',
        'help':'unit End Temperature',
        'ptext':'End Temperature(degC) Unit'
        },
    
    }
    fb=FormBuilder(data=fields,passThruText="temperature coefficient of resistivity")
    if fb in BooleanAnswers.NONE:
        return
    ratr=QTY(fb["Resistivity at reference temperature"],fb["Resistivity at reference temperature unit"])
    tcor=QTY(fb["Temperature coefficient of resistivity"],fb["Temperature coefficient of resistivity unit"])
    start_temp=QTY(fb['Start Temperature'],fb['Start Temperature unit'])
    end_temp=QTY(fb['End Temperature'],fb['End Temperature unit'])
    


    formula=QTY(Decimal(ratr.to('ohm * meter').magnitude)*(1+(Decimal(tcor.to('degC ** -1').magnitude)*(Decimal(end_temp.to('degC').magnitude)-Decimal(start_temp.to('degC').magnitude)))),'ohm * meter')
    print("=",formula)
    return formula.magnitude


def temperature_coefficient_of_resistivity_pre_temp_diff():
    
    fields={
    'Resistivity at reference temperature':{
        'type':'float',
        'default':1.68e-8,
        'help':'Resistivity at reference temperature',
        'ptext':'Resistivity at reference temperature(ohm * meter)'
        },
    'Resistivity at reference temperature unit':{
        'type':'string',
        'default':'ohm * meter',
        'help':'unit for Resistivity at reference temperature',
        'ptext':'Resistivity at reference temperature Unit'
        },
    'Temperature coefficient of resistivity':{
        'type':'float',
        'default':0.00393,
        'help':'Temperature coefficient of resistivity of conductor',
        'ptext':'Temperature coefficient of resistivity(degC ** -1)'
        },
    'Temperature coefficient of resistivity unit':{
        'type':'string',
        'default':'degC',
        'help':'unit Temperature coefficient of resistivity',
        'ptext':'Temperature coefficient of resistivity(degC ** -1) Unit'
        },
    'Temperature Change':{
        'type':'float',
        'default':1,
        'help':'Temperature Temperature Change for conductor',
        'ptext':'Temperature Temperature Change(degC)'
        },
    'Temperature Change unit':{
        'type':'string',
        'default':'degC',
        'help':'unit Temperature Change',
        'ptext':'Temperature(degC) Change Unit'
        },   
    }
    fb=FormBuilder(data=fields,passThruText="temperature coefficient of resistivity")
    if fb in BooleanAnswers.NONE:
        return
    ratr=QTY(fb["Resistivity at reference temperature"],fb["Resistivity at reference temperature unit"])
    tcor=QTY(fb["Temperature coefficient of resistivity"],fb["Temperature coefficient of resistivity unit"])
    temp_change=QTY(fb['Temperature Change'],fb['Temperature Change unit'])
    


    formula=QTY(Decimal(ratr.to('ohm * meter').magnitude)*(1+(Decimal(tcor.to('degC').magnitude)*Decimal(temp_change.to('degC').magnitude))),'ohm * meter') 
    print("=",formula)
    return formula.magnitude


def capacitance_charge_voltage():
    
    fields={
        'charge':{
            'type':'float',
            'default':1,
            'help':'unit of charge in coulomb',
            'ptext':'Charge in Coulomb'
        },
        'charge unit':{
            'type':'string',
            'default':'coulomb',
            'help':'unit of charge in coulomb',
            'ptext':'Charge in Coulomb'
        },
        'volts':{
        'type':'float',
        'default':1,
        'help':'voltage across the load',
        'ptext':'Voltage(Volts)'
        },
        'volts unit':{
            'type':'string',
            'default':'volt',
            'help':'unit of voltage across the load',
            'ptext':'Voltage(Volts) Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="capacitance=Charge_Q/Voltage")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    charge=QTY(fb["charge"],fb["charge unit"])
    voltage=QTY(fb["volts"],fb["volts unit"])
    capacitance=QTY(Decimal(charge.to('coulomb').magnitude)/Decimal(voltage.to('volt').magnitude),"farad")

    formula=capacitance
    print("=",formula)
    return formula.magnitude


def total_energy_dissipated_over_time():
    
    fields={
        'power':{
            'type':'float',
            'default':1,
            'help':'power in watts',
            'ptext':'Power(Watt)'
        },
        'power unit':{
            'type':'string',
            'default':'watt',
            'help':'unit of charge in coulomb',
            'ptext':'Power(Watt) Unit'
        },
        'time':{
        'type':'timedelta',
        'default':1,
        'help':'time energy is dissipated across',
        'ptext':'time in seconds'
        },
        'time unit':{
            'type':'string',
            'default':'second',
            'help':'time of Dissipation unit',
            'ptext':'Time Unit'
        },
        'output':{
            'type':'string',
            'default':'kilowatt * hour',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="total energy dissipated over time = watts * time")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    power=QTY(fb["power"],fb["power unit"])
    time_of_dissipation=QTY(fb["time"].total_seconds(),fb["time unit"])
    energy_dissipated_over_time_v=QTY(decc(((power.to('watt')*time_of_dissipation.to('seconds'))).to(fb['output']).magnitude,cf=6),fb['output'])

    formula=energy_dissipated_over_time_v
    print("=",formula)
    return formula.magnitude


def inductive_reactance():
    
    fields={
        'f = Frequency of the AC signal in Hertz (Hz)':{
            'type':'float',
            'default':1,
            'help':'Frequency of the AC signal',
            'ptext':'Frequency(Hertz)'
        },
        'f = Frequency of the AC signal in Hertz (Hz) unit':{
            'type':'string',
            'default':'hertz',
            'help':'unit of Frequency of the AC signal',
            'ptext':'Frequency Unit'
        },
        'L = Inductance of the coil in Henrys (H)':{
            'type':'float',
            'default':1,
            'help':'Inductance of the coil',
            'ptext':'Inductance(Henry)'
        },
        'L = Inductance of the coil in Henrys (H) unit':{
            'type':'string',
            'default':'henry',
            'help':'unit of Inductance of the coil',
            'ptext':'Inductance Unit'
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="inductive reactance")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    freq=QTY(Decimal(fb['f = Frequency of the AC signal in Hertz (Hz)']),fb['f = Frequency of the AC signal in Hertz (Hz) unit'])
    inductance=QTY(Decimal(fb['L = Inductance of the coil in Henrys (H)']),fb['L = Inductance of the coil in Henrys (H) unit'])
    ohms=((2*Decimal(math.pi))*freq.to('hertz')*inductance.to('henry')).to('ohm')

    formula=ohms
    print("=",formula)
    return formula.magnitude

def capacitive_reactance():
    
    fields={
        'f = Frequency of the AC signal in Hertz (Hz)':{
            'type':'float',
            'default':1,
            'help':'Frequency of the AC signal',
            'ptext':'Frequency(Hertz)'
        },
        'f = Frequency of the AC signal in Hertz (Hz) unit':{
            'type':'string',
            'default':'hertz',
            'help':'unit of Frequency of the AC signal',
            'ptext':'Frequency Unit'
        },
        'C: Capacitance in farads (F).':{
            'type':'float',
            'default':1,
            'help':'Capacitance',
            'ptext':'Capacitance(farad)'
        },
        'C: Capacitance in farads (F). unit':{
            'type':'string',
            'default':'farad',
            'help':'unit of capacitance',
            'ptext':'Capacitance Unit'
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="capacitive reactance")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    freq=QTY(Decimal(fb['f = Frequency of the AC signal in Hertz (Hz)']),fb['f = Frequency of the AC signal in Hertz (Hz) unit'])
    capacitance=QTY(Decimal(fb['C: Capacitance in farads (F).']),fb['C: Capacitance in farads (F). unit'])
    ohms=QTY(
        1/
        (2*(Decimal(math.pi))
        *Decimal(freq.to('hertz').magnitude)
        *Decimal(capacitance.to('farad').magnitude))
        ,'ohm')

    formula=ohms
    print("=",formula)
    return formula.magnitude

def impedance_rlc():
    
    fields={
        'capacitive_reactance':{
            'type':'float',
            'default':1,
            'help':'capacitive_reactance',
            'ptext':'capacitive_reactance(ohm)'
        },
        'capacitive_reactance unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of capacitive_reactance',
            'ptext':'capacitive_reactance Unit'
        },
        'inductive_reactance':{
            'type':'float',
            'default':1,
            'help':'inductive_reactance',
            'ptext':'inductive_reactance(ohm)'
        },
        'inductive_reactance unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of inductive_reactance',
            'ptext':'inductive_reactance Unit'
        },
        'ohm':{
            'type':'float',
            'default':1,
            'help':'resistance through the load',
            'ptext':'Resistance(ohm)'
        },
        'ohm unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of resistance through the load',
            'ptext':'Resistance(ohm) Unit'
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="impedance of rlc circuit")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    creact=QTY(Decimal(fb['capacitive_reactance']),fb['capacitive_reactance unit'])
    lreact=QTY(Decimal(fb['inductive_reactance']),fb['inductive_reactance unit'])
    resist=QTY(Decimal(fb['ohm']),fb['ohm unit'])
    ohms=QTY(
        (
            ((resist**2)+((lreact-creact)**2))**Decimal(0.5)

        )
        ,'ohm')

    formula=ohms
    print("=",formula)
    return formula.magnitude

def impedance_rc():
    
    fields={
        'capacitive_reactance':{
            'type':'float',
            'default':1,
            'help':'capacitive_reactance',
            'ptext':'capacitive_reactance(ohm)'
        },
        'capacitive_reactance unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of capacitive_reactance',
            'ptext':'capacitive_reactance Unit'
        },
        'ohm':{
            'type':'float',
            'default':1,
            'help':'resistance through the load',
            'ptext':'Resistance(ohm)'
        },
        'ohm unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of resistance through the load',
            'ptext':'Resistance(ohm) Unit'
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="impedance of rc circuit")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    creact=QTY(Decimal(fb['capacitive_reactance']),fb['capacitive_reactance unit'])
    resist=QTY(Decimal(fb['ohm']),fb['ohm unit'])
    ohms=QTY(
        (
            ((resist**2)+(creact**2))**Decimal(0.5)

        )
        ,'ohm')

    formula=ohms
    print("=",formula)
    return formula.magnitude


def impedance_rl():
    
    fields={
        'inductive_reactance':{
            'type':'float',
            'default':1,
            'help':'inductive_reactance',
            'ptext':'inductive_reactance(ohm)'
        },
        'inductive_reactance unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of inductive_reactance',
            'ptext':'inductive_reactance Unit'
        },
        'ohm':{
            'type':'float',
            'default':1,
            'help':'resistance through the load',
            'ptext':'Resistance(ohm)'
        },
        'ohm unit':{
            'type':'string',
            'default':'ohm',
            'help':'unit of resistance through the load',
            'ptext':'Resistance(ohm) Unit'
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="impedance of rl circuit")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    lreact=QTY(Decimal(fb['inductive_reactance']),fb['inductive_reactance unit'])
    resist=QTY(Decimal(fb['ohm']),fb['ohm unit'])
    ohms=QTY(
        (
            ((resist**2)+(lreact**2))**Decimal(0.5)

        )
        ,'ohm')

    formula=ohms
    print("=",formula)
    return formula.magnitude

def single_phase_DC_voltage_drop():
    
    fields={
        'L: The one-way length of the wire run in feet (ft).':{
            'type':'float',
            'default':1,
            'help':'The one-way length of the wire run feet',
            'ptext':'The one-way length of the wire run(ohm)'
        },
        'L: The one-way length of the wire run in feet (ft). unit':{
            'type':'string',
            'default':'feet',
            'help':'unit of The one-way length of the wire run',
            'ptext':'L: The one-way length of the wire run in feet (ft). unit'
        },
        'I: The load current in amperes (A).':{
            'type':'float',
            'default':1,
            'help':'I: The load current in amperes (A).',
            'ptext':'load current in amperes (A).'
        },
        'I: The load current in amperes (A). unit':{
            'type':'string',
            'default':'amp',
            'help':'unit of I: The load current in amperes (A).',
            'ptext':'I: The load current in amperes (A). Unit'
        },
        "R: The conductor's resistance in ohms per 1,000 feet":{
            'type':'float',
            'default':1,
            'help':"R: The conductor's resistance in ohms per 1,000 feet",
            'ptext':"R: The conductor's resistance in ohms per 1,000 feet"
        },
        "R: The conductor's resistance in ohms per 1,000 feet unit":{
            'type':'string',
            'default':'ohm',
            'help':"R: The conductor's resistance in ohms per 1,000 feet",
            'ptext':"R: The conductor's resistance in ohms per 1,000 feet Unit"
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="1-Phase or DC Voltage Drop")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    length=QTY(Decimal(fb['L: The one-way length of the wire run in feet (ft).']),fb['L: The one-way length of the wire run in feet (ft). unit'])
    current=QTY(Decimal(fb['I: The load current in amperes (A).']),fb['I: The load current in amperes (A). unit'])
    resistance=QTY(Decimal(fb["R: The conductor's resistance in ohms per 1,000 feet"]),fb["R: The conductor's resistance in ohms per 1,000 feet unit"])
    vdrop=QTY(((2*length.to('feet')*current.to('amp')*resistance.to('ohm'))/1000).magnitude,"volt")
    formula=vdrop
    print("=",formula)
    return formula.magnitude

def three_phase_voltage_drop():
    
    fields={
        'L: The one-way length of the wire run in feet (ft).':{
            'type':'float',
            'default':1,
            'help':'The one-way length of the wire run feet',
            'ptext':'The one-way length of the wire run(ohm)'
        },
        'L: The one-way length of the wire run in feet (ft). unit':{
            'type':'string',
            'default':'feet',
            'help':'unit of The one-way length of the wire run',
            'ptext':'L: The one-way length of the wire run in feet (ft). unit'
        },
        'I: The load current in amperes (A).':{
            'type':'float',
            'default':1,
            'help':'I: The load current in amperes (A).',
            'ptext':'load current in amperes (A).'
        },
        'I: The load current in amperes (A). unit':{
            'type':'string',
            'default':'amp',
            'help':'unit of I: The load current in amperes (A).',
            'ptext':'I: The load current in amperes (A). Unit'
        },
        "R: The conductor's resistance in ohms per 1,000 feet":{
            'type':'float',
            'default':1,
            'help':"R: The conductor's resistance in ohms per 1,000 feet",
            'ptext':"R: The conductor's resistance in ohms per 1,000 feet"
        },
        "R: The conductor's resistance in ohms per 1,000 feet unit":{
            'type':'string',
            'default':'ohm',
            'help':"R: The conductor's resistance in ohms per 1,000 feet",
            'ptext':"R: The conductor's resistance in ohms per 1,000 feet Unit"
        },
        'output':{
            'type':'string',
            'default':'ohm',
            'help':'output unit',
            'ptext':'Output Unit'
        }
    }
    fb=FormBuilder(data=fields,passThruText="3-Phase Voltage Drop")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    length=QTY(Decimal(fb['L: The one-way length of the wire run in feet (ft).']),fb['L: The one-way length of the wire run in feet (ft). unit'])
    current=QTY(Decimal(fb['I: The load current in amperes (A).']),fb['I: The load current in amperes (A). unit'])
    resistance=QTY(Decimal(fb["R: The conductor's resistance in ohms per 1,000 feet"]),fb["R: The conductor's resistance in ohms per 1,000 feet unit"])
    vdrop=QTY(((Decimal(3**0.5)*length.to('feet')*current.to('amp')*resistance.to('ohm'))/1000).magnitude,"volt")
    formula=vdrop
    print("=",formula)
    return formula.magnitude

def jobAppliedTo_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        ttlCarb=[]
        

        carbs=QTY(0,"grams")
        fat=QTY(0,"grams")
        cholesterol=QTY(0,"grams")
        sodium=QTY(0,"mg")
        ttlSodiumConsumed=QTY(0,"mg")
        ss=QTY(0,"grams")
        ttlsugars=QTY(0,"grams")
        ttladdsugars=QTY(0,"grams")
        protien=QTY(0,"grams")
        cal=QTY(0,"kilocalorie")

        ttlCarbConsumed=QTY(0,"grams")
        ttlFatConsumed=QTY(0,"grams")
        ttlCholesterolConsumed=QTY(0,"mg")
        ttlSodiumConsumed=QTY(0,"mg")
        ttlDietaryFiberConsumed=QTY(0,"grams")
        ttlTTLSugarsConsumed=QTY(0,"grams")
        ttlTTLAddedSugarsConsumed=QTY(0,"grams")
        ttlProtienConsumed=QTY(0,"grams")
        ttlCalConsumed=QTY(0,"kilocalorie")

        for xnum,i in enumerate(data):
            msg=f'''
{Fore.light_green}Company={Fore.light_magenta}'{Fore.orange_red_1}{i.Company}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}Location={Fore.light_magenta}'{Fore.orange_red_1}{i.Location}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}Address={Fore.light_magenta}'{Fore.orange_red_1}{i.Address}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}Title={Fore.light_magenta}'{Fore.orange_red_1}{i.Title}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}InPerson={Fore.light_magenta}'{Fore.orange_red_1}{i.InPerson}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}WebApplication={Fore.light_magenta}'{Fore.orange_red_1}{i.WebApplication}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}WebApplicationAddress={Fore.light_magenta}'{Fore.orange_red_1}{i.WebApplicationAddress}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}Interview={Fore.light_magenta}'{Fore.orange_red_1}{i.Interview}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}InterviewWith={Fore.light_magenta}'{Fore.orange_red_1}{i.InterviewWith}{Fore.light_magenta}'{Style.reset}
{Fore.light_green}InterviewDTOE={Fore.light_magenta}'{Fore.orange_red_1}{i.InterviewDTOE}{Fore.light_magenta}'{Style.reset}
            '''
            msg=std_colorize(msg,xnum,ct)
            xtext.append(msg.replace("\n"," | "))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def jobAppliedTo_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_jobAppliedTo(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=jobAppliedTo_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def jobAppliedTo_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
jobAppliedTo_menu={
    str(uuid1()):{
    "cmds":['jobAppliedTo custom',],
    "exec":lambda self:s2cb_jobAppliedTo(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def jobAppliedToLogger(Model=JobAppliedTo,short_view=jobAppliedTo_short_view,menu=jobAppliedTo_menu):
    return ModelLogger(Model=JobAppliedTo,short_view=jobAppliedTo_short_view,menu=jobAppliedTo_menu)


def generate_item_name_sku():
    
    while True:
        try:
            fields={
                'name':{
                    'type':'string',
                    'default':detectGetOrSet("gen item name","Item",setValue=False,literal=True),
                    'help':'name of item to be sold',
                    'ptext':'Product Name'
                },
                'price':{
                    'type':'float',
                    'default':detectGetOrSet("gen item price",1,setValue=False,literal=False),
                    'help':'price of the item',
                    'ptext':'Price of Item'
                },
                'taxRate':{
                    'type':'float',
                    'default':detectGetOrSet("gen item taxRate",63/100,setValue=False,literal=False),
                    'help':'tax rate for item',
                    'ptext':'Tax Rate'
                },
                'crv':{
                    'type':'float',
                    'default':detectGetOrSet("gen item crv",0,setValue=False,literal=False),
                    'help':'CRV Total PKG Sold',
                    'ptext':'CRV For Qty Sold'
                },
                'sku':{
                    'type':'string',
                    'default':nanoid.generate(alphabet='1234567890',size=8),
                    'help':'reference code to item label',
                    'ptext':'Product Reference/SKU'
                },
                'gps-coordinates':{
                    'type':'string',
                    'default':detectGetOrSet("gen item gps","",setValue=False,literal=True),
                    'help':'Location Item was Named',
                    'ptext':'GPS Coorinates'
                },
                'chunkS':{
                    'type':'integer',
                    'default':detectGetOrSet("gen item chunkS",4,setValue=False,literal=False),
                    'help':'length of chunks of code',
                    'ptext':'Chunk Size'
                },
                'delim':{
                    'type':'string',
                    'default':detectGetOrSet("gen item delim","-",setValue=False,literal=False),
                    'help':'what to put between the chunks for quick viewing',
                    'ptext':'Deiminator'
                },
                'caseid':{
                    'type':'string',
                    'default':detectGetOrSet("gen item caseid","",setValue=False,literal=True),
                    'help':'Where the item was stored pre-transaction',
                    'ptext':'Case ID'
                },
            }
            fb=FormBuilder(data=fields,passThruText="Generate A New Name With SKU and GPS Location")
            if fb in BooleanAnswers.NONE:
                return
            #chunkS=fb['chunkS']
            
            
            gps=detectGetOrSet('gen item gps',fb['gps-coordinates'],setValue=False,literal=True)
            if gps != fb['gps-coordinates']:
                gps=detectGetOrSet('gen item gps',fb['gps-coordinates'],setValue=True,literal=True)
                #gps=fb['gps-coordinates']
            
            name=detectGetOrSet('gen item name',fb['name'],setValue=False,literal=True)
            if name != fb['name']:
                name=detectGetOrSet('gen item name',fb['name'],setValue=True,literal=True)
                #gps=fb['gps-coordinates']

            caseid=detectGetOrSet('gen item caseid',fb['caseid'],setValue=False,literal=True)
            if caseid != fb['name']:
                caseid=detectGetOrSet('gen item caseid',fb['caseid'],setValue=True,literal=True)
                #gps=fb['gps-coordinates']

            chunkS=detectGetOrSet('gen item chunkS',fb['chunkS'],setValue=False,literal=False)
            if chunkS != fb['name']:
                chunkS=detectGetOrSet('gen item chunkS',fb['chunkS'],setValue=True,literal=False)
                #gps=fb['gps-coordinates']

            price=detectGetOrSet('gen item price',fb['price'],setValue=False,literal=False)
            if price != fb['name']:
                price=detectGetOrSet('gen item price',fb['price'],setValue=True,literal=False)
                #gps=fb['gps-coordinates']
            price=decc(price)

            crv=detectGetOrSet('gen item crv',fb['crv'],setValue=False,literal=False)
            if crv != fb['name']:
                crv=detectGetOrSet('gen item crv',fb['crv'],setValue=True,literal=False)
                #gps=fb['gps-coordinates']
            crv=decc(crv)

            taxRate=detectGetOrSet('gen item taxRate',fb['taxRate'],setValue=False,literal=False)
            if taxRate != fb['name']:
                taxRate=detectGetOrSet('gen item taxRate',fb['taxRate'],setValue=True,literal=False)
                #gps=fb['gps-coordinates']
            taxRate=decc(taxRate)

            tax=(price+crv)*taxRate
            TTL=price+tax+crv

            delim=detectGetOrSet('gen item delim',fb['delim'],setValue=False,literal=True)
            if delim != fb['delim']:
                delim=detectGetOrSet('gen item delim',fb['delim'],setValue=True,literal=True)
                #gps=fb['gps-coordinates']

            code=f'{delim}'.join([fb['sku'][i:i+chunkS] for i in range(0,len(fb['sku']),chunkS)])
            now=datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            msg=f"""Name:'{fb['name']}' 
Ref/SKU:'{fb['sku']}' ( {code} ) 
DTOC:'{now}' 
SKU w/ TStamp:'{code} {now}'
Price: '{price}'
 CRV:{crv:.2f}
 Tax:'{tax:.2f}' 
 TaxRate Decimal:'{taxRate:.10f}' 
 TaxRate Percent:'{taxRate*100:.3f}'
 
Per Item TTL:'{TTL:.3f}'
CaseID:'{caseid}'
GPS:'{gps}'"""
            return msg
        except Exception as e:
            print(e,"retrying")

def change_from_cash():
    
    fields={
        'Price Total':{'type':'float',
            'default':1,
            'help':"Total Price For Product",
            'ptext':"Total Price For Product"
        },
        'Cash Given By Customer':{
            'type':'float',
            'default':1,
            'help':'Cash Given By Customer',
            'ptext':'Cash Given By Customer'
        },
        'resolution':{
            'type':'integer',
            'default':3,
            'help':'Number of Digits behind decimal',
            'ptext':'Number of Digits'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Calculate Change to Give Customer From (Price - Cash Given)")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    z=f".{fb['resolution']}f"
    formula=f"{decc(fb['Price Total'])-decc(fb['Cash Given By Customer']):z}"
    x=f"{Fore.light_green}{formula}"
    act=''
    if float(formula) < 0:
        act=f"{Fore.light_red}Give '{abs(float(formula))}'{Fore.light_blue} to Customer.{Style.reset}"
    elif float(formula) > 0:
        act=f"{Fore.light_cyan}'{abs(float(formula))}'{Fore.light_blue} Is Needed from the Customer.{Style.reset}"
    print(f"Price({Fore.light_yellow}{decc(fb['Price Total']):z}) - CashFromCustomer({Fore.light_magenta}{decc(fb['Cash Given By Customer']):z}){Fore.orange_red_1}","=",formula,act,f"{Style.reset}")
    return formula

def CashierQuizlet():
    qs={}
    l=Control(ptext="How many questions?",helpText="an integer",data="integer")
    if l in BooleanAnswers.NONE:
        return
    l=abs(l)
    wrong=0
    for num in range(0,l):
        price=Decimal(random.randint(0,250))+Decimal(f"{random.random():.2}")
        cash=Decimal(random.randint(0,250))+Decimal(f"{random.random():.2}")
        taxRate=Decimal(f"{random.random():.2f}")
        change=price-cash
        if change < 0:
            state="give"
        elif change > 0:
            state="take"

        qs[str(num)]={
            'price':price,
            'cash from customer':cash,
            'change':change,
            'give or take':state,
            'taxRate':taxRate,
                }
        x=qs[str(num)]
        #print(f" Q#{num}) Price( {x['price']} ) - FromCustomer( {x['cash from customer']} ) = Change( {x['change']} )")
    lock_before_procede=detectGetOrSet("cashq lock before procede",nanoid.generate(alphabet=string.ascii_letters+string.digits+"/-.",size=10),setValue=False,literal=True)
    
    for i in qs:
        while True:
            x=qs[i]
            answer=Control(ptext=f" Q#{i}) Price( {x['price']:.2f} ) + ( Price( {x['price']:.2f} ) * TaxRate( {x['taxRate']:.2f} )) = Answer( ________ ) : ",helpText="type you answer",data="string")
            if answer in BooleanAnswers.NONE:
                return
            try:
                answer=Decimal(f"{Decimal(answer):.2f}")
                if str(answer) == f"{x['price']+(qs[i]['taxRate']*x['price']):.2f}":
                    print('correct')
                else:
                    wrong+=(1/3)
                print(f"The Answer is: {x['price']+(qs[i]['taxRate']*x['price']):.2f}")
            except Exception as e:
                print(e)

            answer=Control(ptext=f" Q#{i}) Price( {x['price']} ) - FromCustomer( {x['cash from customer']} ) = Answer( ________ ) : ",helpText="type you answer",data="string")
            if answer in BooleanAnswers.NONE:
                return
            try:
                answer=Decimal(f"{Decimal(answer):.2f}")
                if str(answer) == str(qs[i]['change']):
                    print('correct')
                else:
                    wrong+=(1/3)
                print(f"The Answer is: {qs[i]['change']}")

                which=''
                while which == '':
                    answer=Control(ptext=f"'[g]ive' change or '[t]ake' more from customer?",helpText="[g]ive or [t]ake",data="string")
                    if answer in BooleanAnswers.NONE:
                        return
                    answer=answer.lower()
                    if answer in ['give','g']:
                        which="give"
                        break
                    elif answer in ['take','t']:
                        which="take"
                        break
                    else:
                        continue
                
                if x['give or take'] != which:
                    wrong+=(1/3)
                print(f"You gave: {which}, the answer is: {x['give or take']}")

                unlock=Control(ptext=f"'enter the admin unlock code to continue?",helpText="enter the unlock code",data="string")
                if unlock in BooleanAnswers.NONE:
                    return

                if unlock != lock_before_procede:
                    continue
                break
            except Exception as e:
                print(e)

    print(f"your grade is {Decimal(((l-wrong)/l)*100):.2f}%")



formulaZZZ="""
import math, random
fmla_diameter=random.randint(1,100)
fmla_radius_hide=fmla_diameter/2
circumference_fmla=f"(fmla_radius_hide*2)*{math.pi:.2f}"
answer_fmla=2*math.pi*fmla_radius_hide
"""
def generate_formula_from_template(template=formulaZZZ,qnum=0,tqoof=0):
    qnum+=1
    lcl={}
    formula=template
    exec(formula,lcl)
    #question with answer
    notes=[
    '* use python code as normal, including imports',
    '* include fmla_ or _fmla in variable name to include natext',
    '* include "hide" in variable name to replace with boiler plate text to hide its value in natext',
    '* use "answer", "answr", "result", "rslt", or "fnl" to store final answer which will be exclude in natext',
    "* the strings in ['_hide_','_hide','hide_','fmla_','_fmla']  will be excluded in the final output",
    '**** Grading is as follows',
    f'** answers_correct / total_answers for {sys._getframe().f_code.co_name}({qnum}) = decimal grade for question, i.e. answers_correct/total_answers=DGFQ',
    f'** DGFQ\'s are decimals less than, or equal to, 1',
    '** once all questions are answered, sum all of the DGFQ\'s. this will be sDGFQ',
    f'** sDGFQ\'s will also be a a decimal that will be equal to less than, or equal to,  TQOOF [{tqoof}] (Total Questions Outside Of Function)',
    f'** divide sDGFQ by the total the number of questions outside of {sys._getframe().f_code.co_name}(qnum={qnum})[TQOOF({tqoof})] where "qnum" is "question number x" of however many questions total outside of the {sys._getframe().f_code.co_name}(qnum={qnum})[TQOOF({tqoof})]. this will be GradeStage1',
    '** multiply GradeStage1  by 100 for Test/Quiz Grade, or TQG'
            ]

    notes='\n'.join(notes)
    qatext=('\n'.join([f"Answers {qnum}.) | {i} = "+str(lcl[i]) for i in lcl.keys() if '_fmla' in i.lower() or 'fmla_' in i.lower()]))
    #print('\n'.join([i for i in lcl.keys() if '_fmla' in i.lower() or 'fmla_' in i.lower()]))
    #question without answer
    for i in lcl:
        if 'hide' in i:
            lcl[i]=f"??? Required_Solution:ID='"+nanoid.generate(alphabet=string.ascii_letters+string.digits+"-./",size=3)+"'??? _______________________"
    answer=[ 'answer','answr','result','rslt','fnl']
    for i in lcl:
        for ii in answer:
            if ii.lower() in i:
                lcl[i]=f"??? Answer:ID='"+nanoid.generate(alphabet=string.ascii_letters+string.digits+"-./",size=3)+"'??? _______________________"

    natext=[f"Question {qnum}.) | {i} = "+str(lcl[i]) for i in lcl.keys() if ('_fmla' in i.lower() or 'fmla_' in i.lower()) and i.lower() not in answer]
    for i in ['_hide_','_hide','hide_','fmla_','_fmla','fmla','hide']:
        for numx,ii in enumerate(natext):
            natext[numx]=natext[numx].replace(i,'')
    natext='\n'.join(natext)

    for i in ['_hide_','_hide','hide_','fmla_','_fmla','fmla','hide']:
        qatext=qatext.replace(i,'')
    ttl_answer=len(natext.split(':ID='))-1
    new={}
    delete_keys=[]
    for i in lcl.keys():
        for ii in ['_hide','hide_','_hide_','fmla_','_fmla','_fmla_','fmla','hide']:
            if ii in i:
                new[i.replace(ii,'')]=deepcopy(lcl[i])
                delete_keys.append(i)

    for i in new:
        lcl[i]=new[i]
    for i in delete_keys:
        if i in lcl:
            lcl.pop(i) 


    qatext+=f"\nID\'s To Review:\n{'_'*os.get_terminal_size().columns}\nQuestion Grade for {qnum}/{tqoof}.) Correct ( total_correct for {qnum}.) (____) / total_answers({ttl_answer}) =  _______))\n"

    natext+=f"\nID\'s To Review:\n{'_'*os.get_terminal_size().columns}\nQuestion Grade for {qnum}/{tqoof}.) Correct ( total_correct for {qnum}.) (____) / total_answers({ttl_answer}) =  _______))\n"

    #print(natext)
    PRACTICE=namedtuple("Practice",["question_num","formula","data","question_answer","just_question","notes"])
    return PRACTICE(question_num=qnum,formula=formula,data=lcl,question_answer=qatext,just_question=natext,notes=notes)


#print(generate_formula_from_template(template=formula).notes)



def CashierQuizletAuto():
    qs={}
    l=Control(ptext="How many loops of questions?",helpText="an integer",data="integer")
    if l in BooleanAnswers.NONE:
        return
    if l == ['d',]:
        l=1
    l=abs(l)
    wrong=0
    for num in range(0,l):
        price=Decimal(random.randint(0,250))+Decimal(f"{random.random():.2}")
        cash=Decimal(random.randint(0,250))+Decimal(f"{random.random():.2}")
        taxRate=Decimal(f"{random.random():.2f}")
        produceLb=Decimal(f"{random.random():.2f}")
        change=price-cash
        if change < 0:
            state="give"
        elif change > 0:
            state="take"

        qs[str(num)]={
            'price':price,
            'cash from customer':cash,
            'change':change,
            'give or take':state,
            'taxRate':taxRate,
            'produceLb':produceLb
                }
        x=qs[str(num)]
        #print(f" Q#{num}) Price( {x['price']} ) - FromCustomer( {x['cash from customer']} ) = Change( {x['change']} )")
    qsa=[]
    As=[]
    
    qcount=0
    for i in qs:
        while True:
            x=qs[i]
            use=random.choice([True,False])
            if use:
                qcount+=1
                q=f"{qcount}.) Answer_Is_Correct( Y / N ) | Price( {x['price']:.2f} ) + ( Price( {x['price']:.2f} ) * TaxRate( {x['taxRate']:.2f} )) = Answer( ________ ) : \n"
                a=f"{qcount}.) Answer_Is_Correct( Y / N ) | Price( {x['price']:.2f} ) + ( Price( {x['price']:.2f} ) * TaxRate( {x['taxRate']:.2f} )) = Answer( {x['price']+(qs[i]['taxRate']*x['price']):.2f} ) : \n"
                qsa.append(q)
                As.append(a)


            use=random.choice([True,False])
            if use:
                qcount+=1
                q=f"{qcount}.) Answer_Is_Correct( Y / N ) | Price( {x['price']} ) - FromCustomer( {x['cash from customer']} ) = Answer( ________ ) : \n"
                a=f"{qcount}.) Answer_Is_Correct( Y / N ) | Price( {x['price']} ) - FromCustomer( {x['cash from customer']} ) = Answer( {str(qs[i]['change'] )} : \n"
                qsa.append(q)
                As.append(a)

                use=random.choice([True,False])
                if use:
                    qcount+=1
                    q=f"{qcount}.) Answer_Is_Correct( Y / N ) | Using the previous question, do you '[g]ive' change or do you '[t]ake' more from the customer?\n"
                    a=f"{qcount}.) Answer_Is_Correct( Y / N ) | Using the previous question, do you '[g]ive' change or do you '[t]ake' more from the customer? Answer( {x['give or take']} )\n"
                    qsa.append(q)
                    As.append(a)

            use=random.choice([True,False])
            if use:
                qcount+=1
                q=f"{qcount}.) Answer_Is_Correct( Y / N ) | You go to the store and go to the section where items are priced by the pound and select an item whose price is '{x['price']:.2f} per pound'. You plan to purchase {x['produceLb']} lbs of the item. What total price are you expecting to see at the register, given tax on the item is {x['taxRate']*100}% ?\n"
                a=f"{qcount}.) Answer_Is_Correct( Y / N ) | You go to the store and go to the section where items are priced by the pound and select an item whose price is '{x['price']:.2f} per pound'. You plan to purchase {x['produceLb']} lbs of the item. What total price are you expecting to see at the register, given tax on the item is {x['taxRate']*100}% ? Answer( {(x['price']*x['produceLb'])+((x['price']*x['produceLb'])*x['taxRate']):.2f} )\n"
                qsa.append(q)
                As.append(a)

            if len(qsa) > 0:
                break

        l=Control(ptext="How many questions to pull from the QuestionPool for this section?",helpText="an integer",data="integer")
        if l in BooleanAnswers.NONE:
            return
        if l in ['d',]:
            l=1
        l=abs(l)
        tsp=[]
        qsp=[]
        cta=0
        with Session(ENGINE) as session:
            count_statement=session.scalar(select(func.count(QuestionPool.emoid)))
            if count_statement < 1:
                msg=f"""
Question Section {datetime.now().ctime()}")
{'-'*os.get_terminal_size().columns}
{'\n'.join(qsa)}

Answer Section {datetime.now().ctime()}
{'\n'.join(As)}
            """
                return msg

            statement=select(QuestionPool).order_by(func.random()).limit(l)
            a=session.execute(statement).scalars().all()
            for i in a:
                tsp.append(i)
            tsp=random.choices(tsp,k=l)
           
            for num,i in enumerate(tsp):
                cta=num
                qsp.append(generate_formula_from_template(i.template,qnum=num,tqoof=len(tsp)))
        
        if len(qsp) > 0:
            notes=qsp[0].notes
        else:
            notes=""
        
        try:
            msg=f"""
Question Section {datetime.now().ctime()}")
{'-'*os.get_terminal_size().columns}
{'\n'.join(qsa)}
{'-'*os.get_terminal_size().columns}
Question Pool Questions {datetime.now().ctime()}")
{"\n".join(i.just_question for i in qsp)}
{'-'*os.get_terminal_size().columns}
{'\n'*3}
Answer Section {datetime.now().ctime()}
{'\n'.join(As)}
{'-'*os.get_terminal_size().columns}
Question Pool Notes {datetime.now().ctime()}
{'-'*os.get_terminal_size().columns}
{notes}
Question Pool Answers {datetime.now().ctime()}
{'-'*os.get_terminal_size().columns}
{"\n".join(i.question_answer for i in qsp)}
        """
        except Exception as e:
            msg=f"""
Question Section {datetime.now().ctime()}")
{'-'*os.get_terminal_size().columns}
{'\n'.join(qsa)}

Answer Section {datetime.now().ctime()}
{'\n'.join(As)}
            """
        return msg
    


def questionPool_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        
        for xnum,i in enumerate(data):
            msg=f'''{i}'''
            msg=std_colorize(msg,xnum,ct)
            xtext.append(msg.replace("\n"," | "))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def questionPool_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_questionPool(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=questionPool_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def questionPool_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""
def qp_test_file():
    try:
        fields={
            'file':{
                'type':'rpath',
                'default':None,
                'help':'filename of script to test',
                'ptext':'Script File Name'
                },
            'dir':{
                'type':'rpath',
                'default':Path("Math.d"),
                'help':'directory of scripts to test',
                'ptext':'Script Directory Name'
                }
            }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        if not fb['dir'].exists():
                fb['dir'].mkdir(parents=True)
        print(fb)
        if (fb['dir']/fb['file']).exists():
            with (fb['dir']/fb['file']).open("r") as ifile:
                data=ifile.read()
                cta=len(data.split("\n"))
                for num,line in enumerate(data.split("\n")):
                    print(std_colorize(line,num,cta))

                lcl={}
                exec(data,lcl)
                for i in lcl:
                    print(f"{Fore.orange_red_1}{i}:{Fore.light_yellow}{type(lcl[i]).__name__}{Fore.cyan} = {Fore.light_steel_blue}{lcl[i]}{Style.reset}")

    except Exception as e:
        print(e)

def qp_install_file():
    try:
        fields={
            'file':{
                'type':'rpath',
                'default':None,
                'help':'filename of script to test',
                'ptext':'Script File Name'
                },
            'dir':{
                'type':'rpath',
                'default':Path("Math.d"),
                'help':'directory of scripts to test',
                'ptext':'Script Directory Name'
                }
            }
        fb=FormBuilder(data=fields)
        if fb in BooleanAnswers.NONE:
            return
        if not fb['dir'].exists():
                fb['dir'].mkdir(parents=True)
        print(fb)
        if (fb['dir']/fb['file']).exists():
            with (fb['dir']/fb['file']).open("r") as ifile:
                data=ifile.read()
                cta=len(data.split("\n"))
                for num,line in enumerate(data.split("\n")):
                    print(std_colorize(line,num,cta))
                    
                lcl={}
                exec(data,lcl)
                for i in lcl:
                    print(f"{Fore.orange_red_1}{i}:{Fore.light_yellow}{type(lcl[i]).__name__}{Fore.cyan} = {Fore.light_steel_blue}{lcl[i]}{Style.reset}")

                with Session(ENGINE) as session:
                    qp=QuestionPool(template=data)
                    session.add(qp)
                    session.commit()
                    session.refresh(qp)
                    print(qp)

    except Exception as e:
        print(e)

questionPool_menu={
    str(uuid1()):{
    "cmds":['questionPool custom',],
    "exec":lambda self:s2cb_questionPool(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
    str(uuid1()):{
    "cmds":['questionPool custom testfile','tf'],
    "exec":lambda self:qp_test_file(),
    "desc":"test file for errors",
    },
    str(uuid1()):{
    "cmds":['questionPool custom installfile','if'],
    "exec":lambda self:qp_install_file(),
    "desc":"test file and install file data in QuestionPool",
    }
}

#TriedToWake
def questionPoolLogger(Model=QuestionPool,short_view=questionPool_short_view,menu=questionPool_menu):
    return ModelLogger(Model=QuestionPool,short_view=questionPool_short_view,menu=questionPool_menu)

def Break_Time():
    
    fields={
        'now':{
            'type':'datetime',
            'default':datetime.now(),
            'help':"what time is it now",
            'ptext':"What is Now"
        },
        'for every x hours':{
            'type':'float',
            'default':4,
            'help':'for every number of hours',
            'ptext':'How many hours for every break'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Get The Time for your break; keep track of your breaks")
    if fb in BooleanAnswers.NONE:
        return

    formula=fb['now']+(timedelta(hours=fb['for every x hours']/2))
    return formula

def Meal_Time():
    
    fields={
        'now':{
            'type':'datetime',
            'default':datetime.now(),
            'help':"what time is it now",
            'ptext':"What is Now"
        },
        'for every x hours':{
            'type':'float',
            'default':6,
            'help':'for every number of hours',
            'ptext':'How many hours for every break'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Get The Time for your Meal; keep track of your Meals")
    if fb in BooleanAnswers.NONE:
        return

    formula=fb['now']+(timedelta(hours=fb['for every x hours']/2))
    return formula

def QTY_eq_distanceXtrip_over_mpg():
    while True:
        
        fields={
            'distance':{
                'type':'float',
                'default':2.8,
                'help':"distance from point a to point b",
                'ptext':"Distance 1-Way"
            },
            'distance unit':{
                'type':'string',
                'default':"miles",
                'help':"distance from point a to point b unit",
                'ptext':"Distance 1-Way Unit"
            },
            'trips 1-way':{
                'type':'float',
                'default':2,
                'help':'how many 1-way trips are/will/have been made',
                'ptext':'How Many Trips?'
            },
            'fuel economy':{
                'type':'float',
                'default':16.8,
                'help':"Fuel economy for vehicle",
                'ptext':"Fuel economy"
            },
            'fuel economy unit':{
                'type':'string',
                'default':"miles * gallon",
                'help':"fuel economy for vehicle",
                'ptext':"fuel economy Unit"
            },
        }
        fb=FormBuilder(data=fields,passThruText="(QTY=Distance*Trips)/MPG[economy]")
        if fb in BooleanAnswers.NONE:
            return
        for k in fb:
            if fb[k] is None:
                print("certain bits of data were left as None, and this is not useable")
                continue
        fe=QTY(fb['fuel economy'],fb['fuel economy unit'])
        distanceXtrips=QTY(fb['distance'],fb['distance unit'])*fb['trips 1-way']
        qty=distanceXtrips/fe
        formula=qty
        return formula

def inRadius_Area_over_SemiPerimeter():
    while True:
        fields={
            'area':{
                'type':'float',
                'default':2.8,
                'help':"Area of the Triangle",
                'ptext':"Area"
            },
            'area unit':{
                'type':'string',
                'default':"inch ** 2",
                'help':"Area unit",
                'ptext':"Area Unit"
            },
            'semi-perimeter':{
                'type':'float',
                'default':16.8,
                'help':"Triangle Semi-Perimeter",
                'ptext':"Semi-Perimeter"
            },
            'semi-perimeter unit':{
                'type':'string',
                'default':"inches",
                'help':"Semi-Perimeter Unit",
                'ptext':"Semi-Perimeter Unit"
            },
        }
        fb=FormBuilder(data=fields,passThruText="inradius_r=Area/semi_perimeter")
        if fb in BooleanAnswers.NONE:
            return
        for k in fb:
            if fb[k] is None:
                print("certain bits of data were left as None, and this is not useable")
                continue
        area=QTY(fb['area'],fb['area unit'])
        semi_perimeter=QTY(fb['semi-perimeter'],fb['semi-perimeter unit'])
        radius=area/semi_perimeter
        formula=radius
        return formula

def inRadius_a_plus_b_minus_2_over2():
    while True:
        fields={
            'side a':{
                'type':'float',
                'default':2.8,
                'help':"Side A of the Triangle",
                'ptext':"Side A"
            },
            'side a unit':{
                'type':'string',
                'default':"inch",
                'help':"Side A unit",
                'ptext':"Side A Unit"
            },
            'side b':{
                'type':'float',
                'default':2.8,
                'help':"Side of B of the Triangle",
                'ptext':"Side of B"
            },
            'side b unit':{
                'type':'string',
                'default':"inch",
                'help':"Side of B unit",
                'ptext':"Side of B Unit"
            },
            'side c':{
                'type':'float',
                'default':2.8,
                'help':"Side C of the Triangle",
                'ptext':"Side C"
            },
            'side c unit':{
                'type':'string',
                'default':"inch",
                'help':"Side C unit",
                'ptext':"Side C Unit"
            },
        }
        fb=FormBuilder(data=fields,passThruText="inradius_r=Area/semi_perimeter")
        if fb in BooleanAnswers.NONE:
            return
        for k in fb:
            if fb[k] is None:
                print("certain bits of data were left as None, and this is not useable")
                continue
        side_a=QTY(fb['side a'],fb['side a unit'])
        side_b=QTY(fb['side b'],fb['side b unit'])
        side_c=QTY(fb['side c'],fb['side c unit'])
        radius=((side_a+side_b)-side_c)/2
        formula=radius
        return formula

def inRadius_herons():
    while True:
        fields={
            'side a':{
                'type':'float',
                'default':2.8,
                'help':"Side A of the Triangle",
                'ptext':"Side A"
            },
            'side a unit':{
                'type':'string',
                'default':"inch",
                'help':"Side A unit",
                'ptext':"Side A Unit"
            },
            'side b':{
                'type':'float',
                'default':2.8,
                'help':"Side of B of the Triangle",
                'ptext':"Side of B"
            },
            'side b unit':{
                'type':'string',
                'default':"inch",
                'help':"Side of B unit",
                'ptext':"Side of B Unit"
            },
            'side c':{
                'type':'float',
                'default':2.8,
                'help':"Side C of the Triangle",
                'ptext':"Side C"
            },
            'side c unit':{
                'type':'string',
                'default':"inch",
                'help':"Side C unit",
                'ptext':"Side C Unit"
            },
            'semi-perimeter':{
                'type':'float',
                'default':16.8,
                'help':"Triangle Semi-Perimeter",
                'ptext':"Semi-Perimeter"
            },
            'semi-perimeter unit':{
                'type':'string',
                'default':"inches",
                'help':"Semi-Perimeter Unit",
                'ptext':"Semi-Perimeter Unit"
            },
        }
        fb=FormBuilder(data=fields,passThruText="inradius=sqrt((s-side a)*(s-side b)*(s-side c))/s ; herons formula")
        if fb in BooleanAnswers.NONE:
            return
        for k in fb:
            if fb[k] is None:
                print("certain bits of data were left as None, and this is not useable")
                continue
        side_a=QTY(fb['side a'],fb['side a unit'])
        side_b=QTY(fb['side b'],fb['side b unit'])
        side_c=QTY(fb['side c'],fb['side c unit'])
        semi_perimeter=QTY(fb['semi-perimeter'],fb['semi-perimeter unit'])
        radius=(
            (
            semi_perimeter*((semi_perimeter-side_a)*(semi_perimeter-side_b)*(semi_perimeter-side_c))
            )**0.5)/semi_perimeter
        formula=radius
        return formula

def discount():
    while True:
        fields={
            'price':{
                'type':'float',
                'default':1,
                'help':"Side A of the Triangle",
                'ptext':"Side A"
            },
            'discount percentage':{
                'type':'float',
                'default':10,
                'help':"what percentage off",
                'ptext':"Discount Percentage(%)"
            },
            'exceeds warning':{
                'type':'float',
                'default':50,
                'help':"above this value issue a warning",
                'ptext':"Exceeds Warning"
            }
        }
        fb=FormBuilder(data=fields,passThruText="Calculate FinalPrice@Discount% and AmountDiscounted@Discount%")
        if fb in BooleanAnswers.NONE:
            return
        for k in fb:
            if fb[k] is None:
                print("certain bits of data were left as None, and this is not useable")
                continue
        price=decc(fb['price'])
        discount_percentage=decc(fb['discount percentage'])/decc(100)
        exceeds=decc(fb['exceeds warning'])

        if (price*discount_percentage) > exceeds:
            warning=Control(ptext=f"The Discounted Price exceeds {exceeds}. Continue?",helpText="yes or no",data="boolean")
            if warning in BooleanAnswers.NONE:
                return
            elif warning in BooleanAnswers.NO_defaulted:
                continue

        results={
        'amount discounted':price*discount_percentage,
        'discounted price':(1-discount_percentage)*price,
        'maximum discount percentage allowed':(exceeds/price)*100,
        'maximum allowed discount price':(exceeds/price)*price}
        htext=[]
        cta=len(results)
        for num,i in enumerate(results):
            htext.append(std_colorize(f"{i} = {results[i]}",num,cta))
        htext='\n'.join(htext)
        which=Control(func=lambda text,data:FormBuilderMkText(text,data,passThru=['all','a',],PassThru=True),ptext=f"{htext}\n{Fore.orange_red_1}Which Result Index({Fore.light_yellow}'a','all'=return all as str(){Fore.orange_red_1})?: ",helpText=f"{htext}",data="integer")
        if which in BooleanAnswers.NONE:
            return
        if which in range(0,cta):
            return results[which]
        elif which in ['all','a']:
            return str(results)

def max_discount_allowed():
    while True:
        fields={
            'price':{
                'type':'float',
                'default':1,
                'help':"Side A of the Triangle",
                'ptext':"Side A"
            },
            'exceeds warning':{
                'type':'float',
                'default':50,
                'help':"above this value issue a warning",
                'ptext':"Exceeds Warning"
            }
        }
        fb=FormBuilder(data=fields,passThruText="Calculate Max Allowed Discount")
        if fb in BooleanAnswers.NONE:
            return
        for k in fb:
            if fb[k] is None:
                print("certain bits of data were left as None, and this is not useable")
                continue
        price=decc(fb['price'])
        exceeds=decc(fb['exceeds warning'])

        results={
        'maximum discount percentage allowed':(exceeds/price)*100,
        'maximum allowed discount price':(exceeds/price)*price}
        htext=[]
        cta=len(results)
        for num,i in enumerate(results):
            htext.append(std_colorize(f"{i} = {results[i]}",num,cta))
        htext='\n'.join(htext)
        which=Control(func=lambda text,data:FormBuilderMkText(text,data,passThru=['all','a',],PassThru=True),ptext=f"{htext}\n{Fore.orange_red_1}Which Result Index({Fore.light_yellow}'a','all'=return all as str(){Fore.orange_red_1})?: ",helpText=f"{htext}",data="integer")
        if which in BooleanAnswers.NONE:
            return
        if which in range(0,cta):
            return results[which]
        elif which in ['all','a']:
            return str(results)

def algrebaic_calculator():
    headers='''
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar
from decimal import Decimal,getcontext
from decimal import Decimal as DEC
from fractions import Fraction as frctn
from pint import Quantity
import sympy
from radboy.TasksMode.TasksUR import *
from radboy.TasksMode.Tasks import *
prepare_ureg(self=None)
locals().update({str(i):i for i in sp.symbols('a:z')})
            '''
    BooleanAnswers.local_vars={}
    while True:
        try:
            formula=Control(ptext=f"{Fore.light_yellow}TaskMode@{Fore.light_cyan}Algebraic[b returns result]{Fore.light_red}Exec {Fore.light_steel_blue}Calculator{Style.reset}",helpText="",data="string")
            if formula in db.BooleanAnswers.NONE:
                results=BooleanAnswers.local_vars.get("result")
                if isinstance(results,list):
                    htext=[]
                    cta=len(results)
                    for num,i in enumerate(results):
                        htext.append(std_colorize(i,num,cta))
                    htext='\n'.join(htext)
                    which=Control(func=lambda text,data:FormBuilderMkText(text,data,passThru=['all','a',],PassThru=True),ptext=f"{htext}\n{Fore.orange_red_1}Which Result Index({Fore.light_yellow}'a','all'=return all as str(){Fore.orange_red_1})?: ",helpText=f"{htext}",data="integer")
                    #which=Control(ptext=f"{htext}\n{Fore.orange_red_1}Which Result Index?: ",helpText=htext,data="integer")
                    if which in BooleanAnswers.NONE:
                        return
                    if which in range(0,cta):
                        return results[which]
                    elif which in ['all','a']:
                        return str(results)
                else:
                    return

            if formula in ['d','']:
                continue
            formula=f"""
{headers}
{formula}
            """
            
            exec(formula,{},BooleanAnswers.local_vars)
            cta=len(BooleanAnswers.local_vars)
            for num,i in enumerate(BooleanAnswers.local_vars):
                msg=f"{i} = {BooleanAnswers.local_vars.get(i)}"
                print(std_colorize(msg,num,cta))
        except Exception as e:
            print(e)


def giftCardMaxes_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        ttlCarb=[]
        

        carbs=QTY(0,"grams")
        fat=QTY(0,"grams")
        cholesterol=QTY(0,"grams")
        sodium=QTY(0,"mg")
        ttlSodiumConsumed=QTY(0,"mg")
        ss=QTY(0,"grams")
        ttlsugars=QTY(0,"grams")
        ttladdsugars=QTY(0,"grams")
        protien=QTY(0,"grams")
        cal=QTY(0,"kilocalorie")

        ttlCarbConsumed=QTY(0,"grams")
        ttlFatConsumed=QTY(0,"grams")
        ttlCholesterolConsumed=QTY(0,"mg")
        ttlSodiumConsumed=QTY(0,"mg")
        ttlDietaryFiberConsumed=QTY(0,"grams")
        ttlTTLSugarsConsumed=QTY(0,"grams")
        ttlTTLAddedSugarsConsumed=QTY(0,"grams")
        ttlProtienConsumed=QTY(0,"grams")
        ttlCalConsumed=QTY(0,"kilocalorie")

        for xnum,i in enumerate(data):
            msg=f'''
{i}
            '''
            msg=std_colorize(msg,xnum,ct)
            xtext.append(msg.replace("\n"," | "))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def giftCardMaxes_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_giftCardMaxes(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=giftCardMaxes_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

"""               
def giftCardMaxes_short_view(self,data:list,printToScreen=True,num=None):
    xtext=[]
    ct=len(data)
    ii=''

    x=''''''.split("\n")
    cta=len(x)
    for num,xx in enumerate(x):
        print(std_colorize(xx,num,cta))

    for xnum,i in enumerate(data):
        try:
            msg=f'''
{'-'*20}
    {Fore.orange_red_1}fuelid= {Fore.light_steel_blue}{i.fuelid}
    {Fore.orange_red_1}fuel_name= {Fore.light_steel_blue}{i.fuel_name}
    {Fore.orange_red_1}fuel_price= {Fore.light_steel_blue}{i.fuel_price}
    {Fore.orange_red_1}fuel_price_unit= {Fore.light_steel_blue}{i.fuel_price_unit}
    {Fore.orange_red_1}location= {Fore.light_steel_blue}{i.location}
    {Fore.orange_red_1}street_address= {Fore.light_steel_blue}{i.street_address}
    {Fore.orange_red_1}city_county_of= {Fore.light_steel_blue}{i.city_county_of}
    {Fore.orange_red_1}state= {Fore.light_steel_blue}{i.state}
    {Fore.orange_red_1}zipcode= {Fore.light_steel_blue}{i.zipcode}
    {Fore.orange_red_1}country= {Fore.light_steel_blue}{i.country}
    {Fore.orange_red_1}dtoe= {Fore.light_steel_blue}{i.dtoe}
    {Fore.orange_red_1}comment= {Fore.light_steel_blue}{i.comment}
{'-'*20}
    {Style.reset}'''
        except Exception as e:
            print(e)

        if not num:
            m=std_colorize(msg,xnum,ct)
        else:
            m=std_colorize(msg,num,ct)
        xtext.append(m)
        if printToScreen:            
            print(m)
    return '\n'.join(xtext)
"""

giftCardMaxes_menu={
    str(uuid1()):{
    "cmds":['giftCardMaxes custom',],
    "exec":lambda self:s2cb_giftCardMaxes(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    }
}

#TriedToWake
def giftCardMaxesLogger(Model=GiftCardMaxes,short_view=giftCardMaxes_short_view,menu=giftCardMaxes_menu):
    return ModelLogger(Model=GiftCardMaxes,short_view=giftCardMaxes_short_view,menu=giftCardMaxes_menu)

def transactionID_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
           xtext.append(std_colorize(i,xnum,ct))
        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def transactionID_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_transactionID(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=transactionID_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

transactionID_menu={
    str(uuid1()):{
    "cmds":['transactionID custom',],
    "exec":lambda self:s2cb_transactionID(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def transactionIDLogger(Model=TransactionID,short_view=transactionID_short_view,menu=transactionID_menu):
    return ModelLogger(Model=TransactionID,short_view=transactionID_short_view,menu=transactionID_menu)

def compound_interest_standard():
    fields={
        
        'Principle':{
            'type':'float',
            'default':0,
            'help':'Initial Investment Amount',
            'ptext':'Principle(P)'
        },
        'Annual Interest Rate':{
            'type':'float',
            'default':0,
            'help':'nominal interest rate as a decimal',
            'ptext':'Annual Interest Rate(r)'
        },
        'Compounding Frequency':{
            'type':'float',
            'default':0,
            'help':'the number of times interest is applied per year',
            'ptext':'Compounding Frequency(n)'
        },
        'Time':{
            'type':'float',
            'default':0,
            'help':'the number of years the money is invested or borrowed for.',
            'ptext':'Time(t)'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Standard Compounding Interest Formula")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    formula=None
    fod=fod_()

    principal=fod(fb['Principle'])
    r=fod(fb['Annual Interest Rate'])
    n=fod(fb['Compounding Frequency'])
    t=fod(fb['Time'])
    total_months=(n*t)
    monthly_rate=(r/n)
    total_amount=principal*((1+(monthly_rate))**(total_months))

    rslt={}
    results={'principal':principal,
    'interest rate':r,
    'compounding frequency':n,
    'time in years':t,
    'total amount':total_amount,
    'total months':total_months,
    'monthly rate':monthly_rate,
    }
    '''
    for i in results:
        rslt[f'{i} str 2f']=f"{results[i]:,.2f}"
        rslt[f'{i} str 3f']=f"{results[i]:,.3f}"
        rslt[f'{i} str 4f']=f"{results[i]:,.4f}"
        rslt[f'{i} float 2f']=float(f"{results[i]:.2f}")
        rslt[f'{i} float 3f']=float(f"{results[i]:.3f}")
        rslt[f'{i} float 4f']=float(f"{results[i]:.4f}")
        rslt[f'{i} Decimal 2f']=decc(f"{results[i]:.2f}",cf=2)
        rslt[f'{i} Decimal 3f']=decc(f"{results[i]:.3f}",cf=3)
        rslt[f'{i} Decimal 4f']=decc(f"{results[i]:.4f}",cf=4)

    results.update(rslt)
    htext=[]
    cta=len(results)
    for num,i in enumerate(results):
        htext.append(std_colorize(f"{i} = {results[i]}",num,cta))
    htext='\n'.join(htext)
    which=Control(func=lambda text,data:FormBuilderMkText(text,data,passThru=['all','a',],PassThru=True),ptext=f"{htext}\n{Fore.orange_red_1}Which Result Index({Fore.light_yellow}'a','all'=return all as str(){Fore.orange_red_1})?: ",helpText=f"{htext}",data="integer")
    if which in BooleanAnswers.NONE:
        return
    if which in range(0,cta):
        return results[which]
    elif which in ['all','a']:
        return str(results)
    '''
    return results_def(results)


def compound_interest_contributing():
    fields={
        'Principle':{
            'type':'float',
            'default':0,
            'help':'Initial Investment Amount',
            'ptext':'Principle(P)'
        },
        'Payment':{
            'type':'float',
            'default':0,
            'help':'Regular contribution amount added each period (assuming contributions match the compounding frequency)',
            'ptext':'Payment(PMT)'
        },
        'Annual Interest Rate':{
            'type':'float',
            'default':0,
            'help':'nominal interest rate as a decimal',
            'ptext':'Annual Interest Rate(r)'
        },
        'Compounding Frequency':{
            'type':'float',
            'default':0,
            'help':'the number of times interest is applied per year',
            'ptext':'Compounding Frequency(n)'
        },
        'Time':{
            'type':'float',
            'default':0,
            'help':'the number of years the money is invested or borrowed for.',
            'ptext':'Time(t) Years'
        },
    }
    fb=FormBuilder(data=fields,passThruText="Contributing Compounding Interest Formula")
    if fb in BooleanAnswers.NONE:
        return

    #formula qty
    formula=None
    mod=fod_()
    principal=mod(fb['Principle'])
    r=mod(fb['Annual Interest Rate'])
    n=mod(fb['Compounding Frequency'])
    t=mod(fb['Time'])
    monthly_contribution=mod(fb['Payment'])
    

    # Convert annual rate percentage to a decimal
    r = r
    # Number of compounding periods per year (monthly)
    n = n
    # Total number of compounding periods
    total_months = n * t
    # Monthly interest rate fraction
    monthly_rate = r / n
    
    # 1. Growth of the initial principal
    principal_growth = principal * ((1 + monthly_rate) ** total_months)
    
    # 2. Growth of the monthly contributions (Ordinary Annuity formula)
    contributions_growth = monthly_contribution * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
    
    # Total combined balance
    total_balance = principal_growth + contributions_growth
    
    # Calculate out-of-pocket cash contributions
    total_invested = principal + (monthly_contribution * total_months)
    total_interest = total_balance - total_invested

    
    results={'total_invested':total_invested,'total_interest':total_interest,'total_balance':total_balance,'principal':principal,'monthly_contribution':monthly_contribution,'total_months':total_months,'contributions_growth':contributions_growth}
    return results_def(results)

def daily_periodic_rate_to_find_real_world_interest():
    while True:
        fields={
            'End Of Days Balance':{
                'type':'float',
                'default':0,
                'help':'End Of Day Balance',
                'ptext':'End Of Day Balance'
            },
            'Annual Rate':{
                'type':'float',
                'default':0.005,
                'help':'Annual Rate',
                'ptext':'Anual Rate'
            },
            'DTOE':{
                'type':'datetime',
                'default':datetime.now(),
                'help':'End Of Day DTOE',
                'ptext':'End Of Day DTOE'
            }
        }
        fb=FormBuilder(data=fields,passThruText="Contributing Compounding Interest Formula")
        if fb in BooleanAnswers.NONE:
            return
        fod=fod_()

        daily_rate=fod(fb['Annual Rate'])/365
        endOfDayBalance=fod(fb['End Of Days Balance'])
        dayInterestEarned=daily_rate*endOfDayBalance
        balanceWithInterest=dayInterestEarned+endOfDayBalance
        results={'DTOE':fb['DTOE'].strftime("%m/%d/%Y"),'daily_rate':daily_rate,'endOfDayBalance':endOfDayBalance,'dayInterestEarned':dayInterestEarned,'balanceWithInterest':balanceWithInterest}

        return results_def(results)


def annual_percentage_yield():
    fields={
    'interest earned':{
        'type':'float',
        'default':0,
        'help':"interest eaned for period",
        'ptext':'Interest Earned',
    },
    'average Daily Balance':{
        'type':'float',
        'default':0,
        'help':"average daily balance for 29/30/31 day period",
        'ptext':'Average Daily Balance',
    },
    'month number':{
        'type':'integer',
        'default':8,
        'help':"month to count balances for",
        'ptext':'Month Number',
    },
    }
    fb=FormBuilder(data=fields,passThruText="Month to sum balances for")
    if fb in BooleanAnswers.NONE:
        return

    mod=fod_()
    now=datetime.now()
    days=calendar.monthrange(now.year,fb['month number'])[-1]
    
    ie=mod(fb['interest earned'])
    avgDlyBlnc=mod(fb['average Daily Balance'])
    f=( (1+mod(ie/avgDlyBlnc))**mod(365/days))-1
    

    return results_def({'apy':f})


def percent_change():
    fields={
    'new':{
        'type':'float',
        'default':0.126,
        'help':"New Value",
        'ptext':'New Value',
    },
    'new unit':{
        'type':'string',
        'default':'percent',
        'help':"New unit",
        'ptext':'New unit',
    },
    'old':{
        'type':'float',
        'default':0.01,
        'help':"Old Value",
        'ptext':'Old Value',
    },
    'old unit':{
        'type':'string',
        'default':'percent',
        'help':"Old unit",
        'ptext':'Old unit',
    },
    'across':{
        'type':'float',
        'default':251,
        'help':"Old Value",
        'ptext':'Old Value',
    },
    'across unit':{
        'type':'string',
        'default':'day',
        'help':"across unit",
        'ptext':'across unit',
    }
    }
    fb=FormBuilder(data=fields,passThruText="Month to sum balances for")
    if fb in BooleanAnswers.NONE:
        return
    mod=fod_()
    old=QTY(mod(fb['old']),fb['old unit'])
    new=QTY(mod(fb['new']),fb['new unit'])
    across=QTY(mod(fb['across']),fb['across unit'])

    
    
    percent_change=((new-old)/old)*QTY(100,'percent')
    rate=percent_change/across

    expr_human=f"percent_change({percent_change})=((new({new})-old({old}))/old({old}))*100"
    expr=f"(({new}-{old})/{old})*100"

    return results_def({'rate':rate,'old':old,'new':new,'across':across,'percent change':percent_change,'expression_human':expr_human,'expression_machine':expr})


def rate_of_change():
    fields={
    'new':{
        'type':'float',
        'default':20,
        'help':"New Value",
        'ptext':'New Value',
    },
    'new unit':{
        'type':'string',
        'default':'mg/decaliter',
        'help':"New unit",
        'ptext':'New unit',
    },
    'old':{
        'type':'float',
        'default':356,
        'help':"Old Value",
        'ptext':'Old Value',
    },
    'old unit':{
        'type':'string',
        'default':'mg/decaliter',
        'help':"Old unit",
        'ptext':'Old unit',
    },
    'across':{
        'type':'float',
        'default':6,
        'help':"Old Value",
        'ptext':'Old Value',
    },
    'across unit':{
        'type':'string',
        'default':'hours',
        'help':"across unit",
        'ptext':'across unit',
    }
    }
    fb=FormBuilder(data=fields,passThruText="Month to sum balances for")
    if fb in BooleanAnswers.NONE:
        return
    mod=fod_()
    old=QTY(mod(fb['old']),fb['old unit'])
    new=QTY(mod(fb['new']),fb['new unit'])
    across=QTY(mod(fb['across']),fb['across unit'])

    
    
    change=(new-old)
    rate=change/across

    expr_human=f"rate_of_change({percent_change})=(new({new})-old({old}))/across({across})"
    expr=f"(({new}-{old})/{old})/{across}"

    return results_def({'rate':rate,'old':old,'new':new,'across':across,'change':change,'expression_human':expr_human,'expression_machine':expr})


def averageDailyBalance():
    fields={
    'month number':{
        'type':'integer',
        'default':8,
        'help':"month to count balances for",
        'ptext':'Month Number',
    },
    }
    fb=FormBuilder(data=fields,passThruText="Month to sum balances for")
    if fb in BooleanAnswers.NONE:
        return

    balances={}
    now=datetime.now()
    days=calendar.monthrange(now.year,fb['month number'])[-1]
    for i in range(1,days+1):
        key=datetime(now.year,fb['month number'],i).strftime("%m/%d/%Y")
        balances[key]={
                'type':'dec.dec',
                'default':0,
                'help':f'End of Day Balance for {key}',
                'ptext':f'End Of Day Balance for {key}'
        }
        
    fb=FormBuilder(data=balances)
    if fb in BooleanAnswers.NONE:
        return
    try:
        mod=fod_()
        for i in fb:
            print(i,fb[i],sep="=")
        average_daily_balance=mod(np.average([mod(i) for i in list(fb.values())]))
        return average_daily_balance
    except Exception as e:
        print(e)
        return


def rollTheDie():
    fields={
    'Number of Contestants':{
        'type':'integer',
        'default':2,
        'help':"Contestants being Chosen at Random: integer",
        'ptext':'Contestants being Chosen at Random',
    },
    }
    fb=FormBuilder(data=fields,passThruText="Who gets selected?")
    if fb in BooleanAnswers.NONE:
        return

    choices={}
    for i in range(1,fb['Number of Contestants']+1):
        choices[str(i)]=i

    dump=False
    for i in range(0,fb['Number of Contestants']):
        result=random.choices(list(choices.keys()))[0]
        print(f"Contestant {i}: {result}")
        
        
        if not dump:
            while True:
                nxt=Control(ptext="Next Contestant?",helpText="yes or no, NaN will dump the data list and will not be the same as the if yes was used",data="boolean")
                if nxt in BooleanAnswers.NONE:
                    dump=True
                    for i in range(0,fb['Number of Contestants']):
                        result=random.choices(list(choices.keys()))[0]
                        print(f"Contestant {i}: {result}")
                        choices.pop(result)
                    return 
                if not nxt:
                    print(f"Contestant {i}: {result}")
                else:
                    break
            choices.pop(result)
            continue
        
def basicFoodLog_short_view(self,data:list,printToScreen=True,num=None):
        xtext=[]
        ct=len(data)
        ii=''
        #template text
        #{Fore.cyan}{i.}{Fore.light_steel_blue} ={Fore.sea_green_1a}'{i.}{Style.reset}'
        for xnum,i in enumerate(data):
            try:
                x={}
                for z in i.__table__.columns:
                    try:
                        if z.type in ['varchar',]:
                            x[z.name]=QTY(getattr(i,z.name))
                        else:
                            x[z.name]=getattr(i,z.name)
                    except Exception as e:
                        x[z.name]=getattr(i,z.name)
                bfl=BasicFoodLog(**x)
                xtext.append(std_colorize(bfl,xnum,ct))
            except Exception as e:
                print(e)
                xtext.append(std_colorize(i,xnum,ct))

        if printToScreen:
            print('\n'.join(xtext))
        return '\n'.join(xtext)

def basicFoodLog_StoreForCDP(self,item):
    try:
        with Session(ENGINE) as session:
            log=session.query(self.Model).filter(self.primaryKey(self.Model)==self.primaryKey(item)).first()
            keys={
           
            }
            htext=[]
            cta=len(keys)
            for num,k in enumerate(keys):
                htext.append(std_colorize(f"Field {k} = '{keys[k]}'",num,cta))
            htext='\n'.join(htext)
            while True:
                try:
                    print(htext)
                    which=Control(func=FormBuilderMkText,ptext=f"Which {Fore.light_blue}index {Fore.light_yellow}for{Fore.light_red} field{Fore.light_yellow} do you wish to return?",helpText=f"index integer for field starting at 0:\n{htext}",data="integer")
                    if which is None:
                        return
                    elif which in ['NAN','NaN',None,'None','d','']:
                        return
                    else:
                        self.StoreInCB(ncb_text=str(tuple(keys.values())[which]))
                    return
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
        return item
    pass

def s2cb_basicFoodLog(self,menu=False,short=True):
        with Session(ENGINE) as session:
            filt=abstract_filter(self.Model)

            core={
                'limit':{
                'default':None,
                'type':"integer"
                },
                'offset':{
                'default':None,
                'type':'integer,'
                }
            }
            fd=FormBuilder(data=core,passThruText="limit your results.")
            if fd is None:
                print("exited early")
                return
            if filt is not None:
                query=session.query(self.Model).filter(filt)
            else:
                query=session.query(self.Model)
            
            
            orderedQuery=orderQuery(query,self.Model.dtoe)
            limited=limitOffset(orderedQuery,limit=fd['limit'],offset=fd['offset'])
            results=limited.all()
            if short:
                htext=self.short_view(self=self,data=results,printToScreen=False)
            else:
                htext=self.long_view(data=results,printToScreen=False)

            if menu:
                #next update
                cta=len(results)
                gotoNext=None
                for num,log in enumerate(results):
                    if log == None:
                        continue
                    while True:
                        if log is None:
                            gotoNext=True
                            break
                        
                        cmds=['edit=ed/edit/e','delete=rm/del/delete/remove','save2cb=s2cb/clipbd/memo']
                        try:
                            if short:
                                l=self.short_view(self=self,data=[log,],printToScreen=False,num=num)
                            else:
                                l=self.long_view(self=self,data=[log,],printToScreen=False,num=num)
                            doWhat=Control(func=FormBuilderMkText,ptext=f"{l}\n[{cmds}]?",helpText=f"{l}\n{cmds}",data="string")
                            if doWhat in ['NaN',None]:
                                return
                            elif doWhat.lower() in ['d','']:
                                gotoNext=True
                                break
                            elif doWhat.lower() in [i.lower() for i in 'edit=ed/edit/e'.split('=')[-1].split("/")]:
                                log=self.edit_id(log)

                                continue
                            elif doWhat.lower() in [i.lower() for i in 'save2cb=s2cb/clipbd/memo'.split('=')[-1].split("/")]:
                                log=basicFoodLog_StoreForCDP(self,log)
                                continue
                            elif doWhat.lower() in [i.lower() for i in 'delete=rm/del/delete/remove'.split('=')[-1].split("/")]:
                                log=self.delete_id(log)
                                continue
                            else:
                                gotoNext=True
                                break
                            if gotoNext:
                                gotoNext=False
                                break
                        except Exception as e:
                            print(e)
                            gotoNext=True
                            break
            else:
                print(htext)    

basicFoodLog_menu={
    str(uuid1()):{
    "cmds":['basicFoodLog custom',],
    "exec":lambda self:s2cb_basicFoodLog(self,menu=True,short=True),
    "desc":"Save to Clipboard custom formats",
    },
}
#bptxt - bill paid text

#TriedToWake
def basicFoodLogLogger(Model=BasicFoodLog,short_view=basicFoodLog_short_view,menu=basicFoodLog_menu):
    return ModelLogger(Model=BasicFoodLog,short_view=basicFoodLog_short_view,menu=basicFoodLog_menu)