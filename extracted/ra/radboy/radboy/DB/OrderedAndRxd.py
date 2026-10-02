from radboy.DB.db import *
from radboy.FB.FormBuilder import FormBuilder
from copy import deepcopy as copy
from radboy.ExportUtility import *
import radboy.HealthLog as HL
def CountTo():
    fd={
        'Start':{
        'type':'integer',
        'default':0
        },
        'Stop':{
        'default':int(5580*0.75),
        'type':"integer",
        },
        'Steps':{
        'default':int(50),
        'type':"integer"
        }
        }
    start=datetime.now()
    data=FormBuilder(data=fd)
    if data is None:
        print("bad parameters!")
        return
    absolute_start=False
    useLast=False
    while True:
        print(absolute_start)
        if absolute_start:
            fd={
            'Start':{
            'type':'integer',
            'default':0
            },
            'Stop':{
            'default':int(5580*0.75),
            'type':"integer",
            },
            'Steps':{
            'default':int(50),
            'type':"integer"
            }
            }
            start=datetime.now()
            data=FormBuilder(data=fd)
            if data is None:
                print("bad parameters!")
                return
            absolute_start=False
        if useLast:
            print("using last setup!")
        final_msg=''
        if data is not None:
            numeric=range(data['Start'],data['Stop'],data['Steps'])
            cta=len(numeric)
            present=datetime.now()
            for num,i in enumerate(numeric):
                while True:
                    total_duration=datetime.now()-start
                    since_last=datetime.now()-present
                    final_msg=std_colorize(f"{i} of {data['Stop']} TTL DUR:{total_duration}/SNC LST:{since_last}",num,cta)
                    print(final_msg)
                    do=Control(func=FormBuilderMkText,ptext="next?",helpText="just hit enter",data="boolean")
                    if do is None:
                        return
                    elif do in ['d',True]:
                        break
                    elif do in [False,]:
                        continue
                present=datetime.now()
            print(f"{Fore.orange_red_1}Done!{Style.reset}",final_msg)
            rerun=Control(func=FormBuilderMkText,ptext="re-run from absolute start? [y/N]",helpText="yes or no",data="boolean")
            if rerun is None:
                return
            elif rerun in ['d',False]:
                absolute_start=False
            else:
                absolute_start=True
                continue

            rerunLast=Control(func=FormBuilderMkText,ptext="re-run with last setup start? [y/N]",helpText="yes or no",data="boolean")
            if rerunLast is None:
                return
            elif rerunLast in ['d',False]:
                useLast=False
            else:
                useLast=True
                continue
            print(final_msg)
            break
MOOD_STRING='''
'''

