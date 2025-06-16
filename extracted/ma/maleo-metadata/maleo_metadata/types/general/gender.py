from typing import List, Optional
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderGeneralTypes:
    #* Simple blood type
    SimpleGender = MaleoMetadataGenderEnums.Gender
    OptionalSimpleGender = Optional[SimpleGender]
    ListOfSimpleGenders = List[SimpleGender]
    OptionalListOfSimpleGenders = Optional[List[SimpleGender]]

    #* Expanded blood type
    ExpandedGender = GenderTransfers
    OptionalExpandedGender = Optional[ExpandedGender]
    ListOfExpandedGenders = List[ExpandedGender]
    OptionalListOfExpandedGenders = Optional[List[ExpandedGender]]