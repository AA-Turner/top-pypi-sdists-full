from typing import Union

from ..extensions import UnknownType
from ..models.member_collaborator import MemberCollaborator
from ..models.principal_collaborator import PrincipalCollaborator

CollaborationCreate = Union[PrincipalCollaborator, MemberCollaborator, UnknownType]
