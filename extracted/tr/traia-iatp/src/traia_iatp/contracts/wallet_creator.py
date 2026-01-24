"""IATPWallet creation script using IATPWalletFactory.

This script creates a new IATPWallet by calling the IATPWalletFactory contract.
It generates an operator keypair and deploys a wallet for a given owner.

Uses centralized contract configuration from traia_iatp.contracts.config.
"""

import os
import json
from typing import Dict, Optional, Tuple
from pathlib import Path
from eth_account import Account
from web3 import Web3
from web3.contract import Contract


def get_contract_config(network: str = "sepolia") -> Dict:
    """Load contract addresses and ABIs for a network.
    
    Uses the centralized config module from traia_iatp.contracts.config.
    
    Args:
        network: Network name (sepolia, base-sepolia, etc.)
        
    Returns:
        Dict with addresses and ABIs
    """
    from traia_iatp.contracts.iatp_contracts_config import get_contract_address, get_contract_abi
    
    # Get all contract addresses and ABIs
    contract_names = ["IATPWalletFactory", "IATPSettlementLayer", "IATPWallet", "RoleManager"]
    addresses = {}
    abis = {}
    
    for name in contract_names:
        try:
            address = get_contract_address(name, network)
            if address:
                addresses[name] = address
            
            abi = get_contract_abi(name, network)
            if abi:
                abis[name] = {"abi": abi}
        except Exception as e:
            # Some contracts may not be on all networks
            pass
    
    return {
        "addresses": addresses,
        "abis": abis
    }


