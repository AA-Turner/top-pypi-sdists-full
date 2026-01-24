from datetime import datetime
import pytest

from ogmios.datatypes import TxOutputReference, Address, Utxo
from tests.ogmios.test_fixtures import client

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_QueryUtxo_address_empty(client):
    addr = Address(
        "addr1q9d34spgg2kdy47n82e7x9pdd6vql6d2engxmpj20jmhuc2047yqd4xnh7u6u5jp4t0q3fkxzckph4tgnzvamlu7k5psuahzcp"
    )
    id_str = "My ID string"
    utxos, id = client.query_utxo.execute([addr], id_str)

    assert utxos == []
    assert id == id_str


def test_QueryUtxo_address(client):
    # This test relies on this address having UTxO's on the testnet
    addr = Address("addr_test1vz09v9yfxguvlp0zsnrpa3tdtm7el8xufp3m5lsm7qxzclgmzkket")
    id_str = "My ID string"
    utxos, id = client.query_utxo.execute([addr], id_str)

    assert isinstance(utxos, list)
    assert len(utxos) > 0
    assert isinstance(utxos[0], Utxo)
    assert id == id_str


@pytest.mark.skip
def test_QueryUtxo_output_ref(client):
    output_ref = TxOutputReference(
        tx_id="eac76c86b2c8552204b89fdc6f1506f59a6b464ecebd5468aa008ce0fa95c5e8", index=0
    )
    id_str = "My ID string"
    utxos, id = client.query_utxo.execute([output_ref], id_str)
    utxo = utxos[0]

    assert isinstance(utxos, list)
    assert utxo.tx_id == output_ref.tx_id
    assert utxo.index == output_ref.index
    assert (
        utxo.address
        == 'addr_test1qznwxwlxrq9p58c4mfmxdh45zpmu5wfhflwhp69cq7v667h7cvpcq5rkwhjpjmandtq39es7yxvluyts9kfgjcajg24sx9yfqe'
    )
    assert utxo.value.get("ada").get("lovelace") == 11000000
    assert len(utxos) > 0
    assert isinstance(utxos[0], Utxo)
    assert id == id_str
