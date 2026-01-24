"""
Configuration management for CompALGO SDK.

Loads configuration from .env file (if present) and falls back to
environment variables. Never requires system-level env vars.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


# Load .env file from project root (if it exists)
def _load_env_file() -> None:
    """Load .env file from project root or current directory."""
    # Try current directory first
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return
    
    # Try parent directories (up to 3 levels)
    for parent in [Path.cwd().parent, Path.cwd().parent.parent, Path.cwd().parent.parent.parent]:
        env_path = parent / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            return


# Load .env on module import
_load_env_file()


class AlgoConfig:
    """Algorand configuration loaded from .env or environment variables."""
    
    def __init__(
        self,
        mnemonic: Optional[str] = None,
        algod_url: Optional[str] = None,
        algod_token: Optional[str] = None,
        indexer_url: Optional[str] = None,
        indexer_token: Optional[str] = None,
        network: Optional[str] = None,
    ):
        """
        Initialize Algorand configuration.
        
        Args:
            mnemonic: 25-word Algorand mnemonic (overrides env)
            algod_url: Algod API URL (overrides env)
            algod_token: Algod API token (overrides env)
            indexer_url: Indexer API URL (overrides env)
            indexer_token: Indexer API token (overrides env)
            network: Network name - 'testnet' or 'mainnet' (overrides env)
        """
        # Priority: explicit args > .env file > environment variables > defaults
        self.mnemonic = mnemonic or os.getenv("ALGO_MNEMONIC", "")
        self.algod_url = algod_url or os.getenv("ALGOD_URL") or os.getenv("ALGO_URL", "https://testnet-api.algonode.cloud")
        self.algod_token = algod_token or os.getenv("ALGOD_TOKEN") or os.getenv("ALGO_TOKEN", "")
        self.indexer_url = indexer_url or os.getenv("INDEXER_URL") or os.getenv("ALGO_INDEXER_URL", "https://testnet-idx.algonode.cloud")
        self.indexer_token = indexer_token or os.getenv("INDEXER_TOKEN") or os.getenv("ALGO_INDEXER_TOKEN", "")
        self.network = network or os.getenv("ALGO_NETWORK", "testnet")
    
    def validate(self, require_mnemonic: bool = True) -> None:
        """
        Validate configuration.
        
        Args:
            require_mnemonic: If True, raises error if mnemonic is missing
            
        Raises:
            ValueError: If required configuration is missing
        """
        if require_mnemonic and not self.mnemonic:
            raise ValueError(
                "ALGO_MNEMONIC is required but not set. "
                "Create a .env file in your project root with: ALGO_MNEMONIC=\"your 25 word mnemonic here\""
            )
        
        if not self.algod_url:
            raise ValueError("ALGOD_URL is required but not set")
        
        if self.network not in ["testnet", "mainnet"]:
            raise ValueError(f"ALGO_NETWORK must be 'testnet' or 'mainnet', got: {self.network}")
    
    @classmethod
    def from_env(cls) -> AlgoConfig:
        """Create config from .env file and environment variables only."""
        return cls()
    
    def __repr__(self) -> str:
        return (
            f"AlgoConfig(network={self.network}, "
            f"algod_url={self.algod_url}, "
            f"indexer_url={self.indexer_url}, "
            f"mnemonic={'***SET***' if self.mnemonic else 'NOT SET'})"
        )


def get_config(
    mnemonic: Optional[str] = None,
    algod_url: Optional[str] = None,
    network: Optional[str] = None,
) -> AlgoConfig:
    """
    Get Algorand configuration with optional overrides.
    
    Args:
        mnemonic: Override mnemonic
        algod_url: Override algod URL
        network: Override network
        
    Returns:
        AlgoConfig instance
    """
    return AlgoConfig(
        mnemonic=mnemonic,
        algod_url=algod_url,
        network=network,
    )
