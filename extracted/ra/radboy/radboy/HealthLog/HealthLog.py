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
import json,sys,math,re,calendar
import plotext as plt
import pint_pandas
import radboy.DB.ExerciseTracker as ET
import zipfile
from copy import copy

class HealthLogUi:
	def edit_hlid(self):
		with Session(ENGINE) as session:
			hlid=Prompt.__init2__(None,func=FormBuilderMkText,ptext="HLID to Edit?: ",helpText="what healthlod id do you wish to edit?",data="integer")
			if hlid is None:
				return
			elif hlid in ['d',]:
				return
			else:
				hl=session.query(HealthLog).filter(HealthLog.HLID==hlid).first()
				if hl:
					print(std_colorize(f"Updated {hl}",0,1))
					excludes=['HLID',]
					fields={
						i.name:{
							'default':getattr(hl,i.name),
							'type':str(i.type).lower(),
						} for i in hl.__table__.columns if i.name not in excludes
					}
					fd=FormBuilder(data=fields)
					if fd is None:
						return
					for k in fd:
						setattr(hl,k,fd[k])
					session.commit()
					session.refresh(hl)
					print(std_colorize(f"Updated {hl}",0,1))

	def new_health_log(self):
		with Session(ENGINE) as session:
			hl=HealthLog()
			excludes=['HLID','DTOE',]
			def retVal(i):
				if i == None:
					return None
				else:
					return i.arg
			fields={
			str(i.name):{
				'default':retVal(i.default),
				'type':str(i.type).lower(),
				} for i in hl.__table__.columns if str(i.name) not in excludes
			}
			data=FormBuilder(data=fields)
			if data in [None,]:
				return
			for i in data:
				setattr(hl,i,data[i])
			session.add(hl)
			session.commit()
			session.refresh(hl)
			print(hl)

	def add_healthlog_specific(self,useColumns=[]):
		if 'Comments' not in useColumns:
			useColumns.append('Comments')
		excludes=['HLID','DTOE',]
		barcode=''
		with Session(ENGINE) as session:
			entry=None
			if 'EntryBarcode' in useColumns:
				h=f'{Fore.light_red}HealthLog{Fore.light_yellow}@{Style.bold}{Fore.deep_sky_blue_3b}AHS{Fore.light_yellow} : '
				barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Barcode|Code|Name[b=skips search]: ",helpText="what was consumed?",data="string")
				if barcode not in [None,'d']:
					while True:
						try:
							entry=session.query(Entry).filter(or_(Entry.Barcode==barcode,Entry.Barcode.icontains(barcode),Entry.Name.icontains(barcode),Entry.Code==barcode,Entry.Code.icontains(barcode)))

							entry=orderQuery(entry,Entry.Timestamp)
							entry=entry.all()
							ct=len(entry)
							if ct > 0:
								htext=[]
								for num, i in enumerate(entry):
									msg=f"{Fore.light_red}{num}/{Fore.medium_violet_red}{num+1} of {Fore.light_sea_green}{ct} -> {i.seeShort()}"
									htext.append(msg)
									print(msg)
								htext='\n'.join(htext)
								which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Which {Fore.light_red}index?{Fore.light_yellow}",helpText=f"{htext}\n{Fore.light_red}number{Fore.light_yellow} farthest to left of screen{Style.reset}",data="integer")
								if which not in [None,]:
									excludes.extend(["EntryBarcode","EntryName","EntryId"])
									if which == 'd':
										entry=entry[0]
									else:
										entry=entry[which]
								else:
									htext=f"{Fore.orange_red_1}No Results for '{Fore.cyan}{barcode}{Fore.orange_red_1}'{Style.reset}"
									again=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Try another search?[yes/no=default]",helpText=htext,data="boolean")
									if again is None:
										return
									elif again in [False,'d']:
										entry=None
										break
									else:
										barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Barcode|Code|Name[b=skips search]: ",helpText="what was consumed?",data="string")
										continue
									
							else:
								entry=None
								htext=f"{Fore.orange_red_1}No Results for '{Fore.cyan}{barcode}{Fore.orange_red_1}'{Style.reset}"
								again=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Try another search?[yes/no=default]",helpText=htext,data="boolean")
								if again is None:
									return
								elif again in [False,'d']:
									break
								else:
									barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Barcode|Code|Name[b=skips search]: ",helpText="what was consumed?",data="string")
									continue
							break
						except Exception as e:
							print(e)
							return

			hl=HealthLog()
			
			def retVal(i):
				if i == None:
					return None
				else:
					return i.arg
			fields={
			str(i.name):{
				'default':retVal(i.default),
				'type':str(i.type).lower(),
				} for i in hl.__table__.columns if str(i.name) not in excludes and str(i.name) in useColumns
			}
			if fields in [{},None]:
				print(fields,"empty!")
				return
			data=FormBuilder(data=fields)
			if data is None:
				return
			if 'LongActingInsulinName' in useColumns or 'ShortActingInsulinName' in useColumns:
				def searchNames(code):
					mp=[]
					for im in string.printable:
						mp.extend([f'{im}'*i for i in range(os.get_terminal_size().columns)])
					if code is None:
						if 'LongActingInsulinName' in useColumns:
							return 'Long Acting Insuline Unspecificied - see comments'
						elif 'ShortActingInsulinName' in useColumns:
							return 'Short Acting Insulin Unspecificied - see comments'
						else:
							return 'see comments'
					elif code in ['d','',*mp]:
						if 'LongActingInsulinName' in useColumns:
							return 'Long Acting Insuline Unspecificied - see comments'
						elif 'ShortActingInsulinName' in useColumns:
							return 'Short Acting Insulin Unspecificied - see comments'
						else:
							return 'see comments'
					with Session(ENGINE) as session:
						query=session.query(Entry)
						filters=[
							Entry.Barcode.icontains(code),
							Entry.Code.icontains(code),
							Entry.Name.icontains(code)
						]
						results=query.filter(or_(*filters)).all()
						ct=len(results)
						if ct == 0:
							msg=f"{Fore.orange_red_1}Nothing was found to match {Fore.grey_15}'{code}'{Style.reset}"
							print(msg)
							return code
						htext=[]
						print(f"{Fore.orange_red_1}Getting Results({Fore.light_green}{ct}{Fore.orange_red_1}) for Display!{Style.reset}")
						for num,i in enumerate(results):
							msg=f"{Fore.light_cyan}{num}/{Fore.light_magenta}{num+1} of {Fore.light_red}{ct} {Fore.medium_violet_red} -> {i.seeShort()}"
							htext.append(msg)
						htext='\n'.join(htext)
						while True:
							try:
								print(htext)
								which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Which {Fore.light_cyan}index{Fore.light_yellow}?",helpText=htext+f"\n Pick a {Fore.light_cyan}number in this color{Fore.light_yellow}. Back keeps original {Fore.grey_15}{code}{Fore.light_yellow}",data="integer")
								if which in [None,]:
									return code
								elif which in ['d',]:
									which=0
									out=f"'Name':'{results[which].Name}','BARCODE':'{results[which].Barcode}','Code':'{results[which].Code}'"
									out="{"+out+"}"
									return out
								else:
									out=f"'Name':'{results[which].Name}','BARCODE':'{results[which].Barcode}','Code':'{results[which].Code}'"
									out="{"+out+"}"
									return out
							except Exception as e:
								print(e)
								return code
				if 'LongActingInsulinName' in useColumns:
					data['LongActingInsulinName']=searchNames(data['LongActingInsulinName'])
				elif 'ShortActingInsulinName' in useColumns:
					data['ShortActingInsulinName']=searchNames(data['ShortActingInsulinName'])
				else:
					print("You Should not be having 'ShortActingInsulinName and LongActingInsulinName in add_healthlog_specific(useColumns)!")
					return
				'''search for name in entry and auto replace name'''

			if 'EntryBarcode' in useColumns and entry != None:
				if data is not None:
					data['EntryBarcode']=entry.Barcode
					data['EntryName']=entry.Name
					data['EntryId']=entry.EntryId

			if data in [None,]:
				return
			for i in data:
				setattr(hl,i,data[i])
			session.add(hl)
			session.commit()
			session.refresh(hl)
			print(f"{Fore.light_steel_blue}HLID={Fore.light_green}{hl.HLID}{Fore.light_steel_blue}/"+f"{Style.reset}{Fore.medium_violet_red}|{Fore.light_steel_blue}".join([f'{i}' for i in useColumns])+f"{Style.reset}")
			print(f"{Fore.light_steel_blue}HLID={Fore.light_green}{hl.HLID}{Fore.light_steel_blue}/"+f'{Style.reset}{Fore.medium_violet_red}|{Fore.light_steel_blue}'.join(str(getattr(hl,i)) for i in useColumns)+f"{Style.reset}")
	
	def del_hlid(self):
		try:
			with Session(ENGINE) as session:
				h=f"{Fore.light_red}HealthLog{Fore.light_yellow}@{Style.bold}{Fore.deep_sky_blue_3b}DEL{Fore.light_yellow} : "
				HLID_=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}HLID to delete?",helpText="what id do you wish to delete, or list of ids",data="list")
				if HLID_ in [None,'d']:
					return
				for HLID in HLID_:
					try:
						HLID=int(HLID)
						x=session.query(HealthLog).filter(HealthLog.HLID==HLID).delete()
						session.commit()
						session.flush()
						x=session.query(HealthLog).filter(HealthLog.HLID==HLID).all()
					except Exception as e:
						print(e)
				print(len(x),"IDS remains!")
		except Exception as e:
			print(e)

	def showAll(self):
		try:
			with Session(ENGINE) as session:
				results=session.query(HealthLog)
				results=orderQuery(results,HealthLog.DTOE)
				results=results.all()
				ct=len(results)
				for num,i in enumerate(results):
					view=[]
					for x in i.__table__.columns:
						if getattr(i,str(x.name)) not in [None]:
							view.append(f'{Fore.green_3b}{Style.bold}{str(x.name)}{Fore.deep_sky_blue_1}={Fore.sea_green_2}{str(getattr(i,str(x.name)))}{Style.reset}')
					msg=f"{Fore.light_green}{num}{Fore.light_yellow}/{num+1} of {Fore.light_red}{ct} ->{'|'.join(view)}"
					print(msg)
		except Exception as e:
			print(e)

	def export_log(self):
		useDateRange=Prompt.__init2__(None,func=FormBuilderMkText,ptext="use a date range?",helpText="yes or no",data="boolean")
		if useDateRange is None:
			return
		elif useDateRange in ['d',]:
			useDateRange=True
		fil=Path("HealthLogAll.xlsx")
		output=pd.ExcelWriter(fil)
		with Session(ENGINE) as session:
			query=session.query(HealthLog)
			query=orderQuery(query,HealthLog.DTOE)
			if useDateRange:
				default_sd=datetime.now()-timedelta(days=30)
				start_date=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Start Date(default = {default_sd}):",helpText="start date",data="datetime")
				if start_date is None:
					return
				elif start_date in ['d',]:
					start_date=default_sd

				default_ed=datetime.now()
				end_date=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"End Date(default = {default_ed}):",helpText="end date",data="datetime")
				if end_date is None:
					return
				elif end_date in ['d',]:
					end_date=default_ed

				query=query.filter(and_(HealthLog.DTOE>=start_date,HealthLog.DTOE<=end_date))

			df=pd.read_sql(query.statement,session.bind)
			
			#str.replace(lambda x:x,lambda x:strip_colors(x))
			#df=df.apply(remove_illegals)
			def remove_illegals(x):
				return x
			for i in df:
				df[i]=df[i].apply(lambda x:remove_illegals(strip_colors(x)) if isinstance(x,str) else x)
				#df[i]=df[i].apply(remove_illegals)
			sheetName="HealthLog"
			df.to_excel(output,sheet_name=sheetName,index=False)

			try:
				for column in df:
					column_length = 5+len(column)+5
					col_idx = df.columns.get_loc(column)
					output.sheets[sheetName].set_column(col_idx, col_idx, column_length)

					col_idx = df.columns.get_loc('DTOE')
					dtoe_length = max(df['DTOE'].astype(str).map(len).max(), len('DTOE'))
					output.sheets[sheetName].set_column(col_idx, col_idx, dtoe_length)

				
				output.close()
			except Exception as e:
				print(e)


			with zipfile.ZipFile(BooleanAnswers.HealthLogZip,"w") as oz:
				oz.write(output)
			print(fil.absolute())
			print(f"{Fore.orange_red_1}The Below file only contains the above files!{Style.reset}")
			print(BooleanAnswers.HealthLogZip.absolute())

	def export_log_field(self,fields=[],not_none=[]):
		useDateRange=Prompt.__init2__(None,func=FormBuilderMkText,ptext="use a date range?",helpText="yes or no",data="boolean")
		if useDateRange is None:
			return
		elif useDateRange in ['d',]:
			useDateRange=True

		if 'DTOE' not in fields:
			fields.append('DTOE')
		if 'Comments' not in fields:
			fields.append('Comments')
		fil=Path(f"HealthLog-fields.xlsx")
		output=pd.ExcelWriter(fil)
		not_none=[i for i in HealthLog.__table__.columns if str(i.name) in not_none]
		with Session(ENGINE) as session:
			query=session.query(HealthLog).filter(or_(*[i!=None for i in not_none]))
			query=orderQuery(query,HealthLog.DTOE)
			if useDateRange:
				default_sd=datetime.now()-timedelta(days=30)
				start_date=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Start Date(default = {default_sd}):",helpText="start date",data="datetime")
				if start_date is None:
					return
				elif start_date in ['d',]:
					start_date=default_sd

				default_ed=datetime.now()
				end_date=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"End Date(default = {default_ed}):",helpText="end date",data="datetime")
				if end_date is None:
					return
				elif end_date in ['d',]:
					end_date=default_ed

				query=query.filter(and_(HealthLog.DTOE>=start_date,HealthLog.DTOE<=end_date))
			query=orderQuery(query,HealthLog.DTOE)
			df=pd.read_sql(query.statement,session.bind)

			df=df[fields]
			def remove_illegals(x):
				return x
			for i in df:
				df[i]=df[i].apply(lambda x:remove_illegals(strip_colors(x)) if isinstance(x,str) else x)
			
			sheetName="HealthLog"
			df.to_excel(output,sheet_name=sheetName,index=False)

			try:
				for column in df:
					column_length = 5+len(column)+5
					col_idx = df.columns.get_loc(column)
					output.sheets[sheetName].set_column(col_idx, col_idx, column_length)

					col_idx = df.columns.get_loc('DTOE')
					dtoe_length = max(df['DTOE'].astype(str).map(len).max(), len('DTOE'))
					output.sheets[sheetName].set_column(col_idx, col_idx, dtoe_length)

					
				
				output.close()

			except Exception as e:
				print(e)
			with zipfile.ZipFile(BooleanAnswers.HealthLogZip,"w") as oz:
				oz.write(output)
			print(fil.absolute())
			print(f"{Fore.orange_red_1}The Below file only contains the above files!{Style.reset}")
			print(BooleanAnswers.HealthLogZip.absolute())


	def fixtable(self):
		HealthLog.__table__.drop(ENGINE)
		HealthLog.metadata.create_all(ENGINE)


	def GraphIt(self,query,session,fields=['BloodSugar','HeartRate'],errors=True):
		while True:
			print(f"{Fore.light_magenta}Dates on the Graph(s) are in the format of {Fore.orange_red_1}Day/Month/Year{Fore.light_magenta}, whereas Date Input will remain {Fore.light_steel_blue}Month/Day/Year{Style.reset}")
			df_from_records = pd.read_sql_query(query.statement,session.bind)
			
			for num,field in enumerate(fields):
				try:
					if 'DrugQtyConsumed' == field:
						names=df_from_records['DrugConsumed'].unique()
						for name in names:
							
							
							q=session.query(HealthLog).filter(and_(HealthLog.DrugConsumed==name,HealthLog.DrugQtyConsumed!=None))
							dfTmp=pd.read_sql_query(q.statement,session.bind)

							dfTmp['DTOES']=dfTmp['DTOE'].dt.strftime("%d/%m/%Y")
							z=[[v,u] for v,u in zip(dfTmp[field],dfTmp['DrugQtyConsumedUnitName'])]
							units=[i for i in dfTmp['DrugQtyConsumedUnitName'].unique()]
							

							for i in z:
								print(pint.Quantity(i[0],i[1]).magnitude,i[-1])
							unit=''

							while True:
								try:
									unit=Prompt.__init2__(self,func=FormBuilderMkText,ptext=f"unit of measure to convert all to?[{units}]",helpText=f"{units}",data="string")
									if unit is None:
										return
									elif unit in ['d',]:
										unit="milligram"
									if unit not in units:
										continue

									dfTmp['qty']=[pint.Quantity(v,u).to(unit).magnitude for v,u in zip(dfTmp[field],dfTmp['DrugQtyConsumedUnitName']) ]
									break
								except Exception as e:
									print(e)
							barLabel=f'Maxes {field}:{name} {unit}'
							plt.bar(dfTmp['DTOES'],dfTmp['qty'],label=barLabel)
							plt.show()
							plt.clf()
							print(f"{Fore.orange_red_1}{barLabel}{Style.reset}")

							plt.scatter(dfTmp['DTOES'],dfTmp['qty'],label=barLabel)
							plt.show()
							plt.clf()
							print(f"{Fore.orange_red_1}{barLabel}{Style.reset}")
							try:
								mx=int(dfTmp['qty'].max())
								multiplier=1
								while mx < 1:
									multiplier*=10
									mx=int(dfTmp['qty'].max()*multiplier)
								histoLabel=f"{multiplier}X -> Histogram {field}:{name}"
								bins=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Histogram Bins[5]",helpText="5",data="integer")
								if bins is None:
									return
								elif bins in ['d',]:
									bins=5
								plt.hist(dfTmp['qty'],bins=bins,label=histoLabel)
								plt.show()
								plt.clf()
								print(f"{Fore.magenta}{histoLabel}total Entry Data Points = {len(dfTmp[field])}{Style.reset}")
							except Exception as e:
								if errors:
									print(e)

							try:
								df_from_records['tsa']=pd.to_datetime(df_from_records['DTOE'])
								times_recorded=[int(f"{i.hour}") for i in df_from_records['tsa']]
								bins=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Histogram Bins[bins for 24H]",helpText=f"bins for 24H",data="integer")
								if bins is None:
									return
								elif bins in ['d',]:
									bins=24
								plt.hist(times_recorded,bins=bins,label=histoLabel)
								plt.show()
								plt.clf()
								print(f"{Fore.orange_red_1}Hours of the Day Recorded{Fore.magenta}{histoLabel}total Entry Data Points = {len(dfTmp[field])}{Style.reset}")
							except Exception as e:
								if errors:
									print(e,'#ec2')
					
					barLabel=f'Maxes {field} TotalView:Bar'
					
					df_from_records['DTOES']=df_from_records['DTOE'].dt.strftime("%d/%m/%Y")
					plt.bar(df_from_records['DTOES'],df_from_records[field],label=f'Maxes {field}')
					plt.show()
					plt.clf()
					print(f"{Fore.light_green}{barLabel}{Style.reset}")

					barLabel=f'Maxes {field} TotalView:Scatter'
					
					df_from_records['DTOES']=df_from_records['DTOE'].dt.strftime("%d/%m/%Y")
					plt.scatter(df_from_records['DTOES'],df_from_records[field],label=f'Maxes {field}')
					plt.show()
					plt.clf()
					print(f"{Fore.light_green}{barLabel}{Style.reset}")
					'''print(f"{Fore.light_steel_blue}{histoLabel}{Style.reset}")
					plt.hist(df_from_records[field],df_from_records[field].max(),label=f"Histogram {field}")
					plt.show()
					plt.clf()'''
					mx=-1
					mx=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Histogram Bins[5]",helpText="5",data="integer")
					if mx is None:
						return
					elif mx in ['d',]:
						mx=5
					
					try:
						if mx == -1:
							mx=int(df_from_records[field].max())
							multiplier=1
							while mx < 1:
								multiplier*=10
								mx=int(df_from_records[field].max()*multiplier)
							histoLabel=f"{multiplier}X -> Histogram {field}"
						else:
							histoLabel=f"Histogram {field}"

						plt.hist(df_from_records[field],mx,label=histoLabel)
						plt.show()
						plt.clf()
						print(f"{Fore.magenta}{histoLabel} total Entry Data Points = {len(df_from_records[field])} {Style.reset}")
					except Exception as e:
						if errors:
							print(e)

					try:
						df_from_records['tsa']=pd.to_datetime(df_from_records['DTOE'])
						times_recorded=[int(f"{i.hour}") for i in df_from_records['tsa']]
						bins=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Histogram Bins[bins for 24H]",helpText=f"bins for 24H",data="integer")
						if bins is None:
							return
						elif bins in ['d',]:
							bins=24
						plt.hist(times_recorded,bins=bins,label=histoLabel)
						plt.show()
						plt.clf()
						print(f"{Fore.orange_red_1}Hours of the Day Recorded{Fore.magenta}{histoLabel}total Entry Data Points = {len(df_from_records[field])}{Style.reset}")
					except Exception as e:
						if errors:
							print(e,'ec3')
				except Exception as ee:
					if errors:
						print(ee,repr(ee))
					else:
						pass
			print(f"{Fore.light_magenta}Dates on the Graph(s) are in the format of {Fore.orange_red_1}Day/Month/Year{Fore.light_magenta}, whereas Date Input will remain {Fore.light_steel_blue}Month/Day/Year{Style.reset}")
			n=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Next?",helpText="next y/n",data="boolean")
			if n in ['None',]:
				return None
			elif n in [True,]:
				return True


	def showAllField(self,fields=[],not_none=[],total_drg=False,total_fd=False):
		unit_registry=pint.UnitRegistry()
		try:
			useDateRange=Prompt.__init2__(None,func=FormBuilderMkText,ptext="use a date range?",helpText="yes or no",data="boolean")
			if useDateRange is None:
				return
			elif useDateRange in ['d',]:
				useDateRange=True

			gf=fields
			fields.extend(["DTOE","HLID","Comments"])
			fields=[i for i in HealthLog.__table__.columns if str(i.name) in fields]
			not_none=[i for i in HealthLog.__table__.columns if str(i.name) in not_none]
			with Session(ENGINE) as session:
				results=session.query(HealthLog).filter(or_(*[i!=None for i in not_none]))
				if useDateRange:
					default_sd=datetime.now()-timedelta(days=30)
					start_date=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Start Date(default = {default_sd}):",helpText="start date",data="datetime")
					if start_date is None:
						return
					elif start_date in ['d',]:
						start_date=default_sd

					default_ed=datetime.now()
					end_date=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"End Date(default = {default_ed}):",helpText="end date",data="datetime")
					if end_date is None:
						return
					elif end_date in ['d',]:
						end_date=default_ed

					results=results.filter(and_(HealthLog.DTOE>=start_date,HealthLog.DTOE<=end_date))

				results=orderQuery(results,HealthLog.DTOE)
				
				graph_it=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Graph Results (if possible)[y/N]:",helpText="yes or no; default is No.",data="boolean")
		
				if graph_it in [None,]:
					return
				elif graph_it in ['d',]:
					graph_it=False

				if graph_it:
					includes=["int","integer","float","decimal"]
					excludes=["HLID","EntryId"]
					fields_for_total=[i.name for i in HealthLog.__table__.columns if i.name in gf and str(i.type).lower() in includes and i.name not in excludes]
					print(fields_for_total)
					x=self.GraphIt(results,session,fields_for_total)
					if x is None:
						return
				
				if total_drg or total_fd:
					dummy={}

				results=results.all()
				ct=len(results)
				for num,i in enumerate(results):
					if total_drg or total_fd:
						if total_drg:
							if i.DrugConsumed in dummy:
								try:
									#normalize the values first
									old=unit_registry.Quantity(dummy[i.DrugConsumed].DrugQtyConsumed,dummy[i.DrugConsumed].DrugQtyConsumedUnitName)
									new=unit_registry.Quantity(i.DrugQtyConsumed,i.DrugQtyConsumedUnitName)
									f=old+new
									dummy[i.DrugConsumed].DrugQtyConsumed=f.magnitude
									dummy[i.DrugConsumed].DrugQtyConsumedUnitName=f.units
								except Exception as e:
									print(e,"processing will not include this")
									print(f"{Back.grey_11}{i}{Style.reset}")
							else:
								dummy[i.DrugConsumed]=copy(i)
						if total_fd:
							if 'total_fd' in dummy:
								for x in fields:
									includes=[
											"CarboHydrateIntake",
											"ProtienIntake",
											"FiberIntake",
											"TotalFat",
											"SodiumIntake",
											"CholesterolIntake",
											]
									if x.name not in includes:
										continue
									if getattr(dummy['total_fd'],x.name) is None:
										setattr(dummy['total_fd'],x.name,0)
									else:
										try:
											uname=x.name+"UnitName"
											old=unit_registry.Quantity(getattr(dummy['total_fd'],x.name),getattr(dummy['total_fd'],uname))
											new=unit_registry.Quantity(getattr(i,x.name),getattr(i,uname))
											f=old+new
											setattr(dummy['total_fd'],x.name,f.magnitude)
											setattr(dummy['total_fd'],uname,f.units)
										except Exception as e:
											print(e,"processing will not include this value")
											print(f"{Back.grey_11}{i}{Style.reset}")
							else:
								dummy['total_fd']=copy(i)
							
					view=[]
					for x in fields:
						if getattr(i,str(x.name)) == None:
							color=f"{Fore.grey_15}"
							color_date=f"{Fore.grey_15}"
						else:
							color=f"{Fore.sea_green_2}"
							color_date=f"{Fore.green_3b}"
						view.append(f'{color_date}{Style.bold}{str(x.name)}{Fore.deep_sky_blue_1}={color}{str(getattr(i,str(x.name)))}{Style.reset}')
					msg=f"{Fore.light_green}{num}{Fore.light_yellow}/{num+1} of {Fore.light_red}{ct} ->{'|'.join(view)}"
					print(msg)
				if total_drg or total_fd:
					print(f"{Fore.orange_red_1}Broken into Totals{Style.reset}")
					ct=len(dummy)
					
					for num,i in enumerate(dummy):
						view=[]
						i=dummy[i]
						for x in fields:
							if getattr(i,str(x.name)) == None:
								color=f"{Fore.grey_15}"
								color_date=f"{Fore.grey_15}"
							else:
								color=f"{Fore.sea_green_2}"
								color_date=f"{Fore.green_3b}"
							view.append(f'{color_date}{Style.bold}{str(x.name)}{Fore.deep_sky_blue_1}={color}{str(getattr(i,str(x.name)))}{Style.reset}')
						msg=f"{Fore.light_green}{num}{Fore.light_yellow}/{num+1} of {Fore.light_red}{ct} ->{'|'.join(view)}"
						print(msg)
		except Exception as e:
			print(e)

	def __init__(self):
		#this cmd extension format is so later i can add a findcmd equivalent here as well
		self.cmds={
			'fix table':{
			'cmds':['fix table','fixtable','fxtbl'],
			'desc':'Drop table and all data in table and regenerate new table; most useful when a new column is added/removed',
			'exec':self.fixtable
			},
			'export all':{
			'cmds':['xpt all','export all','xpta'],
			'desc':'Export HealthLog to excel',
			'exec':self.export_log
			},
			'nhl all':{
			'cmds':['nhla','nhl all','nhla','new health log all','new healthlog all','new healthlogall','newhealthlogall','newhealthlog all'],
			'desc':'Create a NEW HealthLog with ALL fields available',
			'exec':self.new_health_log
			},
			'add blood sugar':{
			'cmds':['abs','add bld sgr','add blood sugar','+bs','+bg','add bld glcs','add blood glucose','ad bld glcs'],
			'desc':'Create a NEW HealthLog for JUST Blood Sugar/Glucose Levels',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['BloodSugar','BloodSugarUnitName'])
			},
			'add short insulin':{
			'cmds':['asai','add short acting insulin','add short insulin',],
			'desc':'Create a NEW HealthLog for JUST Short Acting Insulin Intake',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['ShortActingInsulinName','ShortActingInsulinTaken','ShortActingInsulinUnitName'])
			},
			'add long insulin':{
			'cmds':['alai','add long acting insulin','add long insulin',],
			'desc':'Create a NEW HealthLog for JUST long Acting Insulin Intake',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['LongActingInsulinName','LongActingInsulinTaken','LongActingInsulinUnitName'])
			},
			'add hr':{
			'cmds':['ahr','add heart rate','add hrt rt',],
			'desc':'Create a NEW HealthLog for JUST Heart Rate',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['HeartRate','HeartRateUnitName'])
			},
			'show all':{
			'cmds':['sa','show all','showall',],
			'desc':'Show all HealthLogs',
			'exec':self.showAll
			},
			'add height':{
			'cmds':['aht','add height','add ht',],
			'desc':'Create a NEW HealthLog for JUST Height',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['Height','HeightUnitName'])
			},
			'add weight':{
			'cmds':['awt','add weight','add wt',],
			'desc':'Create a NEW HealthLog for JUST Weight',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['Weight','WeightUnitName'])
			},
			'add consumed':{
				'cmds':['afd','add fd','add food','adfd','add fuel','ad fl','afl'],
				'desc':'Create a NEW HealthLog for JUST food',
				'exec':lambda self=self:self.add_healthlog_specific(
					useColumns=["EntryBarcode",
								"EntryName",
								"CarboHydrateIntake",
								"CarboHydrateIntakeUnitName",
								"ProtienIntake",
								"ProtienIntakeUnitName",
								"FiberIntake",
								"FiberIntakeUnitName",
								"TotalFat",
								"TotalFatUnitName",
								"SodiumIntake",
								"SodiumIntakeUnitName",
								"CholesterolIntake",
								"CholesterolIntakeUnitName",])
			},
			'del hlid':{
			'cmds':['del','del hlid','rm','rm hlid'],
			'desc':'Delete a healthlog entry',
			'exec':self.del_hlid
			},
			'lsbs':{
			'cmds':['ls bs','lsbs','list blood sugars'],
			'desc':'list blood sugars',
			'exec':lambda self=self:self.showAllField(fields=['BloodSugar','BloodSugarUnitName'],not_none=['BloodSugar',])
			},
			'et':{
			'cmds':['et','exercise tracker','exrcse trckr',],
			'desc':'exercise tracker short cut',
			'exec':ET.ExerciseTracker
			},
			'lsdrug':{
			'cmds':['ls drug','ls dg','list drug','lsdrug','lsdrg'],
			'desc':'list drug data',
			'exec':lambda self=self:self.showAllField(total_fd=False,total_drg=True,fields=['EntryBarcode','EntryName','DrugConsumed','DrugQtyConsumed','DrugQtyConsumedUnitName'],not_none=['DrugQtyConsumed',])
			},
			'xpt drug':{
			'cmds':['xpt drug','xpt dg','export drug','xptdrug','xptdrg'],
			'desc':'export drug data to excel',
			'exec':lambda self=self:self.export_log_field(fields=['EntryBarcode','EntryName','DrugConsumed','DrugQtyConsumed','DrugQtyConsumedUnitName'],not_none=['DrugQtyConsumed',])
			},
			'add drug':{
			'cmds':['adrg','add drug','add drg','adddrug','adrug'],
			'desc':'Add a new drug consumption entry',
			'exec':lambda self=self:self.add_healthlog_specific(useColumns=['EntryBarcode','EntryName','DrugConsumed','DrugQtyConsumed','DrugQtyConsumedUnitName'])
			},
			'ls lai':{
			'cmds':['ls lai','lslai','list long insulin','list long acting insulin'],
			'desc':'list long acting insulin intake',
			'exec':lambda self=self:self.showAllField(fields=['LongActingInsulinName','LongActingInsulinTaken','LongActingInsulinUnitName'],not_none=['LongActingInsulinTaken',])
			},
			uuid1():{
			'cmds':generate_cmds(startcmd=['edit','ed'],endCmd=['hl','hlid',' ','']),
			'desc':'edit health log by hlid',
			'exec':self.edit_hlid,
			},
			uuid1():{
			'cmds':generate_cmds(startcmd=['ls','list','l'],endCmd=['cmts','cmt','comments','comment',' ','']),
			'desc':'ls only comments',
			'exec':lambda self=self:self.showAllField(fields=['Comments',],not_none=['Comments',])
			},
			uuid1():{
			'cmds':generate_cmds(startcmd=['a','add','+'],endCmd=['cmts','cmt','comments','comment',' ','']),
			'desc':'add a comment to the log',
			'exec':lambda self=self:self.add_healthlog_specific(
					useColumns=["Comments",])
			},
			'ls sai':{
			'cmds':['ls sai','lssai','list short insulin','list short acting insulin'],
			'desc':'list long acting insulin intake',
			'exec':lambda self=self:self.showAllField(fields=['ShortActingInsulinName','ShortActingInsulinTaken','ShortActingInsulinUnitName'],not_none=['ShortActingInsulinTaken',])
			},
			'ls heart rate':{
			'cmds':['lshr','ls heart rate','ls hrt rt'],
			'desc':'list heart rate',
			'exec':lambda self=self:self.showAllField(fields=['HeartRate','HeartRateUnitName'],not_none=['HeartRate',])
			},
			'ls weight':{
			'cmds':['lswt','ls weight','ls wt',],
			'desc':'list weight',
			'exec':lambda self=self:self.showAllField(fields=['Weight','WeightUnitName'],not_none=['Weight',])
			},
			'ls height':{
			'cmds':['lsht','ls height','ls ht',],
			'desc':'list height',
			'exec':lambda self=self:self.showAllField(fields=['Height','HeightUnitName'],not_none=['Height',])
			},
			'ls welsh':{
			'cmds':['ls welsh','list welsh'],
			'desc':'list data for diabete\'s dr.',
			'exec':lambda self=self:self.showAllField(fields=['BloodSugar','BloodSugarUnitName','LongActingInsulinName','LongActingInsulinTaken','LongActingInsulinUnitName','ShortActingInsulinName','ShortActingInsulinTaken','ShortActingInsulinUnitName','HeartRate','HeartRateUnitName','DrugConsumed','DrugQtyConsumed','DrugQtyConsumedUnitName','CarboHydrateIntake','CarboHydrateIntakeUnitName','Comments',],not_none=['Comments',])
			},
			'ls consumed':{
				'cmds':['lsfd','ls fd','ls food','lfd','ls fuel','ls fl','lfl'],
				'desc':'list food',
				'exec':lambda self=self:self.showAllField(total_fd=True,total_drg=False,
					fields=["EntryBarcode",
								"EntryName",
								"CarboHydrateIntake",
								"CarboHydrateIntakeUnitName",
								"ProtienIntake",
								"ProtienIntakeUnitName",
								"FiberIntake",
								"FiberIntakeUnitName",
								"TotalFat",
								"TotalFatUnitName",
								"SodiumIntake",
								"SodiumIntakeUnitName",
								"CholesterolIntake",
								"CholesterolIntakeUnitName",],
								not_none=[
								"CarboHydrateIntake",
								"ProtienIntake",
								"FiberIntake",
								"TotalFat",
								"SodiumIntake",
								"CholesterolIntake",
								]
								)
			},
			'xptbs':{
			'cmds':['xpt bs','xptbs','export blood sugars'],
			'desc':'export blood sugars',
			'exec':lambda self=self:self.export_log_field(fields=['BloodSugar','BloodSugarUnitName'],not_none=['BloodSugar',])
			},
			'xpt lai':{
			'cmds':['xpt lai','xptlai','export long insulin','export long acting insulin'],
			'desc':'export long acting insulin intake',
			'exec':lambda self=self:self.export_log_field(fields=['LongActingInsulinName','LongActingInsulinTaken','LongActingInsulinUnitName'],not_none=['LongActingInsulinTaken',])
			},
			'xpt sai':{
			'cmds':['xpt sai','xptsai','export short insulin','export short acting insulin'],
			'desc':'export long acting insulin intake',
			'exec':lambda self=self:self.export_log_field(fields=['ShortActingInsulinName','ShortActingInsulinTaken','ShortActingInsulinUnitName'],not_none=['ShortActingInsulinTaken',])
			},
			'xpt heart rate':{
			'cmds':['xpthr','xpt heart rate','xpt hrt rt'],
			'desc':'export heart rate',
			'exec':lambda self=self:self.export_log_field(fields=['HeartRate','HeartRateUnitName'],not_none=['HeartRate',])
			},
			'xpt weight':{
			'cmds':['xptwt','xpt weight','xpt wt',],
			'desc':'export weight',
			'exec':lambda self=self:self.export_log_field(fields=['Weight','WeightUnitName'],not_none=['Weight',])
			},
			'xpt height':{
			'cmds':['xptht','xpt height','xpt ht',],
			'desc':'export height',
			'exec':lambda self=self:self.export_log_field(fields=['Height','HeightUnitName'],not_none=['Height',])
			},
			'xpt cmts':{
			'cmds':['xptcmts','xpt cmts','xpt cmt',],
			'desc':'export height',
			'exec':lambda self=self:self.export_log_field(fields=['Comments',],not_none=['Comments',])
			},
			'xpt welsh':{
			'cmds':['export welsh','xpt welsh'],
			'desc':'export data for diabete\'s dr.',
			'exec':lambda self=self:self.export_log_field(fields=['BloodSugar','BloodSugarUnitName','LongActingInsulinName','LongActingInsulinTaken','LongActingInsulinUnitName','ShortActingInsulinName','ShortActingInsulinTaken','ShortActingInsulinUnitName','HeartRate','HeartRateUnitName','DrugConsumed','DrugQtyConsumed','DrugQtyConsumedUnitName','CarboHydrateIntake','CarboHydrateIntakeUnitName','Comments',],not_none=['Comments',])
			},
			'xpt consumed':{
				'cmds':['xptfd','xpt fd','xpt food','xpt-fd','xpt fuel','xpt fl','xlfl'],
				'desc':'export food',
				'exec':lambda self=self:self.export_log_field(
					fields=["EntryBarcode",
								"EntryName",
								"CarboHydrateIntake",
								"CarboHydrateIntakeUnitName",
								"ProtienIntake",
								"ProtienIntakeUnitName",
								"FiberIntake",
								"FiberIntakeUnitName",
								"TotalFat",
								"TotalFatUnitName",
								"SodiumIntake",
								"SodiumIntakeUnitName",
								"CholesterolIntake",
								"CholesterolIntakeUnitName",],
								not_none=[
								"CarboHydrateIntake",
								"ProtienIntake",
								"FiberIntake",
								"TotalFat",
								"SodiumIntake",
								"CholesterolIntake",]
								)
			},
		}
		helpText='\n'.join([
		'-'.join(
					[
						"* "+f"{Fore.light_sea_green}{f'{Fore.dark_goldenrod},{Style.reset}{Fore.light_sea_green}'.join(self.cmds[i]['cmds'])}{Style.reset}",
						f"{Fore.light_steel_blue}{self.cmds[i]['desc']}{Style.reset}",
					]
				) for i in self.cmds])
		while True:
			doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_red}HealthLog{Fore.light_yellow}@{Style.bold}{Fore.deep_sky_blue_3b}Menu{Fore.light_yellow} : Do What?",helpText=helpText,data="string")
			if doWhat not in [None,]:
				if doWhat.lower() in ['d',]:
					print(helpText)
					continue
				for i in self.cmds:
					if doWhat.lower() in  self.cmds[i]['cmds']:
						if callable(self.cmds[i]['exec']):
							self.cmds[i]['exec']()
			elif doWhat in [None,]:
				return

