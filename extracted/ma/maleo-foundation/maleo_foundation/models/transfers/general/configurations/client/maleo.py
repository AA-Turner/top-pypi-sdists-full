from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class MaleoClientConfigurations(BaseModel):
    key: str = Field(..., description="Client's key")
    name: str = Field(..., description="Client's name")
    url: str = Field(..., description="Client's URL")

class MaleoClientsConfigurations(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    telemetry: Optional[MaleoClientConfigurations] = Field(None, description="MaleoTelemetry client's configuration")
    metadata: Optional[MaleoClientConfigurations] = Field(None, description="MaleoMetadata client's configuration")
    identity: Optional[MaleoClientConfigurations] = Field(None, description="MaleoIdentity client's configuration")
    access: Optional[MaleoClientConfigurations] = Field(None, description="MaleoAccess client's configuration")
    workshop: Optional[MaleoClientConfigurations] = Field(None, description="MaleoWorkshop client's configuration")
    soapie: Optional[MaleoClientConfigurations] = Field(None, description="MaleoSOAPIE client's configuration")
    medix: Optional[MaleoClientConfigurations] = Field(None, description="MaleoMedix client's configuration")
    dicom: Optional[MaleoClientConfigurations] = Field(None, description="MaleoDICOM client's configuration")
    scribe: Optional[MaleoClientConfigurations] = Field(None, description="MaleoScribe client's configuration")
    cds: Optional[MaleoClientConfigurations] = Field(None, description="MaleoCDS client's configuration")
    imaging: Optional[MaleoClientConfigurations] = Field(None, description="MaleoImaging client's configuration")
    mcu: Optional[MaleoClientConfigurations] = Field(None, description="MaleoMCU client's configuration")