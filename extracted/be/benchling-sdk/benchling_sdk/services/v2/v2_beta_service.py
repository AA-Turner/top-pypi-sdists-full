from __future__ import annotations

from functools import cached_property
from typing import Optional, TYPE_CHECKING

from benchling_api_client.v2.stable.client import Client

from benchling_sdk.helpers.client_helpers import v2_beta_client
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.v2.base_service import BaseService

if TYPE_CHECKING:
    from benchling_sdk.services.v2.beta.v2_beta_access_policy_service import V2BetaAccessPolicyService
    from benchling_sdk.services.v2.beta.v2_beta_analysis_service import V2BetaAnalysisService
    from benchling_sdk.services.v2.beta.v2_beta_app_definition_service import V2BetaAppDefinitionService
    from benchling_sdk.services.v2.beta.v2_beta_app_service import V2BetaAppService
    from benchling_sdk.services.v2.beta.v2_beta_collaboration_service import V2BetaCollaborationService
    from benchling_sdk.services.v2.beta.v2_beta_custom_notation_alias_service import (
        V2BetaCustomNotationAliasService,
    )
    from benchling_sdk.services.v2.beta.v2_beta_custom_notation_service import (
        V2BetaCustomNotationService,
    )
    from benchling_sdk.services.v2.beta.v2_beta_data_frame_service import V2BetaDataFrameService
    from benchling_sdk.services.v2.beta.v2_beta_dataset_service import V2BetaDatasetService
    from benchling_sdk.services.v2.beta.v2_beta_entry_service import V2BetaEntryService
    from benchling_sdk.services.v2.beta.v2_beta_file_service import V2BetaFileService
    from benchling_sdk.services.v2.beta.v2_beta_folder_service import V2BetaFolderService
    from benchling_sdk.services.v2.beta.v2_beta_project_service import V2BetaProjectService
    from benchling_sdk.services.v2.beta.v2_beta_worklist_service import V2BetaWorklistService
    from benchling_sdk.services.v2.beta.v2_beta_worksheet_service import V2BetaWorksheetService


