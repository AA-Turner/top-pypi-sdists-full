import dataclasses as DC
from dataclasses import dataclass
from hashlib import sha512
from datetime import datetime
from radboy.DB.rad_types import *
from pathlib import Path
from uuid import uuid1
import base64,calendar
from colored import Fore,Style,Back
from radboy.FB.FormBuilder import *
from radboy.DB.db import *
@dataclass
class MSG:
    DTOE:datetime=datetime.now()
    Title:str=''
    Salutations:str=''
    BODY:str=''
    ComplimentaryClose:str=''
    Signature:str=''
    PostScript:str=''


def WriteLetter():
    page=Control(func=FormBuilderMkText,ptext="Page The Letter?",helpText="page?",data="boolean")
    if page is None:
        return
    elif page in ['NAN',]:
        return
    elif page in ['d',True]:
        page=True
    else:
        page=False
    letter=MSG()

    d={}
    for k in DC.asdict(letter):
        d[k]={}
        d[k]['default']=DC.asdict(letter)[k]
        d[k]['type']=str(type(DC.asdict(letter)[k]).__name__)
    print(d)
    fd=FormBuilder(data=d)
    if fd is None:
        return

    ct=len(fd)
    mtext=[]
    for num,i in enumerate(fd):
        if fd[i] not in ['',' ',None]:
            if (num%2)!=0:
                color_1=Fore.pale_violet_red_1
                color_2=Fore.light_steel_blue
            else:
                color_1=Fore.medium_purple_3a
                color_2=Fore.cyan
            try:
                dms=f"""{color_1}{i}:{color_2}\n\t{eval(f"f\"{fd[i]}\"")}\n"""            
            except Exception as e:
                print(e)
                dms=f"""{color_1}{i}:{color_2}\n\t{fd[i]}\n"""
            msg=std_colorize(dms,num,ct)
            mtext.append(msg)
            if page:
                while True:
                    print(msg)
                    nxt=Control(func=FormBuilderMkText,ptext="Next?",helpText="next?",data="boolean")
                    if nxt is None:
                        return
                    elif nxt in ['NAN',]:
                        return
                    elif nxt in ['d',True]:
                        break
                    else:
                        continue
                continue

            print(msg)
    mtext='\n'.join(mtext)
    returnIt=Control(func=lambda text,data:FormBuilderMkText(text,data,passThru=['plain','pln'],PassThru=True),ptext=f"Return the letter text? [y/n/plain/pln]: ",helpText="return the letter as text, pln/plain has not colors",data="boolean")
    if returnIt in [None,'NAN']:
        return None
    elif returnIt in [True,]:
        return mtext
    elif returnIt in ['plain','pln']:
        return strip_colors(mtext)
    else:
        return None