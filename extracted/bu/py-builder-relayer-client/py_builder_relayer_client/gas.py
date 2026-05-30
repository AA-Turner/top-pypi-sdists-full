import requests

# Fallback used when RPC estimation fails. Must fit within the relay hub's gas budget
# (~650k total). Sized to cover most proxy calls while leaving room for relay overhead.
DEFAULT_GAS_LIMIT = 500_000


def estimate_gas(rpc_url: str, from_address: str, to: str, data: str) -> int:
    """
    Estimate gas for a transaction via eth_estimateGas JSON-RPC call.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_estimateGas",
        "params": [{"from": from_address, "to": to, "data": data}],
        "id": 1,
    }

    response = requests.post(rpc_url, json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()

    if "error" in result:
        raise ValueError(f"RPC error: {result['error']}")

    if "result" not in result:
        raise ValueError("No result in RPC response")

    return int(result["result"], 16)
