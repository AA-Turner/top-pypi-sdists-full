import pathlib
import warnings

from nexuscli import exception
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['NpmHostedRepository', 'NpmProxyRepository', 'NpmGroupRepository']


class _NpmRepository(Repository):
    RECIPE_NAME = 'npm'


class NpmGroupRepository(_NpmRepository, GroupRepository):
    pass


class NpmHostedRepository(_NpmRepository, HostedRepository):
    def upload_file(self, src_file, dst_dir=None, dst_file=None):
        """
        Upload a single file to a npm repository.

        :param src_file: path to the local file to be uploaded.
        :param dst_dir: NOT USED
        :param dst_file: NOT USED
        :raises exception.NexusClientInvalidRepositoryPath: invalid repository path.
        :raises exception.NexusClientAPIError: unknown response from Nexus API.
        """
        if dst_dir or dst_file:
            warnings.warn(f'dst_dir={dst_dir} and dst_file={dst_file} are ignored')

        params = {'repository': self.name}
        src_file = pathlib.Path(src_file)
        files = {src_file.name: src_file.open('rb').read()}

        response = self._client.post('components', files=files, params=params, stream=True)

        if response.status_code != 204:
            raise exception.NexusClientAPIError(
                f'Uploading to {self.name}. Reason: {response.reason} '
                f'Status code: {response.status_code} Text: {response.text}')


class NpmProxyRepository(_NpmRepository, ProxyRepository):
    pass
