from radboy.DB.db import *
from radboy.DB.Prompt import *
from radboy.FB.FormBuilder import *
from radboy.FB.FBMTXT import *
from radboy.HealthLog.HealthLog import *

import pandas as pd
import csv
from datetime import datetime,date,time,timedelta
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
import nanoid

class RoutineDuration(BASE,Template):
    __tablename__="RoutineDuration"
    rdid=Column(Integer,primary_key=True)
    RoutineName=Column(String)
    Duration=Column(Float)
    DTOE=Column(DateTime)

    def __init__(self,**kwargs):
        kwargs['__tablename__']=self.__tablename__
        self.init(**kwargs,)

RoutineDuration.metadata.create_all(ENGINE)

class Exercise(BASE,Template):
    __tablename__="Exercise"
    exid=Column(Integer,primary_key=True)
    Name=Column(String,default=f'Generic Exercise Name [{nanoid.generate()}]')
    Note=Column(String,default=json.dumps({'completed':0}))
    Reps=Column(Integer,default=1) # 8 reps of 30 repcounts NAME
    RepCount=Column(Integer,default=30) #30 times rep
    CurrentRep=Column(Integer,default=0)
    cdt=Column(DateTime) #CurrentDateTime
    ldt=Column(DateTime) #LastDateTime

    def __init__(self,**kwargs):
        kwargs['__tablename__']=self.__tablename__
        self.init(**kwargs,)
        if 'cdt' not in kwargs.keys():
            self.cdt=datetime.now()

        if 'ldt' not in kwargs.keys():
            self.ldt=datetime.now()


class Routine(BASE,Template):
    __tablename__="Routine"
    roid=Column(Integer,primary_key=True)
    Name=Column(String)
    Note=Column(String)
    exid=Column(Integer)
    precedence=Column(Integer)
    doe=Column(Date)
    toe=Column(Time)
    dtoe=Column(DateTime)

    sdt=Column(DateTime) #StartDateTime
    edt=Column(DateTime) #EndDateTime

Exercise.metadata.create_all(ENGINE)
Routine.metadata.create_all(ENGINE)

'''
            #for use with header
            fieldname='ALL_INFO'
            mode='LU'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
'''
#header='{Fore.grey_70}[{Fore.light_steel_blue}{mode}{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} '
e_data={'Name':{
            'type':'str',
            'default':'',
            },
        'Note':{
            'type':'str',
            'default':'',
            },
        'Reps':{
           'type':'int',
           'default':8,
            },
        'RepCount':{
            'type':'int',
            'default':30,
            },
        'CurrentRep':{
            'type':'int',
            'default':'0',
            },
      }    

def gethpv(routine):
    with Session(ENGINE) as session:
        if isinstance(routine,dict):
            hpv=session.query(Routine).filter(Routine.Name==routine.get("Name")).order_by(Routine.precedence.desc()).first()
        elif isinstance(routine,Routine):
            hpv=session.query(Routine).filter(Routine.Name==getattr(routine,"Name")).order_by(Routine.precedence.desc()).first()
        else:
            raise Exception(f"Unsupported Type! {routine} -> type({type(routine)})")
        #print(hpv)
        if hpv:
            return hpv.precedence
        else:
            return 0

