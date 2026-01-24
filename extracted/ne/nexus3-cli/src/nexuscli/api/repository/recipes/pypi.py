from nexuscli import exception
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

from twine.exceptions import TwineException
import twine.package
import twine.repository

__all__ = ['PypiHostedRepository', 'PypiProxyRepository', 'PypiGroupRepository']


class _PypiRepository(Repository):
    RECIPE_NAME = 'pypi'


class PypiGroupRepository(_PypiRepository, GroupRepository):
    pass


class PypiHostedRepository(_PypiRepository, HostedRepository):
    def upload_file(self, src_file, dst_dir=None, dst_file=None):
        """
        Upload a single file to a PyPI repository.

        :param src_file: path to the local file to be uploaded.
        :param dst_dir: NOT USED
        :param dst_file: NOT USED
        :raises exception.NexusClientInvalidRepositoryPath: invalid repository
            path.
        :raises exception.NexusClientAPIError: unknown response from Nexus API.
        """
        try:
            twine_package = twine.package.PackageFile.from_filename(str(src_file), '')
            twine_repository = twine.repository.Repository(
                repository_url=self._url + '/',
                username=self._client.config.auth[0],
                password=self._client.config.auth[1],
                disable_progress_bar=True
            )
            response = twine_repository.upload(twine_package)
        except TwineException as e:
            raise exception.NexusClientAPIError(
                f'Uploading to {self.name}. Reason: {e}') from None

        if response.status_code != 200:
            raise exception.NexusClientAPIError(
                f'Uploading to {self.name}. Reason: {response.reason} '
                f'Status code: {response.status_code} Text: {response.text}')


class PypiProxyRepository(_PypiRepository, ProxyRepository):
    pass
