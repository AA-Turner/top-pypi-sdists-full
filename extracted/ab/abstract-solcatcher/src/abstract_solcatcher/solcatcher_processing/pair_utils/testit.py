from getSignatures import *
from abstract_solcatcher import *
from getTransactions import *
from getMetaData import get_or_fetch_meta_data
def gert_transaction(signature=None):
    method = 'getTransaction'
    params = [signature,{"maxSupportedTransactionVersion":0}]
    payload = get_rpc_payload(method=method,params=params,id=None,jsonrpc=None)
    response = requests.post(url=fall_back_rpc,data=json.dumps(payload),headers=get_headers())
    result = get_response(response)
    return result
solana_rpc_url="http://api.mainnet-beta.solana.com"
fall_back_rpc = get_env_value('solana_fallback_rpc_url')
mint='H5j8EftXhWZACixKJ1dn5cuwZXfup2EwqZzy4b1x6BPL'
meta_data = call_solcatcher_ts('get-or-fetch-metadata',mint=mint,url=solana_rpc_url,umi=None)
signature = get_genesis_signature_from_mint(mint=mint)

meta_data = call_solcatcher_ts('get-or-fetch-metadata',mint=mint,url=solana_rpc_url,umi=None)

input(result)
