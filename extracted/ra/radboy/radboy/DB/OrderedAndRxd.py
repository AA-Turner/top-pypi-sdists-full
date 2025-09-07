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
    select an order date by name and date , and at a later date 
    set the rx datetime
    '''
    __tablename__='OrderedAndRecieved'
    Name=Column(String,default=None)
    ForWhom=Column(String,default=None)
    Description=Column(String,default=None)
    oarid=Column(Integer,primary_key=True)
    dtoe=Column(DateTime,default=datetime.now())

    order_dt=Column(DateTime,default=datetime.now())
    rx_dt=Column(DateTime,default=datetime.today()+timedelta(days=1))

    was_what_was_ordered_get_recieved=Column(Boolean,default=None)
    frozen_pallets_rxd=Column(Integer,default=0)
    grocery_pallets_rxd=Column(Integer,default=0)
    variety_pallets_rxd=Column(Integer,default=0)
    tote_pallets_rxd=Column(Integer,default=0)
    bread_stacks_rxd=Column(Integer,default=0)
    red_totes_rxd=Column(Integer,default=0)

    one_gallon_stacks_rxd=Column(Integer,default=0)
    one_gallon_stacks_ordered=Column(Integer,default=0)
    one_gallon_stacks_size=Column(Integer,default=5)
    one_gallon_per_crate=Column(Integer,default=6)

    two_and_half_gallon_stacks_rxd=Column(Integer,default=0)
    two_and_half_gallon_stacks_ordered=Column(Integer,default=0)
    two_and_half_gallon_stack_size=Column(Integer,default=5)
    two_and_half_gallon_per_crate=Column(Integer,default=3)

    one_gallon_crates_ordered=Column(Integer,default=0)
    one_gallon_crates_rxd=Column(Integer,default=0)
    one_gallon_per_crate=Column(Integer,default=6)
    one_gallon_names=Column(String,default="distilled and/or spring water")

    two_and_half_gallon_crates_ordered=Column(Integer,default=0)
    two_and_half_gallon_crates_rxd=Column(Integer,default=0)
    two_and_half_gallon_per_crate=Column(Integer,default=3)
    two_and_half_gallon_names=Column(String,default="distilled and/or spring water")

    dairy_fluid_thrown=Column(Boolean,default=False)
    dairy_fluid_dropped=Column(Boolean,default=False)
    dairy_crated_fluids_thrown=Column(Boolean,default=False)
    dairy_cmt=Column(String,default='')

    was_frozen_assisted=Column(Boolean,default=False)
    frozne_load_thrown=Column(Boolean,default=False)
    frozne_load_dropped=Column(Boolean,default=False)
    frozne_load_broken=Column(Boolean,default=False) 
    frozen_old_load_broken=Column(Boolean,default=False)
    frozen_old_load_broken=Column(Boolean,default=False)
    frozen_old_load_cmt=Column(String,default='')
    sixteen_lb_ice_thrown=Column(Boolean,default=False)
    nine_lb_ice_thrown=Column(Boolean,default=False)
    frozen_cmt=Column(String,default='')

    empty_pallets_exported=Column(Integer,default=0)
    crate_pallets_exported=Column(Integer,default=0)
    bales_exported=Column(Integer,default=0)
    bales_tied=Column(Integer,default=0)

    beverage_pallets_restacked=Column(Integer,default=0)
    beverage_pallets_restacked_cmt=Column(String,default='')

    meat_barrel_pallets_exported=Column(Integer,default=0)

    produce__waxbins_exported=Column(Integer,default=0)
    produce_waxbins_constructed=Column(Integer,default=0)
    produce_compost_bins_exported=Column(Integer,default=0)
    produce_compost_bins_constructed=Column(Integer,default=0)
    produce_foldable_crate_pallets_exported=Column(Integer,default=0)

    sick_calls_total=Column(Integer,default=0)
    sick_calls_cmt=Column(String,default='')

    workers_present=Column(String,default='')
    workers_present_cmt=Column(String,default='')

    was_hallway_cleared=Column(Boolean,default=False)
    was_hallway_cleared_cmt=Column(String,default='')

    DT_punched_in=Column(DateTime,default=None)
    DT_out_of_recieving=Column(DateTime,default=None)
    DT_first_break=Column(DateTime,default=None)
    DT_on_aisle_from_first_break=Column(DateTime,default=None)
    DT_to_lunch=Column(DateTime,default=None)
    DT_from_lunch=Column(DateTime,default=None)
    DT_punched_out=Column(DateTime,default=None)
    DT_grocery_breakdown_finished=Column(DateTime,default=None)
    DT_frozen_breakdown_finished=Column(DateTime,default=None)

    clocked_in_early=Column(Boolean,default=False)
    clocked_in_late=Column(Boolean,default=False)
    clocked_out_early=Column(Boolean,default=False)
    clocked_out_late=Column(Boolean,default=False)
    lunch_out_early=Column(Boolean,default=False)
    lunch_in_early=Column(Boolean,default=False)
    lunch_out_late=Column(Boolean,default=False)
    lunch_in_late=Column(Boolean,default=False)

    assisted_deli=Column(Boolean,default=False)
    assisted_deli_with=Column(String,default='')

    rate_your_anger_0_to_10=Column(Integer,default=0)
    rate_your_anxiety_0_to_10=Column(Integer,default=0)
    rate_your_mood_0_to_10=Column(Integer,default=0)
    rate_your_energy_0_to_10=Column(Integer,default=0)
    rate_your_worriedness_0_to_10=Column(Integer,default=0)
    personal_comment_related_to_rating=Column(String,default=MOOD_STRING)

    was_receiving_assisted=Column(Boolean,default=False)
    recieving_comments=Column(Text,default=None)
    reciever_name=Column(String,default='')
    reciever_present_by_dt=Column(DateTime,default=None)
    was_there_a_reciever=Column(Boolean,default=False)

    was_gm_assisted=Column(Boolean,default=False)
    gm_comments=Column(Text,default=None)
    gm_manager_name=Column(String,default='')
    gm_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_gm_manager=Column(Boolean,default=False)

    was_liquor_assisted=Column(Boolean,default=False)
    liquor_comments=Column(Text,default=None)
    liquor_manager_name=Column(String,default='')
    liquor_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_liquor_manager=Column(Boolean,default=False)

    was_grocery_assisted=Column(Boolean,default=False)
    grocery_comments=Column(Text,default=None)
    grocery_manager_name=Column(String,default='')
    grocery_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_grocery_manager=Column(Boolean,default=False)

    was_dairy_assisted=Column(Boolean,default=False)
    dairy_comments=Column(Text,default=None)
    dairy_manager_name=Column(String,default='')
    dairy_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_dairy_manager=Column(Boolean,default=False)

    was_meat_department_assisted=Column(Boolean,default=False)
    meat_department_comments=Column(Text,default=None)
    meat_department_manager_name=Column(String,default='')
    meat_department_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_meat_department_manager=Column(Boolean,default=False)

    was_deli_assisted=Column(Boolean,default=False)
    deli_comments=Column(Text,default=None)
    deli_manager_name=Column(String,default='')
    deli_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_deli_manager=Column(Boolean,default=False)

    was_bakery_assisted=Column(Boolean,default=False)
    bakery_comments=Column(Text,default=None)
    bakery_manager_name=Column(String,default='')
    #Column(String,default=None)
    bakery_manager_present_by_dt=Column(DateTime,default=None)
    was_there_a_bakery_manager=Column(Boolean,default=False)

    did_you_deliver_general_merchadise=Column(String,default=None)
    did_you_break_down_general_merchandise=Column(String,default=None)
    did_throw_general_merchandise=Column(String,default=None)
    did_you_face_general_merchandise=Column(String,default=None)
    did_you_face_endcaps_frontend_displays=Column(String,default=None)
    did_you_deliver_tote_pallets=Column(String,default=None)
    did_you_deliver_bread_stacks=Column(String,default=None)
    did_you_deliver_red_totes_to_icc=Column(String,default=None)
    did_deliver_warehouse39=Column(String,default=None)
    did_you_deliver_kehe=Column(String,default=None)
    did_you_throw_kehe=Column(String,default=None)
    did_you_break_down_kehe=Column(String,default=None)
    did_you_break_down_warehouse39=Column(String,default=None)
    did_you_throw_warehouse39=Column(String,default=None)
    did_deliver_bakery_items=Column(String,default=None)
    did_you_deliver_meat_items=Column(String,default=None)
    did_you_deliver_deli_items=Column(String,default=None)
    did_you_deliver_starbucks_items=Column(String,default=None)
    did_you_deliver_anything_to_file_maintenance=Column(String,default=None)
    did_you_deliver_anything_to_the_front_end_or_customer_service=Column(String,default=None)
    did_you_condense_beverage=Column(String,default=None)
    did_you_deliver_anything_for_anyother_department_other_than_assigned=Column(String,default=None)
    your_assigned_department=Column(String,default=None)


    comment=Column(String,default='')
    
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