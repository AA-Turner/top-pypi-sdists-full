from typing import List, Optional
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums
from maleo_metadata.models.transfers.general.user_type import UserTypeTransfers

class MaleoMetadataUserTypeGeneralTypes:
    #* Simple user type
    SimpleUserType = MaleoMetadataUserTypeEnums.UserType
    OptionalSimpleUserType = Optional[SimpleUserType]
    ListOfSimpleUserTypes = List[SimpleUserType]
    OptionalListOfSimpleUserTypes = Optional[List[SimpleUserType]]

    #* Expanded user type
    ExpandedUserType = UserTypeTransfers
    OptionalExpandedUserType = Optional[ExpandedUserType]
    ListOfExpandedUserTypes = List[ExpandedUserType]
    OptionalListOfExpandedUserTypes = Optional[List[ExpandedUserType]]