from pydantic import BaseModel, Field
from maleo_metadata.types.general.service import MaleoMetadataServiceGeneralTypes

class MaleoMetadataServiceExpandedSchemas:
    class SimpleService(BaseModel):
        service:MaleoMetadataServiceGeneralTypes.SimpleService = Field(..., description="Service")

    class OptionalService(BaseModel):
        service:MaleoMetadataServiceGeneralTypes.OptionalSimpleService = Field(None, description="Service")

    class ListOfSimpleServices(BaseModel):
        services:MaleoMetadataServiceGeneralTypes.ListOfSimpleServices = Field([], description="Services")

    class OptionalListOfSimpleServices(BaseModel):
        services:MaleoMetadataServiceGeneralTypes.OptionalListOfSimpleServices = Field(None, description="Services")

    class ExpandedService(BaseModel):
        service_details:MaleoMetadataServiceGeneralTypes.ExpandedService = Field(..., description="Service's details")

    class OptionalExpandedService(BaseModel):
        service_details:MaleoMetadataServiceGeneralTypes.OptionalExpandedService = Field(None, description="Service's details")

    class ListOfExpandedServices(BaseModel):
        services_details:MaleoMetadataServiceGeneralTypes.ListOfExpandedServices = Field([], description="Services's details")

    class OptionalListOfExpandedServices(BaseModel):
        services_details:MaleoMetadataServiceGeneralTypes.OptionalListOfExpandedServices = Field(None, description="Services's details")