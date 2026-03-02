from imports import *
import json
import clipboard
from abstract_utilities import *
from bs4 import BeautifulSoup
import re
from abstract_webtools import *
from gert_inst_test import *
def get_transaction_data(signature):
    url = 'https://solcatcher.io/ratelimiter/fetch-transaction'
    return postRequest(url,data={"signature":signature})
    
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
def decode_transaction_instructions(tx, registry):
    msg = tx["transaction"]["message"]
    keys = msg["accountKeys"]

    for ix in msg["instructions"]:
        raw = base64.b64decode(ix["data"])
        disc = raw[:8]

        result = registry.decode(raw)
        if not result:
            continue

        category, decoded = result

        if category != "instruction":
            continue

        schema = registry.get_instruction_schema(disc)

        yield {
            "level": "top",
            "program_id": keys[ix["programIdIndex"]],
            "instruction": schema.name,
            "args": decoded,
            "pda_seeds": schema.pda_accounts,
            "accounts": [keys[i] for i in ix["accounts"]],
        }
def decode_inner_instructions(tx, registry):
    msg = tx["transaction"]["message"]
    keys = msg["accountKeys"]

    for block in tx["meta"].get("innerInstructions", []):
        for ix in block["instructions"]:
            raw = base64.b64decode(ix["data"])
            disc = raw[:8]

            result = registry.decode(raw)
            if not result:
                continue

            category,event, decoded = result
            if category != "instruction":
                continue

            schema = registry.get_instruction_schema(disc)

            yield {
                "level": "inner",
                "program_id": keys[ix["programIdIndex"]],
                "instruction": schema.name,
                "args": decoded,
                "pda_seeds": schema.pda_accounts,
                "accounts": [keys[i] for i in ix["accounts"]],
                "stackHeight": ix.get("stackHeight"),
            }
def get_all_idls():
    directory = '/home/flerb/Downloads/solana-defi-main/PumpFun/Typescript/'
    idl_dirs = """grpc-stream-and-parse-pump-amm-account
grpc-stream-and-parse-pump-amm-transaction
stream_and_parse_pump_fun_transactions
stream_new_pool_pump_swap_amm
stream_pump_amm_token_price
stream_pump_amm_transactions_and_detect_buy_sell_events
stream_pump_fun_new_minted_tokens
stream_pumpfun_token_price
stream_pumpfun_to_pumpAmm_migration_transactions
stream_pump_fun_transactions_and_detect_buy_sell_events
stream_pumpfun_txns_fetch_bonding_pool_liquidity""".split('\n')
    idls=[]
    for idl_dir in idl_dirs:
        idls_directory = os.path.join(directory,idl_dir,'idls')
        dirs,files = get_files_and_dirs(idls_directory)
        for file in files:
            data = safe_load_from_json(file)
            idls.append(data)
    return idls
_DECODER_REGISTRY = None
def get_decoder_registry():
    global _DECODER_REGISTRY
    if _DECODER_REGISTRY is None:
        _DECODER_REGISTRY = build_registry_from_idls(get_all_idls())
    return _DECODER_REGISTRY           
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
    event_registry = get_decoder_registry()
    for row in make_list(rows):
        b64 = row.get('b64')
        raw = base64.b64decode(b64)
        disc = raw[:8]
        result = event_registry.decode(raw)
        try:
            
            if not result:
                raise KeyError("unknown discriminator")

            category,event, decoded = result
            
            schema = None
            if category == "instruction":
                schema = registry.get_instruction_schema(disc)

            yield {
                "category": category,
                "decoded": decoded,
                "schema": schema,   # ← PDA seeds live here
                "row": row,
            }
        except Exception as e:
            disc_hex = disc.hex()
            if disc_hex not in missing:
                missing[disc_hex] = row
                print("Missing / failed decode:")
                
                #get_inspect(row)
    print(f"{missing}")               
           
   
   
datas = decode_record_rows(limit=10000)

for record in datas:
    print(record["category"])
##    print(record["decoded"])

    schema = record["schema"]
    if schema:
        print("Instruction:", schema.name)
        print("PDA accounts:", schema.pda_accounts)
input()

input(decoded)