class OrderedAndRecieved(BASE,Template):
    '''
    work notes
    '''
    __tablename__='OrderedAndRecieved'
    TitleOrSubject=Column(String,default=None)
    NameForWhom=Column(String,default=None)
    Description=Column(String,default=None)
    AddressForWhom=Column(String,default=None)
    RecieptId=Column(String,default=None)
    NanoId=Column(String,default=None)
    dtoe=Column(DateTime,default=datetime.now())

    #Organizational info.
    payee_name=Column(String,default=None)
    payor_name=Column(String,default=None)
    what_is_the_address_worked_at=Column(String,default=None)
    if_necessary_what_is_the_payors_address=Column(String,default=None)
    did_the_payor_specify_restrictions_and_if_so_what_are_they=Column(String,default=None)
    are_there_any_special_requirements_that_need_to_be_mentioned=Column(String,default=None)
    was_this_for_a_residence=Column(Boolean,default=None)
    was_this_for_a_business=Column(Boolean,default=None)
    what_was_the_organizations_name=Column(String,default=None)
    was_this_for_something_else=Column(String,default=None)
    is_the_address_worked_at_owned_by_the_payor=Column(Boolean,default=None)
    is_the_address_worked_at_lived_at_by_the_payor=Column(Boolean,default=None)
    is_the_address_worked_at_a_bussiness_address=Column(Boolean,default=None)
    is_the_address_worked_at_a_home_address=Column(Boolean,default=None)
    #Contact info
    payor_comments=Column(String,default=None)
    payee_comments=Column(String,default=None)
    payor_home_phone_1=Column(String,default=None)
    payor_work_phone_1=Column(String,default=None)
    payor_business_phone_1=Column(String,default=None)
    payor_mobile_phone_1=Column(String,default=None)
    payor_home_phone_2=Column(String,default=None)
    payor_work_phone_2=Column(String,default=None)
    payor_business_phone_2=Column(String,default=None)
    payor_mobile_phone_2=Column(String,default=None)
    payor_home_phone_3=Column(String,default=None)
    payor_work_phone_3=Column(String,default=None)
    payor_business_phone_3=Column(String,default=None)
    payor_mobile_phone_3=Column(String,default=None)
    payor_email_1=Column(String,default=None)
    payor_fax_1=Column(String,default=None)
    payor_email_2=Column(String,default=None)
    payor_fax_2=Column(String,default=None)
    payor_email_3=Column(String,default=None)
    payor_fax_1_3=Column(String,default=None)

    #segment 11 driving record
    #678-659-9383
    #dmv error processing unit
    #let them know that i filled out my application on sept. 9.
    How_are_wages_being_dispensed=Column(String,default=None)

    RateOfPay=Column(Float,default=None)
    RateOfPayComment=Column(Float,default=None)
    RateOfPayBy=Column(String,default=None)

    Amount_Paid=Column(Float,default=None)
    Duration_For_Amount_Paid=Column(String,default=None)
    Amount_Paid_Form=Column(String,default=None)

    Paid_When_DT=Column(DateTime,default=None)
    Shift_Started_DT=Column(DateTime,default=None)
    Shift_Lunch_Start=Column(DateTime,default=None)
    Shift_Lunch_End=Column(DateTime,default=None)
    Shift_Ended_DT=Column(DateTime,default=None)
    Shift_Labor_Breaks=Column(Text,default=None)
    is_lunch_paid=Column(Boolean,default=None)
    is_break_paid=Column(Boolean,default=None)

    #schedule 
    Was_This_A_Scheduled_Shift=Column(Boolean,default=None)
    ScheduledShiftDTOE=Column(DateTime,default=None)
    ScheduledDays=Column(String,default=None)
    ScheduledShiftNotes=Column(String,default=None)
    Assigned_Department=Column(String,default=None)
    Departments_Handled_or_Touched=Column(Text,default=None)

    #shift info
    TasksPerformed=Column(Text,default=None)
    TasksAssigned=Column(Text,default=None)
    TasksNotes=Column(Text,default=None)
    order_dt=Column(DateTime,default=datetime.now())
    rx_dt=Column(DateTime,default=datetime.today()+timedelta(days=1))
    #management
    ManagerPresent=Column(Boolean,default=None)
    Manager_Name=Column(Boolean,default=None)
    ManagerNotes=Column(Text,default=None)

    SupervisorPresent=Column(Boolean,default=None)
    SupervisorName=Column(String,default=None)
    SupervisorNotes=Column(Text,default=None)

    PersonInChargePresent=Column(Boolean,default=None)
    PersonInChargeName=Column(String,default=None)
    PersonInChargeNotes=Column(Text,default=None)

    MentalEpisode=Column(Boolean,default=None)
    MentalEpisodeTotal=Column(Integer,default=None)
    MentalEpisodeNotes=Column(Text,default=None)

    HealthViolations=Column(Boolean,default=None)
    HealthViolationsTotal=Column(Integer,default=None)
    HealthViolationsNotes=Column(Text,default=None)

    SafetyViolations=Column(Boolean,default=None)
    SafetyViolationsTotal=Column(Integer,default=None)
    SafetyViolationsNotes=Column(Text,default=None)

    web_links=Column(Text,default=None)
    comment=Column(String,default=None)
    oarid=Column(Integer,primary_key=True)
    def __init__(self,*args,**kwargs):
        for k in kwargs:
            if k in [i.name for i in self.__table__.columns]:
                setattr(self,k,kwargs[k])
try:
    OrderedAndRecieved.metadata.create_all(ENGINE)
except Exception as e:
    OrderedAndRecieved.__table__.drop(ENGINE)
    OrderedAndRecieved.metadata.create_all(ENGINE) 
 
