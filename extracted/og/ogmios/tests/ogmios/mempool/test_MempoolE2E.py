import pytest
import time
import pycardano as pyc

from ogmios.errors import ResponseError
from tests.ogmios.test_fixtures import (
    client,
    chain_context,
    test_psk,
    test_ssk,
    test_pvk,
    test_svk,
    test_address,
)

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


@pytest.mark.skip
def test_Mempool_E2E(client, chain_context, test_psk, test_pvk, test_svk, test_address):
    # Make sure mempool is empty
    wait_for_mempool_empty(client)

    # Build and submit a transaction
    tx_builder = pyc.TransactionBuilder(chain_context)
    tx_builder.add_input_address(test_address)

    utxos = chain_context.utxos(test_address)
    tx_utxo = None
    for utxo in utxos:
        if utxo.output.amount.coin > 1_000_000:
            tx_utxo = utxo
            break

    if tx_utxo is None:
        pytest.fail("No suitable UTxO found")

    tx_builder.add_input(tx_utxo)
    tx_builder.add_output(
        pyc.TransactionOutput(
            test_address,
            pyc.Value.from_primitive([1_000_000]),
        )
    )
    signed_tx = tx_builder.build_and_sign([test_psk], change_address=test_address)
    client.submit_transaction.execute(signed_tx.to_cbor_hex())

    # Acquire a mempool snapshot and get the transaction
    client.acquire_mempool.execute()
    tx, id = client.next_transaction.execute()
    assert tx.get("id") == str(signed_tx.id)
    client.release_mempool.execute()

    wait_for_mempool_empty(client)
    assert True


def wait_for_mempool_empty(client) -> None:
    # Wait for the transaction to be removed from the mempool
    while True:
        client.acquire_mempool.execute()
        tx, id = client.next_transaction.execute()
        client.release_mempool.execute()
        if tx is None:
            break
        time.sleep(1)
