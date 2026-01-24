import json
import base64
from cardano_tools import WalletHTTP
import ogmios


"""
This example shows how to build and sign a transaction using the CardanoTools wallet API. This requires
cardano-wallet to be running.

https://gitlab.com/viperscience/cardano-tools
https://github.com/cardano-foundation/cardano-wallet
"""

WALLET_URL = "http://localhost"
WALLET_PORT = 8090
WALLET_NAME = "my-wallet"
MNEMONIC_FILE = "./tests/test_wallet/test.seed"

# Unsafe to use in production - read from environment variable instead
WALLET_PASSPHRASE = "my-passphrase"


cw_api = WalletHTTP(WALLET_URL, WALLET_PORT)

# Import wallet if it hasn't been already
if not (wallet_id := cw_api.get_wallet_by_name(WALLET_NAME).get("id")):
    with open(MNEMONIC_FILE, "r") as f:
        mnemonic = f.read()
        cw_api.create_wallet(WALLET_NAME, mnemonic.strip().split(" "), WALLET_PASSPHRASE)
        wallet_id = cw_api.get_wallet_by_name(WALLET_NAME).get("id")

# Send 2 ADA and a native asset (CHOC) in quantity of 2000 to an address.
target_addr = "addr_test1wztjpvnxahymaejx9qa9c3xddkt3ujhjykmt83uu8xfvprq7hxv53"
lovelace_amt = 2 * 1e6
token_policy = "57fca08abbaddee36da742a839f7d83a7e1d2419f1507fcbf3916522"
asset_name = "CHOC"
token_qty = 2000

payload = json.loads(
    f"""{{
        "payments": [
            {{
                "address": "{target_addr}",
                "amount": {{
                    "quantity": {lovelace_amt},
                    "unit": "lovelace"
                }},
                "assets": [
                    {{
                        "policy_id": "{token_policy}",
                        "asset_name": "{asset_name}",
                        "quantity": {token_qty}
                    }}
                ]
            }}
        ],
        "withdrawal": "self",
        "validity_interval": {{
            "invalid_hereafter": {{
                "quantity": 3600,
                "unit": "second"
            }}
        }},
        "encoding": "base16"
    }}"""
)

tx = cw_api.construct_transaction(wallet_id, payload)
encoded_tx = tx.get("transaction")
signed_tx = cw_api.sign_transaction(wallet_id, WALLET_PASSPHRASE, encoded_tx)
tx_cbor = base64.b64decode(signed_tx.get("transaction")).hex()

with ogmios.Client() as client:
    tx_id, _ = client.submit_transaction.execute(tx_cbor)
