from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import (
    ClientServiceControllers,
    ClientControllers
)

from maleo_metadata.client.controllers.http.blood_type \
    import MaleoMetadataBloodTypeHTTPController
class MaleoMetadataBloodTypeControllers(ClientServiceControllers):
    http:MaleoMetadataBloodTypeHTTPController = Field(..., description="Blood type's http controller")

from maleo_metadata.client.controllers.http.gender \
    import MaleoMetadataGenderHTTPController
class MaleoMetadataGenderControllers(ClientServiceControllers):
    http:MaleoMetadataGenderHTTPController = Field(..., description="Gender's http controller")

from maleo_metadata.client.controllers.http.medical_role \
    import MaleoMetadataMedicalRoleHTTPController
class MaleoMetadataMedicalRoleHTTPControllers(ClientServiceControllers):
    http:MaleoMetadataMedicalRoleHTTPController = Field(..., description="Medical role's http controller")

from maleo_metadata.client.controllers.http.organization_type \
    import MaleoMetadataOrganizationTypeHTTPController
class MaleoMetadataOrganizationTypeControllers(ClientServiceControllers):
    http:MaleoMetadataOrganizationTypeHTTPController = Field(..., description="Organization type's http controller")

from maleo_metadata.client.controllers.http.service \
    import MaleoMetadataServiceHTTPController
class MaleoMetadataServiceControllers(ClientServiceControllers):
    http:MaleoMetadataServiceHTTPController = Field(..., description="Service's http controller")

from maleo_metadata.client.controllers.http.system_role \
    import MaleoMetadataSystemRoleHTTPController
class MaleoMetadataSystemRoleControllers(ClientServiceControllers):
    http:MaleoMetadataSystemRoleHTTPController = Field(..., description="System role's http controller")

from maleo_metadata.client.controllers.http.user_type \
    import MaleoMetadataUserTypeHTTPController
class MaleoMetadataUserTypeControllers(ClientServiceControllers):
    http:MaleoMetadataUserTypeHTTPController = Field(..., description="User type's http controller")

class MaleoMetadataControllers(ClientControllers):
    blood_type:MaleoMetadataBloodTypeControllers = Field(..., description="Blood type's controllers")
    gender:MaleoMetadataGenderControllers = Field(..., description="Gender's controllers")
    medical_role:MaleoMetadataMedicalRoleHTTPControllers = Field(..., description="Medical role's controllers")
    organization_type:MaleoMetadataOrganizationTypeControllers = Field(..., description="Organization type's controllers")
    service:MaleoMetadataServiceControllers = Field(..., description="Service's controllers")
    system_role:MaleoMetadataSystemRoleControllers = Field(..., description="System role's controllers")
    user_type:MaleoMetadataUserTypeControllers = Field(..., description="User type's controllers")