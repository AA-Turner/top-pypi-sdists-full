from time import sleep

from smoldot_light import SmoldotClient


client = SmoldotClient()

# Load relay chain spec JSON (Polkadot, Kusama, etc).
with open("../chains/polkadot.json", "r", encoding="utf-8") as f:
    relay_spec = f.read()

# Load parachain spec JSON.
with open("../chains/polkadot_asset_hub.json", "r", encoding="utf-8") as f:
    parachain_spec = f.read()

relay_chain_id = client.add_chain(relay_spec)
parachain_id = client.add_chain(parachain_spec, relay_chain_ids=[relay_chain_id])

# Send a JSON-RPC request to the parachain.
client.json_rpc_request(parachain_id, '{"id":1,"jsonrpc":"2.0","method":"system_chain","params":[]}')

while True:
    responses = client.drain_responses(parachain_id, max=10)
    for msg in responses:
        print(msg)
    sleep(0.5)
