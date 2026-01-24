"""D402 client for IATP agent-to-agent payments."""

import logging
from typing import Optional, Dict, Any
from eth_account import Account
from .clients.base import d402Client
from .types import PaymentRequirements

logger = logging.getLogger(__name__)


class D402IATPClient:
    """Client for making d402 payments in IATP protocol.
    
    This wraps the Coinbase d402 client and provides IATP-specific functionality,
    including integration with utility agent smart contracts.
    """
    
    def __init__(
        self,
        account: Account,
        max_value: Optional[int] = None,
        agent_contract_address: Optional[str] = None,
        operator_private_key: Optional[str] = None
    ):
        """Initialize the d402 IATP client.
        
        Args:
            account: eth_account.Account instance for signing payments
            max_value: Optional maximum allowed payment amount in base units
            agent_contract_address: Optional address of the client agent's smart contract
            operator_private_key: Optional operator private key for signing service requests
        """
        self.account = account
        self.max_value = max_value
        self.agent_contract_address = agent_contract_address
        self.operator_private_key = operator_private_key
        
        # Initialize the underlying d402 client
        self.d402_client = d402Client(
            operator_account=account,
            max_value=max_value
        )
    
    def create_payment_header(
        self,
        payment_requirements: PaymentRequirements,
        d402_version: int = 1
    ) -> str:
        """Create a payment header for the given requirements.
        
        This creates an EIP-3009 signed payment authorization that the facilitator
        can use to pull funds from the client agent's wallet.
        
        Args:
            payment_requirements: Selected payment requirements from server
            d402_version: d402 protocol version
            
        Returns:
            Base64-encoded signed payment header for X-PAYMENT header
        """
        return self.d402_client.create_payment_header(
            payment_requirements=payment_requirements,
            d402_version=d402_version
        )
    
    def select_payment_requirements(
        self,
        accepts: list[PaymentRequirements],
        network_filter: Optional[str] = None,
        scheme_filter: Optional[str] = "exact"
    ) -> PaymentRequirements:
        """Select payment requirements from available options.
        
        Args:
            accepts: List of accepted payment requirements from server
            network_filter: Optional network to filter by
            scheme_filter: Optional scheme to filter by (default: "exact")
            
        Returns:
            Selected payment requirements
            
        Raises:
            UnsupportedSchemeException: If no supported scheme found
            PaymentAmountExceededError: If amount exceeds max_value
        """
        return self.d402_client.select_payment_requirements(
            accepts=accepts,
            network_filter=network_filter,
            scheme_filter=scheme_filter
        )
    
    def get_payment_info_for_agent_card(self, agent_card: dict) -> Optional[Dict[str, Any]]:
        """Extract d402 payment information from an agent card.
        
        Args:
            agent_card: Agent card dictionary
            
        Returns:
            Payment information if available, None otherwise
        """
        metadata = agent_card.get("metadata", {})
        return metadata.get("d402")


def create_iatp_payment_client(
    private_key: str,
    max_value_usd: Optional[float] = None,
    agent_contract_address: Optional[str] = None
) -> D402IATPClient:
    """Convenience function to create an IATP payment client.
    
    Args:
        private_key: Hex-encoded private key (with or without 0x prefix)
        max_value_usd: Optional maximum payment in USD
        agent_contract_address: Optional agent contract address
        
    Returns:
        Configured D402IATPClient
        
    Example:
        client = create_iatp_payment_client(
            private_key="0x...",
            max_value_usd=10.0  # Max $10 per request
        )
        
        # Use with httpx
        from .clients.httpx import Httpd402Client
        http_client = Httpd402Client(client)
        response = await http_client.get("https://agent.example.com/api")
    """
    # Remove 0x prefix if present
    if private_key.startswith("0x"):
        private_key = private_key[2:]
    
    # Create eth_account.Account
    account = Account.from_key(private_key)
    
    # Convert USD to atomic units (assuming USDC with 6 decimals)
    max_value = None
    if max_value_usd is not None:
        max_value = int(max_value_usd * 1_000_000)  # USDC has 6 decimals
    
    return D402IATPClient(
        account=account,
        max_value=max_value,
        agent_contract_address=agent_contract_address,
        operator_private_key=private_key
    )

