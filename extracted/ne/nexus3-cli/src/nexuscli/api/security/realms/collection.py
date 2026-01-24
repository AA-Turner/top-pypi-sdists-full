import json
from typing import List, Optional

from nexuscli.api import util
from nexuscli.api.base_collection import BaseCollection
from nexuscli.api.security.realms.model import Realm


class RealmCollection(BaseCollection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active: Optional[List[str]] = None
        self._collection: Optional[List[Realm]] = None

    def reset(self) -> None:
        super().reset()
        self._active = None
        self._collection = None

    @property
    def active(self) -> List[str]:
        """Cached version of :py:meth:`raw_active`. Use :py:meth:`reset` to refresh."""
        if self._active is None:
            self._active = self.raw_active()
        return self._active

    @property
    def collection(self) -> List[Realm]:
        """Representation of :py:meth:`raw_list` as objects. Use :py:meth:`reset` to refresh."""
        if self._collection is None:
            self._collection = []
            for raw_realm in self.list:
                active = raw_realm['id'] in self.active
                self._collection.append(Realm(nexus_http=self._http, active=active, **raw_realm))

        return self._collection

    @util.with_min_version('3.19.0')
    def raw_active(self) -> List[str]:
        """List of active security realms on the Nexus 3 service."""
        return self._service_get('security/realms/active', api_version='beta')

    @util.with_min_version('3.19.0')
    def raw_list(self) -> List[dict]:
        """The raw Nexus server response for available security realms."""
        return self._service_get('security/realms/available', api_version='beta')

    @util.with_min_version('3.19.0')
    def activate(self, realm_id: str) -> None:
        """
        Activate a security realm.

        :param realm_id: realm id to activate

        :raises exception.NexusClientAPIError: if list cannot be retrieved; i.e.: any HTTP code
        other than 204.
        """
        service_url = self._http.rest_url + 'beta/'
        headers = {'Content-type': 'application/json'}
        data = json.dumps(self.active + [realm_id])

        resp = self._http.put(
            'security/realms/active', service_url=service_url, headers=headers, data=data)

        util.validate_response(resp, 204)

        self.reset()
