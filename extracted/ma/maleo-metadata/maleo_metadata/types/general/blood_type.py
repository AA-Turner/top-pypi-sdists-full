from typing import List, Optional
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeGeneralTypes:
    #* Simple blood type
    SimpleBloodType = MaleoMetadataBloodTypeEnums.BloodType
    OptionalSimpleBloodType = Optional[SimpleBloodType]
    ListOfSimpleBloodTypes = List[SimpleBloodType]
    OptionalListOfSimpleBloodTypes = Optional[List[SimpleBloodType]]

    #* Expanded blood type
    ExpandedBloodType = BloodTypeTransfers
    OptionalExpandedBloodType = Optional[ExpandedBloodType]
    ListOfExpandedBloodTypes = List[ExpandedBloodType]
    OptionalListOfExpandedBloodTypes = Optional[List[ExpandedBloodType]]