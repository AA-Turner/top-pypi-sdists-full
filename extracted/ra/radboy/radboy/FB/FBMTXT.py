import radboy.TasksMode as TM
import radboy.DB.db as db
import string
from datetime import datetime,date,time
from pathlib import Path
from decimal import Decimal,getcontext
import re
from datetime import timedelta
import calendar
from colored import Fore,Back,Style
import itertools
from uuid import uuid1
import pint
import pandas as pd
from fractions import Fraction

def generate_cmds(startcmd,endCmd):
    cmd=(startcmd,endCmd)
    cmds=[]
    for i in itertools.product(startcmd,endCmd):
        if ''.join(i) not in cmds:
            cmds.append(''.join(i))
        if ' '.join(i) not in cmds:
            cmds.append(' '.join(i))
    return cmds

fm_data={
        'Decimal':{
            'type':'decimal',
            'default':Decimal('0.00000'),
            },
        'decimal.decimal':{
            'type':'decimal.decimal',
            'default':Decimal('0.00000'),
            },
        'Name':{
            'type':'str',
            'default':'',
            },
        'Value':{
            'type':'int',
            'default':0,
            },
        'Price':{
           'type':'float',
           'default':0.0,
            },
        'Barcode':{
            'type':'str',
            'default':'000000000000',
            },
        'Code':{
            'type':'str',
            'default':'12345678',
            },
        'DOE':{
            'type':'date',
            'default':None,
            },
        'TOE':{
            'type':'time',
            'default':None,
            },
        'DTOE':{
            'type':'datetime',
            'default':None,
            },
        'DEFAULT':{
            'type':'bool',
            'default':False,
            },
        'List':{
            'type':'list',
            'default':[],
            },
        'Quantity':{
            'type':'quantity',
            'default':'1 oz',
            },
        'Path':{
            'type':'path',
            'default':'./',
            },
        'rPath':{
            'type':'rpath',
            'default':'./',
            },
        'Timedelta':{
        'type':'timedelta',
        'default':timedelta()
        },
        'Fraction':{
        'type':'fraction',
        'default':Fraction()
        }
      }
