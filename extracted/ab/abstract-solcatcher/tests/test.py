from imports import *
import json
import clipboard
from abstract_utilities import *
from bs4 import BeautifulSoup
import re
from abstract_webtools import *
from gert_inst_test import *
def make_dir(name,directory=None):
    directory = directory or get_caller_dir()
    nudir = os.path.join(directory,name)
    os.makedirs(nudir,exist_ok=True)
    return nudir

events_dir = make_dir('events')
def get_inspect(row):
    init_paste = clipboard.paste()
    event = row.get('event')
    if event:
        event_dir = make_dir(event,events_dir)
        signature = row.get('signature')
        for sig in os.listdir(event_dir):
            sig_dir = os.path.join(event_dir,sig)
            if os.path.isfile(os.path.join(sig_dir,'instructions.json')):
                return 
            
        
        if signature:
            signature_dir = make_dir(signature,event_dir)
            call_path = os.path.join(signature_dir,'call.json')
            row = dict(row)
            del row['created_at']
            safe_dump_to_json(data=row,file_path=call_path)
            solscan_path = os.path.join(signature_dir,'solscan.html')
            instructions_path = os.path.join(signature_dir,'instructions.json')
            if not os.path.isfile(solscan_path):
                os.system(f"firefox https://solscan.io/tx/{signature}")
                while True:
                    nupaste = clipboard.paste()
                    
                    if nupaste and nupaste != init_paste:
                        write_to_file(contents=nupaste,file_path=solscan_path)
                        break
       
            instructions = get_instructions_tree(solscan_path)
            safe_dump_to_json(data=instructions,file_path=instructions_path)
            
api_endpoint = 'https://pro-api.solscan.io/v2.0/transaction/detail/multi'
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3Njg5NzA5NjQ5NjAsImVtYWlsIjoianJwdXRrZXlAc2JjZ2xvYmFsLm5ldCIsImFjdGlvbiI6InRva2VuLWFwaSIsImFwaVZlcnNpb24iOiJ2MiIsImlhdCI6MTc2ODk3MDk2NH0.jrTTaF5hTkyFSBY_g5lD1D6P3qpuhdjCkcdWnEVTUvk"
def get_decode_rows(table=None,limit=None,offset=None,asc=None):
    return get_latest_from_table(table=table,limit=limit,offset=offset,asc=asc)

def decode_record_rows(rows=None,limit=None,table=None,offset=None,asc=None):
    rows = rows or get_decode_rows(
        table=table,
        offset=offset,
        limit=limit,
        asc=asc
        )
    missing = {}
    event_registry = build_event_registry()
    for row in make_list(rows):
        
        raw = base64.b64decode(row.get('b64'))
        try:
            decoded = event_registry[raw[:8]](raw)
            
        except Exception as e:
            descriminator = row.get('discriminator')
            if descriminator not in missing:
                signature = row.get('signature')
                
                missing[descriminator] = row
                print(row,'\n\n')
                get_inspect(row)
    print(f"{missing}")               
           
   
datas = decode_record_rows(limit=10000)
for key,values in datas.items():
    print(key)
    input(values)
    for event,value in values.items():
        print(event)
        input(value)
input()

input(decoded)
