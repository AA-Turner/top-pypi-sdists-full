from . import *

@dataclass
class CookingConversion(BASE,Template):
    ccid=Column(Integer,primary_key=True)
    __tablename__="CookingConversions"
    Mass_with_unit=Column(String,default='')
    ResourceName=Column(String,default='butter')
    Converts_To_Volume_With_Unit=Column(String,default='')

    def __str__(self):
        msg=[]
        f=f"Cooking Conversion(ccid={self.ccid},{Fore.orange_red_1}Mass_with_unit='{Fore.light_steel_blue}{self.Mass_with_unit}{Fore.orange_red_1}' of ResourceName='{Fore.light_yellow}{self.ResourceName}' {Fore.medium_violet_red}~={Fore.magenta} Converts_To_Volume_With_Unit='{Fore.light_green}{self.Converts_To_Volume_With_Unit}'){Style.reset}"
        msg.append(f)
        return '\n'.join(msg)

try:
    CookingConversion.metadata.create_all(ENGINE)
except Exception as e:
    CookingConversion.__table__.drop(ENGINE)
    CookingConversion.metadata.create_all(ENGINE)


class CC_Ui:
    def fix_table(self):
        CookingConversion.__table__.drop(ENGINE)
        CookingConversion.metadata.create_all(ENGINE)

    def new_conversion(self):
        try:
            excludes=['ccid',]
            fields={
            i.name:{
            'default':None,
            'type':str(i.type).lower()
            } for i in CookingConversion.__table__.columns if i.name not in excludes
            }
            fb=FormBuilder(data=fields)
            if fb is None:
                return

            with Session(ENGINE) as session:
                try:
                    ncc=CookingConversion()
                    for k in fb:
                        setattr(ncc,k,fb[k])
                    session.add(ncc)
                    session.commit()
                    session.refresh(ncc)
                    print(ncc)
                except Exception as ee:
                    print(ee)
                    session.rollback()
                    session.commit()
        except Exception as e:
            print(e)

    def edit_cvt(self,cvt):
        with Session(ENGINE) as session:
            fields={i.name:{'default':getattr(cvt,i.name),'type':str(i.type).lower()} for i in cvt.__table__.columns}
            fb=FormBuilder(data=fields,passThruText="Edit CookingConversion")

            r=session.query(CookingConversion).filter(CookingConversion.ccid==cvt.ccid).first()
            for i in fb:
                setattr(r,i,fb[i])
            session.commit()
            session.refresh(r)



    def search_conversion(self,menu=False):
        try:
            excludes=['ccid',]
            fields={
            i.name:{
            'default':None,
            'type':str(i.type).lower()
            } for i in CookingConversion.__table__.columns if i.name not in excludes
            }
            fb=FormBuilder(data=fields)
            if fb is None:
                return

            tmp={}
            for i in fb:
                if fb[i] is not None:
                    tmp[i]=fb[i]


            FILTER=[]
            for i in tmp:
                try:
                    FILTER.append(getattr(CookingConversion,i).icontains(tmp[i]))
                except Exception as e:
                    print(e)

            with Session(ENGINE) as session:
                try:
                    if len(FILTER) < 1:
                        query=session.query(CookingConversion)
                    else:
                        query=session.query(CookingConversion).filter(or_(*FILTER))

                    ordered=orderQuery(query,CookingConversion.ResourceName,inverse=True)
                    results=ordered.all()
                    cta=len(results)
                    display=[]
                    
                    modified=True
                    while True:
                        da=False
                        for num,i in enumerate(results):
                            msg=std_colorize(f"{i}",num,cta)
                            if menu:
                                print(msg)
                                if not da:
                                    action=Control(func=FormBuilderMkText,ptext=f"Delete All({Fore.light_red}delete all{Fore.light_yellow} or {Fore.light_red}da{Fore.light_yellow})/Delete({Fore.light_red}del{Fore.light_yellow})/Edit({Fore.light_red}ed{Fore.light_yellow})",helpText="edit or delete",data="string")
                                else:
                                    action='da'
                                if action.lower() in ['delete','del']:
                                    session.delete(i)
                                    session.commit()
                                    continue
                                elif action.lower() in ['ed','edit']:
                                    self.edit_cvt(i)
                                    session.refresh(results[num])
                                    msg=std_colorize(f"{i}",num,cta)
                                elif action.lower() in ['u','use']:
                                    print('not implemented!')
                                    continue
                                elif action.lower() in ['da','delete all']:
                                    da=True
                                    session.delete(i)
                                    session.commit()
                                else:
                                    pass
                                
                            try:
                                display.append(msg)
                            except Exception as e:
                                print(e)
                        break
                    if not da: 
                        display='\n'.join(display)
                        print(display)
                    
                except Exception as ee:
                    print(ee)
        except Exception as e:
            print(e)

    def findAndUse2(self):
        with Session(ENGINE) as session:
            cmd=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.light_red}[FindAndUse2]{Fore.light_yellow}what cmd are your looking for?",helpText="type the cmd",data="string")
            if cmd in ['d',None]:
                return
            else:
                options=copy(self.options)
                
                session.query(FindCmd).delete()
                session.commit()
                for num,k in enumerate(options):
                    stage=0
                    cmds=options[k]['cmds']
                    l=[]
                    l.extend(cmds)
                    l.append(options[k]['desc'])
                    cmdStr=' '.join(l)
                    cmd_string=FindCmd(CmdString=cmdStr,CmdKey=k)
                    session.add(cmd_string)
                    if num % 50 == 0:
                        session.commit()
                session.commit()
                session.flush()

                results=session.query(FindCmd).filter(FindCmd.CmdString.icontains(cmd)).all()


                ct=len(results)
                if ct == 0:
                    print(f"No Cmd was found by {Fore.light_red}{cmd}{Style.reset}")
                    return
                for num,x in enumerate(results):
                    msg=f"{Fore.light_yellow}{num}/{Fore.light_steel_blue}{num+1} of {Fore.light_red}{ct} -> {Fore.turquoise_4}{f'{Fore.light_yellow},{Style.reset}{Fore.turquoise_4}'.join(options[x.CmdKey]['cmds'])} - {Fore.green_yellow}{options[x.CmdKey]['desc']}"
                    print(msg)
                select=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left before the /",data="integer")
                if select in [None,'d']:
                    return
                try:
                    ee=options[results[select].CmdKey]['exec']
                    if callable(ee):
                        ee()
                except Exception as e:
                    print(e)

    

    def __init__(self):
        
        self.options={}
        self.options[str(uuid1())]={
            'cmds':generate_cmds(startcmd=["fix","fx"],endCmd=['tbl','table']),
            'desc':'''
drop and regenerate CookingConversion Table
            ''',
            'exec':self.fix_table
        }
        self.options[str(uuid1())]={
            'cmds':generate_cmds(startcmd=["search","s","sch"],endCmd=['cvt','cvn','conversion']),
            'desc':'''
search conversions
            ''',
            'exec':self.search_conversion
        }
        self.options[str(uuid1())]={
            'cmds':generate_cmds(startcmd=["search","s","sch"],endCmd=['mnu','menu','m']),
            'desc':'''
search for and edit/use/delete cooking conversions that were stored
            ''',
            'exec':lambda self=self:self.search_conversion(menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['',],
            'desc':f'',
            'exec':print
        }
        #new methods() start
        self.options[str(uuid1())]={
            'cmds':['ncc','new cooking conversion','nw ckng cvt'],
            'desc':f'save a new conversion',
            'exec':self.new_conversion
        }

        #new methods() end
        self.options[str(uuid1())]={
            'cmds':['fcmd','findcmd','find cmd'],
            'desc':f'Find {Fore.light_yellow}cmd{Fore.medium_violet_red} and excute for return{Style.reset}',
            'exec':self.findAndUse2
        }
        self.DESCRIPTION=f'''
Review Cooking Conversions so you can get dat recipe fo gud. u good cheech?.
        '''

        self.options[str(uuid1())]={
            'cmds':['desciption','describe me','what am i','help me','?+'],
            'desc':f'print the module description',
            'exec':lambda self=self:print(self.DESCRIPTION)
        }

        for num,i in enumerate(self.options):
            if str(num) not in self.options[i]['cmds']:
                self.options[i]['cmds'].append(str(num))
        options=copy(self.options)

        while True:                
            helpText=[]
            for i in options:
                msg=f"{Fore.light_green}{options[i]['cmds']}{Fore.light_red} -> {options[i]['desc']}{Style.reset}"
                helpText.append(msg)
            helpText='\n'.join(helpText)

            cmd=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{__class__.__name__}|Do What?:",helpText=helpText,data="string")
            if cmd is None:
                return None
            result=None
            for i in options:
                els=[ii.lower() for ii in options[i]['cmds']]
                if cmd.lower() in els:
                    print(i)
                    options[i]['exec']()
                    break


