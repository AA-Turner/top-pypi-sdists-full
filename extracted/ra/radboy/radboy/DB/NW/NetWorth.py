from . import *
from decimal import Decimal as float
@dataclass
class NetWorth(BASE,Template):
    __tablename__="NetWorth"
    nwid=Column(Integer,primary_key=True)

    Name=Column(String,default=None)
    ForWhom=Column(String,default=None)
    NetWorth=Column(Float,default=None)
    DTOE=Column(DateTime,default=datetime.now())


    '''liabilities ; if balance in name it is a liability'''
    Morgage_balance=Column(Float,default=0)
    Loan_balance=Column(Float,default=0)
    Credit_card_balance=Column(Float,default=0)
    Unlisted_balance=Column(Float,default=0)
    
    '''current liabilities'''
    Accounts_payable_balance=Column(Float,default=0)
    #Money a company owes to its suppliers for goods or services purchased on credit.
    Accrued_expenses_balance=Column(Float,default=0)
    #Expenses that have been incurred but not yet paid, such as employee wages and utility bills.
    ShortTerm_notes_or_loans_payable_balance=Column(Float,default=0)
    #Debts from a bank or other lender that must be repaid within the year.
    Taxes_payable_balance=Column(Float,default=0)
    #Sales, income, or payroll taxes collected or owed but not yet paid to the government.
    Unearned_revenue_balance=Column(Float,default=0)
    #Cash received from customers for a product or service that has not yet been delivered. The company has a liability to provide the good or service in the future.
    Dividends_payable_balance=Column(Float,default=0)
    #Dividends that have been declared by a company's board of directors but have not yet been paid to shareholders.
    Current_portion_of_LongTerm_debt_balance=Column(Float,default=0)
    #The portion of a long-term loan or mortgage that is due within the next year. 
    LongTerm_NonCurrent_liabilities_balance=Column(Float,default=0)
    LongTerm_notes_payable_or_loans_balance=Column(Float,default=0)
    # Debts with a maturity date extending beyond one year.
    Mortgages_payable_balance=Column(Float,default=0)
    # Long-term loans used to purchase property, such as an office building.
    Bonds_payable_balance=Column(Float,default=0)
    # Debt issued by a company to raise capital from investors, with repayment typically scheduled over a fixed period.
    Deferred_tax_liabilities_balance=Column(Float,default=0)
    # A tax a business owes that is not payable in the current period, often resulting from differences between tax rules and accounting rules for revenue or expenses.
    Lease_obligations_balance=Column(Float,default=0)
    # Payments owed under long-term capital lease agreements for assets like equipment or vehicles.
    Pension_liabilities_balance=Column(Float,default=0)
    # The obligation a company has to pay future retirement benefits to its employees. 
    Contingent_liabilities_balance=Column(Float,default=0)
    Pending_lawsuits_balance=Column(Float,default=0)
    # If a company is being sued, it may face a liability if the lawsuit is successful.
    Product_warranties_balance=Column(Float,default=0)
    # The estimated cost to repair or replace products under a warranty.
    Environmental_cleanup_costs_balance=Column(Float,default=0)
    # A potential liability for environmental damage caused by the business. 
    Student_loans_balance=Column(Float,default=0)
    ''' The total amount owed for educational debt.'''
    Vehicle_loans_balance=Column(Float,default=0)
    ''' Debt for a car, boat, or other vehicle.'''
    Personal_loans_balance=Column(Float,default=0)
    ''' Unsecured loans from a bank or other lender.'''
    Lines_of_credit_balance=Column(Float,default=0)
    ''' Revolving credit accounts.'''
    Unpaid_bills_balance=Column(Float,default=0)
    ''' Obligations such as utility bills, medical bills, or taxes.
    Loans from family and friends: Money owed to individuals rather than a commercial lender'''

    '''liabilities notes'''
    liabilities_notes=Column(String,default='')
    '''assets'''
    Real_Estate_assets=Column(Float,default=0)
    Personal_Property_assets=Column(Float,default=0)

    Retirement_assets=Column(Float,default=0)
    plan_401K_assets=Column(Float,default=0)
    Individual_Retirement_Accounts_IRA_assets=Column(Float,default=0)
    Pension_plans_assets=Column(Float,default=0)
    Keogh_plans_assets=Column(Float,default=0)
    college_savings_plans_529_assets=Column(Float,default=0)

    Investments_assets=Column(Float,default=0)
    Stocks_and_bonds_assets=Column(Float,default=0)
    Mutual_funds_and_ExchangeTraded_Funds_EFT_assets=Column(Float,default=0)
    Brokerage_accounts_assets=Column(Float,default=0)
    Investment_properties_and_rental_real_estate_assets=Column(Float,default=0)
    Digital_assets_like_cryptocurrency_and_NFTs_assets=Column(Float,default=0)
    Annuities_assets=Column(Float,default=0)
    Liquid_assets=Column(Float,default=0)
    Cash_assets=Column(Float,default=0)
    Checking_account_assets=Column(Float,default=0)
    Savings_account_assets=Column(Float,default=0)
    Certificates_of_deposit_assets=Column(Float,default=0)
    Treasury_bills_assets=Column(Float,default=0)
    Intangible_assets=Column(Float,default=0)
    Patents_assets=Column(Float,default=0)
    trademarks_assets=Column(Float,default=0)
    copyrights_assets=Column(Float,default=0)
    Royalties_assets=Column(Float,default=0)
    Intellectual_property_assets=Column(Float,default=0)
    business_interests_assets=Column(Float,default=0)
    Equity_in_a_business_assets=Column(Float,default=0)
    Ownership_shares_assets=Column(Float,default=0)
    Business_equipment_and_inventory_assets=Column(Float,default=0)
    Unlisted_assets=Column(Float,default=0)
    assets_notes=Column(String,default='')

    Comments=Column(String,default='')


    def __init__(self,*arg,**kwargs):
        for k in kwargs.keys():
            if k in [s.name for s in self.__table__.columns]:
                setattr(self,k,kwargs.get(k))
        if 'NetWorth' in kwargs.keys():
            if kwargs['NetWorth'] not in [None,0]:
                print(kwargs['NetWorth'])
                return
            else:
                kwargs.pop('NetWorth')
        #print('NetWorth' in kwargs.keys())
        if not 'NetWorth' in kwargs.keys():
            asset_fields=[x.name for x in __class__.__table__.columns if 'assets' in x.name and str(x.type).lower() in ['float','int','integer',]]
            self.asset_fields=tuple(asset_fields)
            print(asset_fields)
            assTTL=0
            for num,i in enumerate(asset_fields):
                try:
                    old=self.NetWorth
                except Exception as e:
                    self.NetWorth=float(0)
                    old=self.NetWorth
                    print(e)
                try:
                    current=float(getattr(self,i))
                except Exception as e:
                    current=0

                print(i,old,current,getattr(self,i))
                if old is None:
                    old=float(0)
                if current is None:
                    current=float(0)
                assTTL+=current
                self.NetWorth=assTTL

            liabilities_fields=[x.name for x in __class__.__table__.columns if 'balance' in x.name and str(x.type).lower() in ['float','int','integer',]]
            self.liabilities_fields=tuple(liabilities_fields)
            lblTTL=0
            for num,i in enumerate(liabilities_fields):
                
                try:
                    old=self.NetWorth
                except Exception as e:
                    self.NetWorth=float(0)
                    old=self.NetWorth
                    print(e)
                try:
                    current=float(getattr(self,i))
                except Exception as e:
                    current=0
                if old is None:
                    old=float(0)
                if current is None:
                    current=float(0)
                lblTTL-=current
                print(i,old,current,getattr(self,i))
            
            self.NetWorth+=lblTTL
            print(self.NetWorth)

