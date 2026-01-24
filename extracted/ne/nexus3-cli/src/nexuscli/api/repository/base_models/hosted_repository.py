from nexuscli.api import validations
from nexuscli.api.repository.base_models import Repository

from urllib.parse import urljoin

DEFAULT_WRITE_POLICY = 'ALLOW'


class HostedRepository(Repository):
    """
    A hosted Nexus repository.

    :param name: name of the repository.
    :type name: str
    :param write_policy: one of :py:attr:`WRITE_POLICIES`. See Nexus
        documentation for details.
    :type write_policy: str
    :param kwargs: see :class:`Repository`
    """
    WRITE_POLICIES = ['ALLOW', 'ALLOW_ONCE', 'DENY']
    """Nexus 3 repository write policies supported by this class."""

    TYPE = 'hosted'

    def __init__(self, *args, **kwargs):
        self.write_policy: str = kwargs.get('write_policy', DEFAULT_WRITE_POLICY)

        super().__init__(*args, **kwargs)

    def _validate_params(self):
        super()._validate_params()
        validations.ensure_known('write_policy', self.write_policy, self.WRITE_POLICIES)

    @property
    def _url(self):
        return urljoin(self._client.config.url, f'repository/{self.name}')

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        repo_config['attributes']['storage'].update({
            'writePolicy': self.write_policy,
        })

        return repo_config
