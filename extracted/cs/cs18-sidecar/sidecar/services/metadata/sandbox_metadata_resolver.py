from enum import Enum

from sidecar.services.input_value_resolver import InputValueResolver
from sidecar.services.metadata.sandbox_public_address_fetcher import SandboxMetadataFetcher


class SandboxMetadataMembers(str, Enum):
    PUBLIC_ADDRESS = "PublicAddress"
    VIRTUAL_NETWORK_ID = "VirtualNetworkId"


class SandboxMetadataResolver(InputValueResolver):
    fetcher = {}
    prefix = 'colony.'

    def __init__(self):
        pass

    def can_resolve(self, value: str) -> bool:
        return value.lower().startswith(self.prefix)

    def resolve(self, value: str):
        value = value[len(self.prefix):]
        return self.get(value)

    def register_fetcher(self, metadata_name: SandboxMetadataMembers, fetcher: SandboxMetadataFetcher):
        metadata_name = metadata_name.lower()
        if metadata_name in self.fetcher:
            raise Exception(f"metadata '{metadata_name}' already registered")
        self.fetcher[metadata_name] = fetcher

    def get(self, metadata_name: SandboxMetadataMembers):
        metadata_name = metadata_name.lower()
        fetcher: SandboxMetadataFetcher = self.fetcher.get(metadata_name, None)
        if not fetcher:
            raise Exception(f"'{self.prefix}{metadata_name}' is not supported")
        return fetcher.get_value()