UNDER_RND="Under Development; not functional!"
def FormBuilderHelpText():
    TODAY_IS=datetime.now()
    z=TODAY_IS
    msg=f'''{Fore.light_magenta}FormBuilder(data=dict()) Help{Style.reset}
    {Fore.light_yellow}Dates useable by KeyWord (Cheat Sheet for DateTime){Style.reset}
    {Fore.light_cyan}'y','yes','1','t','true','+' {Fore.light_green}-{Fore.light_steel_blue} calls the datepicker{Style.reset}
    {Fore.light_cyan}"n,no,false,f,0,-" {Fore.light_green}-{Fore.light_steel_blue} returns default{Style.reset}
    {Fore.light_cyan}now {Fore.light_green}-{Fore.light_steel_blue} {datetime.now()}{Style.reset}
    {Fore.light_cyan}tdy {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)}{Style.reset}
    {Fore.light_cyan}tomorrow {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24)}{Style.reset}
    {Fore.light_cyan}yesterday {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24)}{Style.reset}
    {Fore.light_cyan}last month {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24*30)} {Style.reset}
    {Fore.light_cyan}last year {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24*365)}{Style.reset}
    {Fore.light_cyan}next month {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24*30)}{Style.reset}
    {Fore.light_cyan}next week {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24*7)}{Style.reset}
    {Fore.light_cyan}last week {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24*7)}{Style.reset}
    {Fore.light_cyan}next year {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24*365)}{Style.reset}
    {Fore.light_cyan}end week {Fore.light_green}-{Fore.light_steel_blue} {TODAY_IS+timedelta(days=TODAY_IS.weekday())}{Style.reset}
    {Fore.light_cyan}end month {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=calendar.monthrange(z.year,TODAY_IS.month)[-1])}{Style.reset}
    {Fore.light_cyan}end year {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=12,day=calendar.monthrange(z.year,12)[-1])}{Style.reset}
    {Fore.light_cyan}start week {Fore.light_green}-{Fore.light_steel_blue} {TODAY_IS-timedelta(days=TODAY_IS.weekday())}{Style.reset}
    {Fore.light_cyan}start month {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=1)}{Style.reset}
    {Fore.light_cyan}start year {Fore.light_green}-{Fore.light_steel_blue} {datetime(year=TODAY_IS.year,month=1,day=1)}{Style.reset}
    {Fore.light_cyan}last month start{Fore.light_steel_blue} last month's start date (1) {Style.reset}
    {Fore.light_cyan}last month end{Fore.light_steel_blue} last month's end date(28,29,30, or 31){Style.reset}
    {Fore.light_cyan}next month start{Fore.light_steel_blue} next month's start date (1){Style.reset}
    {Fore.light_cyan}next month end{Fore.light_steel_blue} next month's end date(28,29,30, or 31){Style.reset}
    {Fore.grey_70}**{Fore.light_yellow}A Date Can be represented as {Fore.light_cyan}10.26.25={Fore.cyan}10/26/25=10/26/2025={Fore.light_green}oct.26.25={Fore.spring_green_3a}oct/26/25={Fore.light_steel_blue}oct.26.2025{Style.reset}
    {Fore.grey_70}**{Fore.light_yellow}Any of {Fore.yellow}{string.punctuation} {Fore.light_cyan}in `datetime` can be use as the separator, as long as they are the same throughout the string{Style.reset}
    {Fore.grey_70}**{Fore.light_yellow}10.26.1993@4:30{Fore.light_cyan} represents 10/26/1993 at 4:30am, where at indicates a separation to the time string{Style.reset}
    {Fore.grey_70}**{Fore.light_yellow}when {Fore.light_cyan}-{Fore.light_yellow} is used, ususally when a daterange is expected, needs to be between two(2) datestrings, i.e. {Fore.light_steel_blue}10.26.1993-12.15.1997{Style.reset}
    {Fore.grey_70}**{Fore.light_yellow}RETRY{Fore.light_cyan} is issued when parsing fails.{Style.reset}
    {Fore.light_cyan}**{Fore.light_steel_blue}Boolean True={Fore.spring_green_3a}y,yes,Yes,Y,True,T,t,1 or an equation that results in a True such as {Fore.orange_red_1}`datetime.now()`/{datetime.now()}`!=datetime(2001,1,1)`/{datetime(2001,1,1)} or 1==1.{Style.reset}
    {Fore.light_cyan}**{Fore.light_steel_blue}Boolean False={Fore.spring_green_3a}false,no,n,N,No,False,0 or an equation that results in a False such as {Fore.orange_red_1}`datetime.now()`/{datetime.now()}`==datetime(2001,1,1)`/{datetime(2001,1,1)} or 1==0.{Style.reset}
    {Fore.medium_violet_red}**{Fore.light_magenta}When Asked for a List of integers {Fore.magenta}use 1,2,3 for indexes 1-3, {Fore.orange_red_1}or 1,3 for indexes 1 and 3, {Fore.light_red}or 1,4,6-8,10 for indexes 1,4,6,7,8, and 10,{Fore.purple_1a} or 1 for index 1.{Style.reset}

    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming week start - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming week end - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last week start - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last week end - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}

    {Fore.green_yellow}**{Fore.light_magenta}previous/last saturday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last sunday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last monday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last tuesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last wednesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last thursday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}previous/last friday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}

    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming saturday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming sunday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming monday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming tuesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming wednesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming thursday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming friday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}

    {Fore.green_yellow}**{Fore.light_magenta}saturday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}sunday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}monday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}tuesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}wednesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}thursday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}friday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
    
    {Fore.green_yellow}**{Fore.light_magenta}ff,finish{Fore.orange_red_1}WARNING:{Fore.light_cyan}finish and return without review{Style.reset}
    {Fore.green_yellow}**{Fore.light_magenta}f,finalize{Fore.orange_red_1}WARNING:{Fore.light_cyan}finish and return with review{Style.reset}

    {Style.bold}{Fore.dark_blue}{Back.grey_70} FormBuilder {Fore.dark_red_1}Options {Style.reset}
    {Fore.light_yellow}#b{Fore.light_green} will restart {Fore.light_red}[If it is wired to, might be reverse of 'b']{Style.reset}
    {Fore.light_yellow}b{Fore.light_green} will return to previous menu{Fore.light_red}[If it is wired to, might be reverse of '#b']{Style.reset}
    {Fore.light_yellow}f{Fore.light_green} will proceeds to review, where 'f' finishes,'y/yes/1' will review,'<Enter>/<Return>/n/f/0' will act as finish{Style.reset}
    {Fore.light_yellow}p{Fore.light_green} at field filling lines goes to previous field{Style.reset}
    {Fore.light_yellow}d{Fore.light_green} use default{Style.reset}
    {Fore.light_yellow}m{Fore.light_green} use manually entered data present under m key option{Style.reset}
    {Fore.light_yellow}#done#{Fore.light_green} to finish a str+(MultiLine) Input{Style.reset}
    {Fore.grey_70}*{Fore.light_yellow}goto {Fore.light_cyan}i{Fore.light_yellow}/goto{Fore.light_cyan}i{Fore.light_green} - go to {Fore.light_cyan}index{Style.reset}
    {Fore.grey_70}*{Fore.light_yellow}goto{Fore.light_cyan}k{Fore.light_yellow},goto {Fore.light_cyan}k{Fore.light_green} goto {Fore.light_cyan}key{Fore.light_green} for field in Form {Style.reset}
    {Fore.grey_70}*{Fore.light_yellow}showkeys{Fore.light_green} to see indexes refering to form keys{Style.reset}
    {Fore.grey_70}*{Fore.light_yellow}'schk','search keys','sch ky{Fore.light_green} to search select and goto key{Style.reset}
    {Fore.grey_70}* {Fore.grey_50}These cmds only work with fields that return str/VARCHAR/TEXT/str+/list of str's, i.e. [str,]
    {Fore.grey_70}*{Fore.grey_50}['na','not_a_number','nan']{Fore.light_green} set a field to None{Style.reset}
    {Fore.grey_70}*{Fore.grey_50}['all na','all not_a_number','anan']{Fore.light_green} set all fields to None; useful when all keys have defaults that are not none, but all except certain ones need to be none{Style.reset}
    {Fore.grey_70}*{Fore.grey_50}#ml#start of line
    end of line#ml#{Fore.light_green} enter a multi-line input{Style.reset}'''
    print(msg)


