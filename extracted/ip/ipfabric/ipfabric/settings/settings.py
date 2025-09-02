import logging
from typing import Any, Optional, Union

from httpx import HTTPStatusError
from pydantic import BaseModel, ConfigDict, Field

from .api_tokens import APIToken
from .appliance import ApplianceConfiguration
from .attributes import Attributes
from .authentication import Authentication
from .discovery import Discovery
from .local_users import LocalUsers
from .rbac import Roles, Policies
from .seeds import Seeds
from .site_separation import SiteSeparation
from .vendor_api import VendorAPI
from ipfabric.tools.shared import raise_for_status

logger = logging.getLogger("ipfabric")


class Settings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: Any = Field(exclude=True)
    _local_users: Optional[Union[LocalUsers, bool]] = None
    _api_tokens: Optional[Union[APIToken, bool]] = None
    _site_separation: Optional[Union[SiteSeparation, bool]] = None
    _discovery: Optional[Union[Discovery, bool]] = None
    _authentication: Optional[Union[Authentication, bool]] = None
    _seeds: Optional[Union[Seeds, bool]] = None
    _vendor_api: Optional[Union[VendorAPI, bool]] = None
    _global_attributes: Optional[Union[Attributes, bool]] = None
    _roles: Optional[Union[Roles, bool]] = None
    _policies: Optional[Union[Policies, bool]] = None
    _appliance_configuration: Optional[Union[ApplianceConfiguration, bool]] = None

    def _try_object(self, obj, name, attr):
        if getattr(self, attr) is None:
            try:
                setattr(self, attr, obj(client=self.client))
            except HTTPStatusError:
                setattr(self, attr, False)
        if getattr(self, attr) is not False:
            return getattr(self, attr)
        logger.warning(f"{self.client._api_insuf_rights} for `{name}` class.")
        return None

    @property
    def local_users(self) -> LocalUsers:
        return self._try_object(LocalUsers, "LocalUsers", "_local_users")

    @property
    def roles(self) -> Roles:
        return self._try_object(Roles, "Roles", "_roles")

    @property
    def policies(self) -> Policies:
        return self._try_object(Policies, "Policies", "_policies")

    @property
    def api_tokens(self) -> APIToken:
        return self._try_object(APIToken, "APIToken", "_api_tokens")

    @property
    def site_separation(self) -> SiteSeparation:
        return self._try_object(SiteSeparation, "SiteSeparation", "_site_separation")

    @property
    def discovery(self) -> Union[Discovery, None]:
        if self._discovery is None:
            try:
                settings = raise_for_status(self.client.get("settings")).json()
                self._discovery = Discovery(
                    client=self.client,
                    vendorApi=VendorAPI(client=self.client, vendor_api=settings.pop("vendorApi")),
                    authentication=Authentication(
                        client=self.client,
                        settings={"credentials": settings.pop("credentials"), "privileges": settings.pop("privileges")}
                    ),
                    **settings,
                )
            except HTTPStatusError:
                self._discovery = False
        if self._discovery is not False:
            return self._discovery
        logger.warning(f"{self.client._api_insuf_rights} for `Discovery` class.")
        return None

    @property
    def authentication(self) -> Authentication:
        return self._try_object(Authentication, "Authentication", "_authentication")

    @property
    def seeds(self) -> Seeds:
        return self._try_object(Seeds, "Seeds", "_seeds")

    @property
    def vendor_api(self) -> VendorAPI:
        return self._try_object(VendorAPI, "VendorAPI", "_vendor_api")

    @property
    def global_attributes(self) -> Attributes:
        if self._global_attributes is None:
            self._global_attributes = Attributes(client=self.client)
        return self._global_attributes

    @property
    def appliance_configuration(self) -> ApplianceConfiguration:
        return self._try_object(ApplianceConfiguration, "ApplianceConfiguration", "_appliance_configuration")
