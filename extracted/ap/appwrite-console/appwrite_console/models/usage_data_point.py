from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class UsageDataPoint(AppwriteModel):
    """
    usageDataPoint

    Attributes
    ----------
    time : Optional[str]
        Bucket start timestamp in ISO 8601. Omitted for flat dimension aggregates.
    value : float
        Aggregated value for the point.
    path : Optional[str]
        Value when broken down by `path`.
    method : Optional[str]
        Value when broken down by `method`.
    status : Optional[str]
        Value when broken down by `status`.
    service : Optional[str]
        Value when broken down by `service`.
    country : Optional[str]
        Value when broken down by `country`.
    region : Optional[str]
        Value when broken down by `region`.
    hostname : Optional[str]
        Value when broken down by `hostname`.
    ip : Optional[str]
        Value when broken down by `ip`.
    protocol : Optional[str]
        Value when broken down by `protocol`.
    accept : Optional[str]
        Value when broken down by `accept`.
    acceptlanguage : Optional[str]
        Value when broken down by `acceptLanguage`.
    querykeys : Optional[str]
        Value when broken down by `queryKeys`.
    osname : Optional[str]
        Value when broken down by `osName`.
    clienttype : Optional[str]
        Value when broken down by `clientType`.
    clientname : Optional[str]
        Value when broken down by `clientName`.
    sdk : Optional[str]
        Value when broken down by `sdk`.
    sdkversion : Optional[str]
        Value when broken down by `sdkVersion`.
    devicename : Optional[str]
        Value when broken down by `deviceName`.
    resourceid : Optional[str]
        Value when broken down by `resourceId`.
    resourcetype : Optional[str]
        Value when broken down by `resourceType`.
    ordinal : Optional[str]
        Value when broken down by `ordinal`.
    continentcode : Optional[str]
        Continent code when broken down by `continentCode`.
    city : Optional[str]
        City name when broken down by `city`.
    subdivisions : Optional[str]
        Region/state chain when broken down by `subdivisions`.
    postalcode : Optional[str]
        Postal code when broken down by `postalCode`.
    latitude : Optional[str]
        Latitude when broken down by `latitude`.
    longitude : Optional[str]
        Longitude when broken down by `longitude`.
    timezone : Optional[str]
        Time zone when broken down by `timeZone`.
    weathercode : Optional[str]
        Weather station code when broken down by `weatherCode`.
    isp : Optional[str]
        Internet service provider when broken down by `isp`.
    autonomoussystemnumber : Optional[str]
        Autonomous System Number (ASN) when broken down by `autonomousSystemNumber`.
    autonomoussystemorganization : Optional[str]
        Organization owning the ASN when broken down by `autonomousSystemOrganization`.
    connectiontype : Optional[str]
        Connection type when broken down by `connectionType`.
    connectionusagetype : Optional[str]
        Connection usage type when broken down by `connectionUsageType`.
    connectionorganization : Optional[str]
        Registered organization of the IP when broken down by `connectionOrganization`.
    teamid : Optional[str]
        Owning team ID when broken down by `teamId`.
    """

    time: Optional[str] = Field(default=None, alias='time')
    value: float = Field(..., alias='value')
    path: Optional[str] = Field(default=None, alias='path')
    method: Optional[str] = Field(default=None, alias='method')
    status: Optional[str] = Field(default=None, alias='status')
    service: Optional[str] = Field(default=None, alias='service')
    country: Optional[str] = Field(default=None, alias='country')
    region: Optional[str] = Field(default=None, alias='region')
    hostname: Optional[str] = Field(default=None, alias='hostname')
    ip: Optional[str] = Field(default=None, alias='ip')
    protocol: Optional[str] = Field(default=None, alias='protocol')
    accept: Optional[str] = Field(default=None, alias='accept')
    acceptlanguage: Optional[str] = Field(default=None, alias='acceptLanguage')
    querykeys: Optional[str] = Field(default=None, alias='queryKeys')
    osname: Optional[str] = Field(default=None, alias='osName')
    clienttype: Optional[str] = Field(default=None, alias='clientType')
    clientname: Optional[str] = Field(default=None, alias='clientName')
    sdk: Optional[str] = Field(default=None, alias='sdk')
    sdkversion: Optional[str] = Field(default=None, alias='sdkVersion')
    devicename: Optional[str] = Field(default=None, alias='deviceName')
    resourceid: Optional[str] = Field(default=None, alias='resourceId')
    resourcetype: Optional[str] = Field(default=None, alias='resourceType')
    ordinal: Optional[str] = Field(default=None, alias='ordinal')
    continentcode: Optional[str] = Field(default=None, alias='continentCode')
    city: Optional[str] = Field(default=None, alias='city')
    subdivisions: Optional[str] = Field(default=None, alias='subdivisions')
    postalcode: Optional[str] = Field(default=None, alias='postalCode')
    latitude: Optional[str] = Field(default=None, alias='latitude')
    longitude: Optional[str] = Field(default=None, alias='longitude')
    timezone: Optional[str] = Field(default=None, alias='timeZone')
    weathercode: Optional[str] = Field(default=None, alias='weatherCode')
    isp: Optional[str] = Field(default=None, alias='isp')
    autonomoussystemnumber: Optional[str] = Field(default=None, alias='autonomousSystemNumber')
    autonomoussystemorganization: Optional[str] = Field(default=None, alias='autonomousSystemOrganization')
    connectiontype: Optional[str] = Field(default=None, alias='connectionType')
    connectionusagetype: Optional[str] = Field(default=None, alias='connectionUsageType')
    connectionorganization: Optional[str] = Field(default=None, alias='connectionOrganization')
    teamid: Optional[str] = Field(default=None, alias='teamId')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'value' not in data:
            data['value'] = 0
        return data
