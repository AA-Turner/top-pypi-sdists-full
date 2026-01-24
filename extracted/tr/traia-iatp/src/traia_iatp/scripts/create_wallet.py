#!/usr/bin/env python3
"""Create an IATPWallet for a user.

This script:
1. Takes an owner private key as input
2. Generates a new operator keypair
3. Calls IATPWalletFactory.createWallet() to deploy an IATPWallet
4. Returns the operator keys and wallet address

Usage:
    uv run python -m traia_iatp.scripts.create_wallet \\
        --owner-key 0x... \\
        --network sepolia \\
        [--wait-confirmations 2]
"""

import argparse
import json
import logging
import sys
from eth_account import Account
from web3 import Web3

from traia_iatp.contracts import (
    get_contract_address,
    load_contract,
    ContractName
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_wallet(
    owner_private_key: str,
    network: str = "sepolia",
    wait_confirmations: int = 2
) -> dict:
    """Create an IATP Wallet for an owner.
    
    Args:
        owner_private_key: Owner's private key (0x...)
        network: Network name (default: "sepolia")
        wait_confirmations: Number of confirmations to wait (default: 2)
        
    Returns:
        Dict with operator keys and wallet address:
        {
            "owner_address": "0x...",
            "operator_address": "0x...",
            "operator_private_key": "0x...",
            "wallet_address": "0x...",
            "transaction_hash": "0x...",
            "network": "sepolia"
        }
    """
    logger.info(f"Creating IATP Wallet on {network}")
    
    # Create owner account
    if not owner_private_key.startswith("0x"):
        owner_private_key = f"0x{owner_private_key}"
    
    owner_account = Account.from_key(owner_private_key)
    logger.info(f"Owner address: {owner_account.address}")
    
    # Generate new operator keypair
    operator_account = Account.create()
    logger.info(f"Generated operator address: {operator_account.address}")
    logger.info(f"Operator private key: {operator_account.key.hex()}")
    
    # Load IATPWalletFactory contract
    factory_contract, w3 = load_contract(
        ContractName.IATP_WALLET_FACTORY,
        network=network
    )
    
    factory_address = factory_contract.address
    logger.info(f"IATPWalletFactory address: {factory_address}")
    
    # Check owner balance
    owner_balance = w3.eth.get_balance(owner_account.address)
    logger.info(f"Owner balance: {w3.from_wei(owner_balance, 'ether')} ETH")
    
    if owner_balance == 0:
        logger.error("Owner has no ETH for gas. Please fund the account.")
        raise ValueError("Insufficient balance for gas")
    
    # Build transaction to create wallet
    logger.info("Building createWallet transaction...")
    
    tx = factory_contract.functions.createWallet(
        operator_account.address
    ).build_transaction({
        'from': owner_account.address,
        'nonce': w3.eth.get_transaction_count(owner_account.address),
        'gas': 2000000,  # Estimate gas
        'gasPrice': w3.eth.gas_price,
        'chainId': w3.eth.chain_id
    })
    
    # Sign transaction
    signed_tx = owner_account.sign_transaction(tx)
    
    # Send transaction
    logger.info("Sending transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    logger.info(f"Transaction hash: {tx_hash.hex()}")
    
    # Wait for confirmation
    logger.info(f"Waiting for {wait_confirmations} confirmation(s)...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    
    if tx_receipt['status'] != 1:
        logger.error("Transaction failed!")
        raise Exception(f"Transaction failed: {tx_hash.hex()}")
    
    logger.info(f"Transaction confirmed in block {tx_receipt['blockNumber']}")
    
    # Parse WalletCreated event to get wallet address
    wallet_address = None
    for log in tx_receipt['logs']:
        try:
            event = factory_contract.events.WalletCreated().process_log(log)
            wallet_address = event['args']['wallet']
            logger.info(f"✅ IATPWallet created: {wallet_address}")
            break
        except:
            continue
    
    if not wallet_address:
        logger.error("Could not find WalletCreated event in logs")
        raise Exception("Wallet address not found in transaction logs")
    
    # Return result
    result = {
        "owner_address": owner_account.address,
        "operator_address": operator_account.address,
        "operator_private_key": operator_account.key.hex(),
        "wallet_address": wallet_address,
        "transaction_hash": tx_hash.hex(),
        "block_number": tx_receipt['blockNumber'],
        "network": network,
        "chain_id": w3.eth.chain_id
    }
    
    return result


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create an IATP Wallet via IATPWalletFactory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create wallet on Sepolia
  uv run python -m traia_iatp.scripts.create_wallet \\
      --owner-key 0x0cdda2d9d744d6d2a3ba4b30ac51227590f0e8f44cf5251bb1ed0941d677c0a4 \\
      --network sepolia
  
  # Create wallet with output to JSON file
  uv run python -m traia_iatp.scripts.create_wallet \\
      --owner-key 0x... \\
      --network sepolia \\
      --output wallet_config.json
        """
    )
    
    parser.add_argument(
        "--owner-key",
        required=True,
        help="Owner's private key (0x...)"
    )
    
    parser.add_argument(
        "--network",
        default="sepolia",
        choices=["sepolia", "base-sepolia", "arbitrum-sepolia", "arbitrum_one", "localhost"],
        help="Network to deploy on (default: sepolia)"
    )
    
    parser.add_argument(
        "--wait-confirmations",
        type=int,
        default=2,
        help="Number of confirmations to wait (default: 2)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output JSON file path (prints to stdout if not specified)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create wallet
        result = create_wallet(
            owner_private_key=args.owner_key,
            network=args.network,
            wait_confirmations=args.wait_confirmations
        )
        
        # Output result
        output_json = json.dumps(result, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
            logger.info(f"✅ Configuration saved to: {args.output}")
        else:
            print("\n" + "=" * 80)
            print("IATP Wallet Created Successfully!")
            print("=" * 80)
            print(output_json)
            print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to create wallet: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

