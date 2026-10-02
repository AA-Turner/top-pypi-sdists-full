from radboy.DB.db import *
from radboy.DB.RandomStringUtil import *
import radboy.Unified.Unified as unified
import radboy.possibleCode as pc
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass

def today():
    dt=datetime.now()
    return date(dt.year,dt.month,dt.day)

#use this to store contacts
class MailBoxContacts(BASE,Template):
	__tablename__="MailBoxContacts"
	mbcid=Column(Integer,primary_key=True)
	#name
	FName=Column(String)
	MName=Column(String)
	LName=Column(String)
	Suffix=Column(String)

	#Email GMAIL ONLY for sending
	Email_Address=Column(String)
	app_password=Column(String)
	#Phone
	Phone_Number=Column(String)
	DTOE=Column(DateTime)

	def __init__(self,**kwargs):
		for k in kwargs.keys():
			if k in [s.name for s in self.__table__.columns]:
				setattr(self,k,kwargs.get(k))

#use this to store messages

class MailBox(BASE,Template):
	__tablename__="MailBox"
	mbid=Column(Integer,primary_key=True)

	Title=Column(String)
	MsgText=Column(String)
	
	#when the entry was made
	DTOE=Column(DateTime)
	
	#when the entry is due
	DUE_DTOE=Column(DateTime)
	
	#email addressing options
	Addressed_To_email=Column(String)
	Addressed_From_email=Column(String)
	

	#Phone messaging options
	Addressed_To_Phone=Column(String)
	Addressed_From_Phone=Column(String)

	def __init__(self,**kwargs):
		for k in kwargs.keys():
			if k in [s.name for s in self.__table__.columns]:
				setattr(self,k,kwargs.get(k))
@dataclass
class RxTx:
	def __init__(self,*args,**kwargs):
		print("This Class Has been depreacated and a new option will be designed. no more gmail. bleh!")