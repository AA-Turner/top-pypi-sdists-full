import time
import secrets
import logging
from typing import Dict, Any
from typing_extensions import (
    TypedDict,
)  # use `typing_extensions.TypedDict` instead of `typing.TypedDict` on Python < 3.12
from eth_account import Account
from .encoding import safe_base64_encode, safe_base64_decode
from .types import (
    PaymentRequirements,
)
from .chains import get_chain_id
import json

logger = logging.getLogger(__name__)


def create_nonce() -> bytes:
    """Create a random 32-byte nonce for authorization signatures."""
    return secrets.token_bytes(32)


def prepare_payment_header(
    sender_address: str, d402_version: int, payment_requirements: PaymentRequirements
) -> Dict[str, Any]:
    """Prepare an unsigned payment header with sender address, d402 version, and payment requirements."""
    nonce = create_nonce()
    valid_after = str(int(time.time()) - 60)  # 60 seconds before
    # Ensure at least 24 hours for settlement (facilitator batches payments)
    min_deadline_seconds = max(payment_requirements.max_timeout_seconds, 86400)  # 24 hours
    valid_before = str(int(time.time()) + min_deadline_seconds)

    return {
        "d402Version": d402_version,
        "scheme": payment_requirements.scheme,
        "network": payment_requirements.network,
        "payload": {
            "signature": None,
            "authorization": {
                "from": sender_address,
                "to": payment_requirements.pay_to,
                "value": payment_requirements.max_amount_required,
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce,
            },
        },
    }


class PaymentHeader(TypedDict):
    d402Version: int
    scheme: str
    network: str
    payload: dict[str, Any]


def sign_payment_header(
    operator_account: Account, 
    payment_requirements: PaymentRequirements, 
    header: PaymentHeader,
    wallet_address: str = None,
    request_path: str = None
) -> str:
    """
    Sign a payment header using EIP-712 PullFundsForSettlement signature.
    
    This signature format matches IATPWallet.sol validateConsumerSignature.
    
    Contract Type Hash (IATPWallet.sol line 34-36):
    PullFundsForSettlement(
        address wallet,      // Consumer's IATPWallet contract address
        address provider,    // Provider's IATPWallet contract address
        address token,       // Token address (USDC, etc.)
        uint256 amount,      // Payment amount
        uint256 deadline,    // Signature expiration
        string requestPath   // API path (e.g., "/mcp/tools/call")
    )
    
    Note: chainId is in the EIP-712 domain, NOT in the message (per EIP-712 standard)
    
    Args:
        operator_account: Operator account with private key for signing (EOA)
        payment_requirements: Payment requirements from server
        header: Payment header structure
        wallet_address: Consumer's IATPWallet contract address (if None, uses operator_account.address)
        request_path: API request path (if None, uses payment_requirements.resource)
    """
    try:
        auth = header["payload"]["authorization"]
        
        # Get wallet address (IATPWallet contract, not EOA)
        consumer_wallet = wallet_address or auth["from"]
        
        # Get request path from payment_requirements if not provided
        if request_path is None:
            request_path = payment_requirements.resource or "/mcp"
            logger.info(f"🔍 payment_requirements.resource: {payment_requirements.resource}")
            logger.info(f"🔍 Using request_path: {request_path}")
        
        # Ensure we have a valid request path (contract requires non-empty string)
        if not request_path or request_path.strip() == "":
            logger.warning(f"⚠️  request_path was empty, defaulting to /mcp")
            request_path = "/mcp"
        
        # Get domain info from payment_requirements.extra (IATPWallet domain)
        extra = payment_requirements.extra or {}
        wallet_name = extra.get("name", "IATPWallet")
        wallet_version = extra.get("version", "1")
        
        # Build EIP-712 typed data for PullFundsForSettlement
        # Note: chainId is in the domain, not the message (EIP-712 standard)
        typed_data = {
            "types": {
                "PullFundsForSettlement": [
                    {"name": "wallet", "type": "address"},
                    {"name": "provider", "type": "address"},
                    {"name": "token", "type": "address"},
                    {"name": "amount", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                    {"name": "requestPath", "type": "string"},
                ]
            },
            "primaryType": "PullFundsForSettlement",
            "domain": {
                "name": wallet_name,
                "version": wallet_version,
                "chainId": int(get_chain_id(payment_requirements.network)),  # chainId in domain only
                "verifyingContract": consumer_wallet,  # Consumer's IATPWallet contract
            },
            "message": {
                "wallet": consumer_wallet,  # Consumer's IATPWallet contract address
                "provider": auth["to"],  # Provider's IATPWallet contract address
                "token": payment_requirements.asset,  # Token address (e.g., USDC)
                "amount": int(auth["value"]),
                "deadline": int(auth["validBefore"]),
                "requestPath": request_path,  # Actual API path, not nonce
            },
        }

        signed_message = operator_account.sign_typed_data(
            domain_data=typed_data["domain"],
            message_types=typed_data["types"],
            message_data=typed_data["message"],
        )
        signature = signed_message.signature.hex()
        if not signature.startswith("0x"):
            signature = f"0x{signature}"

        header["payload"]["signature"] = signature
        
        # Store wallet address and request path in header for verification
        header["payload"]["authorization"]["from"] = consumer_wallet
        header["payload"]["authorization"]["requestPath"] = request_path

        encoded = encode_payment(header)
        return encoded
    except Exception:
        raise


def encode_payment(payment_payload: Dict[str, Any]) -> str:
    """Encode a payment payload into a base64 string, handling HexBytes and other non-serializable types."""
    from hexbytes import HexBytes

    def default(obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if hasattr(obj, "hex"):
            return obj.hex()
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    return safe_base64_encode(json.dumps(payment_payload, default=default))


def decode_payment(encoded_payment: str) -> Dict[str, Any]:
    """Decode a base64 encoded payment string back into a PaymentPayload object."""
    return json.loads(safe_base64_decode(encoded_payment))