class OrderAndRxdUi():
    def between_dates(self,query):
        '''list everything between start and end
        paged=True -> page results and use menu to edit/delete/stop paging
        paged=False -> print all at once
        limit=True -> limit to number of results with offset ; use prompt to ask for for limit amount and offset amount through formbuilder
        limit=False -> everything is printed
        short_display=True -> display less information
        '''
        start=Control(func=FormBuilderMkText,ptext="Start DateTime: ",helpText="starting datetime",data="datetime")
        if start is None:
            return
        elif not isinstance(start,datetime):
            return

        end=Control(func=FormBuilderMkText,ptext="End DateTime: ",helpText="ending datetime",data="datetime")
        if end is None:
            return
        elif not isinstance(end,datetime):
            return
        print(f""""
{Fore.orange_red_1}Results are for dates between
{Fore.light_green}Start: {start}
{Fore.light_red}End: {end}
{'-'*(os.get_terminal_size().columns-len(Style.reset))}{Style.reset}
            """)
        return orderQuery(query.filter(and_(
            OrderedAndRecieved.dtoe >= start,
            OrderedAndRecieved.dtoe <= end))
        ,OrderedAndRecieved.dtoe,inverse=True)

    def fixtable(self):
        OrderedAndRecieved.__table__.drop(ENGINE)
        OrderedAndRecieved.metadata.create_all(ENGINE) 
    #where cmds are stored
    cmds={}
    #registered cmds
    registry=[]
    def filter(self,src_dict):
        filte=[]
        for k in src_dict:
            if src_dict[k] is not None:
                if isinstance(src_dict[k],str):
                    filte.append(getattr(OrderedAndRecieved,k).icontains(src_dict[k]))
                elif isinstance(src_dict[k],datetime):
                    if k == 'rx_dtoe':
                        pass
                    elif k == 'dtoe':
                        pass
                    elif k == 'order_dt':
                        pass
                else:
                    filte.append(getattr(OrderedAndRecieved,k)==src_dict[k])
        #uncomment these to troubleshoot
        #print('x3',and_(*filte))
        #print('x4')


    def OrderedAndRecieved_as(self,_exlcudes=[],as_=None,item=None):
        excludes=['oarid',]
        for i in _exlcudes:
            if i not in excludes:
                excludes.append(i)
        fields=None
        if as_ is None:
            fields={i.name:
            {
                'default':None,
                'type':str(i.type).lower()

            } for i in OrderedAndRecieved.__table__.columns if i.name not in excludes}
        elif as_ == "default":
            with Session(ENGINE) as session:
                tmp=OrderedAndRecieved()
                session.add(tmp)
                session.commit()
                fields={i.name:
                {
                    'default':getattr(tmp,i.name),
                    'type':str(i.type).lower()

                } for i in OrderedAndRecieved.__table__.columns if i.name not in excludes}
                session.delete(tmp)
                session.commit()
        elif as_ == 'from_item':
            if isinstance(item,OrderedAndRecieved):              
                fields={i.name:
                {
                    'default':getattr(item,i.name),
                    'type':str(i.type).lower()

                } for i in item.__table__.columns if i.name not in excludes}
            else:
                raise TypeError(item)
        else:
            raise Exception(f"Not a registered as_('{as_}')")
        if fields is not None:
            fd=FormBuilder(data=fields)
            if fd is None:
                print("User Cancelled! OrderedAndRecieved_as(self,_exlcudes=[],as_=None,item=None)")
                return
            return fd,fields

    def search(self,selector=False,menu=False):
        nantucket=self.OrderedAndRecieved_as(as_=None)
        if nantucket is None:
            print("User cancelled! search(self,selector=False,menu=False)")
            return
        terms,z=nantucket
        terms=self.filter(terms)
        def selectortext(results,page=False,self=self):
            def edit(i,self=self):
                edits=self.OrderedAndRecieved_as(as_="from_item",item=i)
                if edits is None:
                    return
                with Session(ENGINE) as session:
                    e=session.query(OrderedAndRecieved).filter(OrderedAndRecieved.oarid==i.oarid).first()
                    if e is not None:
                        for k in edits[0]:
                            setattr(e,k,edits[0][k])
                        session.commit()

            def delete(i,self=self):
                with Session(ENGINE) as session:
                    session.query(OrderedAndRecieved).filter(OrderedAndRecieved.oarid==i.oarid).delete()
                    session.commit()
                
            htext=[]
            for num,i in enumerate(results):
                print(std_colorize(i,num,ct))
                if page:
                    ready=False
                    while not ready:
                        menu=Control(func=FormBuilderMkText,ptext="edit/e or r/rm/del/delete/dlt",helpText="edit or delete",data="string")
                        if menu is None:
                            return
                        elif menu in ['d',]:
                            print(std_colorize(i,num,ct))
                            continue
                        elif menu in ['edt','ed','e']:
                            edit(i)
                            ready=True
                        elif menu in ['rm','r','del','delete','dlt']:
                            delete(i)
                            ready=True
                        else:
                            print(std_colorize(i,num,ct))
                            continue
                

        
        with Session(ENGINE) as session:
            query=session.query(OrderedAndRecieved)
            if terms is not None:
                query=query.filter(terms)
            query=orderQuery(query,OrderedAndRecieved.dtoe)
            between_dates=Control(func=FormBuilderMkText,ptext="Between dates? y/n",helpText="values between two dates",data="boolean")
            if between_dates is None:
                return None
            if between_dates in ['d',False]:
                pass
            else:
                query=self.between_dates(query)

            results=query.all()
            ct=len(results)
            plural=''
            if ct > 1:
                plural="s"
            print(f"{ct} result{plural}!")
            zebra=0
                

            if selector:
                #for returning a list of OrderedAndRecieved
                selectortext(resuls)
                zebra+=1
                pass
            if menu:
                #for paged edit/delete of OrderedAndRecieved and returns None
                selectortext(results,page=True)
                zebra+=1
                pass

            if not(zebra > 0):
                for num,i in enumerate(results):
                        print(std_colorize(i,num,ct))


    def __init__(self,*args,**kwargs):
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['add','a'],endCmd=['no lu']),
            'desc':'add OrderedAndRecieved without lookup',
            'exec':self.addRecordNoLookup
        }
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['oar','OrderedAndRecieved'],endCmd=['fb None']),
            'desc':'test generate OrderedAndRecieved without lookup and fields to be used as None',
            'exec':lambda self=self:print(self.OrderedAndRecieved_as(as_=None))
        }
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['oar','OrderedAndRecieved'],endCmd=['fb dflt']),
            'desc':'test generate OrderedAndRecieved without lookup and fields to be used as default',
            'exec':lambda self=self:print(self.OrderedAndRecieved_as(as_="default"))
        }
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['sch','s','search'],endCmd=['', ' ']),
            'desc':'search for OrderedAndRecieved',
            'exec':lambda self=self:self.search()
        }
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['sch','s','search'],endCmd=['m', 'menu','mnu']),
            'desc':'search for OrderedAndRecieved with paged menu',
            'exec':lambda self=self:self.search(menu=True)
        }
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['fix','fx',],endCmd=['tbl', 'table',]),
            'desc':'drop and recreate table',
            'exec':lambda self=self:self.fixtable()
        }
        self.cmds[uuid1()]={
            'cmds':generate_cmds(startcmd=['health','h',],endCmd=['log', 'l',]),
            'desc':'healthlog',
            'exec':lambda self=self:HL.HealthLog.HealthLogUi()
        }
        self.cmds["ExportTables"]={
        'cmds':["export tables","xpttbl",],
        'desc':f'import/export selected tables to/from selected XLSX (Excel)/ODF',
        'exec':ExportTable,
        }
        
        #add cmds above
        
        for x,cmd in enumerate(self.cmds):
            if str(x) not in self.cmds[cmd]['cmds']:
                self.cmds[cmd]['cmds'].append(str(x))
        htext=[]
        cmdCopy=self.cmds
        ct=len(cmdCopy)
        for xnum,cmd in enumerate(cmdCopy):
            for num,i in enumerate(cmdCopy[cmd]['cmds']):

                if i not in self.registry:
                    self.registry.append(i)
                elif i in self.registry:
                    self.cmds[cmd]['cmds'].pop(self.cmds[cmd]['cmds'].index(i))
            htext.append(std_colorize(f"{self.cmds[cmd]['cmds']} - {self.cmds[cmd]['desc']}",xnum,ct))
        htext='\n'.join(htext)
        print(htext)
        while True:
            doWhat=Control(func=FormBuilderMkText,ptext=f"{self.__class__.__name__}:Do What what",helpText=htext,data="string")
            if doWhat is None:
                return
            elif doWhat in ['d','']:
                continue
            for cmd in self.cmds:
                if doWhat.lower() in self.cmds[cmd]['cmds'] and callable(self.cmds[cmd]['exec']):
                    try:
                        self.cmds[cmd]['exec']()
                    except Exception as e:
                        print(e)
                    break
        
    def addRecordNoLookup(self):
        with Session(ENGINE) as session:
            t=OrderedAndRecieved()
            session.add(t)
            session.commit()
            data={
            i.name:{
            'default':getattr(t,i.name),
            'type':str(i.type).lower()} for i in t.__table__.columns
            }
            fd=FormBuilder(data=data)
            if fd is None:
                session.delete(t)
                session.commit()
            else:
                for k in fd:
                    setattr(t,k,fd[k])
                session.commit()
                session.refresh(t)
            
                print(t)