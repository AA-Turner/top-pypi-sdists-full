from typing import List
from eth_abi import encode
from eth_utils import to_bytes, to_checksum_address, keccak

from ..models import ProxyTransaction


def encode_proxy_transaction_data(txns: List[ProxyTransaction]) -> str:
    function_selector = keccak(b"proxy((uint8,address,uint256,bytes)[])")[:4]

    tuples = []
    for tx in txns:
        to_address = to_checksum_address(tx.to)
        data_bytes = (
            to_bytes(hexstr=tx.data)
            if tx.data.startswith("0x")
            else to_bytes(hexstr="0x" + tx.data)
        )
        tuples.append((int(tx.type_code.value), to_address, int(tx.value), data_bytes))

    encoded = encode(["(uint8,address,uint256,bytes)[]"], [tuples])

    return "0x" + (function_selector + encoded).hex()
