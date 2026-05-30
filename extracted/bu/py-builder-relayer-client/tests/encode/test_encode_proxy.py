from unittest import TestCase

from py_builder_relayer_client.models import ProxyTransaction, CallType
from py_builder_relayer_client.encode.proxy import encode_proxy_transaction_data


class TestEncodeProxy(TestCase):

    def test_encode_proxy_transaction_data_single(self):
        # USDC approve calldata
        txn = ProxyTransaction(
            to="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            type_code=CallType.Call,
            data="0x095ea7b30000000000000000000000004d97dcd97ec945f40cf65f87097ace5ea0476045ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            value="0",
        )

        result = encode_proxy_transaction_data([txn])

        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("0x"))

    def test_encode_proxy_transaction_data_multiple(self):
        txn = ProxyTransaction(
            to="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            type_code=CallType.Call,
            data="0x095ea7b30000000000000000000000004d97dcd97ec945f40cf65f87097ace5ea0476045ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            value="0",
        )

        result = encode_proxy_transaction_data([txn, txn])

        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("0x"))
