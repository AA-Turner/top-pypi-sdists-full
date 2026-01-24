import pytest
import pycardano as pyc

from ogmios import Point
from ogmios.client import Client
from ogmios import utils


@pytest.fixture
def client():
    with Client() as client:
        yield client


@pytest.fixture
def chain_context():
    yield pyc.OgmiosV6ChainContext("localhost", 1337)


@pytest.fixture
def era(client):
    yield utils.get_current_era(client)


@pytest.fixture
def test_psk():
    yield pyc.PaymentExtendedSigningKey.load("./tests/test_wallet/test_addr0.skey")


@pytest.fixture
def test_ssk():
    yield pyc.StakeExtendedSigningKey.load("./tests/test_wallet/test_stake.skey")


@pytest.fixture
def test_pvk(test_psk):
    yield pyc.PaymentVerificationKey.from_signing_key(test_psk)


@pytest.fixture
def test_svk(test_ssk):
    yield pyc.StakeVerificationKey.from_signing_key(test_ssk)


@pytest.fixture
def test_address(test_pvk, test_svk):
    yield pyc.Address(test_pvk.hash(), test_svk.hash(), pyc.Network.TESTNET)


@pytest.fixture
def last_byron_block_point():
    yield Point(slot=84242, id="45899e8002b27df291e09188bfe3aeb5397ac03546a7d0ead93aa2500860f1af")


@pytest.fixture
def last_shelley_block_point():
    yield Point(slot=518360, id="f9d8b6c77fedd60c3caf5de0ce63a0aeb9d1753269c9c07503d9aa09d5144481")


@pytest.fixture
def last_allegra_block_point():
    yield Point(slot=950340, id="74c03af754bcde9cd242c5a168689edcab1756a3f7ae4d5dca1a31d86839c7b1")


@pytest.fixture
def last_mary_block_point():
    yield Point(slot=1382348, id="af5fddc7d16a349e1a2af8ba89f4f5d3273955a13095b3709ef6e3db576a0b33")


@pytest.fixture
def last_alonzo_block_point():
    yield Point(slot=3542390, id="f93e682d5b91a94d8660e748aef229c19cb285bfb9830db48941d6a78183d81f")
