# Re-export the openapi_pydantic.v3.v3_0 module as a namespace
# This avoids conflicts with existing models like Info and Discriminator
# Usage: from connector_sdk_types import OAS
#        OAS.OpenAPI.model_validate(...)
import openapi_pydantic.v3.v3_0 as OAS

__all__ = ["OAS"]
