from typing import List, Optional
from maleo_metadata.enums.medical_role import MaleoMetadataMedicalRoleEnums
from maleo_metadata.models.transfers.general.medical_role import MedicalRoleTransfers, StructuredMedicalRoleTransfers

class MaleoMetadataMedicalRoleGeneralTypes:
    #* Simple medical role
    SimpleMedicalRole = MaleoMetadataMedicalRoleEnums.MedicalRole
    OptionalSimpleMedicalRole = Optional[SimpleMedicalRole]
    ListOfSimpleMedicalRoles = List[SimpleMedicalRole]
    OptionalListOfSimpleMedicalRoles = Optional[List[SimpleMedicalRole]]

    #* Expanded medical role
    ExpandedMedicalRole = MedicalRoleTransfers
    OptionalExpandedMedicalRole = Optional[ExpandedMedicalRole]
    ListOfExpandedMedicalRoles = List[ExpandedMedicalRole]
    OptionalListOfExpandedMedicalRoles = Optional[List[ExpandedMedicalRole]]

    #* Structured medical role
    StructuredMedicalRole = StructuredMedicalRoleTransfers
    OptionalStructuredMedicalRole = Optional[StructuredMedicalRole]
    ListOfStructuredMedicalRoles = List[StructuredMedicalRole]
    OptionalListOfStructuredMedicalRoles = Optional[List[StructuredMedicalRole]]