def FormBuilderMkText(text,data,passThru=[],PassThru=True,alternative_false=None,alternative_true=None):
    if text is None:
        return None
    if text.lower() in ['na','not_a_number','nan']:
        return 'NaN'
    try:
        #if text in passThru:
        #    return text
        if PassThru:
            if text in ['f','m','p','d']:
                return text
            if text in passThru:
                return text
        if text == '':
            return 'd'
        value=None
        if data.lower() == 'float':
            try:
                value=float(eval(text))
            except Exception as e:
                try:
                    value=float(text)
                except Exception as e:
                    return 'd'
        elif data.lower() in ['decimal.decimal','dec.dec']:
            try:
                value=Decimal(text)
                return value
            except Exception as e:
                print(e)
                return Decimal('0.0000')
        elif data.lower() in ['decimal','dec']:
            try:
                getcontext().prec=3
                old_str=text
                old_str_list=list(reversed(sorted([i for i in re.findall(r"[0-9.]+",text)],key=len)))
                newstr_list=list(reversed(sorted([str(f'Decimal({i})') for i in re.findall(r"[0-9.]+",text)],key=len)))
                for num,x in enumerate(old_str_list):
                    #print(num,x,newstr_list[num])
                    old_str=old_str.replace(x,newstr_list[num])

                value=eval(old_str)
                print(value)
                return float(value)
            except Exception as e:
                print(e)
                return 'd'
        elif data.lower() in ['int','integer']:
            try:
                value=int(eval(text))
            except Exception as e:
                try:
                    value=int(text)
                except Exception as e:
                    return 'd'
        elif data.lower() in ['bool','boolean','boolean_basic']:
            if alternative_true not in [None,]:
                if text == alternative_true:
                    return True
            if alternative_false not in [None,]:
                if text == alternative_false:
                    return False
            try:
                value=bool(eval(text))
            except Exception as e:
                try:
                    if data.lower() in ['boolean_basic',]:
                        for i in ['n','no','false','f']:
                            if i in text.lower():
                                return False
                        for i in ['y','yes','true','t']:
                            if i in text.lower():
                                return True
                        return None
                    if text.lower() in ['y','yes','true','t','1']:
                        value=True
                    elif text.lower() in ['n','no','false','f','0']:
                        value=False
                    else:
                        try:
                            if data.lower() not in ['boolean_basic',]:
                                value=bool(eval(text))
                            else:
                                return False
                        except Exception as e:
                            return 'd'
                except Exception as e:
                    return 'd'
        elif data.lower() in ['str','string',"varchar","text"]:
            value=text
        elif data.lower() == 'date':
            if text.lower() in ['y','yes','1','t','true']:
                value=TM.Tasks.TasksMode(parent=None,engine=db.ENGINE,init_only=True).DatePkr()
            else:
                try:
                    def try_date(ds,format='%m%d%Y'):
                        try:
                            #print(format)
                            return datetime.strptime(ds,format)
                        except Exception as e:
                            #print(e)
                            return None
                    def process_ds(ds):
                        months=['january','february','march','april','may','june','july','august','september','october','november','december']
                        predate="%m{c}%d{c}{year}"
                        t1=[]
                        chars=[i for i in string.punctuation]
                        chars.pop(chars.index('%'))
                        for i in chars:
                            test=ds.split(i)
                            if len(test) == 3:
                                for num,m in enumerate(months):
                                    if test[0].lower() == m or m.startswith(test[0].lower()):
                                        test[0]=str(num+1).zfill(2)
                                        ds=f'{i}'.join(test)
                                        break
                        for i in chars:
                            for year in ['%y','%Y']:
                                t1.append(predate.format(c=i,year=year))
                                for ii in chars:
                                    for year in ['%y','%Y']:
                                        t1.append(f"%m{i}%d{ii}{year}")
                        for f in t1:
                                dt=try_date(format=f,ds=ds)
                                if dt:
                                    return dt
                    value=process_ds(text)
                except Exception as e:
                    print(e)
        elif data.lower() == 'time':
            if text.lower() in ['y','yes','1','t','true']:
                value=TM.Tasks.TasksMode(parent=None,engine=db.ENGINE,init_only=True).TimePkr()
            else:
                try:
                    def try_time(ds,format='%m%d%Y'):
                        try:
                            #print(format)
                            todaysDate=datetime.strptime(ds,format)
                            return time(todaysDate.hour,todaysDate.minute,todaysDate.second)
                        except Exception as e:
                            print(e)
                            return None
                    def process_time(ds):
                        predate="%H{c}%M{c}%S"
                        t1=[]
                        chars=[i for i in string.punctuation]
                        chars.pop(chars.index('%'))

                        for i in chars:
                            t1.append(predate.format(c=i))
                            for ii in chars:
                                t1.append(f"%H{i}%M{ii}%S")
                        for f in t1:
                            dt=try_time(format=f,ds=ds)
                            if dt:
                                return dt
                    value=process_time(text)
                except Exception as e:
                    print(e)
        elif data.lower() in ['datetime','datetime-','datetime~']:
            try:
                try:
                    if text.lower() not in ['today','tdy']:
                        return pd.to_datetime([text,],format="mixed")[0].to_pydatetime()
                except Exception as e:
                    print(e,"Trying some other methods next...")
                def regexSelect(ds):
                    fmt={}
                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9][0-9]"),"%m#CHAR#%y"]
                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9][0-9][0-9][0-9]"),"%m#CHAR#%Y"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9][0-9][0-9][0-9]"),"%m#CHAR#%Y"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9][0-9]"),"%m#CHAR#%y"]

                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9][0-9].[0-9][0-9]"),"%m#CHAR#%d#CHAR#%y"]
                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9][0-9].[0-9][0-9]"),"%m#CHAR#%d#CHAR#%y"]

                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9][0-9].[0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9][0-9].[0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%y@%H:%M"]

                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9].[0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9].[0-9][0-9][0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9].[0-9][0-9][0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9].[0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%y@%H:%M"]

                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9].[0-9][0-9]@[0-9][0-9]:[0-9]"),"%m#CHAR#%d#CHAR#%y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-1][0-9].[0-9].[0-9][0-9][0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9].[0-9][0-9][0-9][0-9]@[0-9][0-9]:[0-9][0-9]"),"%m#CHAR#%d#CHAR#%Y@%H:%M"]
                    fmt[str(uuid1())]=[re.compile(r"[0-9].[0-9].[0-9][0-9]@[0-9][0-9]:[0-9]"),"%m#CHAR#%d#CHAR#%y@%H:%M"]

                    ct=len(fmt)
                    for num,i in enumerate(fmt):
                        print(db.std_colorize(fmt[i],num,ct))

                    for i in fmt:
                        if fmt[i][0].findall(ds) != []:
                            print(fmt[i][1])
                            for char in ds:
                                if char in string.punctuation:
                                    try:
                                        fmt[i][1]=fmt[i][1].replace("#CHAR#",char)
                                        return True,datetime.strptime(ds,fmt[i][1])
                                    except Exception as e:
                                        print(e)

                    return False,None

                TODAY_IS=datetime.now()
                z=TODAY_IS
                
                if text.lower() in ['y','yes','1','t','true','+']:
                    value=TM.Tasks.TasksMode(parent=None,engine=db.ENGINE,init_only=True).DateTimePkr()
                elif text.lower() in ['now',]:
                    return datetime.now()
                elif regexSelect(text.lower())[0] == True:
                    bild=regexSelect(text.lower())
                    return bild[-1]
                elif text.lower() in ['tdy','today']:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day,hour=0,minute=0,second=0)
                elif text.lower() in ['tomorrow',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24)
                elif text.lower() in ['yesterday',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24)
                    #I might add more for these phrases, where its literally that amount of time to
                elif text.lower() in ['last month',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24*30)
                elif text.lower() in ['last year',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24*365)
                elif text.lower() in ['next month',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24*30)
                elif text.lower() in ['next week',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24*7)
                elif text.lower() in ['last week',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)-timedelta(seconds=60*60*24*7)

                    '''
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming week start - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming week end - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last week start - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last week end - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    [RDY]
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last saturday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last sunday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last monday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last tuesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last wednesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last thursday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}previous/last friday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    [RDY]
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming saturday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming sunday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming monday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming tuesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming wednesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming thursday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}next/this/upcoming friday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} from today{Style.reset}
                    [RDY]
                    {Fore.green_yellow}**{Fore.light_magenta}saturday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}sunday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}monday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}tuesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}wednesday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}thursday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    {Fore.green_yellow}**{Fore.light_magenta}friday - {Fore.orange_red_1}WARNING:{Fore.light_cyan} of this week only{Style.reset}
                    '''
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['week end','w e','we']):
                    today=datetime.now()
                    friday=6
                    weekEnd=today+timedelta(days=(friday-today.weekday())%7)
                    weekEnd-=timedelta(days=7)
                    return weekEnd
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['week start','w s','ws']):
                    today=datetime.now()
                    friday=6
                    Friday=today+timedelta(days=(friday-today.weekday())%7)
                    weekStart=Friday-timedelta(days=7)
                    weekStart-=timedelta(days=6)
                    return weekStart                    
                elif text.lower() in generate_cmds(startcmd=['next','upcoming'],endCmd=['week end','w e','we']):
                    today=datetime.now()
                    friday=6
                    weekEnd=today+timedelta(days=(friday-today.weekday())%7)
                    weekEnd+=timedelta(days=7)
                    return weekEnd
                elif text.lower() in generate_cmds(startcmd=['next','upcoming'],endCmd=['week start','w s','ws']):                    
                    today=datetime.now()
                    friday=0
                    Friday=today+timedelta(days=(friday-today.weekday())%7)
                    weekStart=Friday-timedelta(days=7)
                    weekStart+=timedelta(days=7)
                    return weekStart
                elif text.lower() in generate_cmds(startcmd=['this','current'],endCmd=['week end','w e','we']):                    
                    today=datetime.now()
                    friday=6
                    weekEnd=today+timedelta(days=(friday-today.weekday())%7)
                    return weekEnd
                elif text.lower() in generate_cmds(startcmd=['this','current'],endCmd=['week start','w s','ws']):                    
                    today=datetime.now()
                    friday=6
                    Friday=today+timedelta(days=(friday-today.weekday())%7)
                    weekStart=Friday-timedelta(days=7)
                    return weekStart
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['friday',]):
                    dayNum=4
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['saturday',]):
                    dayNum=5
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['sunday',]):
                    dayNum=6
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['monday',]):
                    dayNum=0
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['tuesday',]):
                    dayNum=1
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['wednesday',]):
                    dayNum=2
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['previous','last','prev'],endCmd=['thursday',]):
                    dayNum=3
                    today=datetime.now()
                    daysUntil=(dayNum-today.weekday())%7
                    dayOf=today+timedelta(days=daysUntil)
                    lastDay=dayOf-timedelta(days=7)
                    return lastDay
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['friday',]):
                    dayOfWeek=4
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['saturday',]):
                    dayOfWeek=5
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['sunday',]):
                    dayOfWeek=6
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['monday',]):
                    dayOfWeek=0
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    #add %7 for next
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['tuesday',]):
                    dayOfWeek=1
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['wednesday',]):
                    dayOfWeek=2
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in generate_cmds(startcmd=['next','this','upcoming'],endCmd=['thursday',]):
                    dayOfWeek=3
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)%7
                    if untilDayOfWeek == 0:
                        untilDayOfWeek=7
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when

                elif text.lower() in ['friday',]:
                    dayOfWeek=4
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in ['saturday',]:
                    dayOfWeek=5
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in ['sunday',]:
                    dayOfWeek=6
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in ['monday',]:
                    dayOfWeek=0
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    #add %7 for next
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in ['tuesday',]:
                    dayOfWeek=1
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in ['wednesday',]:
                    dayOfWeek=2
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when
                elif text.lower() in ['thursday',]:
                    dayOfWeek=3
                    today=datetime.now()
                    todaysDayOfWeek=today.weekday()
                    untilDayOfWeek=(dayOfWeek-todaysDayOfWeek)
                    when=datetime(today.year,today.month,today.day)+timedelta(days=untilDayOfWeek)
                    return when

                elif text.lower() in ['next year',]:
                    TODAY_IS=datetime.now()
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=TODAY_IS.day)+timedelta(seconds=60*60*24*365)

                elif text.lower() in ['last month start',]:
                    TODAY_IS=datetime.now()
                    lastMonth=datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=1)-timedelta(days=1)
                    lastMonth_real=datetime(year=lastMonth.year,month=lastMonth.month,day=1)
                    return lastMonth_real
                elif text.lower() in ['last month end',]:
                    TODAY_IS=datetime.now()
                    lastMonth=datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=1)-timedelta(days=1)
                    #lastMonth_real=datetime(year=lastMonth.year,month=lastMonth.month,day=1)
                    return lastMonth
                elif text.lower() in ['next month start',]:
                    TODAY_IS=datetime.now()
                    days=calendar.monthrange(TODAY_IS.year,TODAY_IS.month)[-1]
                    lastMonth=datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=days)+timedelta(days=1)
                    #lastMonth_real=datetime(year=lastMonth.year,month=lastMonth.month,day=1)
                    return lastMonth
                elif text.lower() in ['next month end',]:
                    TODAY_IS=datetime.now()
                    days=calendar.monthrange(TODAY_IS.year,TODAY_IS.month)[-1]

                    lastMonth=datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=days)+timedelta(days=1)
                    nmdays=calendar.monthrange(lastMonth.year,lastMonth.month)[-1]

                    lastMonth=datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=days)+timedelta(days=nmdays)
                    return lastMonth

                elif text.lower() in ['end week',]:
                    return TODAY_IS+timedelta(days=TODAY_IS.weekday())
                elif text.lower() in ['end month',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=calendar.monthrange(z.year,TODAY_IS.month)[-1])
                elif text.lower() in ['end year',]:
                    return datetime(year=TODAY_IS.year,month=12,day=calendar.monthrange(z.year,12)[-1])
                elif text.lower() in ['start week',]:
                    return TODAY_IS-timedelta(days=TODAY_IS.weekday())
                elif text.lower() in ['start month',]:
                    return datetime(year=TODAY_IS.year,month=TODAY_IS.month,day=1)
                elif text.lower() in ['start year',]:
                    return datetime(year=TODAY_IS.year,month=1,day=1)

                
                elif text.lower() in "n,no,false,f,0,-".split(","):
                    return 'd'
                else:
                    def pandas_try(ds):
                        try:
                            result=pd.to_datetime(ds)

                            result=result.to_pydatetime()
                            return result
                        except Exception as e:
                            print(e)

                    def try_date(ds,format='%m%d%Y'):
                        try:
                            #print(format)
                            return datetime.strptime(ds,format)
                        except Exception as e:
                            #print(e)
                            return None
                    def process_ds(ds):
                        months=['january','february','march','april','may','june','july','august','september','october','november','december']
                        predate="%m{c}%d{c}{year}"
                        t1=[]
                        chars=[i for i in string.punctuation]
                        chars.pop(chars.index('%'))
                        for i in chars:
                            test=ds.split(i)
                            if len(test) == 3:
                                for num,m in enumerate(months):
                                    if test[0].lower() == m or m.startswith(test[0].lower()):
                                        test[0]=str(num+1).zfill(2)
                                        ds=f'{i}'.join(test)
                                        break
                        for i in chars:
                            for year in ['%y','%Y']:
                                t1.append(predate.format(c=i,year=year))
                                for ii in chars:
                                    for year in ['%y','%Y']:
                                        t1.append(f"%m{i}%d{ii}{year}")
                        for f in t1:
                                dt=try_date(format=f,ds=ds)
                                if dt:
                                    return dt
                    x=pandas_try(text)
                    if x:
                        return x
                    if data.lower().endswith('~'):
                        try:
                            text,timeStr=text.split("@")
                        except Exception as e:
                            print(e)
                            return 'RETRY'
                    value=process_ds(text)
                    if value == None:
                        if data.lower() == 'datetime':
                            value=TM.Tasks.TasksMode(parent=None,engine=db.ENGINE,init_only=True).DateTimePkr()
                    if value != None:
                        if data.lower().endswith('~'):
                            def processTS(value,TS):
                                start_end=TS.split("-")
                                
                                start,end=start_end
                                start_hour,start_minute=[int(i) for i in start.split(":")]
                                end_hour,end_minute=[int(i) for i in end.split(":")]
                                start_dt=datetime(value.year,value.month,value.day,start_hour,start_minute)
                                end_dt=datetime(value.year,value.month,value.day,end_hour,end_minute)
                                print(end_dt,"#end#")
                                if (end_dt - start_dt).total_seconds() < 0:
                                    try:
                                        end_dt=datetime(value.year,value.month,value.day+1,end_hour,end_minute)
                                    except ValueError as ve:
                                        print(ve)
                                        try:
                                            end_dt=datetime(value.year,value.month+1,1,end_hour,end_minute)
                                        except Exception as e:
                                            end_dt=datetime(value.year+1,1,1,end_hour,end_minute)
                                        
                                return [start_dt,end_dt]
                            value=processTS(value,timeStr)
            except Exception as e:
                print(repr(e),e,f"String needs to be month/day/year@hh:mm(FROM)-hh:mm(TO) {value}")
                return 'RETRY'
        elif data.lower() == 'list':
            value=text.split(',')
            tmp=[]
            try:
                for i in value:
                    if '-' in i:
                        r=[int(ii) for ii in i.split('-')]
                        r[-1]+=1
                        tmp.extend([str(i) for i in range(*r)])
                    else:
                        tmp.append(i)
                value=tmp
                #print(value,tmp)
            except Exception as e:
                value=text.split(",")
                print(e)
        elif data.lower() == 'quantity':
            try:
                value=pint.Quantity(text)
                #print(value,tmp)
            except Exception as e:
                value=pint.Quantity("0")
                print(e)
        elif data.lower() == 'path':
            value=Path(text).absolute()
        elif data.lower() == 'rpath':
            value=Path(text)
        elif data.lower() == 'timedelta':
            try:
                value=pd.to_timedelta(text).to_pytimedelta()
            except Exception as e:
                print(e)
                value=timedelta()
        elif data.lower() == 'fraction':
            try:
                value=Fraction(text)
            except Exception as e:
                print(e)
                value=Fraction()
        return value
    except Exception as e:
        print(e)