def create_iatp_wallet(
    owner_private_key: str,
    operator_address: Optional[str] = None,
    create_operator: bool = False,
    wallet_name: str = "",
    wallet_type: str = "MCP_SERVER",
    wallet_description: str = "",
    network: str = "sepolia",
    rpc_url: Optional[str] = None,
    maintainer_private_key: Optional[str] = None
) -> Dict[str, str]:
    """Create a new IATPWallet using IATPWalletFactory.
    
    Args:
        owner_private_key: Private key of the wallet owner (REQUIRED INPUT)
        operator_address: Operator address (REQUIRED unless create_operator=True)
        create_operator: If True, generates new operator keypair
        wallet_name: Name for the wallet (e.g., "My MCP Server")
        wallet_type: Type of wallet - one of: CLIENT, HUMAN, MCP_SERVER, WEB_SERVER, AGENT
        wallet_description: Description of the wallet/service
        network: Network name (default: sepolia)
        rpc_url: Optional RPC URL (uses default if not provided)
        maintainer_private_key: Optional maintainer key for createWalletFor (uses env/SSM if not provided)
        
    Returns:
        Dictionary with:
        - wallet_address: Deployed IATPWallet contract address
        - owner_address: Owner address (from owner_private_key)
        - operator_address: Operator address
        - operator_private_key: Operator private key (only if create_operator=True)
        - network: Network name
        - transaction_hash: Deployment transaction
    """
    # Setup Web3
    if not rpc_url:
        rpc_urls = {
            "sepolia": os.getenv("SEPOLIA_RPC_URL", "https://ethereum-sepolia-rpc.publicnode.com"),
            "base-sepolia": os.getenv("BASE_SEPOLIA_RPC_URL", "https://sepolia.base.org"),
            "arbitrum-sepolia": os.getenv("ARBITRUM_SEPOLIA_RPC_URL", "https://sepolia-rollup.arbitrum.io/rpc"),
            "arbitrum_one": os.getenv("ARBITRUM_ONE_RPC_URL", "https://arb1.arbitrum.io/rpc"),
        }
        rpc_url = rpc_urls.get(network)
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        raise ConnectionError(f"Could not connect to {network} at {rpc_url}")
    
    print(f"✅ Connected to {network}")
    print(f"   RPC: {rpc_url}")
    print(f"   Chain ID: {w3.eth.chain_id}")
    
    # Load contract config
    config = get_contract_config(network)
    factory_address = config["addresses"].get("IATPWalletFactory")
    factory_abi = config["abis"].get("IATPWalletFactory", {}).get("abi")
    
    if not factory_address:
        raise ValueError(f"IATPWalletFactory address not found for {network}")
    
    if not factory_abi:
        raise ValueError(f"IATPWalletFactory ABI not found for {network}")
    
    print(f"\n📝 Contract Configuration:")
    print(f"   Factory: {factory_address}")
    
    # Create owner account
    if owner_private_key.startswith("0x"):
        owner_private_key_clean = owner_private_key[2:]
    else:
        owner_private_key_clean = owner_private_key
    owner_account = Account.from_key(owner_private_key_clean)
    print(f"\n👤 Owner Account: {owner_account.address}")
    
    # Handle operator
    operator_private_key_output = None
    if create_operator:
        # Generate new operator keypair
        operator_account = Account.create()
        operator_address = operator_account.address
        operator_private_key_output = operator_account.key.hex()
        
        print(f"\n🔑 Generated Operator:")
        print(f"   Address: {operator_address}")
        print(f"   Private Key: {operator_private_key_output}")
    elif not operator_address:
        raise ValueError("operator_address required (or use --create-operator)")
    else:
        print(f"\n🔑 Using Provided Operator:")
        print(f"   Address: {operator_address}")
    
    # Map wallet type string to enum value
    wallet_type_map = {
        "CLIENT": 0,
        "HUMAN": 1,
        "MCP_SERVER": 2,
        "WEB_SERVER": 3,
        "AGENT": 4
    }
    
    if isinstance(wallet_type, str):
        wallet_type_int = wallet_type_map.get(wallet_type.upper())
        if wallet_type_int is None:
            raise ValueError(f"Invalid wallet_type: {wallet_type}. Must be one of: {list(wallet_type_map.keys())}")
    else:
        wallet_type_int = int(wallet_type)
    
    print(f"\n📝 Wallet Metadata:")
    print(f"   Name: {wallet_name or '(none)'}")
    print(f"   Type: {list(wallet_type_map.keys())[wallet_type_int]} ({wallet_type_int})")
    print(f"   Description: {wallet_description[:50] + '...' if len(wallet_description) > 50 else wallet_description or '(none)'}")
    
    # Create factory contract instance
    factory_contract = w3.eth.contract(
        address=Web3.to_checksum_address(factory_address),
        abi=factory_abi
    )
    
    # Determine which method to call
    if maintainer_private_key:
        # Use createWalletFor (maintainer creates for someone else)
        # This is used by backend deployment scripts
        if maintainer_private_key.startswith("0x"):
            maintainer_private_key = maintainer_private_key[2:]
        caller_account = Account.from_key(maintainer_private_key)
        
        print(f"\n📞 Calling createWalletFor() as maintainer")
        print(f"   Maintainer: {caller_account.address}")
        
        # Check maintainer balance
        maintainer_balance = w3.eth.get_balance(caller_account.address)
        print(f"   Balance: {w3.from_wei(maintainer_balance, 'ether')} ETH")
        
        if maintainer_balance < w3.to_wei(0.001, 'ether'):
            raise ValueError(f"Insufficient maintainer balance: {w3.from_wei(maintainer_balance, 'ether')} ETH (need >= 0.001 ETH)")
        
        # Build transaction with metadata
        tx = factory_contract.functions.createWalletFor(
            Web3.to_checksum_address(owner_account.address),
            Web3.to_checksum_address(operator_address),
            wallet_type_int,  # WalletType enum
            wallet_name,      # Name
            wallet_description  # Description
        ).build_transaction({
            'from': caller_account.address,
            'nonce': w3.eth.get_transaction_count(caller_account.address),
            'gas': 3000000,
            'maxFeePerGas': w3.to_wei('2', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('0.1', 'gwei'),
            'chainId': w3.eth.chain_id
        })
        
        # Estimate gas
        try:
            estimated_gas = w3.eth.estimate_gas(tx)
            tx['gas'] = int(estimated_gas * 1.2)
            print(f"\n⛽ Estimated gas: {estimated_gas}")
        except Exception as e:
            print(f"\n⚠️  Gas estimation failed: {e}, using default")
        
        # Sign and send
        signed_tx = w3.eth.account.sign_transaction(tx, caller_account.key)
        
    else:
        # Use createWallet (owner creates their own wallet)
        # This is the normal path for developers using the CLI
        print(f"\n📞 Calling createWallet() as owner")
        print(f"   Owner: {owner_account.address}")
        
        # Check owner balance
        owner_balance = w3.eth.get_balance(owner_account.address)
        print(f"   Balance: {w3.from_wei(owner_balance, 'ether')} ETH")
        
        if owner_balance < w3.to_wei(0.001, 'ether'):
            raise ValueError(f"Insufficient owner balance: {w3.from_wei(owner_balance, 'ether')} ETH (need >= 0.001 ETH for gas)")
        
        # Build transaction
        tx = factory_contract.functions.createWallet(
            Web3.to_checksum_address(operator_address),
            wallet_type_int,  # WalletType enum
            wallet_name,      # Name
            wallet_description  # Description
        ).build_transaction({
            'from': owner_account.address,
            'nonce': w3.eth.get_transaction_count(owner_account.address),
            'gas': 3000000,
            'maxFeePerGas': w3.to_wei('2', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('0.1', 'gwei'),
            'chainId': w3.eth.chain_id
        })
        
        # Estimate gas
        try:
            estimated_gas = w3.eth.estimate_gas(tx)
            tx['gas'] = int(estimated_gas * 1.2)
            print(f"\n⛽ Estimated gas: {estimated_gas}")
        except Exception as e:
            print(f"\n⚠️  Gas estimation failed: {e}, using default")
        
        # Sign and send with owner key
        signed_tx = w3.eth.account.sign_transaction(tx, owner_account.key)
    
    print(f"\n🚀 Sending transaction...")
    raw_tx = signed_tx.raw_transaction if hasattr(signed_tx, 'raw_transaction') else signed_tx.rawTransaction
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    print(f"   TX Hash: {tx_hash.hex()}")
    
    print(f"\n⏳ Waiting for confirmation...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    
    if tx_receipt['status'] == 1:
        print(f"✅ Transaction confirmed!")
        print(f"   Block: {tx_receipt['blockNumber']}")
        print(f"   Gas Used: {tx_receipt['gasUsed']}")
        
        # Parse logs to get wallet address
        wallet_address = None
        try:
            wallet_created_event = factory_contract.events.WalletCreated()
            logs = wallet_created_event.process_receipt(tx_receipt)
            
            if logs:
                wallet_address = logs[0]['args']['wallet']
                print(f"\n🎉 IATPWallet Deployed!")
                print(f"   Wallet Address: {wallet_address}")
                print(f"   Owner: {logs[0]['args']['owner']}")
                print(f"   Operator: {logs[0]['args']['operatorAddress']}")
        except Exception as e:
            print(f"⚠️  Could not parse event logs: {e}")
        
        # Fallback: Get wallet using getWalletForOwner
        if not wallet_address:
            try:
                wallet_address = factory_contract.functions.getWalletForOwner(
                    Web3.to_checksum_address(owner_account.address)
                ).call()
                print(f"\n🎉 IATPWallet Deployed!")
                print(f"   Wallet Address: {wallet_address}")
            except Exception as e:
                raise Exception(f"Could not retrieve wallet address: {e}")
        
        # Build result dictionary
        result = {
            "wallet_address": wallet_address,
            "owner_address": owner_account.address,
            "operator_address": operator_address,
            "network": network,
            "transaction_hash": tx_hash.hex(),
            "gas_used": tx_receipt['gasUsed'],
            "block_number": tx_receipt['blockNumber']
        }
        
        # Include operator private key if we generated it
        if operator_private_key_output:
            result["operator_private_key"] = operator_private_key_output
        
        return result
    else:
        raise Exception(f"Transaction failed: {tx_receipt}")


def main():
    """CLI entry point for IATP wallet creation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create IATPWallet using IATPWalletFactory")
    parser.add_argument("--owner-key", required=True, help="Owner's private key (REQUIRED INPUT)")
    parser.add_argument("--operator-address", help="Operator address (required unless --create-operator)")
    parser.add_argument("--create-operator", action="store_true", help="Generate new operator keypair")
    parser.add_argument("--wallet-name", default="", help="Name for the wallet")
    parser.add_argument("--wallet-type", default="MCP_SERVER", 
                       help="Wallet type: CLIENT, HUMAN, MCP_SERVER, WEB_SERVER, AGENT (default: MCP_SERVER)")
    parser.add_argument("--wallet-description", default="", help="Description of the wallet/service")
    parser.add_argument("--network", default="sepolia", help="Network name (default: sepolia)")
    parser.add_argument("--rpc-url", help="Custom RPC URL")
    parser.add_argument("--maintainer-key", help="Maintainer key (or use MAINTAINER_PRIVATE_KEY env var)")
    parser.add_argument("--output", help="Output file for wallet info (JSON)")
    
    args = parser.parse_args()
    
    try:
        result = create_iatp_wallet(
            owner_private_key=args.owner_key,
            operator_address=args.operator_address,
            create_operator=args.create_operator,
            wallet_name=args.wallet_name,
            wallet_type=args.wallet_type,
            wallet_description=args.wallet_description,
            network=args.network,
            rpc_url=args.rpc_url,
            maintainer_private_key=args.maintainer_key
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Wallet info saved to: {args.output}")
        
        print(f"\n{'='*80}")
        print("IATPWallet Created Successfully!")
        print(f"{'='*80}")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

