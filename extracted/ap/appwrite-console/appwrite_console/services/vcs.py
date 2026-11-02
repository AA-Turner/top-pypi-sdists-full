from ..service import Service
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Union
from ..exception import AppwriteException
from appwrite_console.utils.deprecated import deprecated
from ..enums.vcs_detection_type import VCSDetectionType
from ..models.detection_runtime import DetectionRuntime
from ..models.detection_framework import DetectionFramework
from ..models.provider_repository_runtime_list import ProviderRepositoryRuntimeList
from ..models.provider_repository_framework_list import ProviderRepositoryFrameworkList
from ..models.provider_repository import ProviderRepository
from ..models.branch_list import BranchList
from ..models.vcs_content_list import VcsContentList
from ..models.installation_list import InstallationList
from ..models.installation import Installation
from ..models.vcs_namespace_list import VcsNamespaceList


class Vcs(Service):

    def __init__(self, client) -> None:
        super(Vcs, self).__init__(client)

    def create_repository_detection(
        self,
        installation_id: str,
        provider_repository_id: str,
        type: VCSDetectionType,
        provider_root_directory: Optional[str] = None,
    ) -> Union[
        DetectionRuntime,
        DetectionFramework,
    ]:
        """
        Analyze a GitHub repository to automatically detect the programming language and runtime environment. This endpoint scans the repository's files and language statistics to determine the appropriate runtime settings for your function. The GitHub installation must be properly configured and the repository must be accessible through your installation for this endpoint to work.

        Parameters
        ----------
        installation_id : str
            Installation Id
        provider_repository_id : str
            Repository Id
        type : VCSDetectionType
            Detector type. Must be one of the following: runtime, framework
        provider_root_directory : Optional[str]
            Path to Root Directory
        Returns
        -------
        Union[DetectionRuntime, DetectionFramework]
            API response as one of the typed response models

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/detections'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if provider_repository_id is None:
            raise AppwriteException('Missing required parameter: "provider_repository_id"')
        if type is None:
            raise AppwriteException('Missing required parameter: "type"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_params['providerRepositoryId'] = self._normalize_value(provider_repository_id)
        api_params['type'] = self._normalize_value(type)
        if provider_root_directory is not None:
            api_params['providerRootDirectory'] = self._normalize_value(provider_root_directory)

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )
        if not isinstance(response, dict):
            raise AppwriteException('Expected object response when hydrating a response model')

        if response.get('type') == 'runtime':
            return self._parse_response(response, model=DetectionRuntime)

        if response.get('type') == 'framework':
            return self._parse_response(response, model=DetectionFramework)

        raise AppwriteException('Unable to match response to any known model')

    def list_repositories(
        self,
        installation_id: str,
        type: VCSDetectionType,
        search: Optional[str] = None,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> Union[
        ProviderRepositoryRuntimeList,
        ProviderRepositoryFrameworkList,
    ]:
        """
        Get a list of GitHub repositories available through your installation. This endpoint returns repositories with their basic information, detected runtime environments, and latest push dates. You can optionally filter repositories using a search term. Each repository's runtime is automatically detected based on its contents and language statistics. The GitHub installation must be properly configured for this endpoint to work.

        Parameters
        ----------
        installation_id : str
            Installation Id
        type : VCSDetectionType
            Detector type. Must be one of the following: runtime, framework
        search : Optional[str]
            Search term to filter your list results. Max length: 256 chars.
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Only supported methods are limit, offset, and equal on namespace.
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        Union[ProviderRepositoryRuntimeList, ProviderRepositoryFrameworkList]
            API response as one of the typed response models

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/providerRepositories'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if type is None:
            raise AppwriteException('Missing required parameter: "type"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_params['type'] = self._normalize_value(type)
        if search is not None:
            api_params['search'] = self._normalize_value(search)
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )
        if not isinstance(response, dict):
            raise AppwriteException('Expected object response when hydrating a response model')

        if response.get('type') == 'runtime':
            return self._parse_response(response, model=ProviderRepositoryRuntimeList)

        if response.get('type') == 'framework':
            return self._parse_response(response, model=ProviderRepositoryFrameworkList)

        raise AppwriteException('Unable to match response to any known model')

    def create_repository(
        self,
        installation_id: str,
        name: str,
        private: bool,
        provider_namespace: Optional[str] = None,
    ) -> ProviderRepository:
        """
        Create a new GitHub repository through your installation. This endpoint allows you to create either a public or private repository by specifying a name and visibility setting. The repository will be created under your GitHub user account or organization, depending on your installation type. The GitHub installation must be properly configured and have the necessary permissions for repository creation.

        Parameters
        ----------
        installation_id : str
            Installation Id
        name : str
            Repository name (slug)
        private : bool
            Mark repository public or private
        provider_namespace : Optional[str]
            Namespace of the git repository. Defaults to the installation's own namespace.
        Returns
        -------
        ProviderRepository
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/providerRepositories'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if name is None:
            raise AppwriteException('Missing required parameter: "name"')
        if private is None:
            raise AppwriteException('Missing required parameter: "private"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_params['name'] = self._normalize_value(name)
        api_params['private'] = self._normalize_value(private)
        if provider_namespace is not None:
            api_params['providerNamespace'] = self._normalize_value(provider_namespace)

        response = self.client.call(
            'post',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ProviderRepository)

    def get_repository(
        self,
        installation_id: str,
        provider_repository_id: str,
    ) -> ProviderRepository:
        """
        Get detailed information about a specific GitHub repository from your installation. This endpoint returns repository details including its ID, name, visibility status, organization, and latest push date. The GitHub installation must be properly configured and have access to the requested repository for this endpoint to work.

        Parameters
        ----------
        installation_id : str
            Installation Id
        provider_repository_id : str
            Repository Id
        Returns
        -------
        ProviderRepository
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/providerRepositories/{providerRepositoryId}'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if provider_repository_id is None or provider_repository_id == '':
            raise AppwriteException('Missing required parameter: "provider_repository_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_path = api_path.replace('{providerRepositoryId}', self._encode_path(provider_repository_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=ProviderRepository)

    def list_repository_branches(
        self,
        installation_id: str,
        provider_repository_id: str,
        search: Optional[str] = None,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> BranchList:
        """
        Get a list of branches from a GitHub repository in your installation. This endpoint supports filtering by a search term and pagination using query strings such as `Query.limit()`, `Query.offset()`, `Query.cursorAfter()`, and `Query.cursorBefore()`. It returns branch names along with the total number of matches. The GitHub installation must be properly configured and have access to the requested repository for this endpoint to work.

        Parameters
        ----------
        installation_id : str
            Installation Id
        provider_repository_id : str
            Repository Id
        search : Optional[str]
            Search term to filter your list results. Max length: 256 chars.
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Only supported methods are limit, offset, cursorAfter, and cursorBefore
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        BranchList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/providerRepositories/{providerRepositoryId}/branches'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if provider_repository_id is None or provider_repository_id == '':
            raise AppwriteException('Missing required parameter: "provider_repository_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_path = api_path.replace('{providerRepositoryId}', self._encode_path(provider_repository_id))
        if search is not None:
            api_params['search'] = self._normalize_value(search)
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=BranchList)

    def get_repository_contents(
        self,
        installation_id: str,
        provider_repository_id: str,
        provider_root_directory: Optional[str] = None,
        provider_reference: Optional[str] = None,
    ) -> VcsContentList:
        """
        Get a list of files and directories from a GitHub repository connected to your project. This endpoint returns the contents of a specified repository path, including file names, sizes, and whether each item is a file or directory. The GitHub installation must be properly configured and the repository must be accessible through your installation for this endpoint to work.

        Parameters
        ----------
        installation_id : str
            Installation Id
        provider_repository_id : str
            Repository Id
        provider_root_directory : Optional[str]
            Path to get contents of nested directory
        provider_reference : Optional[str]
            Git reference (branch, tag, commit) to get contents from
        Returns
        -------
        VcsContentList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/providerRepositories/{providerRepositoryId}/contents'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if provider_repository_id is None or provider_repository_id == '':
            raise AppwriteException('Missing required parameter: "provider_repository_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_path = api_path.replace('{providerRepositoryId}', self._encode_path(provider_repository_id))
        if provider_root_directory is not None:
            api_params['providerRootDirectory'] = self._normalize_value(provider_root_directory)
        if provider_reference is not None:
            api_params['providerReference'] = self._normalize_value(provider_reference)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=VcsContentList)

    def update_external_deployments(
        self,
        installation_id: str,
        repository_id: str,
        provider_pull_request_id: str,
    ) -> Dict[str, Any]:
        """
        Authorize and create deployments for a GitHub pull request in your project. This endpoint allows external contributions by creating deployments from pull requests, enabling preview environments for code review. The pull request must be open and not previously authorized. The GitHub installation must be properly configured and have access to both the repository and pull request for this endpoint to work.

        Parameters
        ----------
        installation_id : str
            Installation Id
        repository_id : str
            VCS Repository Id
        provider_pull_request_id : str
            GitHub Pull Request Id
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/github/installations/{installationId}/repositories/{repositoryId}'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        if repository_id is None or repository_id == '':
            raise AppwriteException('Missing required parameter: "repository_id"')
        if provider_pull_request_id is None:
            raise AppwriteException('Missing required parameter: "provider_pull_request_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        api_path = api_path.replace('{repositoryId}', self._encode_path(repository_id))
        api_params['providerPullRequestId'] = self._normalize_value(provider_pull_request_id)

        response = self.client.call(
            'patch',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def list_installations(
        self,
        queries: Optional[List[str]] = None,
        search: Optional[str] = None,
        total: Optional[bool] = None,
    ) -> InstallationList:
        """
        List all VCS installations configured for the current project. This endpoint returns a list of installations including their provider, organization, and other configuration details.

        Parameters
        ----------
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Maximum of 100 queries are allowed, each 4096 characters long. You may filter on the following attributes: provider, organization
        search : Optional[str]
            Search term to filter your list results. Max length: 256 chars.
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        InstallationList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/installations'
        api_params = {}
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if search is not None:
            api_params['search'] = self._normalize_value(search)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=InstallationList)

    def get_installation(
        self,
        installation_id: str,
    ) -> Installation:
        """
        Get a VCS installation by its unique ID. This endpoint returns the installation's details including its provider, organization, and configuration.

        Parameters
        ----------
        installation_id : str
            Installation Id
        Returns
        -------
        Installation
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/installations/{installationId}'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=Installation)

    def delete_installation(
        self,
        installation_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a VCS installation by its unique ID. This endpoint removes the installation and all its associated repositories from the project.

        Parameters
        ----------
        installation_id : str
            Installation Id
        Returns
        -------
        Dict[str, Any]
            API response as a dictionary

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/installations/{installationId}'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))

        response = self.client.call(
            'delete',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            api_params,
        )

        return response

    def list_namespaces(
        self,
        installation_id: str,
        search: Optional[str] = None,
        queries: Optional[List[str]] = None,
        total: Optional[bool] = None,
    ) -> VcsNamespaceList:
        """
        List provider namespaces available to a VCS installation. This can include the user personal namespace and any groups or organizations the installation can browse.

        Parameters
        ----------
        installation_id : str
            Installation Id
        search : Optional[str]
            Search term to filter your list results. Max length: 256 chars.
        queries : Optional[List[str]]
            Array of query strings generated using the Query class provided by the SDK. [Learn more about queries](https://appwrite.io/docs/queries). Only supported methods are limit and offset
        total : Optional[bool]
            When set to false, the total count returned will be 0 and will not be calculated.
        Returns
        -------
        VcsNamespaceList
            API response as a typed Pydantic model

        Raises
        ------
        AppwriteException
            If API request fails
        """

        api_path = '/vcs/installations/{installationId}/namespaces'
        api_params = {}
        if installation_id is None or installation_id == '':
            raise AppwriteException('Missing required parameter: "installation_id"')
        api_path = api_path.replace('{installationId}', self._encode_path(installation_id))
        if search is not None:
            api_params['search'] = self._normalize_value(search)
        if queries is not None:
            api_params['queries'] = self._normalize_value(queries)
        if total is not None:
            api_params['total'] = self._normalize_value(total)

        response = self.client.call(
            'get',
            api_path,
            {
                'X-Appwrite-Project': self.client.get_config('project'),
                'accept': 'application/json',
            },
            api_params,
        )

        return self._parse_response(response, model=VcsNamespaceList)