try:
    NetWorth.metadata.create_all(ENGINE)
except Exception as e:
    NetWorth.__table__.drop(ENGINE)
    NetWorth.metadata.create_all(ENGINE)


class NetWorthUi:
    def fix_table(self):
        NetWorth.__table__.drop(ENGINE)
        NetWorth.metadata.create_all(ENGINE)

    def add(self):
        with Session(ENGINE) as session:
            nw=NetWorth()
            session.add(nw)
            session.commit()
            session.refresh(nw)
            excludes=['nwid',]
            fields={i.name:{'default':getattr(nw,i.name),'type':str(i.type).lower()} for i in nw.__table__.columns if i.name not in excludes}
            fd=FormBuilder(data=fields,passThruText="Add a New NetWorth Log")
            if fd is None:
                session.delete(nw)
                session.commit()
                return
            nw.__init__(**fd)
            #session.query(NetWorth).filter(NetWorth.nwid==nw.nwid).update(fd)
            session.commit()
            session.refresh(nw)
            print(nw)
            

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
                really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Really delete All NetWorth's?",helpText="yes or no boolean,default is NO",data="boolean")
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
            session.query(NetWorth).delete()
            session.commit()

    def clear_all(self):
        fieldname=f'{__class__.__name__}'
        mode=f'ClearAll'
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
        
        code=''.join([str(random.randint(0,9)) for i in range(10)])
        verification_protection=detectGetOrSet("Protect From Delete",code,setValue=False,literal=True)
        while True:
            try:
                really=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{h}Really Clear All NetWorth's to NetWorth=0?",helpText="yes or no boolean,default is NO",data="boolean")
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
            session.query(NetWorth).update({'NetWorth':0,'DTOE':datetime.now(),'Note':''})
            session.commit()

    def list_scan(self,sch=False,dated=False,menu=False):
        default=True
        FORMAT=self.FORMAT()
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
        
        
        with Session(ENGINE) as session:
            query=session.query(NetWorth)
            
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
                query=query.filter(and_(NetWorth.DTOE<end_date,NetWorth.DTOE>start_date))

            if sch:
                term=Control(func=FormBuilderMkText,ptext="What are you looking for? ",helpText="a string of text",data="string")
                if term is None:
                    return
                elif term in ['d','NaN']:
                    term=''
                query=query.filter(or_(NetWorth.Name.icontains(term),NetWorth.ForWhom.icontains(term),NetWorth.Comments.icontains(term)))

            query=orderQuery(query,NetWorth.DTOE,inverse=True)
            results=query.all()
            cta=len(results)
            if cta < 1:
                print("There are no results!")
                return
            for num, i in enumerate(results):
                
                if not terse:
                    msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                else:
                    msg=self.terse(i,num,cta)
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
                            msg=std_colorize(f"{Fore.light_magenta}{i.Name}:{Fore.light_red}{i.nwid}[{Fore.green_yellow}{i.DTOE}] = {Fore.cyan}{i.NetWorth} {Fore.dark_goldenrod}",num,cta)
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
                            msg=self.tersed(i,num,cta)
                        print(msg)
                    elif doWhat.lower() in "reset/rst".split("/"):
                        self.edit(i,reset=True)
                        session.refresh(i)
                        if not terse:
                            msg=std_colorize(f"{Fore.light_magenta}{__class__.__name__}{Fore.dark_goldenrod}{i}",num,cta)
                        else:
                            msg=self.tersed(i,num,cta)
                        print(msg)
                if (num % 15) == 0 and num > 0:
                    print(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}")
                    if writeToFile:
                        self.save2file_write(f"{Fore.grey_70}{'*'*os.get_terminal_size().columns}")

            print(FORMAT)
            if writeToFile:
                print(f"Written to {str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)))}")
                self.save2file_write(strip_colors(FORMAT))


    def FORMAT(self):
        return f"{Fore.light_magenta}Name:{Fore.light_red}nwID[{Fore.green_yellow}DTOE] = {Fore.cyan}$NETWORTH {Fore.dark_goldenrod}"

    def terse(self,i,num,cta):
        return std_colorize(f"{Fore.light_magenta}{i.Name}:{Fore.light_red}{i.nwid}[{Fore.green_yellow}{i.DTOE}] = {Fore.cyan}{i.NetWorth} {Fore.dark_goldenrod}",num,cta)

    def edit(self,i:NetWorth,excludes=['nwid',],reset=False,clear=False):
        if reset:
            with Session(ENGINE) as session:
                 r=session.query(NetWorth).filter(NetWorth.nwid==i.nwid).first()
                 r.Name=''
                 r.DTOE=datetime.now()
                 r.Note=''
                 r.NetWorth=0
                 session.commit()
            return

        if clear:
            with Session(ENGINE) as session:
                 r=session.query(NetWorth).filter(NetWorth.nwid==i.nwid).first()
                 r.DTOE=datetime.now()
                 r.Note=''
                 r.NetWorth=0
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
            r=session.query(NetWorth).filter(NetWorth.nwid==i.nwid).first()
            r.__init__(**fd)

            session.commit()

    def last_NetWorth(self):
        '''print hight times scanned w/ prompt for how many and offset'''
        default=True
        FORMAT=self.FORMAT()
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
            
            query=session.query(NetWorth)
            query=orderQuery(query,NetWorth.NetWorth)
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
            print(FORMAT)
            if writeToFile:
                print(f"Written to {str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)))}")
                self.save2file_write(strip_colors(FORMAT))

    def clear_file(self):
        with Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)).open('w') as out:
            out.write('')
        print("Cleared!")

    def last_DTOE(self):
        default=True
        FORMAT=self.FORMAT()
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
            
            query=session.query(NetWorth)
            query=orderQuery(query,NetWorth.DTOE)
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
            if writeToFile:
                print(f"Written to {str(Path(db.detectGetOrSet('text2file','TextOut.txt',setValue=False,literal=True)))}")
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
    def fields(self):
        print("assets -------- ")
        zz=NetWorth().asset_fields
        ct=len(zz)
        for num,i in enumerate(zz):
            print(std_colorize(i,num,ct))
        zz=NetWorth().liabilities_fields
        print("liabilities -------- ")
        ct=len(zz)
        for num,i in enumerate(zz):
            print(std_colorize(i,num,ct))



    def __init__(self):
        MENUDO="edit,delete, clear count,reset all fields"
        self.options={}
        self.options[str(uuid1())]={
            'cmds':generate_cmds(startcmd=["fix","fx"],endCmd=['tbl','table']),
            'desc':'''
drop and regenerate NetWorth Table
            ''',
            'exec':self.fix_table
        }
        self.options[str(uuid1())]={
            'cmds':['ca','clearall','clear all','clear-all','clear.all'],
            'desc':f'clear networth of all NetWorths',
            'exec':self.clear_all
        }
        self.options[str(uuid1())]={
            'cmds':['fields','flds'],
            'desc':f'clear networth of all NetWorths',
            'exec':self.fields
        }
        self.options[str(uuid1())]={
            'cmds':['add','new','a'],
            'desc':f'add a new networth',
            'exec':self.add
        }
        self.options[str(uuid1())]={
            'cmds':['da','deleteall','delete all','delete-all','delete.all'],
            'desc':f'delete all of NetWorth\'s',
            'exec':self.delete_all
        }
        self.options[str(uuid1())]={
            'cmds':['list networth','lst nw',],
            'desc':f'List Scans',
            'exec':self.list_scan
        }
        self.options[str(uuid1())]={
            'cmds':['clear file','clr fl',],
            'desc':f'clear outfile',
            'exec':self.clear_file
        }
        self.options[str(uuid1())]={
            'cmds':['list networth search','lst nw sch','lst nw','list find','lst fnd'],
            'desc':f'List NetWorth\'s with search by text',
            'exec':lambda self=self:self.list_scan(sch=True)
        }
        self.options[str(uuid1())]={
            'cmds':['last by dtoe','lst dtoe'],
            'desc':f'List NetWorth with limit and offset using rllo/vllo for ordering by dtoe',
            'exec':lambda self=self:self.last_DTOE()
        }
        self.options[str(uuid1())]={
            'cmds':['last by timesscanned','lst ts'],
            'desc':f'List NetWorth with limit and offset using rllo/vllo for ordering by NetWorth',
            'exec':lambda self=self:self.last_NetWorth()
        }
        self.options[str(uuid1())]={
            'cmds':['list networth dated','lst nw dt','lst dt','list dtd','lst d'],
            'desc':f'List networth within start and end dates',
            'exec':lambda self=self:self.list_scan(dated=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list networth search date','lst nw sch dt','lst sch dt','list find dt','lst fnd dt'],
            'desc':f'List networth with search by scanned text between start and end dates',
            'exec':lambda self=self:self.list_scan(sch=True,dated=True)
        }

        self.options[str(uuid1())]={
            'cmds':['list networth menu','lst nw m',],
            'desc':f'List NetWorth\'s with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list networth search menu','lst nw sch m','lst sch m','list find menu','lst fnd m'],
            'desc':f'List networth with search by scanned text with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(sch=True,menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list networth dated menu','lst nw dt m','lst dt m','list dtd m','lst d m'],
            'desc':f'List Scans within start and end dates with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(dated=True,menu=True)
        }
        self.options[str(uuid1())]={
            'cmds':['list networth search date menu','lst nw sch dt m','lst sch dt m','list find dt m','lst fnd dt m'],
            'desc':f'List networth with search by scanned text between start and end dates with menu to {MENUDO}',
            'exec':lambda self=self:self.list_scan(sch=True,dated=True,menu=True)
        }

        #new methods() start

        #new methods() end
        self.options[str(uuid1())]={
            'cmds':['fcmd','findcmd','find cmd'],
            'desc':f'Find {Fore.light_yellow}cmd{Fore.medium_violet_red} and excute for return{Style.reset}',
            'exec':self.findAndUse2
        }


        self.DESCRIPTION=f'''
record/list your networth logs
'Add' NetWorth or Calculate it?
    if you already know it and just enter your networth, then the calculations are not performed, but the liabilities
and assets are still stored.

    if you don't, then leave networth as None using 'NAN', or as 0, and follow the prompts to enter your 
liabilities and assets. Once you are finished adding your information type one of below:
 'f','<enter>','f'
 'ff' the first time

to save your log.

This allows you to keep track of your NetWorth.
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

