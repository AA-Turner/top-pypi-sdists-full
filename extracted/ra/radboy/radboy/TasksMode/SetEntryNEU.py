from radboy.DB.db import *
from radboy.DB.RandomStringUtil import *
import radboy.Unified.Unified as unified
import radboy.possibleCode as pc
import radboy.DB.db as db
from radboy.DB.Prompt import *
from radboy.DB.Prompt import prefix_text
from radboy.TasksMode.ReFormula import *
from radboy.FB.FormBuilder import *
from radboy.FB.FBMTXT import *
from radboy.RNE.RNE import *
from radboy.Lookup2.Lookup2 import Lookup as Lookup2
from collections import namedtuple,OrderedDict
import nanoid
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar
def today():
    dt=datetime.now()
    return date(dt.year,dt.month,dt.day)


class NEUSetter:
    def next_barcode(self):
        with Session(ENGINE) as session:
            next_barcode=session.query(SystemPreference).filter(SystemPreference.name=="next_barcode").first()
            
            state=False
            
            if next_barcode:
                    try:
                        state=json.loads(next_barcode.value_4_Json2DictString).get("next_barcode")
                    except Exception as e:
                        print(e)
                        next_barcode.value_4_Json2DictString=json.dumps({'next_barcode':False})
                        session.commit()
                        session.refresh(next_barcode)
                        state=json.loads(next_barcode.value_4_Json2DictString).get("next_barcode")
            else:
                next_barcode=db.SystemPreference(name="next_barcode",value_4_Json2DictString=json.dumps({'next_barcode':False}))
                session.add(next_barcode)
                session.commit()
                session.refresh(next_barcode)
                state=json.loads(next_barcode.value_4_Json2DictString).get("next_barcode")
            f=deepcopy(state)
            print(f,"NEXT BARCODE")
            next_barcode.value_4_Json2DictString=json.dumps({'next_barcode':False})
            session.commit()
            return f

    def __init__(self,code=None):
        self.code=code


    def newCodesFromExpireds(self):
        print(f"{Fore.light_green}Expiry{Style.reset}")
        with Session(ENGINE) as session:
            exps=session.query(Expiry).group_by(Expiry.Barcode).all()
            exps_ct=len(exps)
            if exps_ct == 0:
                print(f"{exps_ct} Expiry to Check!")
                return
            for num,exp in enumerate(exps):
                entry_result=session.query(Entry).filter(Entry.Barcode==exp.Barcode).first()
                if entry_result == None:
                    ptext=f"{Fore.light_green}{num}/{Fore.light_yellow}{num+1}/{Fore.light_red}{exps_ct} - {Fore.light_magenta}No Entry found to match {exp.Barcode}|{exp.Name} [[c]reate] Entry/[[s]kip]|[[i]gnore]|<Enter|Return>/d[[r]elete] Expiry"
                    helpText=ptext
                    while True:
                        doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=ptext,helpText=helpText,data="string")
                        nb=self.next_barcode()
                        if doWhat in [None,] and nb == False:
                            continue
                        elif doWhat in [None,] and nb == True:
                            return
                        elif doWhat.lower() in ['s','skip','i','ignore','d']:
                            break
                        elif doWhat.lower() in ['delete','r','rm','del',]:
                            session.delete(exp)
                            session.commit()
                            print(f"Deleted {exp}")
                        elif doWhat.lower() in ['create','new','n']:
                            data={
                            'Barcode':{
                                    'type':'String',
                                    'default':exp.Barcode,
                                },
                            'Code':{
                                    'type':'String',
                                    'default':'',
                                },
                            'Name':{
                                    'type':'String',
                                    'default':'',
                                },
                            'CaseCount':{
                                    'type':'integer',
                                    'default':'1',
                                },
                            'Price':{
                                    'type':'String',
                                    'default':0.0,
                                }
                            }
                            neu=FormBuilder(data)
                            if neu in [None,]:
                                continue
                            new_entry=Entry(**neu)
                            session.add(new_entry)
                            session.commit()
                            session.refresh(new_entry)
                            print(new_entry)
                            break
                else:
                    print(f"{num}/{num+1}/{exps_ct} - {Expiry.Barcode} - checking...")
                    toRM=session.query(Expiry).filter(Expiry.Barcode==entry_result.Barcode).all()
                    toRM_ct=len(toRM)
                    if toRM_ct == 0:
                        print("Nothing to Update!")
                        continue
                    else:
                        for num0,rmt in enumerate(toRM):
                            print(f"{num0}/{num0+1}/{toRM_ct} Updating Located Expiry.Barcode -> Entry.Barcode - {rmt.Barcode} - {entry_result.Name}!")
                            rmt.Name=entry_result.Name
                            if num0%10==0:
                                session.commit()
                        session.commit()
        print(f"{Fore.light_sea_green}Done{Fore.light_yellow} Cleaning Expiry's{Style.reset}")
        pass
        #scan through expireds table and check each barcode for an entry in Entry and update info from first result, or if not exists, prompt to create it/skip it/delete it, perform said action

    def newCodesFromPCs(self):
        print(f"{Fore.light_green}Cleaning PairCollection's{Style.reset}")
        with Session(ENGINE) as session:
            pcs=session.query(PairCollection).group_by(PairCollection.Barcode).all()
            pcs_ct=len(pcs)
            if pcs_ct == 0:
                print(f"{pcs_ct} PairCollection to Check!")
                return
            for num,pc in enumerate(pcs):
                entry_result=session.query(Entry).filter(Entry.Barcode==pc.Barcode).first()
                if entry_result == None:
                    ptext=f"{Fore.light_green}{num}/{Fore.light_yellow}{num+1}/{Fore.light_red}{pcs_ct} - {Fore.light_magenta}No Entry found to match {pc.Barcode}|{pc.Code} [[c]reate] Entry/[[s]kip]|[[i]gnore]|<Enter|Return>/d[[r]elete] PC"
                    helpText=ptext
                    while True:
                        doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=ptext,helpText=helpText,data="string")
                        nb=self.next_barcode()
                        if doWhat in [None,] and nb == False:
                            continue
                        elif doWhat in [None,] and nb == True:
                            return
                        elif doWhat.lower() in ['s','skip','i','ignore','d']:
                            break
                        elif doWhat.lower() in ['delete','r','rm','del',]:
                            session.delete(pc)
                            session.commit()
                            print(f"Deleted {pc}")
                        elif doWhat.lower() in ['create','new','n']:
                            data={
                            'Barcode':{
                                    'type':'String',
                                    'default':pc.Barcode,
                                },
                            'Code':{
                                    'type':'String',
                                    'default':'',
                                },
                            'Name':{
                                    'type':'String',
                                    'default':'',
                                },
                            'CaseCount':{
                                    'type':'integer',
                                    'default':'1',
                                },
                            'Price':{
                                    'type':'String',
                                    'default':0.0,
                                }
                            }
                            neu=FormBuilder(data)
                            if neu in [None,]:
                                continue
                            new_entry=Entry(**neu)
                            session.add(new_entry)
                            session.commit()
                            session.refresh(new_entry)
                            print(new_entry)
                            break
                else:
                    print(f"{num}/{num+1}/{pcs_ct} - {pc.Barcode} - checking...")
                    toRM=session.query(PairCollection).filter(PairCollection.Barcode==entry_result.Barcode).all()
                    toRM_ct=len(toRM)
                    if toRM_ct == 0:
                        print("Nothing to delete!")
                        continue
                    else:
                        for num0,rmt in enumerate(toRM):
                            print(f"{num0}/{num0+1}/{toRM_ct} Deleting Located PC.Barcode -> E.Barcode - {rmt.Barcode} - {entry_result.Name}!")
                            session.delete(rmt)
                            if num0%10==0:
                                session.commit()
                        session.commit()
        print(f"{Fore.light_sea_green}Done{Fore.light_yellow} Cleaning PairCollection's{Style.reset}")

        #scan through PairCollection table and check each barcode for an entry in Entry and if not exists, prompt to create it/skip it/delete it, perform said action, and remove PairCollection with corresponding Barcode
    
    def costPerUnitOfEach(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        data={
                        'For what Qty?':{
                            'type':'string',
                            'default':'16 oz'
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="Generate Price Per Unit Of Qty of Each")
                        if fb is None:
                            return
                        else:
                            v=f"Price Per Unit Of Each = '{pint.Quantity(selected.Price)/pint.Quantity(fb['For what Qty?'])}'"
                            lines=[]
                            t='Price Per Unit Of Each = '
                            if selected.Description not in [None,]:
                                if len(selected.Description.split("\n")) > 0:
                                    if selected.Description in ['',]:
                                        lines.append(v)
                                    else:
                                        for line in selected.Description.split("\n"):
                                            if t in line:
                                                lines.append(v)
                                            else:
                                                lines.append(line)
                                        if t not in '\n'.join(lines):
                                            lines.append(v)
                                else:
                                    lines.append(v)
                            #exit(f"{len(selected.Description.split("\n"))}")
                            selected.Description='\n'.join(lines)
                            selected.Size=v
                            session.commit()
                            session.refresh(selected)
                            print(selected)
                            break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def costPerUnitOfEach_NoQty(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        data={
                        'For what Qty?':{
                            'type':'float',
                            'default':16,
                            },
                        'unit':{
                        'type':'string',
                        'default':'package'
                        }
                        }
                        fb=FormBuilder(data=data,passThruText="Generate Price Per Unit Of Qty of Each")
                        if fb is None:
                            return
                        else:
                            v=f"Price Per Unit Of Each = '${selected.Price/fb['For what Qty?']} per {fb['unit']}'"
                            lines=[]
                            t='Price Per Unit Of Each = '
                            if selected.Description not in [None,]:
                                if len(selected.Description.split("\n")) > 0:
                                    if selected.Description in ['',]:
                                        lines.append(v)
                                    else:
                                        for line in selected.Description.split("\n"):
                                            if t in line:
                                                lines.append(v)
                                            else:
                                                lines.append(line)
                                        if t not in '\n'.join(lines):
                                            lines.append(v)
                                else:
                                    lines.append(v)
                            #exit(f"{len(selected.Description.split("\n"))}")
                            selected.Description='\n'.join(lines)
                            selected.Size=v
                            session.commit()
                            session.refresh(selected)
                            print(selected)
                            break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def UserRating(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[UserRating]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[UserRating] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        data={
                        'Rating 0.0-10.0':{
                            'type':'float',
                            'default':5.0,
                            },
                        'Attribute Being Rated':{
                        'type':'string',
                        'default':'Quality'
                        }
                        }
                        fb=FormBuilder(data=data,passThruText="Generate Price Per Unit Of Qty of Each")
                        if fb is None:
                            return
                        else:
                            v=f"{fb['Attribute Being Rated']} = '{fb['Rating 0.0-10.0']}'"
                            lines=[]
                            t=f'{fb['Attribute Being Rated']} = '
                            if selected.Description not in [None,]:
                                if len(selected.Description.split("\n")) > 0:
                                    if selected.Description in ['',]:
                                        lines.append(v)
                                    else:
                                        for line in selected.Description.split("\n"):
                                            if t in line:
                                                lines.append(v)
                                            else:
                                                lines.append(line)
                                        if t not in '\n'.join(lines):
                                            lines.append(v)
                                else:
                                    lines.append(v)
                            #exit(f"{len(selected.Description.split("\n"))}")
                            selected.Description='\n'.join(lines)
                            session.commit()
                            session.refresh(selected)
                            print(selected)
                            break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def DoNotTotal(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[DoNotTotal]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[DoNotTotal] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        

                        v=f'DoNotTotal = 1'
                        lines=[]
                        t=f'DoNotTotal = 1'
                        if selected.Description not in [None,]:
                            if len(selected.Description.split("\n")) > 0:
                                if selected.Description in ['',]:
                                    lines.append(v)
                                else:
                                    for line in selected.Description.split("\n"):
                                        if t in line:
                                            lines.append(v)
                                        else:
                                            lines.append(line)
                                    if t not in '\n'.join(lines):
                                        lines.append(v)
                            else:
                                lines.append(v)
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.Description='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def rm_DoNotTotal(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[DoNotTotal]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[DoNotTotal] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        lines=[]
                        
                        t=f'DoNotTotal = 1'
                        
                        if selected.Description not in [None,]:
                            if len(selected.Description.split("\n")) > 0:
                                if selected.Description in ['',]:
                                    pass
                                else:
                                    for line in selected.Description.split("\n"):
                                        if t in line:
                                            pass
                                        else:
                                            lines.append(line)
                            else:
                                pass
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.Description='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def rm_line(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[linetext]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[linetext] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        lines=[]
                        
                        data={
                            'line text to detect for removal':{
                            'type':'string',
                            'default':''
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="remove a line of text detected by string")
                        if fb is None:
                            return
                        t=f'{fb['line text to detect for removal']}'
                        
                        if selected.Description not in [None,]:
                            if len(selected.Description.split("\n")) > 0:
                                if selected.Description in ['',]:
                                    pass
                                else:
                                    for line in selected.Description.split("\n"):
                                        if t in line:
                                            pass
                                        else:
                                            lines.append(line)
                            else:
                                pass
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.Description='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def rm_line_note(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note[linetext]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note[linetext] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        lines=[]
                        
                        data={
                            'line text to detect for removal':{
                            'type':'string',
                            'default':''
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="remove a line of text detected by string")
                        if fb is None:
                            return
                        t=f'{fb['line text to detect for removal']}'
                        
                        if selected.Note not in [None,]:
                            if len(selected.Note.split("\n")) > 0:
                                if selected.Note in ['',]:
                                    pass
                                else:
                                    for line in selected.Note.split("\n"):
                                        if t in line:
                                            pass
                                        else:
                                            lines.append(line)
                            else:
                                pass
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.Note='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def rm_line_taxnote(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.TaxNote[linetext]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.TaxNote[linetext] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        lines=[]
                        
                        data={
                            'line text to detect for removal':{
                            'type':'string',
                            'default':''
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="remove a line of text detected by string")
                        if fb is None:
                            return
                        t=f'{fb['line text to detect for removal']}'
                        
                        if selected.TaxNote not in [None,]:
                            if len(selected.TaxNote.split("\n")) > 0:
                                if selected.TaxNote in ['',]:
                                    pass
                                else:
                                    for line in selected.TaxNote.split("\n"):
                                        if t in line:
                                            pass
                                        else:
                                            lines.append(line)
                            else:
                                pass
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.TaxNote='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)


    def rm_UserRating(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        lines=[]
                        
                        data={
                            'Attribute Being Rated':{
                            'type':'string',
                            'default':'Quality'
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="Generate Price Per Unit Of Qty of Each")
                        if fb is None:
                            return
                        t=f'{fb['Attribute Being Rated']} = '
                        
                        if selected.Description not in [None,]:
                            if len(selected.Description.split("\n")) > 0:
                                if selected.Description in ['',]:
                                    pass
                                else:
                                    for line in selected.Description.split("\n"):
                                        if t in line:
                                            pass
                                        else:
                                            lines.append(line)
                            else:
                                pass
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.Description='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def rm_costPerUnitOfEach(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach]] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description[CostPerUnitOfEach] which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        lines=[]
                        t='Price Per Unit Of Each = '
                        if selected.Description not in [None,]:
                            if len(selected.Description.split("\n")) > 0:
                                if selected.Description in ['',]:
                                    pass
                                else:
                                    for line in selected.Description.split("\n"):
                                        if t in line:
                                            pass
                                        else:
                                            lines.append(line)
                            else:
                                pass
                        #exit(f"{len(selected.Description.split("\n"))}")
                        selected.Description='\n'.join(lines)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def delete(self):
        while True:
            try:
                if self.code in [None,]:
                    barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[DELETE] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                    if barcode in ['d',None]:
                        return
                else:
                    barcode=self.code
                with Session(ENGINE) as session:
                    query=session.query(Entry).filter(or_(
                        Entry.Barcode==barcode,
                        Entry.Code==barcode,
                        Entry.Barcode.icontains(barcode),
                        Entry.Code.icontains(barcode),
                        Entry.Name.icontains(barcode)
                        ))
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print("Nothing Found")
                        if self.code in [None,]:
                            continue
                        else:
                            return

                    for num,entry in enumerate(results):
                        msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                        print(msg)
                    whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[DELETE]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="list")
                    if whiches is None:
                        return
                    elif whiches in [[],'d']:
                        return
                    for which in whiches:
                        try:
                            index=int(which)
                            try:
                                session.delete(results[index])
                                session.commit()
                            except Exception as e:
                                print(e)
                                session.rollback()
                        except Exception as e:
                            print(e)
                    break
            except Exception as e:
                print(e)
                return

    def appendToNote(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        data={
                        'Note':{
                            'type':'string',
                            'default':''
                            },
                        'DTOE':{
                            'type':'datetime',
                            'default':datetime.now()
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="Append To Note")
                        if fb is None:
                            return
                        else:
                            selected.Note+=f"\n{'+'*os.get_terminal_size().columns}\nAppended Note({datetime.now().ctime()}):\n{fb['Note']} \nDTOE:{fb['DTOE']}\n{'-'*os.get_terminal_size().columns}"
                            session.commit()
                            session.refresh(selected)
                            print(selected)
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def appendToDescription(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Desc] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        data={
                        'Description':{
                            'type':'string',
                            'default':''
                            },
                        'DTOE':{
                            'type':'datetime',
                            'default':datetime.now()
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="Append To Description")
                        if fb is None:
                            return
                        else:
                            selected.Description+=f"\n{'+'*os.get_terminal_size().columns}\nAppended Description({datetime.now().ctime()}):\n{fb['Description']} \nDTOE:{fb['DTOE']}\n{'-'*os.get_terminal_size().columns}"
                            session.commit()
                            session.refresh(selected)
                            print(selected)
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def DewDecimalSystemDesc(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Description]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        data={
                        'Dewey Decimal System No.':{
                            'type':'float',
                            'default':100
                            },
                        'Cutter No.':{
                            'type':'string',
                            'default':''
                            },
                        }
                        fb=FormBuilder(data=data,passThruText="Append To Description")
                        if fb is None:
                            return
                        else:
                            msg=f"Dewey Decimal System No.:{fb['Dewey Decimal System No.']} {fb['Cutter No.']}\n"
                            if msg not in selected.Description:
                                selected.Description+=msg
                            else:
                                selected.Description=selected.Description.replace(msg,'')
                            session.commit()
                            session.refresh(selected)
                            print(selected)
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def nonify_field(self):
        while True:
            try:
                with Session(ENGINE) as session:
                    locationFields=[str(i.name) for i in Entry.__table__.columns]
                    htext=[]
                    ct=len(locationFields)
                    for num, i in enumerate(locationFields):
                        htext.append(std_colorize(i,num,ct))
                    htext='\n'.join(htext)

                    whichField=Control(ptext=f'{htext}\nWhich field do you need to set to None?',helpText=f'{htext}',data='integer')
                    if whichField in BooleanAnswers.NONE:
                        return
                    if whichField not in range(0,ct):
                        continue

                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.{locationFields[whichField]}]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in BooleanAnswers.NONE:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        print('x')
                        selected=results[which]
                        setattr(selected,locationFields[whichField],None)
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                        break
            except Exception as e:
                print(e)

    def UnMarkUnPaid(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        if BooleanAnswers.DontLog in selected.Note:
                            selected.Note=selected.Note.replace(f"\n{BooleanAnswers.DontLog}\n",'')
                        
                        session.commit()
                        session.refresh(selected)
                        print(selected)
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def MarkUnPaid(self):
        try:
            while True:
                try:
                    if self.code in [None,]:
                        barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                        if barcode in ['d',None]:
                            return
                    else:
                        barcode=self.code
                    with Session(ENGINE) as session:
                        query=session.query(Entry).filter(or_(
                            Entry.Barcode==barcode,
                            Entry.Code==barcode,
                            Entry.Barcode.icontains(barcode),
                            Entry.Code.icontains(barcode),
                            Entry.Name.icontains(barcode)
                            ))
                        results=query.all()
                        ct=len(results)
                        if ct == 0:
                            print("Nothing Found")
                            if self.code in [None,]:
                                continue
                            else:
                                return

                        for num,entry in enumerate(results):
                            msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                            print(msg)
                        which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[Entry.Note]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                        if which in [None,]:
                            if not self.code:
                                continue
                            else:
                                break
                        elif which in ['d',]:
                            which=0
                        selected=results[which]
                        if BooleanAnswers.DontLog not in selected.Note:
                            selected.Note+=f"\n{BooleanAnswers.DontLog}\n"

                        session.commit()
                        session.refresh(selected)
                        print(selected)
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)


    def setFieldByName(self,fname):
        fnames=[]
        if isinstance(fname,str):
            fnames=[fname,]
        elif isinstance(fname,list):
            fnames=fname
        elif fname == None:
            try:
                fields=[
                    'Barcode',
                    'Code',
                    'Price',
                    'Description',
                    'Facings',
                    'UnitsDeep',
                    'UnitsHigh',
                    'Size',
                    'Tax',
                    'TaxNote',
                    'CRV',
                    'Name',
                    'Note',
                    'Location',
                    'ALT_Barcode',
                    'DUP_Barcode',
                    'CaseID_BR',
                    'CaseID_LD',
                    'CaseID_6W',
                    'LoadCount',
                    'PalletCount',
                    'ShelfCount',
                    'CaseCount',
                    'Expiry',
                    'BestBy',
                    'AquisitionDate',
                    'Tags',
                    ]
                fields.extend(LOCATION_FIELDS)
                fields=sorted(fields,key=str)
                fct=len(fields)
                t={i.name:str(i.type).lower() for i in Entry.__table__.columns}
                for num,f in enumerate(fields):

                    msg=std_colorize(f,num,fct)+f"{Fore.red}[{Fore.cyan}{t[f]}{Fore.red}]{Fore.light_yellow}!{Style.reset}"
                    print(msg)
                fnames=[]
                which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"which {Fore.light_green}index{Fore.light_red}({Fore.light_green}es{Fore.light_red}){Fore.light_yellow}?: ",helpText=f"which {Fore.light_green}index{Fore.light_red}({Fore.light_green}es{Fore.light_red}){Fore.light_yellow}, use comma to separate multiple fields{Style.reset}",data="list")
                if which in [None,]:
                    return
                elif which in ['d',]:
                    which=[0,]
                for i in which:
                    try:
                        fnames.append(fields[int(i)])
                    except Exception as e:
                        print(e)
                        try:
                            fnames.append(fields[fields.index(str(i))])
                        except Exception as e:
                            print(e)

            except Exception as e:
                print(e)
                return

        while True:
            try:
                if self.code in [None,]:
                    barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{fnames}] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
                    if barcode in ['d',None]:
                        return
                else:
                    barcode=self.code
                with Session(ENGINE) as session:
                    query=session.query(Entry).filter(or_(
                        Entry.Barcode==barcode,
                        Entry.Code==barcode,
                        Entry.Barcode.icontains(barcode),
                        Entry.Code.icontains(barcode),
                        Entry.Name.icontains(barcode)
                        ))
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print("Nothing Found")
                        if self.code in [None,]:
                            continue
                        else:
                            return

                    for num,entry in enumerate(results):
                        msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                        print(msg)
                    which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{fnames}]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                    if which in [None,]:
                        if not self.code:
                            continue
                        else:
                            break
                    elif which in ['d',]:
                        which=0
                    selected=results[which]
                    tax_adjusted=False
                    for fname in fnames:
                        column=getattr(Entry,fname)
                        oldprice=getattr(selected,'Price')
                        if fname.lower()  in ['tags','tag']:
                            TYPE="list"
                        else:
                            TYPE=str(column.type)
                        newValue=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{Fore.medium_violet_red}old{Fore.light_yellow}] {Fore.light_magenta}{fname} = {Fore.light_red}{getattr(selected,fname)}{Fore.orange_red_1} to: {Style.reset}",helpText="new value",data=TYPE)
                        if newValue in [None,'d']:
                            continue
                        if fname.lower() in ['tags','tag']:
                            newValue=json.dumps(newValue)
                        if fname.lower() == 'tax':
                            if not tax_adjusted:
                                setattr(selected,fname,newValue)
                        else:
                            setattr(selected,fname,newValue)

                        if fname.lower() == 'price':
                            session.commit()
                            session.refresh(selected)
                            self.costPerUnitOfEach_NoQty()
                            adjust_tax=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Adjust Tax using Price({newValue}),CRV({selected.CRV}), and the Tax Rate.",helpText="yes/no/boolean",data="boolean")
                            if adjust_tax in ['d',True]:
                                tax_adjusted=True
                                ROUNDTO=int(db.detectGetOrSet("lsbld ROUNDTO default",3,setValue=False,literal=True))
                                default_taxrate=round(float(db.detectGetOrSet("Tax Rate",0.0925,setValue=False,literal=True)),4)
                                
                                try:
                                    last_taxrate=float(decc(selected.Tax/(oldprice+selected.CRV),cf=4))
                                except Exception as e:
                                    print(e)
                                    last_taxrate=0
                                presets=f'''
{Fore.light_steel_blue}"f",'food','fd','reduced food','rdcd fd tx','rfd' - {decc(db.detectGetOrSet(f"preset food value",0.01,setValue=False,literal=True),cf=8)}
{Fore.light_yellow}'hot food tax','meals tax','hft','mlstx' - {decc(db.detectGetOrSet(f"preset hfd value",0.0917,setValue=False,literal=True),cf=8)}
{Fore.cyan}'medical','rx','med','untaxed','no taxed','ut','nt' - {decc(db.detectGetOrSet(f"preset untaxed value",0.0,setValue=False,literal=True),cf=8)}
{Fore.light_green}'t','tb','tobacco','tbco' - {decc(db.detectGetOrSet(f"preset tobacco value",0.053,setValue=False,literal=True),cf=8)}
{Fore.orange_red_1}'gm','general merchandise','v','vrty','variety' - {decc(db.detectGetOrSet(f"preset gm value",0.063,setValue=False,literal=True),cf=8)}{Style.reset}
'''
                                tax_rate=Prompt.__init2__(None,func=lambda text,data:FormBuilderMkText(text,data,passThru=['l','L','last','hft','mlstx','hot food tax','meals tax','ut','nt','untaxed','no taxed',"f",'food','fd','reduced food','rdcd fd tx','rfd','medical','rx','med','t','tb','tobacco','tbco','gm','general merchandise','v','vrty','variety'],PassThru=True),ptext=f"Tax(default={default_taxrate},{Fore.light_green}{['l','L','last']}{Fore.dark_goldenrod}last_tax_rate={Fore.light_red}{last_taxrate}{Fore.light_yellow}): ",helpText=f"{presets}\nWhat is the tax rate, default is {default_taxrate}; just hit enter.['l','L','last'] will use last taxrate {last_taxrate}.",data="float")
                                if tax_rate in [None,]:
                                    return selected.Tax,selected.CRV
                                elif tax_rate in ['d',]:
                                    tax_rate=default_taxrate
                                elif tax_rate in ['l','L','last']:
                                    tax_rate=last_taxrate
                                elif tax_rate in ["f",'food','fd','reduced food','rdcd fd tx','rfd',]:
                                    default_tx=0.01
                                    txname='food'
                                    tax_rate=decc(db.detectGetOrSet(f"preset {txname} value",default_tx,setValue=False,literal=True),cf=8)
                                elif tax_rate in ['hot food tax','meals tax','hft','mlstx']:
                                    default_tx=0.0917
                                    txname='hfd'
                                    tax_rate=decc(db.detectGetOrSet(f"preset {txname} value",default_tx,setValue=False,literal=True),cf=8)
                                elif tax_rate in ['medical','rx','med','untaxed','no taxed','ut','nt']:
                                    default_tx=0.0
                                    txname='untaxed'
                                    tax_rate=decc(db.detectGetOrSet(f"preset {txname} value",default_tx,setValue=False,literal=True),cf=8)
                                elif tax_rate in ['t','tb','tobacco','tbco',]:
                                    default_tx=0.053
                                    txname='tobacco'
                                    tax_rate=decc(db.detectGetOrSet(f"preset {txname} value",default_tx,setValue=False,literal=True),cf=8)
                                elif tax_rate in ['gm','general merchandise','v','vrty','variety']:
                                    default_tx=0.063
                                    txname='gm'
                                    tax_rate=decc(db.detectGetOrSet(f"preset {txname} value",default_tx,setValue=False,literal=True),cf=8)
                                    #print('x',type(price))
                                tax_rate=float(tax_rate)
                                tax=round(selected.Price+selected.CRV,ROUNDTO)*tax_rate
                                tax=round(tax,ROUNDTO)
                                selected.Tax=tax
                                session.commit()
                                session.refresh(selected)
                                if self.code in [None,]:
                                    continue
                                else:
                                    return
                            elif adjust_tax in [None,False]:
                                if self.code in [None,]:
                                    continue
                                else:
                                    return

                    session.commit()
                    session.flush()
                    session.refresh(selected)
                    print(selected)
            except Exception as e:
                print(e)
                break