class V2BetaService(BaseService):
    """
    V2-beta.

    Beta endpoints have different stability guidelines than other stable endpoints.

    See https://benchling.com/api/v2-beta/reference
    """

    _beta_client: Client

    def __init__(self, client: Client, retry_strategy: Optional[RetryStrategy] = None):
        """
        Initialize a v2-beta service.

        :param client: Underlying generated Client.
        :param retry_strategy: Retry strategy for failed HTTP calls
        """
        super().__init__(client, retry_strategy)
        self._beta_client = v2_beta_client(self.client)

    @cached_property
    def access_policies(self) -> V2BetaAccessPolicyService:
        """
        V2-Beta Access Policies.

        View access policies.

        https://benchling.com/api/v2-beta/reference#/Access%20Policies
        """
        from .beta.v2_beta_access_policy_service import V2BetaAccessPolicyService

        return self._create_service(V2BetaAccessPolicyService)

    @cached_property
    def analyses(self) -> V2BetaAnalysisService:
        """
        V2-Beta Analyses.

        Analyses allow experimental data to be viewed, analyzed, and visualized.

        https://benchling.com/api/v2-beta/reference#/Analyses
        """
        from .beta.v2_beta_analysis_service import V2BetaAnalysisService

        return self._create_service(V2BetaAnalysisService)

    @cached_property
    def apps(self) -> V2BetaAppService:
        """
        V2-Beta Apps.

        Create and manage Apps on your tenant.

        https://benchling.com/api/v2-beta/reference#/Apps
        """
        from .beta.v2_beta_app_service import V2BetaAppService

        return self._create_service(V2BetaAppService)

    @cached_property
    def app_definitions(self) -> V2BetaAppDefinitionService:
        """
        V2-Beta App Definitions.

        Create and manage Benchling app definitions on your tenant.

        https://benchling.com/api/v2-beta/reference#/App%20Definitions
        """
        from .beta.v2_beta_app_definition_service import V2BetaAppDefinitionService

        return self._create_service(V2BetaAppDefinitionService)

    @cached_property
    def collaborations(self) -> V2BetaCollaborationService:
        """
        V2-Beta Collaborations.

        Collaborations represent which user or group has which access policies.

        See https://benchling.com/api/v2-beta/reference?showLA=true#/Collaborations
        """
        from .beta.v2_beta_collaboration_service import V2BetaCollaborationService

        return self._create_service(V2BetaCollaborationService)

    @cached_property
    def custom_notation_aliases(self) -> V2BetaCustomNotationAliasService:
        """
        V2-Beta Custom Notation Aliases.

        A customer-defined alias for a chemical modification on a nucleotide sequence.

        https://benchling.com/api/v2-beta/reference#/Custom%20Notation%20Aliases
        """
        from .beta.v2_beta_custom_notation_alias_service import V2BetaCustomNotationAliasService

        return self._create_service(V2BetaCustomNotationAliasService)

    @cached_property
    def custom_notations(self) -> V2BetaCustomNotationService:
        """
        V2-Beta Custom Notations.

        A customer-defined notation to model chemically-modified nucleotide sequences.

        https://benchling.com/api/v2-beta/reference#/Custom%20Notations
        """
        from .beta.v2_beta_custom_notation_service import V2BetaCustomNotationService

        return self._create_service(V2BetaCustomNotationService)

    @cached_property
    def data_frames(self) -> V2BetaDataFrameService:
        """
        V2-Beta DataFrames.

        DataFrames are Benchling objects that represent tabular data with typed columns and rows of data.

        See https://benchling.com/api/v2-beta/reference#/Data%20Frames
        """
        from .beta.v2_beta_data_frame_service import V2BetaDataFrameService

        return self._create_service(V2BetaDataFrameService)

    @cached_property
    def datasets(self) -> V2BetaDatasetService:
        """
        Datasets.

        Datasets are Benchling objects that represent tabular data with typed columns and rows of data. Unlike
        Data Frames, Datasets are located in folders and can be searched in the UI.

        See https://benchling.com/api/v2-beta/reference#/Datasets
        """
        from .beta.v2_beta_dataset_service import V2BetaDatasetService

        return self._create_service(V2BetaDatasetService)

    @cached_property
    def entries(self) -> V2BetaEntryService:
        """
        V2-Beta Entries.

        Entries are rich text documents that allow you to capture all of your experimental data in one place.

        https://benchling.com/api/v2-beta/reference#/Entries
        """
        from .beta.v2_beta_entry_service import V2BetaEntryService

        return self._create_service(V2BetaEntryService)

    @cached_property
    def files(self) -> V2BetaFileService:
        """
        V2-Beta Files.

        Files are Benchling objects that represent files and their metadata. Compared to Blobs, which are used
        by most Benchling products for attachments, Files are primarily used in the Analysis and Connect
        product.

        See https://benchling.com/api/v2-beta/reference#/Files
        """
        from .beta.v2_beta_file_service import V2BetaFileService

        return self._create_service(V2BetaFileService)

    @cached_property
    def folders(self) -> V2BetaFolderService:
        """
        V2-Beta Folders.

        Folders are nested within projects to provide additional organization.

        https://benchling.com/api/v2-beta/reference?showLA=true#/Folders
        """
        from .beta.v2_beta_folder_service import V2BetaFolderService

        return self._create_service(V2BetaFolderService)

    @cached_property
    def projects(self) -> V2BetaProjectService:
        """
        V2-Beta Projects.

        Manage project objects.

        See https://benchling.com/api/v2-beta/reference?#/Projects
        """
        from .beta.v2_beta_project_service import V2BetaProjectService

        return self._create_service(V2BetaProjectService)

    @cached_property
    def worklists(self) -> V2BetaWorklistService:
        """
        V2-Beta Worklists.

        Worklists are a convenient way to organize items for bulk actions, and are complementary to folders and
        projects.

        See https://benchling.com/api/v2-beta/reference#/Worklists
        """
        from .beta.v2_beta_worklist_service import V2BetaWorklistService

        return self._create_service(V2BetaWorklistService)

    @cached_property
    def worksheets(self) -> V2BetaWorksheetService:
        """
        V2-Beta Worksheets.

        Worksheets are structured documents that help you plan and describe your experiment operations in a
        consistent way.

        See also https://benchling.com/api/v2-beta/reference#/Worksheets
        """
        from .beta.v2_beta_worksheet_service import V2BetaWorksheetService

        return self._create_service(V2BetaWorksheetService)

    def _create_service(self, cls):
        """Instantiate a service using the beta client."""
        return cls(self._beta_client, self._retry_strategy)
