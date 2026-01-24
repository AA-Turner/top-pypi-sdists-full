"""
D402 Price Builder - Helper for creating payment amounts.

Simplifies creating TokenAmount objects for payment configuration with any token.
"""

from .types import TokenAmount, TokenAsset, EIP712Domain


class D402PriceBuilder:
    """
    Helper class for building D402 payment amounts with any token.
    
    Initialize once with your token configuration, then create prices easily.
    
    Usage:
        # Initialize with ANY token configuration
        builder = D402PriceBuilder(
            token_address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",  # Your token
            token_decimals=6,                                              # Your decimals
            network="sepolia",                                             # Your network
            token_symbol="USDC"                                            # Your symbol
        )
        
        # Create prices easily
        price_cheap = builder.create_price(0.001)   # $0.001 
        price_standard = builder.create_price(0.01) # $0.01
        price_premium = builder.create_price(0.05)  # $0.05
        
        # Use in decorators
        @require_payment(price=price_premium, description="Premium API call")
        async def premium_endpoint():
            pass
    
    Examples:
        # USDC on Sepolia (6 decimals)
        usdc_builder = D402PriceBuilder(
            token_address="0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
            token_decimals=6,
            network="sepolia",
            token_symbol="USDC"
        )
        
        # TRAIA token (18 decimals)
        traia_builder = D402PriceBuilder(
            token_address="0x...",
            token_decimals=18,
            network="base-mainnet",
            token_symbol="TRAIA"
        )
        
        # Any custom token
        custom_builder = D402PriceBuilder(
            token_address="0xYourToken...",
            token_decimals=8,  # Your token's decimals
            network="arbitrum-mainnet",
            token_symbol="CUSTOM"
        )
    """
    
    def __init__(
        self,
        token_address: str,
        token_decimals: int,
        network: str,
        token_symbol: str = "TOKEN",
        eip712_name: str = "IATPWallet",
        eip712_version: str = "1"
    ):
        """
        Initialize the price builder with token configuration.
        
        Args:
            token_address: ERC20 token contract address
            token_decimals: Token decimals (6 for USDC, 18 for most ERC20)
            network: Blockchain network (sepolia, base-sepolia, base-mainnet, etc.)
            token_symbol: Token symbol for display (USDC, TRAIA, DAI, etc.)
            eip712_name: EIP-712 domain name (default: "IATPWallet")
            eip712_version: EIP-712 domain version (default: "1")
        """
        self.token_address = token_address
        self.token_decimals = token_decimals
        self.network = network
        self.token_symbol = token_symbol
        self.eip712_domain = EIP712Domain(
            name=eip712_name,
            version=eip712_version
        )
    
    def create_price(self, amount_usd: float) -> TokenAmount:
        """
        Create a TokenAmount from USD amount.
        
        Automatically converts USD to token's atomic units based on decimals.
        
        Args:
            amount_usd: Amount in USD (e.g., 0.01 for 1 cent, 0.05 for 5 cents)
        
        Returns:
            TokenAmount object ready to use in payment configs
        
        Examples:
            # USDC (6 decimals)
            price = builder.create_price(0.01)   # → "10000" wei (0.01 * 10^6)
            price = builder.create_price(0.001)  # → "1000" wei
            price = builder.create_price(1.00)   # → "1000000" wei
            
            # TRAIA (18 decimals)
            price = builder.create_price(0.01)   # → "10000000000000000" wei (0.01 * 10^18)
            
            # Use in decorator
            @require_payment(price=price, description="API call")
            async def my_endpoint():
                pass
        """
        # Convert USD to wei/atomic units based on token decimals
        # Formula: amount_wei = amount_usd * (10 ** decimals)
        amount_wei = str(int(amount_usd * (10 ** self.token_decimals)))
        
        return TokenAmount(
            amount=amount_wei,
            asset=TokenAsset(
                address=self.token_address,
                decimals=self.token_decimals,
                network=self.network,
                symbol=self.token_symbol,
                eip712=self.eip712_domain
            )
        )
    
    def create_price_wei(self, amount_wei: str) -> TokenAmount:
        """
        Create a TokenAmount from wei/atomic units directly.
        
        Useful when you already know the exact atomic amount.
        
        Args:
            amount_wei: Amount in atomic units as string (e.g., "10000" for 0.01 USDC)
        
        Returns:
            TokenAmount object ready to use in payment configs
        
        Example:
            # Exact atomic amount (useful for non-USD pricing)
            price = builder.create_price_wei("10000")  # Exactly 10000 atomic units
        """
        return TokenAmount(
            amount=amount_wei,
            asset=TokenAsset(
                address=self.token_address,
                decimals=self.token_decimals,
                network=self.network,
                symbol=self.token_symbol,
                eip712=self.eip712_domain
            )
        )
    
    def __repr__(self) -> str:
        return f"D402PriceBuilder(token={self.token_symbol}, network={self.network}, decimals={self.token_decimals})"


__all__ = ["D402PriceBuilder"]


