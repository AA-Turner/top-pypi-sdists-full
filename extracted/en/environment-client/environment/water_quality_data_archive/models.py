from pydantic import BaseModel, Field
from typing import Optional


class SamplingPoint(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    easting: Optional[float] = None
    northing: Optional[float] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    description: Optional[str] = None
    # Additional fields based on documentation
    type: Optional[str] = None
    sampledMaterialType: Optional[str] = None
    samplingPointType: Optional[str] = None
    samplingPointTypeGroup: Optional[str] = None
    eaArea: Optional[str] = None
    eaSubArea: Optional[str] = None


class Sample(BaseModel):
    id: str = Field(..., alias="@id")
    sampleDateTime: Optional[str] = None
    samplingPoint: Optional[str] = None
    purpose: Optional[str] = None
    # Additional fields based on documentation
    sampledMaterialType: Optional[str] = None
    determinand: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None


class Measurement(BaseModel):
    id: str = Field(..., alias="@id")
    measurementDateTime: Optional[str] = None
    sample: Optional[str] = None
    determinand: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    # Additional fields based on documentation
    qualifier: Optional[str] = None
    status: Optional[str] = None


class Determinand(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None
    unit: Optional[str] = None


class Unit(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class DeterminandGroup(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class Purpose(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class EAArea(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class EASubArea(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class SampledMaterialType(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class SamplingPointType(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None


class SamplingPointTypeGroup(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    # Additional fields based on documentation
    description: Optional[str] = None
