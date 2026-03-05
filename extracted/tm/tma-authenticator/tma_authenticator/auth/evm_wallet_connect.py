import base64
import json
import logging
from datetime import datetime

from eth_account import Account
from eth_account.messages import encode_defunct

logger = logging.getLogger(__name__)


class WalletConnectAuthError(Exception):
    """Raised when WalletConnect authentication verification fails."""


def verify_signature(
    address: str,
    message: str,
    signature: str,
    exp: int | None = None,
) -> None:
    if exp is not None:
        current_time = int(datetime.now().timestamp())
        if current_time > exp:
            logger.warning(
                "Expired signature. Expiration: %s, Current: %s",
                exp,
                current_time,
            )
            raise WalletConnectAuthError(f"Signature expired at {datetime.fromtimestamp(exp)}")

    try:
        message_encoded = encode_defunct(text=message)
        recovered_address = Account.recover_message(message_encoded, signature=signature)

        if recovered_address.lower() != address.lower():
            logger.warning(
                "Address mismatch. Expected: %s, Recovered: %s",
                address,
                recovered_address,
            )
            raise WalletConnectAuthError("Signature verification failed: address mismatch")

    except WalletConnectAuthError:
        raise
    except Exception as e:
        logger.error("Signature verification error: %s", e)
        raise WalletConnectAuthError("INVALID_SIGNATURE") from e


def verify_wallet_connect_header(header_data: str) -> str:
    try:
        header_data_extracted = json.loads(base64.b64decode(header_data).decode("utf-8"))
    except Exception as e:
        raise WalletConnectAuthError("INVALID_HEADER") from e

    required_fields = ["address", "signature", "message"]
    for field in required_fields:
        if field not in header_data_extracted:
            raise WalletConnectAuthError(f"Missing required field: {field}")

    address = header_data_extracted["address"]
    signature = header_data_extracted["signature"]
    message = header_data_extracted["message"]
    exp = header_data_extracted.get("exp")

    verify_signature(address, message, signature, exp)

    return address
