from pydantic import BaseModel, Field
from typing import List, Optional, Union


class PrefLabel(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: Optional[Union[str, List[str]]] = Field(None, alias="prefLabel")


class Area(BaseModel):
    id: str = Field(..., alias="@id")
    label: str


class AssetSubType(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: str


class AssetType(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: str


class ActivitySubType(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: Optional[Union[str, List[str]]] = None


class ActivityType(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: Optional[Union[str, List[str]]] = None


class MaintenanceTask(BaseModel):
    id: str = Field(..., alias="@id")
    activitySubType: Optional[ActivitySubType] = None
    activityType: Optional[ActivityType] = None


class PrimaryPurpose(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: str


class ProtectionType(BaseModel):
    id: str = Field(..., alias="@id")
    label: str


class TargetCondition(BaseModel):
    id: str = Field(..., alias="@id")
    prefLabel: Optional[str] = None


class Asset(BaseModel):
    id: str = Field(..., alias="@id")
    actualCondition: Optional[Union[PrefLabel, List[PrefLabel]]] = None
    area: Union[List[Area], Area]
    assetStartDate: Optional[str] = None
    assetSubType: Optional[Union[AssetSubType, List[AssetSubType]]] = None
    assetType: Optional[AssetType] = None
    label: Optional[str] = None
    lastInspectionDate: Optional[Union[str, List[str]]] = None
    maintenanceTask: Optional[List[MaintenanceTask]] = None
    notation: Optional[str] = None
    primaryPurpose: Optional[PrimaryPurpose] = None
    protectionType: Optional[ProtectionType] = None
    targetCondition: Optional[PrefLabel] = None
    waterCourseName: Optional[str] = None
    actualDcl: Optional[Union[float, List[float]]] = None
    actualUcl: Optional[Union[float, List[float]]] = None
    assetLength: Optional[Union[float, List[float]]] = None
    bank: Optional[dict] = None
    designDcl: Optional[Union[float, List[float]]] = None
    designUcl: Optional[Union[float, List[float]]] = None
    currentSop: Optional[float] = None
    description: Optional[str] = None
    status: Optional[str] = None
    location: Optional[dict] = None


class MaintenanceActivity(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    description: Optional[str] = None
    activityType: Optional[dict] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class MaintenancePlan(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    description: Optional[str] = None
    planType: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class CapitalScheme(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    description: Optional[str] = None
    schemeType: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
