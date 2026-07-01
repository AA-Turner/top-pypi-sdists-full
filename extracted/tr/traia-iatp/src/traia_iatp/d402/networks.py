"""Network configuration for d402 payments.

This module defines supported networks and their token configurations.
Customized for IATP - uses database-driven network configuration.
"""

import os
from typing import Literal, Dict, Any
from typing_extensions import TypedDict


# Network type definition
SupportedNetworks = Literal[
    "sepolia",
    "base-sepolia",
    "arbitrum-sepolia",
    "base-mainnet",
    "arbitrum_one",
]


class NetworkConfig(TypedDict):
    """Network configuration."""
    chain_id: int
    name: str
    rpc_url: str
    explorer_url: str
    usdc_address: str


# Network configurations
NETWORKS: Dict[str, NetworkConfig] = {
    "sepolia": {
        "chain_id": 11155111,
        "name": "Ethereum Sepolia",
        "rpc_url": "https://ethereum-sepolia-rpc.publicnode.com",
        "explorer_url": "https://sepolia.etherscan.io",
        "usdc_address": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"
    },
    "base-sepolia": {
        "chain_id": 84532,
        "name": "Base Sepolia",
        "rpc_url": "https://sepolia.base.org",
        "explorer_url": "https://sepolia.basescan.org",
        "usdc_address": "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    },
    "arbitrum-sepolia": {
        "chain_id": 421614,
        "name": "Arbitrum Sepolia",
        "rpc_url": "https://arbitrum-sepolia-rpc.publicnode.com",
        "explorer_url": "https://sepolia.arbiscan.io",
        "usdc_address": "0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d"
    },
    "base-mainnet": {
        "chain_id": 8453,
        "name": "Base",
        "rpc_url": "https://mainnet.base.org",
        "explorer_url": "https://basescan.org",
        "usdc_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    },
    "arbitrum_one": {
        "chain_id": 42161,
        "name": "Arbitrum One",
        "rpc_url": os.getenv("ARBITRUM_ONE_RPC_URL", "https://arb1.arbitrum.io/rpc"),
        "explorer_url": "https://arbiscan.io",
        "usdc_address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
    }
}


def get_network_config(network: str) -> NetworkConfig:
    """Get configuration for a network."""
    if network not in NETWORKS:
        raise ValueError(f"Unsupported network: {network}")
    return NETWORKS[network]


def get_usdc_address(network: str) -> str:
    """Get USDC address for a network."""
    return get_network_config(network)["usdc_address"]


def get_chain_id(network: str) -> int:
    """Get chain ID for a network."""
    return get_network_config(network)["chain_id"]


# TODO: Load from database network table
async def load_networks_from_db() -> Dict[str, NetworkConfig]:
    """Load network configurations from database.
    
    This will query the Network table and build NETWORKS dict dynamically.
    For now, returns static config.
    """
    # from db.dal.models import Network
    # networks = await db.query(Network).filter(Network.active == True).all()
    # return {net.shortname: {...} for net in networks}
    return NETWORKS

