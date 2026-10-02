from . import *

from decimal import Decimal

class OccurancesUi:
	first_time_excludes=['oid','created_dtoe',]
	basic_includes=['name','type','unit_of_measure','quantity']

	group_fields=['group_name','group_uid']

	def create_new_all(self):
		with Session(ENGINE) as session:
			try:
				OCT=Occurances()
				session.add(OCT)
				session.commit()
				first_time_fields={i.name:{'default':getattr(OCT,i.name),'type':str(i.type).lower()} for i in OCT.__table__.columns if i.name not in self.first_time_excludes}
				fd=FormBuilder(data=first_time_fields)
				if fd is None:
					session.delete(OCT)
					session.commit()
					print("user backed out, nothing was saved!")
					return
				for k in fd:
					setattr(OCT,k,fd[k])
				session.commit()
				session.refresh(OCT)
				print(std_colorize(OCT,0,1))
			except Exception as e:
				print(e)
				session.rollback()

	def create_new_basic(self):
		with Session(ENGINE) as session:
			try:
				OCT=Occurances()
				session.add(OCT)
				session.commit()
				first_time_fields={i.name:{'default':getattr(OCT,i.name),'type':str(i.type).lower()} for i in OCT.__table__.columns if i.name in self.basic_includes}
				fd=FormBuilder(data=first_time_fields)
				if fd is None:
					session.delete(OCT)
					session.commit()
					print("user backed out, nothing was saved!")
					return
				for k in fd:
					setattr(OCT,k,fd[k])
				session.commit()
				session.refresh(OCT)
				print(std_colorize(OCT,0,1))
			except Exception as e:
				print(e)
				session.rollback()

	def lst_group_names(self):
		with Session(ENGINE) as session:
			hs=[]
			search={
				'group_name':{
					'default':None,
					'type':'string',
				},
				'group_uid':{
					'default':None,
					'type':'string',
				},
				'oid':{
					'default':None,
					'type':'integer',
				}
			}
			fd=FormBuilder(data=search)
			query=None
			if fd is not None:
				filters=[]
				for i in fd:
					if fd[i] is not None:
						filters.append(getattr(Occurances,i).icontains(fd[i]))
				query=session.query(Occurances).filter(or_(*filters))
				query=orderQuery(query,Occurances.created_dtoe)
			else:
				query=session.query(Occurances)
				query=orderQuery(query,Occurances.created_dtoe)
			query=query.group_by(Occurances.group_name,Occurances.group_uid)

			if query is not None:
				results=query.all()
				ct=len(results)
				if ct == 0:
					print(std_colorize("No Results Found",0,1))
					return None,None
				for num,result in enumerate(results):
					hs.append(self.master_display(result,num,ct))
				helpText='\n'.join(hs)
				return results,helpText
			return None,None

	def master_display(self,result,num,ct):
		hstring=std_colorize(f"{Fore.light_sea_green}[group name] '{result.group_name}' {Fore.dodger_blue_3}- [guuid] '{result.group_uid}' -{Fore.green_yellow} [oid] '{result.oid}' - {Fore.light_magenta}[name] '{result.name}' - {Fore.magenta}[type] '{result.type}' - {Fore.orange_red_1}[QUANTITY/QTY] '{result.quantity}' {Fore.light_steel_blue}'{result.unit_of_measure}'{Fore.light_salmon_1} - [uid]'{result.uid}' - {Fore.cyan}[created_dtoe] '{result.created_dtoe}' {Fore.red}[age] '{datetime.now()-result.created_dtoe}'",num,ct)
		print(hstring)
		return hstring

	def setAllTo(self):
		with Session(ENGINE) as session:
			query=session.query(Occurances)
			all_set=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What Value does everything get set to?",helpText="this applies to everythinging",data="float")
			if all_set is None:
				return
			elif all_set in ['d',]:
				all_set=0

			query.update({'quantity':all_set})
			session.commit()

	def lst_names(self):
		with Session(ENGINE) as session:
			hs=[]
			search={
				'name':{
					'default':None,
					'type':'string',
				},
				'uid':{
					'default':None,
					'type':'string',
				},
				'oid':{
					'default':None,
					'type':'integer',
				}
			}
			fd=FormBuilder(data=search)
			query=None
			if fd is not None:
				filters=[]
				for i in fd:
					if fd[i] is not None:
						filters.append(getattr(Occurances,i).icontains(fd[i]))
				query=session.query(Occurances).filter(or_(*filters))
				query=orderQuery(query,Occurances.created_dtoe)
			else:
				query=session.query(Occurances)
				query=orderQuery(query,Occurances.created_dtoe)
			query=query.group_by(Occurances.uid)

			if query is not None:
				results=query.all()
				ct=len(results)
				if ct == 0:
					print(std_colorize("No Results Found",0,1))
					return None,None
				for num,result in enumerate(results):
					hs.append(self.master_display(result,num,ct))
				helpText='\n'.join(hs)
				return results,helpText
			return None,None

	def total_by_only_quantity(self,normalize=False):
		reg=pint.UnitRegistry()
		with Session(ENGINE) as session:
			by=['group_name','group_uid','name','uid','type']
			htext=[]
			ctby=len(by)
			for num,i in enumerate(by):
				htext.append(std_colorize(i,num,ctby))
			htext='\n'.join(htext)
			print(htext)
			whiches=Prompt.__init2__(self,func=FormBuilderMkText,ptext="Which indexes to total by?",helpText=htext,data="list")
			if whiches is None:
				return
			elif whiches in ['d',]:
				whiches=[0,]
			print("ss")
			for i in whiches:
				try:
					which=int(i)
					if which in range(0,len(by)+1):
						fields={
						by[which]:{'default':None,'type':'string'}
						}
						search=FormBuilder(data=fields)
						if search is None:
							continue
						s=[]
						for iii in search:
							
							if search[iii] is not None:
								s.append(
									getattr(Occurances,iii).icontains(search[iii])
									)
						if not normalize:
							total=Decimal('0.00000')
						else:
							total=None
						column_name=by[which]
						
						query=session.query(Occurances)
						query=query.filter(or_(*s))
						

						query=orderQuery(query,Occurances.created_dtoe,inverse=True)
						results=query.all()
						ct=len(results)
						for num,result in enumerate(results):
							try:
								if not normalize:
									msg=self.master_display(result,num,ct)
									current_value=getattr(result,'quantity')
									if current_value is None:
										current_value=0
									print(f"Occurance(name='{result.name}',uid='{result.uid}',oid={result.oid}{column_name}).Total = {total:.f5} + {current_value}")
									total+=Decimal(current_value).quantize(total)
								else:
									msg=self.master_display(result,num,ct)
									current_value=Decimal(getattr(result,'quantity')).quantize(Decimal('0.00000'))
									unit_of_measure=getattr(result,'unit_of_measure')
									if unit_of_measure not in reg:
										reg.define(f"{unit_of_measure} = 1")

									qty=reg.Quantity(current_value,unit_of_measure)
									
									if total is None:
										total=qty
									else:
										total+=qty
							except Exception as eeee:
								print(eeee)

						print(f"{column_name}.Total = {total:.5f}")

				except Exception as e:
					print(e)
	def copy_to_new(self,prompted=True):
		local_excludes=['quantity','uid',]
		#search and copy old details to a new Occurance setting created_dtoe to today, and quantity to 0
		with Session(ENGINE) as session:
			while True:
				search,helpText=self.lst_names()
				if search is None:
					return
				whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which indexes to copy to new Occurances",helpText=helpText,data="list")
				if whiches in [None,'d']:
					return
				cta=len(search)
				try:
					for which in whiches:
						try:
							which=int(which)
							if which in range(0,cta+1):
								oid=search[which].oid
								x=session.query(Occurances).filter(Occurances.oid==oid).first()
								new=Occurances()
								session.add(new)
								excludes=[]
								excludes.extend(self.first_time_excludes)
								excludes.extend(local_excludes)
								if prompted:
									fields={i.name:{'default':getattr(x,i.name),'type':str(i.type).lower()} for i in Occurances.__table__.columns if i.name not in excludes}
									fd=FormBuilder(data=fields)
								else:
									fd={}
									fields=[i.name for i in Occurances.__table__.columns if i.name not in excludes]
									for k in fields:
										old=getattr(x,k)
										fd[k]=old

									includes2=['quantity',]
									fields2={i.name:{'default':getattr(x,i.name),'type':str(i.type).lower()} for i in Occurances.__table__.columns if i.name in includes2}
									fd2=FormBuilder(data=fields2)
									if fd2:
										fd['quantity']=fd2['quantity']
									else:
										fd['quantity']=0
									fd['name']=f"{fd['name']} {dayString(datetime.now())}"
								if fd:
									try:
										for k in fd:
											setattr(new,k,fd[k])
										session.commit()
									except Exception as eee:
										print(eee)
										session.rollback()
						except Exception as e:
							print(e)
					return
				except Exception as ee:
					print(ee)
				break

	def edit_selected(self):
		with Session(ENGINE) as session:
			while True:
				search,helpText=self.lst_names()
				if search is None:
					return
				whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which indexes to edit",helpText=helpText,data="list")
				if whiches in [None,'d']:
					return
				cta=len(search)
				try:
					for which in whiches:
						try:
							which=int(which)
							if which in range(0,cta+1):
								oid=search[which].oid
								x=session.query(Occurances).filter(Occurances.oid==oid).first()
								fields={i.name:{'default':getattr(x,i.name),'type':str(i.type).lower()} for i in Occurances.__table__.columns if i.name not in self.first_time_excludes}
								fd=FormBuilder(data=fields)
								if fd:
									try:
										for k in fd:
											setattr(x,k,fd[k])
										session.commit()
									except Exception as eee:
										print(eee)
										session.rollback()
						except Exception as e:
							print(e)
					return
				except Exception as ee:
					print(ee)
				break

	def edit_selected_qty(self):
		with Session(ENGINE) as session:
			while True:
				search,helpText=self.lst_names()
				if search is None:
					return
				whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which indexes to edit",helpText=helpText,data="list")
				if whiches in [None,'d']:
					return
				cta=len(search)
				try:
					for num,which in enumerate(whiches):
						try:
							which=int(which)
							if which in range(0,cta+1):
								oid=search[which].oid
								x=session.query(Occurances).filter(Occurances.oid==oid).first()
								includes=['quantity',]
								fields={i.name:{'default':getattr(x,i.name),'type':str(i.type).lower()} for i in Occurances.__table__.columns if i.name in includes}
								fd=FormBuilder(data=fields,passThruText=self.master_display(x,num,cta)+"\n")
								if fd:
									try:
										for k in fd:
											setattr(x,k,fd[k])
										session.commit()
									except Exception as eee:
										print(eee)
										session.rollback()
						except Exception as e:
							print(e)
					return
				except Exception as ee:
					print(ee)
				break

	def delete_groups_uid(self):
		with Session(ENGINE) as session:
			while True:
				search,helpText=self.lst_group_names()
				if search is None:
					return
				whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which indexes to delete",helpText=helpText,data="list")
				if whiches in [None,'d']:
					return
				cta=len(search)
				try:
					for which in whiches:
						try:
							which=int(which)
							if which in range(0,cta+1):
								guid=search[which].group_uid
								x=session.query(Occurances).filter(Occurances.group_uid==guid).delete()
								session.commit()
						except Exception as e:
							print(e)
					return
				except Exception as ee:
					print(ee)
				break

	def delete_groups_name(self):
		with Session(ENGINE) as session:
			while True:
				search,helpText=self.lst_group_names()
				if search is None:
					return
				whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which indexes to delete",helpText=helpText,data="list")
				if whiches in [None,'d']:
					return
				cta=len(search)
				try:
					for which in whiches:
						try:
							which=int(which)
							#print(which,which in range(0,cta),cta,range(0,cta))
							if which in range(0,cta+1):
								guid=search[which].group_name
								print(guid)
								x=session.query(Occurances).filter(Occurances.group_name==search[which].group_name).delete()
								session.commit()
						except Exception as e:
							print(e)
					return
				except Exception as ee:
					print(ee)
				break

	def delete(self):
		with Session(ENGINE) as session:
			while True:
				search,helpText=self.lst_names()
				if search is None:
					return
				whiches=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which indexes to delete",helpText=helpText,data="list")
				if whiches in [None,'d']:
					return
				cta=len(search)
				try:
					for which in whiches:
						try:
							which=int(which)
							#print(which,which in range(0,cta),cta,range(0,cta))
							if which in range(0,cta+1):
								oid=search[which].oid
								x=session.query(Occurances).filter(Occurances.oid==oid).delete()
								session.commit()
						except Exception as e:
							print(e)
					return
				except Exception as ee:
					print(ee)
				break

	def list_all(self):
		with Session(ENGINE) as session:
			query=session.query(Occurances)
			query=orderQuery(query,Occurances.created_dtoe)
			results=query.all()
			ct=len(results)
			for num, i in enumerate(results):
				self.master_display(i,num,ct)

	def fix_table(self):
		Occurances.__table__.drop(ENGINE)
		Occurances.metadata.create_all(ENGINE)

	def __init__(self):
		cmds={
			uuid1():{
				'cmds':generate_cmds(startcmd=['fix','fx'],endCmd=['tbl','table']),
				'desc':"reinstall table",
				'exec':self.fix_table,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['cnw','create new','create_new','cn'],endCmd=['all','a','*','']),
				'desc':f"create new excluding fields {self.first_time_excludes}",
				'exec':self.create_new_all,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['cnw','create new','create_new','cn'],endCmd=['basic','b','bsc','-1']),
				'desc':f"create new including fields {self.basic_includes}",
				'exec':self.create_new_basic,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['lst','list','ls','l'],endCmd=['group names','grpnms','group-names','group_names']),
				'desc':f"list group names and group uids",
				'exec':self.lst_group_names,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['lst','list','ls','l'],endCmd=['names','nms','nmes']),
				'desc':f"list names and uids, group by uid",
				'exec':self.lst_names,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['delete','del','remove','rem','rm'],endCmd=['',' ']),
				'desc':f"delete occurances data",
				'exec':self.delete,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['delete','del','remove','rem','rm'],endCmd=['grps uid','groups uid','grps-uid','grpsuid']),
				'desc':f"delete occurances data by group uid",
				'exec':self.delete_groups_uid,
			},	
			uuid1():{
				'cmds':generate_cmds(startcmd=['delete','del','remove','rem','rm'],endCmd=['grps nm','groups name','grps-nm','grpsnm']),
				'desc':f"delete occurances data by group name",
				'exec':self.delete_groups_name,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['lst','list','ls','l'],endCmd=["all","a","*"]),
				'desc':f"list all",
				'exec':self.list_all,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['edit','edt','ed'],endCmd=['occurance','cntr','selected','s',]),
				'desc':f"edit occurances data",
				'exec':self.edit_selected,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['edit','edt','ed'],endCmd=['quantity','qty','amnt','amount']),
				'desc':f"edit occurances quantity only",
				'exec':self.edit_selected_qty,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['cp','copy','cpy'],endCmd=['2new','2 new',' ','']),
				'desc':f"copy all details of Occurances to new Occurance except for quantity and uids prompting for user provided changes to old",
				'exec':self.copy_to_new,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['cp','copy','cpy'],endCmd=['2new np','2 new np','2nw np','2 new no prompt','2new no-prompt']),
				'desc':f"copy all details of Occurances to new Occurance except for quantity and uids prompting for user provided changes to old",
				'exec':lambda self=self:self.copy_to_new(prompted=False),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ttl','total','count'],endCmd=['qty','qty only','quantity only']),
				'desc':f"count only quantity fields by column names without normalization",
				'exec':lambda self=self:self.total_by_only_quantity(),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['ttl','total','count'],endCmd=['nmlz','normalized','normal']),
				'desc':f"count only quantity fields by column names with normalization",
				'exec':lambda self=self:self.total_by_only_quantity(normalize=True),
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['setto','clrto','st2'],endCmd=['all','*',]),
				'desc':f"set all Occurances to user provided value/in essence a clear/pre init",
				'exec':lambda self=self:self.setAllTo(),
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
