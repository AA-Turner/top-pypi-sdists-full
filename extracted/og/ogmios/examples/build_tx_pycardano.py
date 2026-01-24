import ogmios
import pycardano as pyc

"""
This example shows how to build and sign a transaction using PyCardano.

https://github.com/Python-Cardano/pycardano
"""

network = pyc.Network.TESTNET

# Read keys to memory
psk = pyc.PaymentExtendedSigningKey.load("./tests/test_wallet/test_addr0.skey")
ssk = pyc.StakeExtendedSigningKey.load("./tests/test_wallet/test_stake.skey")

pvk = pyc.PaymentVerificationKey.from_signing_key(psk)
svk = pyc.StakeVerificationKey.from_signing_key(ssk)

# Derive an address from payment verification key and stake verification key
address = pyc.Address(pvk.hash(), svk.hash(), network)

# Create an Ogmios chain context. In this example, we will use preprod network.
context = pyc.OgmiosV6ChainContext("localhost", 1337)

# Create a transaction builder
builder = pyc.TransactionBuilder(context)

# Tell the builder that transaction input will come from a specific address, assuming that there are some ADA and native
# assets sitting at this address. "add_input_address" could be called multiple times with different address.
builder.add_input_address(address)

# Get all UTxOs currently sitting at this address
utxos = context.utxos(address)

# We can also tell the builder to include a specific UTxO in the transaction.
# Similarly, "add_input" could be called multiple times.
builder.add_input(utxos[0])

builder.add_output(
    pyc.TransactionOutput(
        pyc.Address.from_primitive(
            "addr_test1vrm9x2zsux7va6w892g38tvchnzahvcd9tykqf3ygnmwtaqyfg52x"
        ),
        pyc.Value.from_primitive(
            [
                1500000,
            ]
        ),
    )
)

# We can add multiple outputs, similar to what we can do with inputs.
# Send 2 ADA and a native asset (CHOC) in quantity of 200 to ourselves
builder.add_output(
    pyc.TransactionOutput(
        address,
        pyc.Value.from_primitive(
            [
                2000000,
                {
                    bytes.fromhex(
                        "57fca08abbaddee36da742a839f7d83a7e1d2419f1507fcbf3916522"  # Policy ID
                    ): {
                        b"CHOC": 200  # Asset name and amount
                    }
                },
            ]
        ),
    )
)

# Create final signed transaction
signed_tx = builder.build_and_sign([psk], change_address=address)
print(signed_tx)

# Submit signed transaction to the network
context.submit_tx(signed_tx)
