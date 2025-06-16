from typing import List, Optional
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleGeneralTypes:
    #* Simple system type
    SimpleSystemRole = MaleoMetadataSystemRoleEnums.SystemRole
    OptionalSimpleSystemRole = Optional[SimpleSystemRole]
    ListOfSimpleSystemRoles = List[SimpleSystemRole]
    OptionalListOfSimpleSystemRoles = Optional[List[SimpleSystemRole]]

    #* Expanded system type
    ExpandedSystemRole = SystemRoleTransfers
    OptionalExpandedSystemRole = Optional[ExpandedSystemRole]
    ListOfExpandedSystemRoles = List[ExpandedSystemRole]
    OptionalListOfExpandedSystemRoles = Optional[List[ExpandedSystemRole]]