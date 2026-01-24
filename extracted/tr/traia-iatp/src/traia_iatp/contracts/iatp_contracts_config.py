"""Contract configuration and utilities for IATP.

This module provides centralized contract configuration management for all IATP packages.
It loads contract addresses and ABIs from the iatp-contracts deployment artifacts.
"""

import json
import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from web3 import Web3

# Contract types
class ContractName(str, Enum):
    """Supported contract names."""
    IATP_WALLET = "IATPWallet"
    IATP_WALLET_FACTORY = "IATPWalletFactory"
    IATP_SETTLEMENT_LAYER = "IATPSettlementLayer"
    ROLE_MANAGER = "RoleManager"


# Supported networks
SUPPORTED_NETWORKS = ["sepolia", "base-sepolia", "arbitrum-sepolia", "localhost", "arbitrum_one"]

# Default RPC URLs
DEFAULT_RPC_URLS = {
    "sepolia": "https://ethereum-sepolia-rpc.publicnode.com",
    "base-sepolia": "https://sepolia.base.org",
    "arbitrum-sepolia": "https://sepolia-rollup.arbitrum.io/rpc",
    "localhost": "http://127.0.0.1:8545",
    "arbitrum_one": "https://arb1.arbitrum.io/rpc"
}

# Cache for loaded data
_contract_addresses_cache: Dict[str, Dict] = {}
_contract_abis_cache: Dict[str, Dict] = {}


def _get_contracts_dir() -> Path:
    """Get the contracts directory path.
    
    Uses the package's data directory where ABIs and addresses are copied.
    This directory should be updated manually whenever contracts are redeployed.
    
    Location: IATP/src/traia_iatp/contracts/data/
    """
    # Use the data directory in the package
    data_dir = Path(__file__).parent / "data"
    
    # Verify it exists and has required subdirectories
    abis_dir = data_dir / "abis"
    addresses_dir = data_dir / "addresses"
        
    if not data_dir.exists():
        raise FileNotFoundError(
            f"Contracts data directory not found: {data_dir}\n"
            "Please ensure contract ABIs and addresses are copied to this location."
        )
    
    if not abis_dir.exists() or not addresses_dir.exists():
        raise FileNotFoundError(
            f"Contract ABIs or addresses directory missing in {data_dir}\n"
            "Expected structure:\n"
            "  data/abis/contract-abis-*.json\n"
            "  data/addresses/contract-*.json"
        )
    
    # Verify files exist
    if not list(abis_dir.glob("*.json")):
        raise FileNotFoundError(f"No ABI files found in {abis_dir}")
    
    if not list(addresses_dir.glob("*.json")):
        raise FileNotFoundError(f"No address files found in {addresses_dir}")
    
    return data_dir


def get_contract_address(contract_name: str, network: str = "sepolia") -> Optional[str]:
    """Get contract address for a given network.
    
    Args:
        contract_name: Name of the contract (e.g., "IATPWallet")
        network: Network name (default: "sepolia")
        
    Returns:
        Contract address as hex string, or None if not found
    """
    if network not in SUPPORTED_NETWORKS:
        raise ValueError(f"Unsupported network: {network}. Supported: {SUPPORTED_NETWORKS}")
    
    # Check cache
    cache_key = f"{network}:addresses"
    if cache_key not in _contract_addresses_cache:
        # Load addresses file
        contracts_dir = _get_contracts_dir()
        
        # Get addresses directory (no symlinks - direct files)
        addresses_dir = contracts_dir / "addresses"
        
        if network == "localhost":
            addresses_file = addresses_dir / "contract-addresses.json"
        else:
            addresses_file = addresses_dir / f"contract-proxies-{network}.json"
        
        if not addresses_file.exists():
            # Try without network suffix
            addresses_file = addresses_dir / "contract-proxies.json"
        
        if not addresses_file.exists():
            return None
        
        with open(addresses_file, 'r') as f:
            data = json.load(f)
            
            # Handle nested structure: {network: {contract: address}}
            if network in data:
                _contract_addresses_cache[cache_key] = data[network]
            else:
                # Flat structure: {contract: address}
                _contract_addresses_cache[cache_key] = data
        
    addresses = _contract_addresses_cache[cache_key]
    return addresses.get(contract_name)


