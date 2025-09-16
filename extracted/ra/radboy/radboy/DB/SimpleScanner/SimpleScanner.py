from . import *

@dataclass
class SimpleScan(BASE,Template):
    __tablename__="SimpleScan"
    ssid=Column(Integer,primary_key=True)

    ScannedText=Column(String,default=None)
    TimesScanned=Column(Float,default=0)
    DTOE=Column(DateTime,default=datetime.now())

    Note=Column(Text,default='')


try:
    SimpleScan.metadata.create_all(ENGINE)
except Exception as e:
    SimpleScan.__table__.drop(ENGINE)
    SimpleScan.metadata.create_all(ENGINE)


class SimpleScanUi:
    def fix_table(self):
        SimpleScan.__table__.drop(ENGINE)
        SimpleScan.metadata.create_all(ENGINE)

    def scan_add(self,value=1):
        default=False
        ask_qty=Control(func=FormBuilderMkText,ptext=f"Ask For Qty Each Scan[False/True](default={default})",helpText="ask for a qty to add each time an item is selected",data="boolean")
        if ask_qty is None:
            return
        elif ask_qty in ['NaN',]:
            ask_qty=False
        elif ask_qty in ['d',]:
            ask_qty=default

        if value is None:
            if not ask_qty:
                value=Control(func=FormBuilderMkText,ptext=f"+/- To old(1):",helpText="How much to decrement or increment",data="float")
                if value in [None,'NaN']:
                    return
                elif value in ['d',]:
                    value=1
            else:
                value=0

        if value > 0:
            inc="add/+"
            by_with="to"
        elif value < 0:
            inc="subtract/-"
            by_with="from"
        else:
            inc="modify"
            by_with='with'
        with Session(ENGINE) as session:
            while True:
                scanText=Control(func=FormBuilderMkText,ptext="Barcode/Code/Text",helpText="whatever it is you are scanning, its just text.",data="string")
                if scanText is None:
                    return
                elif scanText.lower() in ['d','','nan']:
                    continue
                else:
                    pass
                results=session.query(SimpleScan).filter(SimpleScan.ScannedText.icontains(scanText)).all()
                cta=len(results)
                if cta < 1:
                    if ask_qty:
                        value=Control(func=FormBuilderMkText,ptext=f"+/- To old(1):",helpText="How much to decrement or increment",data="float")
                        if value in [None,'NaN']:
                            return
                        elif value in ['d',]:
                            value=1
                    else:
                        value=1
                    scanned=SimpleScan(ScannedText=scanText,DTOE=datetime.now(),TimesScanned=value)
                    session.add(scanned)
                    session.commit()
                elif cta == 1:
                    index=0
                    if ask_qty:
                        value=Control(func=FormBuilderMkText,ptext=f"+/- To old({results[index].TimesScanned}):",helpText="How much to decrement or increment",data="float")
                        if value in [None,'NaN']:
                            return
                        elif value in ['d',]:
                            value=1
                    results[index].TimesScanned+=value
                    session.commit()
                else:
                    while True:
                        try:
                            htext=[]
                            for num,i in enumerate(results):
                                htext.append(std_colorize(i,num,cta))
                            htext='\n'.join(htext)
                            print(htext)
                            selected=Control(func=FormBuilderMkText,ptext=f"{Fore.orange_red_1}DUPLICATE SELECT{Fore.light_yellow} Which indexes do you wish to {inc} TimesScanned {by_with}?",helpText=htext,data="list")
                            if selected in [None,'NAN','NaN']:
                                return
                            elif selected in ['d',]:
                                selected=[0,]
                            for i in selected:
                                try:
                                    index=int(i)
                                    if index_inList(index,results):
                                        if ask_qty:
                                            value=Control(func=FormBuilderMkText,ptext=f"+/- To old({results[index].TimesScanned}):",helpText="How much to decrement or increment",data="float")
                                            if value in [None,'NaN']:
                                                return
                                            elif value in ['d',]:
                                                value=1
                                        results[index].TimesScanned+=value
                                        session.commit()
                                except Exception as e:
                                    print(e)
                            break
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

    def delete_all(self):
        fieldname=f'{__class__.__name__}'
        mode=f'DeleteAll'
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
        
        code=''.join([str(random.randint(0,9)) for i in range(10)])
        verification_protection=detectGetOrSet("Protect From Delete",code,setValue=False,literal=True)
        while True:
            try:
                really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Really delete All SimpleScanItems?",helpText="yes or no boolean,default is NO",data="boolean")
                if really in [None,]:
                    print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                    return True
                elif really in ['d',False]:
                    print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                    return True
                else:
                    pass
                really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"To {Fore.orange_red_1}Delete everything completely,{Fore.light_steel_blue}what is today's date?[{'.'.join([str(int(i)) for i in datetime.now().strftime("%m.%d.%y").split(".")])}]{Style.reset}",helpText="type y/yes for prompt or type as m.d.Y",data="datetime")
                if really in [None,'d']:
                    print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                    return True
                today=datetime.today()
                if really.day == today.day and really.month == today.month and really.year == today.year:
                    really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Please type the verification code {Style.reset}'{Entry.cfmt(None,verification_protection)}'?",helpText=f"type '{Entry.cfmt(None,verification_protection)}' to finalize!",data="string")
                    if really in [None,]:
                        print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                        return True
                    elif really in ['d',False]:
                        print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                        return True
                    elif really == verification_protection:
                        break
                else:
                    pass
            except Exception as e:
                print(e)
        with Session(ENGINE) as session:
            session.query(SimpleScan).delete()
            session.commit()

    def clear_all(self):
        fieldname=f'{__class__.__name__}'
        mode=f'ClearAll'
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
        
        code=''.join([str(random.randint(0,9)) for i in range(10)])
        verification_protection=detectGetOrSet("Protect From Delete",code,setValue=False,literal=True)
        while True:
            try:
                really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Really Clear All SimpleScanItems to TimesScanned=0?",helpText="yes or no boolean,default is NO",data="boolean")
                if really in [None,]:
                    print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Cleared!{Style.reset}")
                    return True
                elif really in ['d',False]:
                    print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Cleared!{Style.reset}")
                    return True
                else:
                    pass
                really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"To {Fore.orange_red_1}Clear everything completely,{Fore.light_steel_blue}what is today's date?[{'.'.join([str(int(i)) for i in datetime.now().strftime("%m.%d.%y").split(".")])}]{Style.reset}",helpText="type y/yes for prompt or type as m.d.Y",data="datetime")
                if really in [None,'d']:
                    print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Deleted!{Style.reset}")
                    return True
                today=datetime.today()
                if really.day == today.day and really.month == today.month and really.year == today.year:
                    really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Please type the verification code {Style.reset}'{Entry.cfmt(None,verification_protection)}'?",helpText=f"type '{Entry.cfmt(None,verification_protection)}' to finalize!",data="string")
                    if really in [None,]:
                        print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Cleared!{Style.reset}")
                        return True
                    elif really in ['d',False]:
                        print(f"{Fore.light_steel_blue}Nothing was {Fore.orange_red_1}{Style.bold}Cleared!{Style.reset}")
                        return True
                    elif really == verification_protection:
                        break
                else:
                    pass
            except Exception as e:
                print(e)
        with Session(ENGINE) as session:
            session.query(SimpleScan).update({'TimesScanned':0,'DTOE':datetime.now(),'Note':''})
            session.commit()

    def list_scan(self,sch=False,dated=False,menu=False):
        default=True
        FORMAT=f"terse==short;default={default};output is short using {Fore.light_steel_blue}[- chunked ScannedText]{Fore.light_magenta}ScannedText:{Fore.light_red}ssid[{Fore.green_yellow}DTOE]={Fore.cyan}TimesScanned | Note = \"if not None or ''\"{Style.reset}"
        terse=Control(func=FormBuilderMkText,ptext="Terse output [False/True] ",helpText=FORMAT,data="boolean")
        if terse is None:
            return
        elif terse in ['NaN',]:
            terse=False
        elif terse in ['d',]:
            terse=default
        writeToFile=Control(func=FormBuilderMkText,ptext="writeToFile output [False/True] ",helpText=str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))),data="boolean")
        if writeToFile is None:
            return
        elif writeToFile in ['NaN',]:
            writeToFile=False
        elif writeToFile in ['d',]:
            writeToFile=default
        
        if writeToFile:
            outfile=Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))
            outfile.open('w').write('')
        
        total=0
        with Session(ENGINE) as session:
            query=session.query(SimpleScan)
            
            if dated:
                start_date=Control(func=FormBuilderMkText,ptext="Start Date:",helpText="start date",data="datetime")
                if start_date in [None,'NaN']:
                    return
                elif start_date in ['d',]:
                    start_date=datetime.today()

                end_date=Control(func=FormBuilderMkText,ptext="end Date:",helpText="end date",data="datetime")
                if end_date in [None,'NaN']:
                    return
                elif end_date in ['d',]:
                    end_date=datetime.today()
                query=query.filter(and_(SimpleScan.DTOE<end_date,SimpleScan.DTOE>start_date))

            if sch:
                term=Control(func=FormBuilderMkText,ptext="What are you looking for? ",helpText="a string of text",data="string")
                if term is None:
                    return
                elif term in ['d','NaN']:
                    term=''
                query=query.filter(SimpleScan.ScannedText.icontains(term))

            query=orderQuery(query,SimpleScan.DTOE,inverse=True)
            results=query.all()
            cta=len(results)
            if cta < 1:
                print("There are no results!")
                return
            for num, i in enumerate(results):
                total+=i.TimesScanned
                if not terse:
                    msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                else:
                    if i.ScannedText == None:
                        i.ScannedText=''
                    chunked=stre(i.ScannedText)/4
                    chunked='-'.join(chunked)
                    note=i.Note
                    if note not in ['',None,' ']:
                        note=f" | Note = '''{i.Note}'''"
                    msg=std_colorize(f"{Fore.light_steel_blue}[{chunked}]{Fore.light_magenta}{i.ScannedText}:{Fore.light_red}{i.ssid}[{Fore.green_yellow}{i.DTOE}] = {Fore.cyan}{i.TimesScanned} {Fore.dark_goldenrod}{note}",num,cta)
                print(msg)
                if writeToFile:
                    self.save2file_write(msg)
                if menu:
                    doWhat=Control(func=FormBuilderMkText,ptext="clear/clr, reset/rst, edit/e/ed, or delete/del/remove/rm (<Enter> Continues)?",helpText="clear/clr, reset/rst, edit/e/ed or delete/del/remove/rm?",data="string")
                    if doWhat in [None,'NaN']:
                        return
                    elif doWhat.lower() in "edit/e/ed".split("/"):
                        self.edit(i)
                        session.refresh(i)
                        if not terse:
                            msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                        else:
                            msg=std_colorize(f"{Fore.light_magenta}{i.ScannedText}:{Fore.light_red}{i.ssid}[{Fore.green_yellow}{i.DTOE}] = {Fore.cyan}{i.TimesScanned} {Fore.dark_goldenrod}",num,cta)
                        print(msg)
                    elif doWhat.lower() in "delete/del/remove/rm".split("/"):
                        session.delete(i)
                        session.commit()
                    elif doWhat.lower() in "clear/clr".split("/"):
                        self.edit(i,clear=True)
                        session.refresh(i)
                        if not terse:
                            msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                        else:
                            msg=self.terse(i,num,cta)
                        print(msg)
                    elif doWhat.lower() in "reset/rst".split("/"):
                        self.edit(i,reset=True)
                        session.refresh(i)
                        if not terse:
                            msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                        else:
                            msg=std_colorize(f"{Fore.light_magenta}{i.ScannedText}:{Fore.light_red}{i.ssid}[{Fore.green_yellow}{i.DTOE}] = {Fore.cyan}{i.TimesScanned} {Fore.dark_goldenrod}",num,cta)
                        print(msg)
                if (num % 15) == 0 and num > 0:
                    print(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}")
                    if writeToFile:
                        self.save2file_write(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}")
            print(f"Total TimesScanned = {total}")
            print(FORMAT)
            if writeToFile:
                print(f"Written to {str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)))}")
                self.save2file_write(f"Total TimesScanned = {total}")
                self.save2file_write(strip_colors(FORMAT))

    def terse(self,i,num,cta):
        return std_colorize(f"{Fore.light_magenta}{i.ScannedText}:{Fore.light_red}{i.ssid}[{Fore.green_yellow}{i.DTOE}] = {Fore.cyan}{i.TimesScanned} {Fore.dark_goldenrod}",num,cta)

    def edit(self,i:SimpleScan,excludes=['ssid',],reset=False,clear=False):
        if reset:
            with Session(ENGINE) as session:
                 r=session.query(SimpleScan).filter(SimpleScan.ssid==i.ssid).first()
                 r.ScannedText=''
                 r.DTOE=datetime.now()
                 r.Note=''
                 r.TimesScanned=0
                 session.commit()
            return

        if clear:
            with Session(ENGINE) as session:
                 r=session.query(SimpleScan).filter(SimpleScan.ssid==i.ssid).first()
                 r.DTOE=datetime.now()
                 r.Note=''
                 r.TimesScanned=0
                 session.commit()
            return
        fields={
        x.name:{
        'default':getattr(i,x.name),
        'type':str(x.type).lower()
        } for x in i.__table__.columns if x.name not in excludes
        }
        fd=FormBuilder(data=fields)
        if fd is None:
            return
        with Session(ENGINE) as session:
            r=session.query(SimpleScan).filter(SimpleScan.ssid==i.ssid).update(fd)
            session.commit()

    def last_TimesScanned(self):
        '''print hight times scanned w/ prompt for how many and offset'''
        default=True
        FORMAT=f"terse==short;default={default};output is short using {Fore.light_steel_blue}[- chunked ScannedText]{Fore.light_magenta}ScannedText:{Fore.light_red}ssid[{Fore.green_yellow}DTOE]={Fore.cyan}TimesScanned | Note = \"if not None or ''\"{Style.reset}"
        terse=Control(func=FormBuilderMkText,ptext="Terse output [False/True] ",helpText=FORMAT,data="boolean")
        if terse is None:
            return
        elif terse in ['NaN',]:
            terse=False
        elif terse in ['d',]:
            terse=default
        '''print the newest scan'''
        writeToFile=Control(func=FormBuilderMkText,ptext="writeToFile output [False/True] ",helpText=str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))),data="boolean")
        if writeToFile is None:
            return
        elif writeToFile in ['NaN',]:
            writeToFile=False
        elif writeToFile in ['d',]:
            writeToFile=default
        
        if writeToFile:
            outfile=Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))
            outfile.open('w').write('')
        with Session(ENGINE) as session:
            total=0
            query=session.query(SimpleScan)
            query=orderQuery(query,SimpleScan.TimesScanned)
            limit=Control(func=FormBuilderMkText,ptext="max to display?",helpText="an integer",data="integer")
            if limit in [None,'NaN']:
                return
            elif limit in ['d',]:
                limit=10

            offset=Control(func=FormBuilderMkText,ptext="what is the offset from 0?",helpText="what is 0/start+offset",data="integer")
            if offset in [None,'NaN']:
                return
            elif offset in ['d',]:
                offset=0
            query=limitOffset(query,limit,offset)

            results=query.all()
            cta=len(results)

            for num,i in enumerate(results):
                total+=i.TimesScanned
                if terse:
                    msg=self.terse(i,num,cta)
                else:
                    msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                if writeToFile:
                    self.save2file_write(strip_colors(msg))
                print(msg)
                if (num % 15) == 0 and num > 0:
                    print(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}")
                    if writeToFile:
                        self.save2file_write(strip_colors(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}"))
            print(f"Total TimesScanned = {total}")
            print(FORMAT)
            if writeToFile:
                print(f"Written to {str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)))}")
                self.save2file_write(f"Total TimesScanned = {total}")
                self.save2file_write(strip_colors(FORMAT))

    def clear_file(self):
        with Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)).open('w') as out:
            out.write('')
        print("Cleared!")

    def last_DTOE(self):
        default=True
        FORMAT=f"terse==short;default={default};output is short using {Fore.light_steel_blue}[- chunked ScannedText]{Fore.light_magenta}ScannedText:{Fore.light_red}ssid[{Fore.green_yellow}DTOE]={Fore.cyan}TimesScanned | Note = \"if not None or ''\"{Style.reset}"
        terse=Control(func=FormBuilderMkText,ptext="Terse output [False/True] ",helpText=FORMAT,data="boolean")
        if terse is None:
            return
        elif terse in ['NaN',]:
            terse=False
        elif terse in ['d',]:
            terse=default
        writeToFile=Control(func=FormBuilderMkText,ptext="writeToFile output [False/True] ",helpText=str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))),data="boolean")
        if writeToFile is None:
            return
        elif writeToFile in ['NaN',]:
            writeToFile=False
        elif writeToFile in ['d',]:
            writeToFile=default
        
        if writeToFile:
            outfile=Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))
            outfile.open('w').write('')

        '''print the newest scan'''
        with Session(ENGINE) as session:
            total=0
            query=session.query(SimpleScan)
            query=orderQuery(query,SimpleScan.DTOE)
            limit=Control(func=FormBuilderMkText,ptext="max to display?",helpText="an integer",data="integer")
            if limit in [None,'NaN']:
                return
            elif limit in ['d',]:
                limit=10

            offset=Control(func=FormBuilderMkText,ptext="what is the offset from 0?",helpText="what is 0/start+offset",data="integer")
            if offset in [None,'NaN']:
                return
            elif offset in ['d',]:
                offset=0
            query=limitOffset(query,limit,offset)

            results=query.all()
            cta=len(results)

            for num,i in enumerate(results):
                total+=i.TimesScanned
                if terse:
                    msg=self.terse(i,num,cta)
                else:
                    msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)

                print(msg)
                if writeToFile:
                    self.save2file_write(strip_colors(msg))
                if (num % 15) == 0 and num > 0:
                    if writeToFile:
                        self.save2file_write(strip_colors(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}"))
                    print(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}")
            print(f"Total TimesScanned = {total}")
            if writeToFile:
                print(f"Written to {str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)))}")
                self.save2file_write(f"Total TimesScanned = {total}")
                self.save2file_write(strip_colors(FORMAT))
            print(FORMAT)


    def save2file_write(self,text):
        outfile=Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True))
        with open(outfile,'a') as x:
            otext=strip_colors(text+"\n")
            if otext in [None,'d','']:
                print("nothing was saved!")
            if otext is None:
                return
            x.write(otext)
            #print(f"wrote '{otext}' to '{outfile}'")


    def __init__(self):
        MENUDO="edit,delete, clear count,reset all fields"
        self.options={}
        self.options[str(uuid1())]={
            'cmds':generate_cmds(startcmd=["fix","fx"],endCmd=['tbl','table']),
            'desc':'''
drop and regenerate SimpleScan Table
            ''',
            'exec':self.fix_table
        }
        self.options[str(uuid1())]={
            'cmds':['ca','clearall','clear all','clear-all','clear.all'],
            'desc':f'clear qty of simple scans',
            'exec':self.clear_all
        }
        self.options[str(uuid1())]={
            'cmds':['da','deleteall','delete all','delete-all','delete.all'],
            'desc':f'delete all of simple scans',
            'exec':self.delete_all
        }
        self.options[str(uuid1())]={
            'cmds':['list scan','lst scn',],
            'desc':f'List Scans',
            'exec':self.list_scan
        }
        self.options[str(uuid1())]={
            'cmds':['clear file','clr fl',],
            'desc':f'clear outfile',
            'exec':self.clear_file
        }
        self.options[str(uuid1())]={
            'cmds':['list scan search','lst scn sch','lst sch','list find','lst fnd'],
            'desc':f'List Scans with search by scanned text',
            'exec':lambda self=self:self.list_scan(sch=True)
        }
        self.options[str(uuid1())]={
            'cmds':['last by dtoe','lst dtoe'],
            'desc':f'List Scans with limit and offset using rllo/vllo for ordering by dtoe',
            'exec':lambda self=self:self.last_DTOE()
        }
        self.options[str(uuid1())]={
            'cmds':['last by timesscanned','lst ts'],
            'desc':f'List Scans with limit and offset using rllo/vllo for ordering by TimesScanned',
            'exec':lambda self=self:self.last_TimesScanned()
        }
        self.options[str(uuid1())]={
            'cmds':['list scan dated','lst scn dt','lst dt','list dtd','lst d'],
            'desc':f'List Scans within start and end dates',
            'exec':lambda self=self:self.list_scan(dated=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list scan search date','lst scn sch dt','lst sch dt','list find dt','lst fnd dt'],
            'desc':f'List Scans with search by scanned text between start and end dates',
            'exec':lambda self=self:self.list_scan(sch=True,dated=True)
        }

        self.options[str(uuid1())]={
            'cmds':['list scan menu','lst scn m',],
            'desc':f'List Scans with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list scan search menu','lst scn sch m','lst sch m','list find menu','lst fnd m'],
            'desc':f'List Scans with search by scanned text with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(sch=True,menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list scan dated menu','lst scn dt m','lst dt m','list dtd m','lst d m'],
            'desc':f'List Scans within start and end dates with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(dated=True,menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list scan search date menu','lst scn sch dt m','lst sch dt m','list find dt m','lst fnd dt m'],
            'desc':f'List Scans with search by scanned text between start and end dates with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(sch=True,dated=True,menu=True)
        }

        self.options[str(uuid1())]={
            'cmds':['scan1','scn1',],
            'desc':f'Scan and add {Fore.light_yellow}1{Fore.medium_violet_red}{Style.reset}',
            'exec':self.scan_add
        }
        self.options[str(uuid1())]={
            'cmds':['scan-multi','scan-batch','scn-btch','scn-mlt','scn1',],
            'desc':f'Scan and add a {Fore.light_yellow}Custom{Fore.medium_violet_red} value{Style.reset}',
            'exec':lambda:self.scan_add(value=None)
        }
        #new methods() start

        #new methods() end
        self.options[str(uuid1())]={
            'cmds':['fcmd','findcmd','find cmd'],
            'desc':f'Find {Fore.light_yellow}cmd{Fore.medium_violet_red} and excute for return{Style.reset}',
            'exec':self.findAndUse2
        }
        self.DESCRIPTION=f'''
A Scanner software that prompts for text, and if a duplicate is found, select the duplicate, and increments a counter TimesScanned.
This is made for making lists, where a name tied to a barcode is not necessary, but keeping qty is.
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
                    options[i]['exec']()
                    break

