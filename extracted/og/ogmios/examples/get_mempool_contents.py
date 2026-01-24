from pycardano import TransactionBody

import ogmios
import pycardano as pyc

"""
This example gets the contents of the mempool and waits for it to be empty.
Note: for this example you need to install pycardano
"""


def submit_transaction():
    """Submit a transaction so we have something in the mempool."""
    with pyc.OgmiosV6ChainContext("localhost", 1337) as context:
        network = pyc.Network.TESTNET
        psk = pyc.PaymentExtendedSigningKey.load("./tests/test_wallet/test_addr0.skey")
        ssk = pyc.StakeExtendedSigningKey.load("./tests/test_wallet/test_stake.skey")
        pvk = pyc.PaymentVerificationKey.from_signing_key(psk)
        svk = pyc.StakeVerificationKey.from_signing_key(ssk)
        address = pyc.Address(pvk.hash(), svk.hash(), network)
        builder = pyc.TransactionBuilder(context)

        builder.add_input_address(address)
        builder.add_output(
            pyc.TransactionOutput(
                address,
                pyc.Value.from_primitive(
                    [
                        10000000,
                    ]
                ),
            )
        )
        signed_tx = builder.build_and_sign([psk], change_address=address)
        context.submit_tx(signed_tx)


def tx_dict_to_pycardano_tx(tx_dict: dict) -> TransactionBody:
    """
    Convert a transaction dictionary to a PyCardano Transaction

    :param tx_dict: The transaction dictionary
    :type tx_dict: dict
    :return: The PyCardano Transaction
    :rtype: pyc.Transaction
    """
    return TransactionBody(tx_dict)


def get_mempool_contents():
    """Get the contents of the mempool and wait for it to be empty."""
    with ogmios.Client() as client:
        mempool_txs = ogmios.utils.get_mempool_transactions(client)
        print(f"Mempool has {len(mempool_txs)} transactions:\n{mempool_txs}")

        # Optionally, turn the TX dicts into PyCardano TransactionBody objects
        for tx in mempool_txs:
            pyc_tx = ogmios.utils.tx_dict_to_pycardano_tx(tx)

        print("Waiting for mempool to be empty...")
        ogmios.utils.wait_for_empty_mempool(client)
        print("Mempool is empty!")


if __name__ == "__main__":
    submit_transaction()
    get_mempool_contents()
