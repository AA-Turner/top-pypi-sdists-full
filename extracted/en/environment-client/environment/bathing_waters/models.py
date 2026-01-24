from pydantic import BaseModel, Field
from typing import List, Union, Optional


class Name(BaseModel):
    value: str = Field(..., alias="_value")
    lang: str = Field(..., alias="_lang")


class AppointedSewerageUndertaker(BaseModel):
    about: str = Field(..., alias="_about")
    name: Name


class Country(BaseModel):
    about: str = Field(..., alias="_about")
    name: Name


class District(BaseModel):
    about: str = Field(..., alias="_about")
    name: Name


class ComplianceClassification(BaseModel):
    about: str = Field(..., alias="_about")
    name: Name


class LatestComplianceAssessment(BaseModel):
    about: str = Field(..., alias="_about")
    compliance_classification: ComplianceClassification = Field(
        ..., alias="complianceClassification"
    )


class RiskLevel(BaseModel):
    about: str = Field(..., alias="_about")
    name: Name


class ExpiresAt(BaseModel):
    value: str = Field(..., alias="_value")
    datatype: str = Field(..., alias="_datatype")


class LatestRiskPrediction(BaseModel):
    about: str = Field(..., alias="_about")
    expires_at: ExpiresAt = Field(..., alias="expiresAt")
    risk_level: RiskLevel = Field(..., alias="riskLevel")


class SamplingPoint(BaseModel):
    about: str = Field(..., alias="_about")
    easting: int
    lat: float
    long: float
    name: Name
    northing: int
    # Additional fields based on documentation
    label: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None


class BathingWater(BaseModel):
    """
    A model for a bathing water.
    """

    about: str = Field(..., alias="_about")
    appointed_sewerage_undertaker: AppointedSewerageUndertaker = Field(
        ..., alias="appointedSewerageUndertaker"
    )
    country: Country
    district: List[Union[District, str]]
    eubwid_notation: str = Field(..., alias="eubwidNotation")
    latest_compliance_assessment: LatestComplianceAssessment = Field(
        ..., alias="latestComplianceAssessment"
    )
    latest_risk_prediction: LatestRiskPrediction = Field(
        ..., alias="latestRiskPrediction"
    )
    latest_sample_assessment: str = Field(..., alias="latestSampleAssessment")
    name: Name
    sampling_point: SamplingPoint = Field(..., alias="samplingPoint")
    sediment_types_present: str = Field(..., alias="sedimentTypesPresent")
    water_quality_impacted_by_heavy_rain: bool = Field(
        ..., alias="waterQualityImpactedByHeavyRain"
    )
    year_designated: str = Field(..., alias="yearDesignated")
    # Additional fields based on documentation
    label: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    classification: Optional[str] = None


class SampleAssessment(BaseModel):
    about: str = Field(..., alias="_about")
    label: Optional[str] = None
    sampleDateTime: Optional[str] = None
    eColi: Optional[float] = None
    intestinalEnterococci: Optional[float] = None
    # Add other fields as per documentation


class ComplianceAssessment(BaseModel):
    about: str = Field(..., alias="_about")
    label: Optional[str] = None
    assessmentDate: Optional[str] = None
    classification: Optional[str] = None
    # Add other fields as per documentation


class PollutionIncident(BaseModel):
    about: str = Field(..., alias="_about")
    label: Optional[str] = None
    incidentDate: Optional[str] = None
    incidentType: Optional[str] = None
    # Add other fields as per documentation


class ZoneOfInfluence(BaseModel):
    about: str = Field(..., alias="_about")
    label: Optional[str] = None
    description: Optional[str] = None
    # Add other fields as per documentation
