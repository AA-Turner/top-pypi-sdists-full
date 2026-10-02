import pint
from radboy.DB.db import *
ureg=pint.UnitRegistry()
def prepare_ureg(self):
    with Session(db.ENGINE) as session:
        results=session.query(CustomUnit).all()
        for xnum,i in enumerate(results):
            useable=None
            try:
                ureg.define(i.definition)
                useable=True
            except Exception as e:
                useable=False
                print(e,i)
            if useable in [None,False]:
                useable=f"{Fore.orange_red_1}Un-Useable"
            else:
                useable=f"{Fore.green_yellow}Useable"
            msg=f"""Loading... {useable} {Fore.light_green}emoid{Fore.light_steel_blue}={Fore.light_yellow}'{i.emoid}' {Fore.light_green}definition{Fore.light_steel_blue}={Fore.light_yellow}'{i.definition}' {Fore.light_green}comment{Fore.light_steel_blue}={Fore.light_yellow}'{i.comment}' {Fore.light_green}group_id{Fore.light_steel_blue}={Fore.light_yellow}'{i.group_id}' {Fore.light_green}dtoe{Fore.light_steel_blue}={Fore.light_yellow}'{i.dtoe}{Style.reset}'"""
            print(msg)
prepare_ureg(self=None)
QTY=ureg.Quantity