def get_contract_abi(contract_name: str, network: str = "sepolia") -> Optional[List[dict]]:
    """Get contract ABI for a given network.
    
    Args:
        contract_name: Name of the contract (e.g., "IATPWallet")
        network: Network name (default: "sepolia")
        
    Returns:
        Contract ABI as list of dicts, or None if not found
    """
    if network not in SUPPORTED_NETWORKS:
        raise ValueError(f"Unsupported network: {network}. Supported: {SUPPORTED_NETWORKS}")
    
    # Check cache
    cache_key = f"{network}:abis"
    if cache_key not in _contract_abis_cache:
        # Load ABIs file
        contracts_dir = _get_contracts_dir()
        
        # Get ABIs directory (no symlinks - direct files)
        abis_dir = contracts_dir / "abis"
        
        abis_file = abis_dir / f"contract-abis-{network}.json"
        
        if not abis_file.exists():
            return None
        
        with open(abis_file, 'r') as f:
            data = json.load(f)
            
            # Handle nested structure: {network: {contract: [abi]}}
            if network in data:
                # Data is nested by network
                _contract_abis_cache[cache_key] = data[network]
            else:
                # Flat structure: {contract: {abi: [...]}} or {contract: [abi]}
                _contract_abis_cache[cache_key] = data
    
    abis = _contract_abis_cache[cache_key]
    
    # Handle different ABI structures
    contract_data = abis.get(contract_name)
    if isinstance(contract_data, list):
        # Direct ABI list: {contract: [abi]}
        return contract_data
    elif isinstance(contract_data, dict) and "abi" in contract_data:
        # Wrapped ABI: {contract: {abi: [...]}}
        return contract_data.get("abi")
    else:
        return None


def get_rpc_url(network: str = "sepolia") -> str:
    """Get RPC URL for a network.
    
    First checks environment variables, then falls back to defaults.
    
    Environment variables:
    - SEPOLIA_RPC_URL
    - BASE_SEPOLIA_RPC_URL
    - ARBITRUM_SEPOLIA_RPC_URL
    - ARBITRUM_ONE_RPC_URL
    - LOCALHOST_RPC_URL
    
    Args:
        network: Network name (default: "sepolia")
        
    Returns:
        RPC URL as string
    """
    if network not in SUPPORTED_NETWORKS:
        raise ValueError(f"Unsupported network: {network}. Supported: {SUPPORTED_NETWORKS}")
    
    # Check environment variable
    env_var = f"{network.upper().replace('-', '_')}_RPC_URL"
    rpc_url = os.getenv(env_var)
    
    if rpc_url:
        return rpc_url
    
    # Fall back to default
    return DEFAULT_RPC_URLS.get(network, DEFAULT_RPC_URLS["sepolia"])


def get_web3_provider(network: str = "sepolia") -> Web3:
    """Get Web3 provider for a network.
    
    Args:
        network: Network name (default: "sepolia")
        
    Returns:
        Web3 instance connected to the network
    """
    rpc_url = get_rpc_url(network)
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to {network} at {rpc_url}")
    
    return w3


def load_contract(
    contract_name: str,
    network: str = "sepolia",
    address: Optional[str] = None
):
    """Load a contract instance with Web3.
    
    Args:
        contract_name: Name of the contract
        network: Network name (default: "sepolia")
        address: Optional contract address (uses deployed address if not provided)
        
    Returns:
        Web3 contract instance
    """
    w3 = get_web3_provider(network)
    
    # Get ABI
    abi = get_contract_abi(contract_name, network)
    if not abi:
        raise ValueError(f"ABI not found for {contract_name} on {network}")
    
    # Get address
    if not address:
        address = get_contract_address(contract_name, network)
        if not address:
            raise ValueError(f"Address not found for {contract_name} on {network}")
    
    # Create contract instance
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(address),
        abi=abi
    )
    
    return contract, w3

