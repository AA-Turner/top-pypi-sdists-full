from pathlib import Path
from dataclasses import dataclass
import platform
try:
    raise Exception()
    import grp,pwd
except Exception as e:
    @dataclass
    class grp:
        gr_name=f'grp is incompatible w/ "{platform.system()}"'
        def getgrgid(dummy):
            return pwd
    @dataclass
    class pwd:
        pw_name=f'pwd is incompatible w/ "{platform.system()}"'
        def getpwuid(dummy):
            return pwd

import os,sys
import argparse
from datetime import datetime,timedelta
from colored import Fore,Back,Style
import stat
from humanfriendly import format_size
from radboy.DB.db import *
from radboy.FB.FBMTXT import *
from radboy.FB.FormBuilder import *
from radboy.DB.Prompt import *

def systemls(path:Path=None,today:datetime=None,search=None,cmdline=False):
    now=datetime.now()
    if today is None:
        today=datetime(now.year,now.month,now.day)-timedelta(days=1)
    
    start=datetime.now()
    def std_colorize(msg,count,total,post_msg="\n\t"):
        return f"""{Fore.dark_olive_green_3b}{msg}{post_msg}{Fore.light_blue}{count}/{count+1} of {total}{Style.reset}"""

    if path is None:
        if cmdline == True:
            if len(sys.argv) == 2:
                path=Path(sys.argv[1])
        else:
            fields={
                    'path to examine':{
                        'default':str(Path.cwd()),
                        'type':'string'
                        },
                    'search':{
                        'default':None,
                        'type':'string',
                        },
                    'dtoe':{
                        'default':today-timedelta(days=1),
                        'type':'datetime'
                        },
                    }
            fd=FormBuilder(data=fields,passThruText="What/Where for Everything Past a Date")
            if fd is None:
                return
            path=Path(fd['path to examine'])
            today=fd['dtoe']
            search=fd['search']

    if not path.exists():
        raise FileNotFoundError(path)
    ct_top=len([i for i in path.walk(top_down=True,follow_symlinks=False,on_error=print)])
    break_page=False
    for num,(root,dirs,names) in enumerate(path.walk(top_down=True,follow_symlinks=False,on_error=print)):
        ct_dirs=len(dirs)
        for numd,d in enumerate(dirs):
            dirpath=root/d
            try:
                if isinstance(dirpath,Path):
                    l=[]
                    if datetime.fromtimestamp(dirpath.stat().st_mtime) > today:
                        if dirpath not in l:
                            if search is not None:
                                if search.lower() in str(dirpath).lower():
                                    print(f"Matched '{search}' ~= {dirpath}")
                                    l.append(dirpath)
                            else:
                                l.append(dirpath)

                    if datetime.fromtimestamp(dirpath.stat().st_ctime) > today:
                        if dirpath not in l:
                            if search is not None:
                                if search.lower() in str(dirpath).lower():
                                    print(f"Matched '{search}' ~= {dirpath}")
                                    l.append(dirpath)
                            else:
                                l.append(dirpath)

                    if datetime.fromtimestamp(dirpath.stat().st_atime) > today:
                        if dirpath not in l:
                            if search is not None:
                                if search.lower() in str(dirpath).lower():
                                    print(f"Matched '{search}' ~= {dirpath}")
                                    l.append(dirpath)
                            else:
                                l.append(dirpath)
                    for i in l:
                        try:
                            username=''
                            username=pwd.getpwuid(i.stat().st_uid).pw_name
                        except Exception as e:
                            print(e)
                            username='USERNM#ERROR:UnResolved'
                        try:
                            grpname=''
                            grpname=pwd.getpwuid(i.stat().st_gid).pw_name
                        except Exception as e:
                            print(e)
                            grpname='GRP#ERROR:UnResolved'

                        
                        print(std_colorize(f"""{Fore.light_cyan}[Directory]{Fore.light_steel_blue}{i} 
\t{Fore.orange_red_1}MTIME:{datetime.fromtimestamp(i.stat().st_mtime)} Age:{datetime.now()-datetime.fromtimestamp(i.stat().st_mtime)} 
\t{Fore.light_yellow}CTIME:{datetime.fromtimestamp(i.stat().st_ctime)} Age:{datetime.now()-datetime.fromtimestamp(i.stat().st_ctime)}
\t{Fore.light_green}ATIME: {datetime.fromtimestamp(i.stat().st_atime)} Age:{datetime.now()-datetime.fromtimestamp(i.stat().st_atime)}
\t{Fore.light_red}MODE: {stat.filemode(i.stat().st_mode)}
\t{Fore.dark_green}GID:{i.stat().st_gid} ({grpname})
\t{Fore.medium_violet_red}UID:{i.stat().st_uid} ({username})
\t{Fore.magenta}Size:{format_size(i.stat().st_size)}{Style.reset}""",numd,ct_dirs))
                        print(std_colorize(f"Since Exe:{datetime.now()-start}",num,ct_top))
                        if not break_page:
                            NEXT=Control(func=FormBuilderMkText,ptext="Next?",helpText="yes==advances 1,no==stops paging",data="boolean")
                            if NEXT in ['NaN',None]:
                                return
                            elif NEXT in ['d',True]:
                                continue
                            elif NEXT == False:
                                break_page=True


            except Exception as e:
                print(e)
        ctn=len(names)
        for numn,name in enumerate(names):
            try:
                npath=root/name
                if isinstance(npath,Path):
                    l=[]
                    if datetime.fromtimestamp(npath.stat().st_mtime) > today:
                        if npath not in l:
                            if search is not None:
                                if search.lower() in str(npath).lower():
                                    print(f"Matched {search} ~= {npath}")
                                    l.append(npath)
                            else:
                                l.append(npath)
                    if datetime.fromtimestamp(npath.stat().st_ctime) > today:
                        if npath not in l:
                            if search is not None:
                                if search.lower() in str(npath).lower():
                                    print(f"Matched {search} ~= {npath}")
                                    l.append(npath)
                            else:
                                l.append(npath)

                    if datetime.fromtimestamp(npath.stat().st_atime) > today:
                        if npath not in l:
                            if search is not None:
                                if search.lower() in str(npath).lower():
                                    print(f"Matched {search} ~= {npath}")
                                    l.append(npath)
                            else:
                                l.append(npath)

                    for i in l:
                        try:
                            username=''
                            username=pwd.getpwuid(i.stat().st_uid).pw_name
                        except Exception as e:
                            print(e)
                            username='USERNM#ERROR:UnResolved'
                        try:
                            grpname=''
                            grpname=pwd.getpwuid(i.stat().st_gid).pw_name
                        except Exception as e:
                            print(e)
                            grpname='GRP#ERROR:UnResolved'

                        print(std_colorize(f"""  {Fore.dark_cyan}[File]{Fore.light_steel_blue}{i}
    \t{Fore.orange_red_1}MTIME:{datetime.fromtimestamp(i.stat().st_mtime)} Age:{datetime.now()-datetime.fromtimestamp(i.stat().st_mtime)} 
    \t{Fore.light_yellow}CTIME:{datetime.fromtimestamp(i.stat().st_ctime)} Age:{datetime.now()-datetime.fromtimestamp(i.stat().st_ctime)} 
    \t{Fore.light_green}ATIME: {datetime.fromtimestamp(i.stat().st_atime)} Age:{datetime.now()-datetime.fromtimestamp(i.stat().st_atime)}
    \t{Fore.light_red}MODE: {stat.filemode(i.stat().st_mode)}
    \t{Fore.dark_green}GID:{i.stat().st_gid} ({grpname})
    \t{Fore.medium_violet_red}UID:{i.stat().st_uid} ({username})
    \t{Fore.magenta}Size:{format_size(i.stat().st_size)}{Style.reset}""",numn,ctn))
                        print(std_colorize(f"  \tSince Exe:{datetime.now()-start}",num,ct_top))
                        if not break_page:
                            NEXT=Control(func=FormBuilderMkText,ptext="Next?",helpText="yes==advances 1,no==stops paging",data="boolean")
                            if NEXT in ['NaN',None]:
                                return
                            elif NEXT in ['d',True]:
                                continue
                            elif NEXT == False:
                                break_page=True

            except Exception as e:
                print(e)

