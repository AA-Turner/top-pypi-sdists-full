from . import *
from radboy.DayLog.BhTrSa.bhtrsaa import *

class PhoneBookUi:
	def list_uids_names(self):
		while True:
			try:
				with Session(ENGINE) as session:
					stext=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Name or UID?[b=skip]",helpText="b|back skips",data="string")
					if stext is None:
						return None,None
					if stext in ['d',]:
						query=session.query(PhoneBook)
					else:
						query=session.query(PhoneBook).filter(or_(PhoneBook.phone_uid.icontains(stext),PhoneBook.phone_name.icontains(stext)))	
					
					query=query.group_by(PhoneBook.phone_uid,PhoneBook.phone_name)
					query=orderQuery(query,PhoneBook.DTOE,inverse=True)
					results=query.all()
					ct=len(results)
					htext=[]
					for num,i in enumerate(results):
						htext.append(std_colorize(f"{i.phone_name}[Name] - {i.phone_uid}[UID] - {i.pbid}[pbid]",num,ct))
					htext='\n'.join(htext)
					print(htext)
					which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index to use?",helpText=htext,data="integer")
					if which is None:
						return None,None
					elif which in ['d',]:
						which=0
					return results[which].phone_uid,results[which].phone_name
			except Exception as e:
				print(e)

	def create_new_rcp(self):
		with Session(ENGINE) as session:
			uid=uuid1()
			uid=str(uid)
			phonebook=PhoneBook()
			session.add(phonebook)
			session.commit()
			excludes=['pbid','DTOE']
			uid,name=self.list_uids_names()
			instructions={i.name:{'default':getattr(phonebook,i.name),'type':str(i.type).lower()} for i in PhoneBook.__table__.columns if i.name not in excludes}
			if name is not None:
				instructions['phone_name']['default']=name
			if uid is not None:
				instructions['phone_uid']['default']=uid
			fdi=FormBuilder(data=instructions)
			if fdi is None:
				print("User Quit Early, so all work has been deleted!")
				r=session.delete(phonebook)
				session.commit()
			else:
				
				session.query(PhoneBook).filter(PhoneBook.pbid==phonebook.pbid).update(fdi)
				session.commit()

			results=session.query(PhoneBook).filter(PhoneBook.pbid==phonebook.pbid)
			results=orderQuery(results,PhoneBook.DTOE,inverse=True)
			results=results.all()
			ctt=len(results)
			for num,i in enumerate(results):
				msg=std_colorize(i,num,ctt)
				print(msg)


	def fix_table(self):
		PhoneBook.__table__.drop(ENGINE)
		PhoneBook.metadata.create_all(ENGINE)


	def rm_rcp(self):
		with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True,grouped=True)
			if rcp is None:
				print("User returned, or no results!")
				return
			ct=len(rcp[0])
			htext=[]
			for i in rcp[0]:
				htext.append(i)
			htext='\n'.join(htext)
			print(htext)
			which=Prompt.__init2__(self,func=FormBuilderMkText,ptext="which index",helpText=f"{htext}\nindex of rcp to delete",data="integer")
			if which in [None,'d']:
				return
			try:
				query_2=session.query(PhoneBook).filter(PhoneBook.phone_uid==rcp[-1][which].phone_uid).delete()
				session.commit()
				print("Done Deleting!")
			except Exception as e:
				print(e)
		#delete everything found by searchtext using recipe_uid as the final selection parameter
		
	def edit_rcp(self):
		with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True)
			if rcp is None:
				print("User returned, or no results!")
				return
			ct=len(rcp[0])
			htext=[]
			for i in rcp[0]:
				htext.append(i)
			htext='\n'.join(htext)
			print(htext)
			whiches=Prompt.__init2__(self,func=FormBuilderMkText,ptext="which index",helpText=f"{htext}\nindex of contact to edit",data="list")
			if whiches in [None,'d']:
				return
			for which in whiches:
				try:
					which=int(which)
					query_2=session.query(PhoneBook).filter(PhoneBook.pbid==rcp[-1][which].pbid).first()
					fields={
					'phone_name':{'default':getattr(query_2,'phone_name'),'type':"string"},
					'phone_uid':{'default':getattr(query_2,'phone_uid'),'type':"string"},
					}
					fd=FormBuilder(data=fields)
					if fd is not None:
						r=session.query(PhoneBook).filter(PhoneBook.pbid==query_2.pbid)
						r.update(fd)
						session.commit()
					print("Done Editing!")
				except Exception as e:
					print(e)
		#edit everything found by searchtext using recipe_uid as the final selection parameter

	def rm_ingredient(self):
		with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True)
			if rcp is None:
				print("User returned, or no results!")
				return
			ct=len(rcp[0])
			htext=[]
			for i in rcp[0]:
				htext.append(i)
			htext='\n'.join(htext)
			print(htext)
			whiches=Prompt.__init2__(self,func=FormBuilderMkText,ptext="which index",helpText=f"{htext}\nindex of contact to delete ",data="list")
			if whiches in [None,'d']:
				return
			for which in whiches:
				try:
					which=int(which)
					query_2=session.query(PhoneBook).filter(PhoneBook.pbid==rcp[-1][which].pbid)
					ordered_2=orderQuery(query_2,PhoneBook.DTOE)
					results_2=ordered_2.all()
					ct=len(results_2)
					for num,i in enumerate(results_2):
						print(std_colorize(i,num,ct))
						delete=Prompt.__init2__(self,func=FormBuilderMkText,ptext="Delete[default=False]?",helpText="delete it, yes or no?",data="boolean")
						if delete in [None,]:
							return
						elif delete in ['d',]:
							continue
						elif delete == True:
							session.delete(i)
							session.commit()
				except Exception as e:
					print(e)
		#find a recipe, list its ingredients, select ingredients to delete, delete selected ingredients

	#asSelector==False,whole==True,names==False - print selector_string_whole
	#asSelector==False,whole==False,names==True - print selector_string_names
	#asSelector==False,whole==True,names==True - print selector_string_whole,selector_string_names
	#asSelector==True,whole==True,names==False - return selector_string_whole,selector_list
	#asSelector==True,whole==False,names==True - return selector_string_names,selector_list
	#asSelector==True,whole==True,names==True - return selector_string_names,selector_string_whole,selector_list
	def ls_rcp_names(self,asSelector=False,whole=False,names=False,grouped=False):
		with Session(ENGINE) as session:
			selector_list=[]
			selector_string_names=[]
			selector_string_whole=[]

			searchText=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What are you looking for?",helpText="text to search for",data="string")
			if searchText is None:
				return
			includes=["string","varchar","text"]
			excludes=['pbid','DTOE']
			fields=[i.name for i in PhoneBook.__table__.columns if str(i.name) not in excludes and str(i.type).lower() in includes]
			q=[]
			
			if searchText not in ['','d','all','*']:
				for i in fields:
					q.append(getattr(PhoneBook,i).icontains(searchText))
				query=session.query(PhoneBook).filter(or_(*q))
			else:
				query=session.query(PhoneBook)
			if grouped:
				query=query.group_by(PhoneBook.phone_uid,PhoneBook.phone_name)
			ordered=orderQuery(query,PhoneBook.DTOE,inverse=True)

			results=ordered.all()
			ct=len(results)
			if ct <= 0:
				print("No Results")
				return None
			for num,i in enumerate(results):
				selector_list.append(i)
				selector_string_whole.append(std_colorize(i,num,ct))
				msg=[]
				other_excludes=[None,'','N/A',' ','0','-1']
				f=[ii.name for ii in PhoneBook.__table__.columns if ii.name not in excludes and str(ii.type).lower() in includes and getattr(i,ii.name) not in other_excludes]
				for ff in f:
					x=f"{Fore.light_sea_green}{ff}{Fore.light_steel_blue}={Fore.orange_red_1}{getattr(i,ff)}{Style.reset}"
					msg.append(x)
				msg='|'.join(msg)
				selector_string_names.append(std_colorize(msg,num,ct))
				#selector_string_names.append(std_colorize(f"[PN]{i.phone_name}[PUID]{i.phone_uid}|[NPN]{i.non_personnel_name}|[LN]{i.lastName},[MN]{i.middleName},[FN]{i.firstName}|",num,ct))
				if not asSelector:
					if whole:
						print(selector_string_whole[num])
					if names:
						print(selector_string_names[num])
			if asSelector:
				if whole and not names:
					return selector_string_whole,selector_list
				elif names and not whole:
					return selector_string_names,selector_list
				elif names and whole:
					return selector_string_names,selector_string_whole,selector_list
	'''			
	def list_groups(self):
				with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True,grouped=True)
			if rcp is None:
				print("User returned, or no results!")
				return
			ct=len(rcp[0])
			htext=[]
			for i in rcp[0]:
				htext.append(i)
			htext='\n'.join(htext)
			print(htext)
			whiches=Prompt.__init2__(self,func=FormBuilderMkText,ptext="which index",helpText=f"{htext}\nindex of contact uid to view its grouped",data="list")
			if whiches in [None,'d']:
				return
			for which in whiches:
				try:
					which=int(which)
					query_2=session.query(PhoneBook).filter(PhoneBook.phone_uid==rcp[-1][which].phone_uid)
					ordered_2=orderQuery(query_2,PhoneBook.DTOE)
					results_2=ordered_2.all()
					ct=len(results_2)
					for num,i in enumerate(results_2):
						print(std_colorize(i,num,ct))
				except Exception as e:
					print(e)
	'''
	def list_contacts(self):
		with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True)
			if rcp is None:
				print("User returned, or no results!")
				return
			ct=len(rcp[0])
			htext=[]
			for i in rcp[0]:
				htext.append(i)
			htext='\n'.join(htext)
			print(htext)
			whiches=Prompt.__init2__(self,func=FormBuilderMkText,ptext="which index",helpText=f"{htext}\nindex of phonebook.pbid to view its content",data="list")
			if whiches in [None,'d']:
				return
			for which in whiches:
				try:
					which=int(which)
					query_2=session.query(PhoneBook).filter(PhoneBook.pbid==rcp[-1][which].pbid)
					ordered_2=orderQuery(query_2,PhoneBook.DTOE)
					results_2=ordered_2.all()
					ct=len(results_2)
					for num,i in enumerate(results_2):
						print(std_colorize(i,num,ct))
				except Exception as e:
					print(e)

	def ls_rcp_ingredients(self):
		with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True,grouped=True)
			if rcp is None:
				print("User returned, or no results!")
				return	
			else:
				print('next_state')		
			try:
				query_2=session.query(PhoneBook).filter(PhoneBook.phone_uid==rcp[-1][0].phone_uid)
				ordered_2=orderQuery(query_2,PhoneBook.DTOE)
				results_2=ordered_2.all()
				ct=len(results_2)
				for num,i in enumerate(results_2):
					print(std_colorize(i,num,ct))
			except Exception as e:
				print(e)

	def edit_rcp_ingredients(self):
		with Session(ENGINE) as session:
			rcp=self.ls_rcp_names(asSelector=True,whole=True,names=True)
			if rcp is None:
				print("User returned, or no results!")
				return
			ct=len(rcp[0])
			htext=[]
			for i in rcp[0]:
				htext.append(i)
			htext='\n'.join(htext)
			print(htext)
			whiches=Prompt.__init2__(self,func=FormBuilderMkText,ptext="which index",helpText=f"{htext}\nindex of rcp to view its ingredients",data="list")
			if whiches in [None,'d']:
				return
			for which in whiches:
				try:
					which=int(which)
					query_2=session.query(PhoneBook).filter(PhoneBook.pbid==rcp[-1][which].pbid)
					ordered_2=orderQuery(query_2,PhoneBook.DTOE)
					results_2=ordered_2.all()
					ct=len(results_2)
					for num,i in enumerate(results_2):
						print(std_colorize(i,num,ct))
						edit=Prompt.__init2__(self,func=FormBuilderMkText,ptext="Edit[default=False]?",helpText="Edit it, yes or no?",data="boolean")
						if edit in [None,]:
							return
						elif edit in ['d',]:
							continue
						elif edit == True:
							excludes=['pbid','phone_uid','phone_name','DTOE']
							fields={ii.name:{'default':getattr(i,ii.name),'type':str(ii.type).lower()} for ii in PhoneBook.__table__.columns if ii.name not in excludes}
							fd=FormBuilder(data=fields)
							if fd is not None:
								for k in fd:
									setattr(i,k,fd[k])
								session.commit()
							else:
								continue
				except Exception as e:
					print(e)
					

	def __init__(self):
		cmds={
			str(uuid1()):{
				'cmds':generate_cmds(startcmd=['create new','cn','cnw'],endCmd=['contact','cnct','c']),
				'desc':"create a new contact",
				'exec':self.create_new_rcp,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['fix','fx'],endCmd=['tbl','table']),
				'desc':"reinstall table",
				'exec':self.fix_table,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['rm','del','remove','delete'],endCmd=['grps','groups','g']),
				'desc':"delete a group of contacts by uid(delete everything found by searchtext using recipe_uid as the final selection parameter)",
				'exec':self.rm_rcp,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['rm','del','remove','delete'],endCmd=['contact','cnct','c']),
				'desc':"delete a contact(find a recipe, list its ingredients, select ingredients to delete, delete selected ingredients)",
				'exec':self.rm_ingredient,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ls','list','lst'],endCmd=['grps','groups','g']),
				'desc':"list contacts grouped by uid or basically list of groups",
				'exec':lambda self=self:self.ls_rcp_names(asSelector=False,whole=False,names=True,grouped=True),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ls','list','lst'],endCmd=['groups','grps','g']),
				'desc':"list contacts in a group",
				'exec':lambda self=self:self.ls_rcp_ingredients(),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ls','list','lst'],endCmd=['contact','cnct','c']),
				'desc':"list contacts from search without group by phone_uid",
				'exec':lambda self=self:self.list_contacts(),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ed','edt','edit'],endCmd=['contact','cnct','c']),
				'desc':"edit phone contact",
				'exec':lambda self=self:self.edit_rcp_ingredients(),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ed','edt','edit'],endCmd=['grps','groups','g']),
				'desc':"edit phone name and phone uid",
				'exec':lambda self=self:self.edit_rcp(),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['bhtrsa','business hours tax rates scheduled and appointments'],endCmd=['',]),
				'desc':"Business Hours, Tax Rates, Scheduled and Appointments {Fore.orange_red_1}[Indirectly Related]{Style.reset}",
				'exec':BhTrSa_Gui,
			},
		}

		htext=[]
		ct=len(cmds)
		for num,i in enumerate(cmds):
			m=f"{Fore.light_sea_green}{cmds[i]['cmds']}{Fore.orange_red_1} - {Fore.light_steel_blue}{cmds[i]['desc']}"
			msg=f"{std_colorize(m,num,ct)}"
			htext.append(msg)
		htext='\n'.join(htext)
		while True:
			doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{self.__class__.__name__} @ Do What? ",helpText=htext,data="string")
			if doWhat is None:
				return
			elif doWhat in ['','d',]:
				print(htext)
				continue
			for i in cmds:
				if doWhat.lower() in [i.lower() for i in cmds[i]['cmds']]:
					if callable(cmds[i]['exec']):
						cmds[i]['exec']()
						break
					else:
						print(f"{i} - {cmds[i]['cmds']} - {cmds[i]['exec']}() - {cmds[i]['desc']}")
						return
