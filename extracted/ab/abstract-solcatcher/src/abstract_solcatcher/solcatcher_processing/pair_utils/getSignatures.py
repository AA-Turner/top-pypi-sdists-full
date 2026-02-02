from abstract_utilities import *
from getMetaData import *
from abstract_solana import get_signatures
def get_addresses_from_meta(metadata,mint):
    addresses = get_any_value(metadata,'publicKey')
    if addresses:
        addresses = [addr for addr in addresses if addr != mint]
        return addresses
async def async_pull_genesis_signature_from_address(address=None,url_1_only=None,url_2_only=None):
        signatures = await async_get_signatures(address,url_1_only=url_1_only,url_2_only=url_2_only)
        if signatures:
            signature = signatures[-1]
            return signature.get('signature')
def pull_genesis_signature_from_address(address=None,url_1_only=None,url_2_only=None):
        signatures = get_signatures(address,url_1_only=url_1_only,url_2_only=url_2_only)
        if signatures:
            signature = signatures[-1]
            return signature.get('signature')
async def async_get_addresses_for_genesis_from_mint(mint=None,url_1_only=None,url_2_only=None):
    metadata = await async_get_or_fetch_meta_data(mint=mint)
    return get_addresses_from_meta(metadata,mint)
def get_addresses_for_genesis_from_mint(mint=None,url_1_only=None,url_2_only=None):
    metadata = get_or_fetch_meta_data(mint=mint)
    return get_addresses_from_meta(metadata,mint)
async def async_get_genesis_signature_from_mint(mint=None, url_1_only=None, url_2_only=None):
    addresses = await async_get_addresses_for_genesis_from_mint(mint=mint,url_1_only=url_1_only,url_2_only=url_2_only)
    if addresses:
        address = addresses[0]
        signature = await async_pull_genesis_signature_from_address(address, url_1_only=url_1_only, url_2_only=url_2_only)
        return signature
def get_genesis_signature_from_mint(mint=None,url_1_only=None,url_2_only=None):
    addresses = get_addresses_for_genesis_from_mint(mint=mint,url_1_only=url_1_only,url_2_only=url_2_only)
    if addresses:
        address = addresses[0]
        signature = pull_genesis_signature_from_address(address, url_1_only=url_1_only, url_2_only=url_2_only)
        return signature

