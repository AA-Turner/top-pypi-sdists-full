from __future__ import annotations
from maleo_metadata.client.controllers import MaleoMetadataControllers
from maleo_metadata.client.services import MaleoMetadataServices
from maleo_metadata.client.manager import MaleoMetadataClientManager

class MaleoMetadataClients:
    Controllers = MaleoMetadataControllers
    Services = MaleoMetadataServices
    Manager = MaleoMetadataClientManager