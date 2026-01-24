from nexuscli import exception, nexus_util
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository
from requests_toolbelt.multipart.encoder import MultipartEncoder
__all__ = ['RawHostedRepository', 'RawProxyRepository', 'RawGroupRepository']


class _RawRepository(Repository):
    RECIPE_NAME = 'raw'


class RawGroupRepository(_RawRepository, GroupRepository):
    pass


class RawHostedRepository(_RawRepository, HostedRepository):
    def upload_file(self, source, destination):
        """
        Upload a single file to a raw repository.

        :param source: path to the local file to be uploaded.
        :param destination: directory under dst_repo to place file in. When None,
            the file is placed under the root of the raw repository
        :raises exception.NexusClientInvalidRepositoryPath: invalid repository path.
        :raises exception.NexusClientAPIError: unknown response from Nexus API.
        """
        destination, dst_file = nexus_util.get_dst_path_and_file(source, destination)

        params = {'repository': self.name}
        data = MultipartEncoder(
            fields={
                'raw.directory': (None, destination),
                'raw.asset1': (str(source), open(source, 'rb')),
                'raw.asset1.filename': (None, dst_file),
            }
        )
        headers = {'Content-Type': data.content_type}
        response = self._client.post(
            'components', data=data, params=params, headers=headers, stream=True)

        if response.status_code != 204:
            raise exception.NexusClientAPIError(
                f'Uploading to {self.name}. Reason: {response.reason} '
                f'Status code: {response.status_code} Text: {response.text}')


class RawProxyRepository(_RawRepository, ProxyRepository):
    pass