class ExerciseTracker:
    def newExercise(self):
        while True:
            try:
                newE=FormBuilder(data=e_data)
                if newE in [None,]:
                    return
                newEx=Exercise(**newE)

                with Session(ENGINE) as session:
                    check=session.query(Exercise)
                    for f in newE.keys():
                        check=check.filter(getattr(Exercise,f)==getattr(newEx,f))
                    results=check.all()
                    ct=len(results)
                    if ct > 0:
                        print(f"There is already an exercise with that data! {check}")
                    else:
                        session.add(newEx)
                        session.commit()
                        session.flush()
                        session.refresh(newEx)
                        print(newEx)

            except Exception as e:
                print(e)

    def searchExercise(self,returnable=False,oneShot=False):
        while True:
            try:
                search=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Search? ",helpText="What are you looking for in Name/Note/exid?",data="string")
                if search in [None,]:
                    return
                exid=None
                try:
                    exid=int(search)
                except Exception as e:
                    print(e,"exid will be None")
                    exid=None
                with Session(ENGINE) as session:
                    if search == 'd':
                        query=session.query(Exercise)
                    else:
                        query=session.query(Exercise).filter(or_(Exercise.Name.icontains(search),Exercise.Note.icontains(search),Exercise.exid==exid))
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print("no results")
                    if returnable:
                        return results
                    for num,i in enumerate(results):
                        msg=f'''{Fore.light_green}{num+1}/{Fore.light_yellow}{ct} -> {i}'''
                        print(msg)
                if oneShot:
                    break
            except Exception as e:
                print(e)

    def rmExercise(self):
        results=self.searchExercise(returnable=True,oneShot=True)
        ct=len(results)
        if ct == 0:
            print("nothing to delete")
        for num,i in enumerate(results):
            msg=f'''{Fore.light_magenta}{num}/{Fore.light_yellow}{ct} -> {i}'''
            print(msg)
        which=Prompt.__init2__(self,func=FormBuilderMkText,ptext="Which result[s(,) do you wish to delete?",helpText="comma separated list of indexes",data="list")
        if which in [None,'d']:
            print("nothing was selected!")
            return
        else:
            deleted=0
            with Session(ENGINE) as session:
                for i in which:
                    try:
                        exindex=int(i)
                        if exindex >= 0 and exindex <= ct:
                            exes=session.query(Exercise).filter(Exercise.exid==results[exindex].exid).all()
                            for e in exes:
                                session.query(Routine).filter(Routine.exid==e.exid).delete()
                                session.delete(e)
                                session.commit()
                                session.flush()
                            session.commit()
                            deleted+=1
                    except Exception as e:
                        print(e)
            print(f"deleted {deleted} exercises!")
             
    def editExercise(self):
        results=self.searchExercise(returnable=True,oneShot=True)
        ct=len(results)
        if ct == 0:
            print("nothing to edit")
        for num,i in enumerate(results):
            msg=f'''{Fore.light_magenta}{num}/{Fore.light_yellow}{ct} -> {i}'''
            print(msg)
        which=Prompt.__init2__(self,func=FormBuilderMkText,ptext="Which result[s(,) do you wish to edit?",helpText="comma separated list of indexes",data="list")
        if which in [None,'d']:
            print("nothing was selected!")
            return
        else:
            edited_=0
            with Session(ENGINE) as session:
                for i in which:
                    try:
                        exindex=int(i)
                        if exindex >= 0 and exindex <= ct:
                            exercise=session.query(Exercise).filter(Exercise.exid==results[exindex].exid).first()
                            print(f"{Fore.light_green}OLD{Style.reset} -> {exercise}")
                            data_l={}
                            for k in exercise.__table__.columns:
                                if k.name not in ['exid',]:
                                    data_l[k.name]={
                                    'default':getattr(exercise,k.name),
                                    'type':str(k.type)
                                    }
                            edited=FormBuilder(data=data_l)
                            if edited in [None,]:
                                continue
                            for k in edited:
                                setattr(exercise,k,edited[k])
                            session.commit()
                            session.flush()
                            session.refresh(exercise)
                            print(f"{Fore.light_magenta}EDITED{Style.reset} -> {exercise}")
                            edited_+=1
                    except Exception as e:
                        print(e)
            print(f"edited {edited_} exercises!")
    def newRoutine(self):
        with Session(ENGINE) as session:
            data_r={
            'Name':{
                'default':'',
                'type':'string',
                },
            }
            routine=FormBuilder(data=data_r)
            while True:
                exercises=self.searchExercise(returnable=True,oneShot=True)
                if exercises in [None,]:
                    break
                precedence=None

                precedence=gethpv(routine)
                for num,i in enumerate(exercises):
                    print(i)
                    use=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Use?",helpText="yes or no?",data="boolean")
                    if use in [None,]:
                        break
                    elif use in [True,]:
                        dtoe=datetime.now()
                        doe=date(dtoe.year,dtoe.month,dtoe.day)
                        toe=time(dtoe.hour,dtoe.minute,dtoe.second)
                        nt=gethpv(routine)
                        #print(nt)
                        nt+=1
                        rts=Routine(Name=routine.get("Name"),Note=json.dumps({'completed':0}),exid=i.exid,precedence=nt,doe=doe,dtoe=dtoe,toe=toe)
                        session.add(rts)
                        session.commit()
                        session.refresh(rts)
                        '''
                        self.clearRoutine(rts)
                        #print(gethpv(routine))
                        rout[num].Note=json.dumps({'completed':0})
                        session.commit()
                        session.flush()
                        session.refresh(rout[num])
                        '''
                    else:
                        pass
    def reset_routine(self):
        if not shield(self,mode='ExerciseTracker',fieldname='Routine',action_text='Delete All Routines'):
            with Session(ENGINE) as session:
                session.query(Routine).delete()
                session.commit()
                print(f"Remaining Routines: {session.query(Routine).count()}")

    def reset_exercises(self):
        if not shield(self,mode='ExerciseTracker',fieldname='Exercise',action_text='Delete All Exercises'):
            with Session(ENGINE) as session:
                session.query(Exercise).delete()
                session.commit()
                print(f"Remaining Exercises: {session.query(Exercise).count()}")

    def reset_er(self):
        self.reset_exercises()
        self.reset_routine()

    def Add2Routine(self):
        with Session(ENGINE) as session:
            fields={
                'are you adding a new excercise or using an old one [New=True,False=Old]?':{
                'default':True,
                'type':'boolean',
                },
                'Routine ID(RID)':{
                'default':None,
                'type':'integer'
                }
            }
            fd=FormBuilder(data=fields)
            if fd is not None:
                routine=session.query(Routine).filter(Routine.roid==fd['Routine ID(RID)']).first()
                if routine is None:
                    print(f"{Fore.orange_red_1}There is no Routine by that ID (Make sure it is an RID)")
                    return

                mode=fd['are you adding a new excercise or using an old one [New=True,False=Old]?']
                if mode in [None,True]:
                    excludes=['exid',]
                    tmp=Exercise()
                    session.add(tmp)
                    session.commit()
                    session.refresh(tmp)
                    fields={
                    i.name:{
                        'default':getattr(tmp,i.name),
                        'type':str(i.type).lower()
                        } for i in tmp.__table__.columns if i.name not in excludes
                    }
                    fd=FormBuilder(data=fields,passThruText=f"Create a New Exercise\n To Attach to Routine(roid={routine.roid},RoutineName={routine.Name})")
                    if fd is None:
                        print(f"{Fore.orange_red_1}User Cancelled!{Style.reset}")
                        session.delete(tmp)
                        session.commit()
                        return
                    try:
                        for k in fd:
                            setattr(tmp,k,fd[k])
                        session.commit()
                        session.refresh(tmp)
                        dtoe=datetime.now()
                        doe=date(dtoe.year,dtoe.month,dtoe.day)
                        toe=time(dtoe.hour,dtoe.minute,dtoe.second)
                        nt=gethpv(routine)
                        #print(nt)
                        nt+=1
                        rts=Routine(Name=getattr(routine,"Name"),Note=getattr(routine,"Note"),exid=tmp.exid,precedence=nt,doe=doe,dtoe=dtoe,toe=toe)
                        session.add(rts)
                        session.commit()
                    except Exception as e:
                        print(e,repr(e),str(e))
                        session.rollback()
                        session.commit()
                elif mode in [False,]:
                    excludes=['exid',]
                    fields={
                    'What are looking for':{
                        'type':'string',
                        'default':''
                        }
                    }
                    fd=FormBuilder(data=fields,passThruText="What are looking to copy to this routine?")
                    if fd is None:
                        print(f"{Fore.orange_red_1}User Cancelled!{Style.reset}")
                        return
                    search=fd['What are looking for']
                    OR=or_(Exercise.Name.icontains(search),Exercise.Note.icontains(search))
                    AND=and_(Exercise.Name.icontains(search),Exercise.Note.icontains(search))

                    query=session.query(Exercise).filter(or_(OR,AND))
                    ordered=orderQuery(query,Exercise.Name)
                    results=ordered.all()
                    cta=len(results)
                    htext=[]
                    for num,i in enumerate(results):
                        htext.append(std_colorize(i,num,cta))
                    htext='\n'.join(htext)
                    print(htext)
                    whichIndexes=Control(func=FormBuilderMkText,ptext="Which index(es)?",helpText=f"{htext}\nseperate the indexes by commas",data="list")
                    if whichIndexes in ['NaN',None,'d']:
                        print(f"{Fore.orange_red_1}User Cancelled!{Style.reset}")
                        return
                    elif whichIndexes in [[],]:
                        print(f"{Fore.orange_red_1}the list provided was empty, so user may have cancelled!{Style.reset}")
                        return
                    for index in whichIndexes:
                        try:
                            index=int(index)
                            exercise=results[index]
                            nex=Exercise()
                            fields={
                                i.name:{
                                    'default':getattr(exercise,i.name),
                                    'type':str(i.type).lower()
                                    } for i in exercise.__table__.columns if i.name not in excludes
                                }
                            for f in fields:
                                setattr(nex,f,getattr(exercise,f))
                            session.add(nex)
                            session.commit()
                            session.refresh(nex)
                            print(nex)
                            dtoe=datetime.now()
                            doe=date(dtoe.year,dtoe.month,dtoe.day)
                            toe=time(dtoe.hour,dtoe.minute,dtoe.second)
                            nt=gethpv(routine)
                            #print(nt)
                            nt+=1
                            rts=Routine(Name=getattr(routine,"Name"),Note=getattr(routine,"Note"),exid=nex.exid,precedence=nt,doe=doe,dtoe=dtoe,toe=toe)
                            session.add(rts)
                            session.commit()
                        except Exception as e:
                            print(e)
                            print(f"{Fore.magenta}Processing will attempt to continue!")
                print("Added Exercise to Routine!")
            else:
                print(f"{Fore.orange_red_1}User Cancelled!{Style.reset}")
                return

    def summarize(self):
        try:
            start=datetime.now()
            rs=self.viewRoutine(returnable=True)
            if rs == None:
                return
            whichList=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Which Routine would you like to use?",helpText="first number of a line",data="list")
            if whichList in ['d']:
                whichList=[]
            elif whichList in [None,]:
                return
            for which in whichList:
                routine=None
                try:
                    which=int(which)
                except Exception as e:
                    print(e)
                    continue
                if which in [None,]:
                    return
                elif which in ['d']:
                    routine=rs[0]
                else:
                    routine=rs[which]
                if routine != None:
                    print(routine)
                    with Session(ENGINE) as session:

                        rout=session.query(Routine).filter(Routine.Name==routine).order_by(Routine.precedence.asc()).all()
                        ct=len(rout)
                        completed=0
                        if ct < 1:
                            print(f"Nothing is in this routine '{rout}'")
                            return
                        total_lap=timedelta(seconds=0)
                        total_dur=''
                        for num,i in enumerate(rout):
                            ex=session.query(Exercise).filter(Exercise.exid==i.exid).first()
                            backColor=Back.black
                            try:
                                eta=ex.ldt-ex.cdt
                            except Exception as e:
                                eta=timedelta(seconds=0)
                            total_lap+=eta
                            msg=f'''{Fore.light_yellow}{num+1}/{Fore.light_red}{ct}{backColor} -> {Fore.cyan}[RNa]{i.Name} | {Fore.light_steel_blue}[RNo]{i.Note} | {Fore.light_sea_green}[RP]{i.precedence} | {Fore.light_salmon_1}[ENa]{ex.Name} | {Fore.light_yellow}[ER]{ex.Reps} | {Fore.dark_goldenrod}[ERC]{ex.RepCount} | {Fore.grey_50}[RID]{i.roid} | {Fore.grey_70}[ExID]{ex.exid}|{Fore.grey_50}[ExCDT]{ex.cdt}|{Fore.grey_70}{ex.ldt}|{Fore.light_steel_blue}[DUR]{eta}{Style.reset}'''
                            try:
                                total_dur=json.loads(i.Note).get('Total Duration')
                            except Exception as e:
                                print(e)
                            print(msg)
                        helper=f'''
        {Fore.light_yellow}#num#/{Style.reset} - of total
        {Fore.light_red}#ct# -> {Style.reset} - total exercises
        {Fore.cyan}[RNa]#Name# |{Style.reset} - Routine Name
        {Fore.light_steel_blue}[RNo]#Note# | {Style.reset} - Routine Note
        {Fore.light_sea_green}[RP]#precedence# |{Style.reset} - order number for exercise
        {Fore.light_salmon_1}[ENa]#Name# |{Style.reset} - Exercise Name
        {Fore.light_yellow}[ER]#Reps# |{Style.reset} - Exercise Reps
        {Fore.dark_goldenrod}[ERC]#RepCount# |{Style.reset} - Exercise Rep Count
        {Fore.grey_50}[RID]#roid# |{Style.reset} - Routine Id, or {Fore.light_red}roid{Style.reset}
        {Fore.grey_70}[ExID]#exid#{Style.reset} - Exercise Id, or {Fore.light_red}exid{Style.reset}
        {Fore.grey_50}[ExCDT]#DateTime# |{Style.reset} - exercise {Fore.light_red}started{Style.reset}
        {Fore.grey_70}[ExLDT]#DateTime#{Style.reset} - exercise {Fore.light_red}ended{Style.reset}
        {Fore.light_steel_blue}[DUR]#TimeDelta#{Style.reset} - exercise {Fore.light_sea_green}duration{Style.reset}
                        '''
                        print(helper)
                        print(f"{Fore.chartreuse_1}Total Last Lap Time is: {Fore.light_yellow}{total_lap}{Style.reset}")
                        print(f"{Fore.chartreuse_1}Total Duration is: {Fore.light_yellow}{total_dur}{Style.reset}")
        except Exception as e:
            print(e)

    def viewRoutine(self,returnable=False):
        with Session(ENGINE) as session:
            query=session.query(Routine).group_by(Routine.Name)
            results=query.all()
            ct=len(results)
            if ct < 1:
                print(f"{Fore.light_red}No Routine's available!{Style.reset}")
                return
            else:
                if returnable:
                    lite=[]
                for num,r in enumerate(results):
                    msg=f"{Fore.light_yellow}{num}/{Fore.light_red}{ct}{Style.reset}{Fore.light_steel_blue} -> {r.Name} (roid={r.roid}){Style.reset}"
                    print(msg)
                    if returnable:
                        lite.append(r.Name)
                if returnable:
                    return lite

    def viewRoutineList(self,returnable=False):
        with Session(ENGINE) as session:
            query=session.query(Routine).order_by(Routine.roid)
            results=query.all()
            ct=len(results)
            if ct < 1:
                print(f"{Fore.light_red}No Routine's available!{Style.reset}")
                return
            else:
                if returnable:
                    lite=[]
                hr=None
                for num,r in enumerate(results):

                    ex=session.query(Exercise).filter(Exercise.exid==r.exid).first()
                    if ex:
                        name,note,exid=ex.Name,ex.Note,ex.exid
                    else:
                        name,note,exid="NotFound?","NotFound?","NotFound?"
                    msg=f"{Fore.light_yellow}{num}/{Fore.light_red}{ct}{Style.reset}{Fore.light_steel_blue} -> {r.Name}  (roid={r.roid},exid={exid}) Exercise(Name='{name}',Note='{note}',exid='{exid}'){Style.reset}"
                    print(msg)
                    if returnable:
                        lite.append(r.Name)
                    if hr != r.Name and num != 0:
                        if hr != None:
                            print(f"{'*'*os.get_terminal_size().columns}")
                        hr=r.Name
                if returnable:
                    return lite

    def useRoutine(self,reset_only=False,reset_note=False):
        try:
            
            logMe=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Log a comment in HealthLog(hl[default=True/Yes])?",helpText="yes or no/boolean",data="boolean")
            if logMe is None:
                return
            elif logMe in ['d',]:
                logMe=True
            
            start=datetime.now()
            rs=self.viewRoutine(returnable=True)
            if rs == None:
                return

           
            whichList=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Which Routine would you like to use?",helpText="first number of a line",data="list")
            if whichList in ['d']:
                whichList=[]
            elif whichList in [None,]:
                return
            
            for which in whichList:
                try:
                    which=int(which)
                except Exception as e:
                    print(e)
                    continue
                routine=None
                if which in [None,]:
                    return
                elif which in ['d']:
                    routine=rs[0]
                else:
                    routine=rs[which]
                if routine != None:
                    print(routine)
                    with Session(ENGINE) as session:
                        rout=session.query(Routine).filter(Routine.Name==routine).order_by(Routine.precedence.asc()).all()
                        ct=len(rout)
                        completed=0
                        if ct < 1:
                            print(f"Nothing is in this routine '{rout}'")
                            return
                        total_reps=0
                        completed_reps=0
                        for num, i in enumerate(rout):
                            exercise=session.query(Exercise).filter(Exercise.exid==i.exid).first()
                            total_reps+=exercise.Reps
                       
                        for num, i in enumerate(rout):
                                exercise=session.query(Exercise).filter(Exercise.exid==i.exid).first()
                                exercise.CurrentRep=0
                                #total_reps+=exercise.Reps
                                session.commit()
                                session.refresh(exercise)
                        
                        if reset_note:
                            for num, i in enumerate(rout):
                                rout[num].Note=json.dumps({'completed':0})
                                session.commit()
                                session.flush()
                                session.refresh(rout[num])
                        if reset_only:
                            #resume
                            if logMe:
                                hl=HealthLog(Comments=f"{exercise.Name}:Exercise({i})\t\nResetting! {datetime.now().ctime()}")
                                session.add(hl)
                                session.commit()
                            continue
                            #return
                        total_dur=timedelta(seconds=0)
                        l=0
                        while completed < total_reps:
                            lapStart=datetime.now()
                            for num, i in enumerate(rout):
                                if completed_reps > total_reps:
                                    completed=ct
                                    if logMe:
                                        hl=HealthLog(Comments=f"{exercise.Name}:Exercise({i})\t\nCompleted Stage 2! {datetime.now().ctime()}")
                                        session.add(hl)
                                        session.commit()
                                    break
                                exercise=session.query(Exercise).filter(Exercise.exid==i.exid).first()
                                exercise.cdt=datetime.now()
                                
                                if exercise.CurrentRep < exercise.Reps:
                                    setattr(exercise,"CurrentRep",getattr(exercise,"CurrentRep")+1)
                                    if logMe:
                                        hl=HealthLog(Comments=f"{exercise.Name}:Exercise({i})\t\nstarted! {datetime.now().ctime()}")
                                        session.add(hl)
                                        session.commit()
                                else:
                                    setattr(exercise,"CurrentRep",getattr(exercise,"CurrentRep"))
                                    completed+=1
                                    #completed_reps+=1
                                    if logMe:
                                        hl=HealthLog(Comments=f"{exercise.Name}:Exercise({i})\t\nResuming! {datetime.now().ctime()}")
                                        session.add(hl)
                                        session.commit()
                                    continue
                                #os.system("clear")
                                session.commit()
                                session.refresh(exercise)
                                old=json.loads(rout[num].Note).get("completed")
                                #print(exercise,rout[num],completed_reps,completed_reps < json.loads(rout[num].Note).get("completed"))
                                print(exercise)
                                if old == completed_reps:
                                    while True:
                                        nxt=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"(ELAPSED:{datetime.now()-start})({completed_reps+1}/{total_reps}|{round(((completed_reps+1)/total_reps)*100,2)})Next?",helpText="Go to next exercise, just hit enter, or q to quit it will remember for the most part. And to See the current exercise type 'remind' or 'rmnd' & 'hl','healthlog','health log','hlth lg' to access the health log menu",data="string")
                                        #print(nxt)
                                        setattr(exercise,'ldt',datetime.now())
                                        total_dur+=(exercise.ldt-exercise.cdt)
                                        session.commit()
                                        session.refresh(exercise)
                                        if nxt in [None,]:
                                            return
                                        elif nxt.lower() in ['remind','rmnd']:
                                            print(exercise)
                                            continue
                                        elif nxt.lower() in ['hl','healthlog','health log','hlth lg']:
                                            HealthLogUi()
                                            print(exercise)
                                            continue
                                        else:
                                            break
                                #print(completed_reps)
                                completed_reps+=1
                                if old > completed_reps:
                                    if logMe:
                                        hl=HealthLog(Comments=f"{exercise.Name}:Exercise({i})\t\nCompleted Stage 1! {datetime.now().ctime()}")
                                        session.add(hl)
                                        session.commit()
                                    continue
                                for num2, i in enumerate(rout):
                                    rout[num2].Note=json.dumps({'completed':completed_reps,'Total Duration':str(total_dur)})
                                session.commit()
                                session.flush()
                                session.refresh(rout[num])
                            if completed < ct:
                                l+=1
                                logName=f'{routine}-Lap-{l}'
                                lapdur=datetime.now()-lapStart
                                ld=RoutineDuration(RoutineName=logName,Duration=lapdur.total_seconds(),DTOE=datetime.now())
                                session.add(ld)
                                session.commit()
                                session.flush()
                                session.refresh(ld)
                                print(ld)
                                lapMsg=f'{Fore.light_green}Lap Time: {Style.bold}{Fore.cyan}{lapdur}{Style.reset}'
                                print(lapMsg)
                        tdMsg=f'{Fore.light_red}Current Elapsed Time: {Style.bold}{Fore.green_yellow}{str(total_dur)}{Style.reset}'
                        print(tdMsg)
                        rd=RoutineDuration(RoutineName=routine,Duration=total_dur.total_seconds(),DTOE=datetime.now())
                        session.add(rd)
                        session.commit()
                        session.refresh(rd)
                        if logMe:
                            hl=HealthLog(Comments=f"{exercise.Name}:Exercise({i})\t\nCompleted Stage 3! {datetime.now().ctime()}")
                            session.add(hl)
                            session.commit()
                        print(rd)
        except Exception as e:
            print(e)
    def removeRoutine(self):
        try:
            rs=self.viewRoutine(returnable=True)
            which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Which Routine would you like to use?",helpText="first number of a line",data="integer")
            routine=None
            if which in [None,]:
                return
            elif which in ['d']:
                routine=None
            else:
                routine=rs[which]
            if routine != None:
                with Session(ENGINE) as session:
                    rr=session.query(Routine).filter(Routine.Name==routine).delete()
                    session.commit()
                    session.flush()
        except Exception as e:
            print(e)

    def clearRoutine(self):
        self.useRoutine(reset_only=True,reset_note=True)

    def __init__(self):
        fieldname='Menu'
        mode='ExerciseTracker'
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
        header='{Fore.grey_70}[{Fore.light_steel_blue}{mode}{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} '

        helpText=f'''{Fore.light_green}Exercises{Fore.grey_70}
    ** ne,NewExercise - create a new exercise
    ** re,RemoveExercise - delete an exercise
    ** se,SearchExercise - search for an exercise from it's Note,Name, or ID
    ** ee,EditExercise - edit an exercise
{Fore.dark_goldenrod}Routines{Fore.grey_70}
    ** nr,NewRoutine - a new routine of exercises
    ** vr,ViewRoutines - show available routines
    ** vrl,ViewRoutines - show available routines and their exercises as a list
    ** a2r,add2routine - add an exercise to a routine specified by RID
    ** ur,UseRoutine - use a set routine
    ** rr,RemoveRoutine - delete a routine
    ** cr,ClearRoutine - reset routine CurrentRep
    ** su,summarize,Summarize - show the contents of a specified Routine
{Fore.orange_red_1}DANGER{Fore.grey_70}
    ** rst rtn,reset routine,reset-routine - delete all routines {Fore.light_red}ONLY{Fore.grey_70}
    ** rst ex,reset exercises,reset-exercises - delete all exercises {Fore.light_red}ONLY{Fore.grey_70}
    ** rst a,reset all,reset-all - delete {Fore.dark_goldenrod}<{Fore.orange_red_1}<<{Fore.medium_violet_red}<<{Fore.light_cyan}Everything{Fore.medium_violet_red}>>{Fore.orange_red_1}>>{Fore.dark_goldenrod}> {Fore.cyan} in the ExerciseTracker!
{Fore.light_salmon_1}WARNING{Fore.grey_70}
    ignore '**' ; this is not part of the cmd; it's just a bullet point representation.
{Style.reset}'''
        while True:
            doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h} Do what?",helpText=helpText,data="string")
            if doWhat in [None,]:
                return
            elif doWhat in ['d',]:
                print(helpText)
                continue
            elif doWhat.lower() in ['NewExercise'.lower(),'ne']:
                self.newExercise()
            elif doWhat.lower() in ['RemoveExercise'.lower(),'re']:
                self.rmExercise()
            elif doWhat.lower() in ['se','SearchExercise'.lower()]:
                self.searchExercise()
            elif doWhat.lower() in ['ee','EditExercise'.lower()]:
                self.editExercise()
            elif doWhat.lower() in ['nr','NewRoutine'.lower()]:
                self.newRoutine()
            elif doWhat.lower() in ['vr','ViewRoutine'.lower()]:
                self.viewRoutine()
            elif doWhat.lower() in ['vrl','ViewRoutineList'.lower()]:
                self.viewRoutineList()
            elif doWhat.lower() in ['ur','UseRoutine'.lower()]:
                self.useRoutine()
            elif doWhat.lower() in ['rr','RemoveRoutine'.lower()]:
                self.removeRoutine()
            elif doWhat.lower() in ['cr','ClearRoutine'.lower()]:
                self.clearRoutine()
            elif doWhat.lower() in ['hl','healthlog'.lower()]:
                HealthLogUi()
            elif doWhat.lower() in "su,summarize".split(","):
                self.summarize()
            elif doWhat.lower() in 'a2r,add2routine'.split(","):
                self.Add2Routine()
            elif doWhat.lower() in 'rst rtn,reset routine,reset-routine'.split(','):
                self.reset_routine()
            elif doWhat.lower() in 'rst ex,reset exercises,reset-exercises'.split(','):
                self.reset_exercises()
            elif doWhat.lower() in 'rst a,reset all,reset-all'.split(','):
                self.reset_er()