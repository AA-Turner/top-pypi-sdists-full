from typing import List, Optional
from maleo_metadata.enums.service import MaleoMetadataServiceEnums
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceGeneralTypes:
    #* Simple blood type
    SimpleService = MaleoMetadataServiceEnums.Service
    OptionalSimpleService = Optional[SimpleService]
    ListOfSimpleServices = List[SimpleService]
    OptionalListOfSimpleServices = Optional[List[SimpleService]]

    #* Expanded blood type
    ExpandedService = ServiceTransfers
    OptionalExpandedService = Optional[ExpandedService]
    ListOfExpandedServices = List[ExpandedService]
    OptionalListOfExpandedServices = Optional[List[ExpandedService]]