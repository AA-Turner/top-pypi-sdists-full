from cnvrgv2._version import __version__
from cnvrgv2.config import routes
from cnvrgv2.config.error_messages import PROXY_UNAUTH_ERROR
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.datasource.datasource import StorageTypes
from cnvrgv2.modules.datasource.datasources_client import DatasourcesClient
from cnvrgv2.modules.datasets_client import DatasetsClient
from cnvrgv2.modules.images.images_client import ImagesClient
from cnvrgv2.modules.registries.registries_client import RegistriesClient
from cnvrgv2.modules.libhub.libraries.libraries_client import LibrariesClient
from cnvrgv2.modules.members.members_client import MembersClient
from cnvrgv2.modules.labels.labels_client import LabelsClient
from cnvrgv2.modules.projects_client import ProjectsClient
from cnvrgv2.modules.resources.clusters_client import ClustersClient
from cnvrgv2.modules.ssh.ssh_client import SshClient
from cnvrgv2.modules.users.user import ROLES, User
from cnvrgv2.modules.users.users_client import UsersClient
from cnvrgv2.modules.organization.organization_settings import OrganizationSettings
from cnvrgv2.modules.storage_class.storage_classes_client import StorageClassesClient
from cnvrgv2.modules.volumes.volumes_client import VolumesClient
from cnvrgv2.proxy import HTTP, Proxy


class Cnvrg:
    def __init__(self, domain=None, email=None, password=None, organization=None, token=None):

        self._context = Context(
            domain=domain,
            user=email,
            password=password,
            organization=organization,
            token=token
        )

        self.check_version_compatibility(__version__)

        self._proxy = Proxy(context=self._context)

        self._init_clients()
        self._organization = organization or self._context.organization
        self.StorageTypes = StorageTypes

    def me(self):
        """
        Retrieves information about the current user
        @return: A dictionary representing the current logged in user
        """
        users_client = UsersClient(self._context.domain, self._context.token)
        return users_client.me()

    def is_admin(self):
        """
        @return: Returns if the logged user is an admin in the current organization or not
        """
        user_membership = next(membership for membership in self.me().roles
                               if membership["organization"] == self._organization)
        return user_membership["access_level"] == ROLES.ADMIN

    def get_users(self):
        """
        Shows all the users in the current organization
        Can only be used by admins
        @return: A list with all the users in the organization
        """
        if not self.is_admin():
            raise CnvrgError(PROXY_UNAUTH_ERROR)

        response = self._proxy.call_api(
            route=routes.ORGANIZATION_USERS.format(self._organization),
            http_method=HTTP.GET,
        )
        users = map(lambda x: User(self._context.domain, x.attributes["token"], x.attributes), response.items)
        return list(users)

    def set_organization(self, organization):
        """
        Replaces the organization with the given one
        @param organization: Organization name (String)
        @return: None
        """
        self._context.set_scope(scope=SCOPE.ORGANIZATION, slug=organization)
        self._init_clients()
        self._organization = organization

    def check_version_compatibility(self, version):
        """
        Check sdk version compatibility against the server
        @param version:
        @return:
        """
        # TODO: IMPLEMENT
        pass

    def _init_clients(self):
        """
        Sets up the clients that are exposed to the user.
        @return: None
        """
        try:

            self.projects = ProjectsClient(self)
            self.datasets = DatasetsClient(self)
            self.libraries = LibrariesClient(self)
            self.images = ImagesClient(self)
            self.registries = RegistriesClient(self)
            self.settings = OrganizationSettings(self)
            self.clusters = ClustersClient(self)
            self.ssh = SshClient(self)
            self.members = MembersClient(self)
            self.storage_classes = StorageClassesClient(self)
            self.volumes = VolumesClient(self)
            self.datasources = DatasourcesClient(self)
            self.labels = LabelsClient(self)

        except CnvrgError as e:
            print(f'There is an error: {e}')
            # TODO: How to handle exceptions
            pass
