from typing import List

from nexuscli.api import util
from nexuscli.api.blobstore.model import Blobstore
from nexuscli.api.base_collection import BaseCollection


class BlobstoreCollection(BaseCollection):
    @util.with_min_version('3.19.0')
    def raw_list(self) -> List[str]:
        """
        List of all blobstores on the Nexus 3 service.

        :return: a list of names
        :raises exception.NexusClientAPIError: if list cannot be retrieved; i.e.: any HTTP code
        other than 200.
        """
        return self._service_get('blobstores')

    @util.with_min_version('3.19.0')
    def get_by_name(self, name: str) -> Blobstore:
        """
        Get a Nexus 3 blobstore by its name.

        :param name: name of the wanted blobstore
        :return: the requested object
        :raise exception.NexusClientInvalidRepository: when a repository with
            the given name isn't found.
        """
        self.reset()  # ensure we have the latest items
        raw_blobstore = self._get_by_key(self.list, 'name', name)
        blobstore_type = raw_blobstore['type'].lower()
        endpoint = f'blobstores/{blobstore_type}/{name}'

        # Only return attributes that are accepted by the server when creating an object
        for key in ['blobCount', 'totalSizeInBytes', 'availableSpaceInBytes']:
            raw_blobstore.pop(key, None)

        raw_blobstore.update(self._service_get(endpoint))
        return Blobstore(**raw_blobstore)

    @util.with_min_version('3.19.0')
    def quota_status(self, name: str) -> dict:
        """See Nexus 3 API documentation."""
        return self._service_get(f'blobstores/{name}/quota-status')

    @util.with_min_version('3.19.0')
    def delete(self, name: str) -> None:
        """See Nexus 3 API documentation."""
        resp = self._http.delete(f'blobstores/{name}')
        util.validate_response(resp, 204)
        self.reset()

    @util.with_min_version('3.19.0')
    def create(self, blobstore: Blobstore) -> None:
        resp = self._http.post(
            f'blobstores/{blobstore.type.lower()}', json=blobstore.configuration)
        util.validate_response(resp, [201, 204])
        self.reset()
