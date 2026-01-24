import time
from typing import Optional, Callable, Dict, Any, List
from eth_account import Account
from ..payment_signing import sign_payment_header
from ..types import (
    PaymentRequirements,
    UnsupportedSchemeException,
)
from ..common import d402_VERSION
import secrets
from ..encoding import safe_base64_decode
import json

# Define type for the payment requirements selector
PaymentSelectorCallable = Callable[
    [List[PaymentRequirements], Optional[str], Optional[str], Optional[int]],
    PaymentRequirements,
]


def decode_x_payment_response(header: str) -> Dict[str, Any]:
    """Decode the X-PAYMENT-RESPONSE header.

    Args:
        header: The X-PAYMENT-RESPONSE header to decode

    Returns:
        The decoded payment response containing:
        - success: bool
        - transaction: str (hex)
        - network: str
        - payer: str (address)
    """
    decoded = safe_base64_decode(header)
    result = json.loads(decoded)
    return result


class PaymentError(Exception):
    """Base class for payment-related errors."""

    pass


class PaymentAmountExceededError(PaymentError):
    """Raised when payment amount exceeds maximum allowed value."""

    pass


class MissingRequestConfigError(PaymentError):
    """Raised when request configuration is missing."""

    pass


class PaymentAlreadyAttemptedError(PaymentError):
    """Raised when payment has already been attempted."""

    pass


class d402Client:
    """Base client for handling d402 payments."""

    def __init__(
        self,
        operator_account: Account,
        wallet_address: str = None,
        max_value: Optional[int] = None,
        payment_requirements_selector: Optional[PaymentSelectorCallable] = None,
    ):
        """Initialize the d402 client.

        Args:
            operator_account: Operator account with private key for signing payments (EOA)
            wallet_address: Consumer's IATPWallet contract address (if None, uses operator_account.address for testing)
            max_value: Optional safety limit for maximum payment amount per request in base units.
                      This is a global safety check that prevents paying more than intended.
                      WARNING: This is a simple numeric comparison and does NOT account for:
                      - Different tokens (USDC vs TRAIA vs others) - amounts are compared directly
                      - Token decimals - ensure max_value uses the same decimals as expected tokens
                      - Exchange rates - this is not a USD limit, it's a token amount limit
                      Each endpoint can have different payment requirements (amount and token),
                      but this limit applies to all requests. Set it based on your most expensive
                      expected payment in the token's base units.
                      If None, no limit is enforced (not recommended for production).
            payment_requirements_selector: Optional custom selector for payment requirements
        """
        self.operator_account = operator_account  # Operator EOA for signing
        self.wallet_address = wallet_address or operator_account.address  # IATPWallet contract or EOA for testing
        self.max_value = max_value
        self._payment_requirements_selector = (
            payment_requirements_selector or self.default_payment_requirements_selector
        )

    @staticmethod
    def default_payment_requirements_selector(
        accepts: List[PaymentRequirements],
        network_filter: Optional[str] = None,
        scheme_filter: Optional[str] = None,
        max_value: Optional[int] = None,
    ) -> PaymentRequirements:
        """Select payment requirements from the list of accepted requirements.

        Args:
            accepts: List of accepted payment requirements
            network_filter: Optional network to filter by
            scheme_filter: Optional scheme to filter by
            max_value: Optional maximum allowed payment amount

        Returns:
            Selected payment requirements (PaymentRequirements instance from ..types)

        Raises:
            UnsupportedSchemeException: If no supported scheme is found
            PaymentAmountExceededError: If payment amount exceeds max_value
        """
        for paymentRequirements in accepts:
            scheme = paymentRequirements.scheme
            network = paymentRequirements.network

            # Check scheme filter
            if scheme_filter and scheme != scheme_filter:
                continue

            # Check network filter
            if network_filter and network != network_filter:
                continue

            if scheme == "exact":
                # Check max value if set
                # NOTE: This is a simple numeric comparison. It does NOT account for:
                # - Different tokens (USDC vs TRAIA vs others)
                # - Token decimals differences
                # - Exchange rates between tokens
                # This is a safety limit to prevent accidentally paying too much.
                # The comparison is done on the raw amount values in base units.
                if max_value is not None:
                    max_amount = int(paymentRequirements.max_amount_required)
                    if max_amount > max_value:
                        raise PaymentAmountExceededError(
                            f"Payment amount {max_amount} (token: {paymentRequirements.asset}) "
                            f"exceeds maximum allowed value {max_value} base units. "
                            f"Note: This comparison does not account for token differences or decimals."
                        )

                return paymentRequirements

        raise UnsupportedSchemeException("No supported payment scheme found")

    def select_payment_requirements(
        self,
        accepts: List[PaymentRequirements],
        network_filter: Optional[str] = None,
        scheme_filter: Optional[str] = None,
    ) -> PaymentRequirements:
        """Select payment requirements using the configured selector.

        Args:
            accepts: List of accepted payment requirements (PaymentRequirements models)
            network_filter: Optional network to filter by
            scheme_filter: Optional scheme to filter by

        Returns:
            Selected payment requirements (PaymentRequirements instance from ..types)

        Raises:
            UnsupportedSchemeException: If no supported scheme is found
            PaymentAmountExceededError: If payment amount exceeds max_value
        """
        return self._payment_requirements_selector(
            accepts, network_filter, scheme_filter, self.max_value
        )

   
    def create_payment_header(
        self,
        payment_requirements: PaymentRequirements,
        d402_version: int = d402_VERSION,
        request_path: str = None,
    ) -> str:
        """Create a payment header for the given requirements.

        Args:
            payment_requirements: Selected payment requirements
            d402_version: d402 protocol version
            request_path: Optional API request path (if None, uses payment_requirements.resource)

        Returns:
            Signed payment header with PullFundsForSettlement signature
        """
        unsigned_header = {
            "d402Version": d402_version,
            "scheme": payment_requirements.scheme,
            "network": payment_requirements.network,
            "payload": {
                "signature": None,
                "authorization": {
                    "from": self.wallet_address,  # IATPWallet contract address
                    "to": payment_requirements.pay_to,  # Provider's IATPWallet
                    "value": payment_requirements.max_amount_required,
                    "validAfter": str(int(time.time()) - 60),  # 60 seconds before
                    "validBefore": str(
                        int(time.time()) + payment_requirements.max_timeout_seconds
                    ),
                },
            },
        }

        signed_header = sign_payment_header(
            self.operator_account,
            payment_requirements,
            unsigned_header,
            wallet_address=self.wallet_address,
            request_path=request_path or payment_requirements.resource
        )
        return signed_header
