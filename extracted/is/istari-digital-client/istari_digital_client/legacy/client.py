from __future__ import annotations

import os
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Iterable, Union
from uuid import UUID

from pydantic import StrictStr

from istari_digital_client.legacy.v2.models.auth_integration import AuthIntegration
from istari_digital_client.legacy.v2.models.auth_integration_update import (
    AuthIntegrationUpdate,
)
from istari_digital_client.legacy.v2.models.auth_integration_type import (
    AuthIntegrationType,
)
from istari_digital_client.legacy.v2.models.new_auth_integration import NewAuthIntegration
from istari_digital_client.legacy.v2.api.v2_api import V2Api
from istari_digital_client.legacy.storage.api.storage_api import StorageApi
from istari_digital_client.legacy.api_client import ApiClient
from istari_digital_client.sdk._auth_deprecation import AuthDeprecationResult
from istari_digital_client.legacy.configuration import Configuration
from istari_digital_client.legacy.configuration import ConfigurationError
from istari_digital_client.legacy.key_management import KeyManagementMixin
from istari_digital_client.legacy.v2.models.artifact import Artifact
from istari_digital_client.legacy.v2.models.comment import Comment
from istari_digital_client.legacy.v2.models.control_tag import ControlTag
from istari_digital_client.legacy.v2.models.control_tagging_object_type import (
    ControlTaggingObjectType,
)
from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.v2.models.function_auth_secret import FunctionAuthSecret
from istari_digital_client.legacy.v2.models.function_auth_type import FunctionAuthType
from istari_digital_client.legacy.v2.models.job import Job
from istari_digital_client.legacy.v2.models.model import Model
from istari_digital_client.legacy.v2.models.new_function_auth_secret import (
    NewFunctionAuthSecret,
)
from istari_digital_client.legacy.v2.models.new_source import NewSource
from istari_digital_client.legacy.v2.models.patch_op import PatchOp
from istari_digital_client.legacy.v2.models.resource_control_tagging import (
    ResourceControlTagging,
)
from istari_digital_client.legacy.v2.models.user import User
from istari_digital_client.legacy.v2.models.user_control_tagging import UserControlTagging
from istari_digital_client.legacy.v2.models.token import Token
from istari_digital_client.legacy.log_utils import log_method

from istari_digital_client.legacy.v2.models.new_system import NewSystem

from istari_digital_client.legacy.v2.models.system import System
from istari_digital_client.legacy.v2.models.revision_bulk_create_item import RevisionBulkCreateItem

PathLike = Union[str, os.PathLike, Path]

logger = logging.getLogger("istari-digital-client.client")


class Client(KeyManagementMixin, V2Api):
    """Create a new instance of the Istari client

    Args:
        config (Configuration | None): The configuration for the client
    """

    def __init__(
        self,
        config: Configuration | None = None,
    ) -> None:
        config = config or Configuration()

        if not config.registry_url and not config._registry_base_url():
            logger.error("The registry URL is not set")

            raise ConfigurationError(
                "Registry URL is not set! Set the registry directly via the ISTARI_REGISTRY_URL env variable (or the "
                "registry_url config attribute), or route it through the service-router gateway via the "
                "ISTARI_DIGITAL_API_URL env variable (or the digital_api_url config attribute)."
            )
        if not config.registry_auth_token and not config.identity_service_enabled:
            logger.error("The registry auth token is not set")

            raise ConfigurationError(
                "Registry auth token is not set! It must be specified either via an ISTARI_REGISTRY_AUTH_TOKEN env "
                "variable or by explicitly setting the registry_auth_token attribute in the (optional) config object "
                "on client initialization."
            )

        self.configuration: Configuration = config

        self._api_client = ApiClient(config, spec_ids=(V2Api._SPEC_ID, StorageApi._SPEC_ID))

        super().__init__(self.configuration, self._api_client)

    @property
    def _identity_service_config(self) -> Configuration:
        return self.configuration

    @property
    def last_compatibility_result(self):
        """Return the latest compatibility check result from the server, or None."""
        return self._api_client.compatibility_checker.last_result

    @property
    def auth_deprecation(self) -> Optional[AuthDeprecationResult]:
        """Return the latest auth-deprecation advisory from the server, or None.

        Set when authenticating with a legacy personal access token against an
        Identity-Service-enabled registry. Migrate via `client.keys.exchange_pat()`.
        """
        return self._api_client.auth_deprecation_checker.last_result

    def check_compatibility(self):
        """Check compatibility with the server by calling the readiness endpoint.

        :return: A CompatibilityResult with the server's version and compatibility
            status, or None if the server didn't return compatibility headers.
        """
        self.readiness_check()
        return self.last_compatibility_result

    def check_auth_deprecation(self) -> Optional[AuthDeprecationResult]:
        """Check for an auth-deprecation advisory from the server.

        Makes a lightweight *authenticated* request so the server can attach its
        auth-deprecation header.

        :return: An AuthDeprecationResult when authenticating with a legacy personal
            access token against an Identity-Service-enabled registry, or None if the
            server didn't return the auth-deprecation header.
        """
        self.get_current_user()
        return self.auth_deprecation

    @log_method
    def __del__(self):
        # __init__ may raise before configuration is set (e.g. a config guard);
        # such a partially-constructed instance has no cache to clean up.
        if getattr(self, "configuration", None) is None:
            return
        if (
            self.configuration.filesystem_cache_enabled
            and self.configuration.filesystem_cache_clean_on_exit
            and self.configuration.filesystem_cache_root.exists()
            and self.configuration.filesystem_cache_root.is_dir()
        ):
            logger.debug("Cleaning up cache contents for client exit")
            for child in self.configuration.filesystem_cache_root.iterdir():
                if child.is_dir():
                    logger.debug("deleting cache directory - %s", child)
                    shutil.rmtree(
                        self.configuration.filesystem_cache_root, ignore_errors=True
                    )
                elif child.is_file() and not child.is_symlink():
                    logger.debug("deleting cache file - %s", child)
                    child.unlink(missing_ok=True)
                else:
                    logger.debug(
                        "not deleting cache item (is neither a directory nor a regular file) -  %s",
                        child,
                    )

    @log_method
    def add_artifact(
        self,
        model_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        source_job_id: str | None = None,
    ) -> Artifact:
        """
        Add a new artifact to a model.

        This method creates a new artifact by uploading a file located at the given path and
        associating it with the specified model. Optionally, you can include metadata such as
        version name, description, external identifier, and source references.

        :param model_id: Unique identifier of the model to which the artifact will be added.
        :type model_id: str
        :param path: Filesystem path to the artifact file to upload.
        :type path: PathLike
        :param sources: Optional list of sources associated with the artifact. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional text describing the artifact's contents or purpose.
        :type description: str | None
        :param version_name: Optional user-defined version label for the artifact.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for cross-referencing.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the artifact.
        :type display_name: str | None
        """
        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._create_artifact(
            model_id=model_id,
            file_revision=file_revision,
            source_job_id=source_job_id,
        )

    @log_method
    def add_artifacts_bulk(
        self,
        model_id: str,
        revision_create_dtos: list[RevisionBulkCreateItem]
    ) -> list[Artifact]:
        """
        THIS METHOD IS DEPRECATED AND UNSTABLE: use add_artifact instead

        Add multiple artifacts to a model in a single bulk operation.

        This method creates multiple artifacts by uploading files specified in the revision
        items and associating them with the specified model. This is more efficient than
        calling `add_artifact` multiple times when uploading several small files.

        Note: This method is limited to 10 items per call and does not support files
        larger than the multipart upload threshold.

        :param model_id: Unique identifier of the model to which the artifacts will be added.
        :type model_id: str
        :param revision_create_dtos: List of revision creation items, each specifying a file path
                                     and optional metadata (sources, description, version_name,
                                     external_identifier, display_name).
        :type revision_create_dtos: list[RevisionBulkCreateItem]
        :return: List of created artifact objects
        :rtype: list[Artifact]
        :raises ValueError: If more than 10 items are provided or if any file exceeds the
                           multipart upload threshold.
        """
        logger.warning("Using deprecated and unstable add_artifacts_bulk method. Use add_artifacts instead.")

        chunk_size = 10

        if len(revision_create_dtos) > chunk_size:
            msg = "Passed list of revisions to bulk artifact endpoint with size >10"
            raise ValueError(msg)

        revisions = self.create_revisions_bulk(
            revision_create_dtos
        )

        return self._create_artifacts_bulk(
            model_id,
            revisions
        )

    @log_method
    def update_artifact(
        self,
        artifact_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        source_job_id: str | None = None,
    ) -> Artifact:
        """
        Update an existing artifact with a new file and optional metadata.

        This method replaces the contents of an existing artifact by uploading a new file
        and optionally modifying associated metadata such as sources, version, or identifiers.

        :param artifact_id: Unique identifier of the artifact to update.
        :type artifact_id: str
        :param path: Filesystem path to the new artifact file.
        :type path: PathLike
        :param sources: Optional list of sources associated with the artifact. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional text describing the updated artifact.
        :type description: str | None
        :param version_name: Optional user-defined version label for the updated artifact.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for cross-referencing.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the updated artifact.
        :type display_name: str | None
        """

        salt = self.get_artifact(artifact_id=artifact_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_artifact(
            artifact_id=artifact_id,
            file_revision=file_revision,
            source_job_id=source_job_id,
        )

    @log_method
    def add_comment(
        self,
        resource_id: str,
        path: PathLike,
        description: str | None = None,
    ) -> Comment:
        """
        Add a new comment to a resource.

        This method uploads a file as a comment and associates it with the specified resource.
        An optional description can be provided to summarize or contextualize the comment content.

        :param resource_id: Unique identifier of the resource to which the comment will be added.
        :type resource_id: str
        :param path: Filesystem path to the comment file to upload.
        :type path: PathLike
        :param description: Optional text describing the comment or its relevance.
        :type description: str | None
        """

        file_revision = self.create_revision(
            file_path=path,
            sources=None,
            display_name=None,
            description=description,
            version_name=None,
            external_identifier=None,
        )

        return self._create_comment(
            resource_id=resource_id,
            file_revision=file_revision,
        )

    @log_method
    def update_comment(
        self,
        comment_id: str,
        path: PathLike,
        description: str | None = None,
    ) -> Comment:
        """
        Update an existing comment with a new file and optional description.

        This method replaces the contents of an existing comment by uploading a new file.
        An optional description can be provided to revise or clarify the comment’s purpose.

        :param comment_id: Unique identifier of the comment to update.
        :type comment_id: str
        :param path: Filesystem path to the new comment file.
        :type path: PathLike
        :param description: Optional updated description of the comment.
        :type description: str | None
        """

        salt = self.get_comment(comment_id=comment_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=None,
            display_name=None,
            description=description,
            version_name=None,
            external_identifier=None,
        )

        return self._update_comment(
            comment_id=comment_id,
            file_revision=file_revision,
        )

    @log_method
    def add_file(
        self,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> File:
        """
        Add a new file to the system.

        This method uploads a file from the specified path and optionally attaches metadata such as
        description, version name, external identifier, and associated sources.

        :param path: Filesystem path to the file to upload.
        :type path: PathLike
        :param sources: Optional list of sources related to the file. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional text describing the file's contents or purpose.
        :type description: str | None
        :param version_name: Optional user-defined version label for the file.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for the file.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the file.
        :type display_name: str | None
        """

        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._create_file(
            file_revision=file_revision,
        )

    @log_method
    def update_file(
        self,
        file_id: str,
        path: PathLike | str,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> File:
        """
        Update an existing file with a new version and optional metadata.

        This method replaces the contents of a file by uploading a new version from the specified path.
        You can also update metadata such as sources, description, version name, or external identifier.

        :param file_id: Unique identifier of the file to update.
        :type file_id: str
        :param path: Filesystem path or string path to the new file contents.
        :type path: PathLike | str
        :param sources: Optional list of sources related to the file. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional updated description of the file.
        :type description: str | None
        :param version_name: Optional user-defined version label for the updated file.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for the file.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the file.
        :type display_name: str | None
        """

        salt = self.get_file(file_id=file_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_file(
            file_id=file_id,
            file_revision=file_revision,
        )

    @log_method
    def update_file_properties(
        self,
        file: File,
        display_name: str | None = None,
        description: str | None = None,
        external_identifier: str | None = None,
        version_name: str | None = None,
    ) -> File:
        """
        Update metadata properties of an existing file.

        This method updates non-content attributes of a file, such as display name, description,
        version name, or external identifier, without modifying the file's contents.

        :param file: The file object whose metadata will be updated.
        :type file: File
        :param display_name: Optional human-readable name to assign to the file.
        :type display_name: str | None
        :param description: Optional text describing the file.
        :type description: str | None
        :param external_identifier: Optional external system identifier for cross-referencing the file.
        :type external_identifier: str | None
        :param version_name: Optional user-defined version label for the file.
        :type version_name: str | None
        """

        token_with_properties = self.update_revision_properties(
            file_revision=file.revision,
            display_name=display_name,
            description=description,
            external_identifier=external_identifier,
            version_name=version_name,
        )

        return self._update_file_properties(
            file_id=file.id,
            token_with_properties=token_with_properties,
        )

    @log_method
    def update_job(
        self,
        job_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Job:
        """
        Update an existing job with a new file and optional metadata.

        This method replaces the contents of a job by uploading a new file and allows updating
        associated metadata such as description, version name, external identifier, and sources.

        :param job_id: Unique identifier of the job to update.
        :type job_id: str
        :param path: Filesystem path to the new job file.
        :type path: PathLike
        :param sources: Optional list of sources associated with the job. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional updated description of the job.
        :type description: str | None
        :param version_name: Optional user-defined version label for the job.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for the job.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the job.
        :type display_name: str | None
        """

        salt = self.get_job(job_id=job_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_job(
            job_id=job_id,
            file_revision=file_revision,
        )

    @log_method
    def add_model(
        self,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        source_job_id: str | None = None,
    ) -> Model:
        """
        Add a new model to the system.

        This method uploads a model file from the specified path and optionally attaches metadata,
        including description, version name, external identifier, display name, and sources.

        :param path: Filesystem path to the model file to upload.
        :type path: PathLike
        :param sources: Optional list of sources associated with the model. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional text describing the model's purpose or contents.
        :type description: str | None
        :param version_name: Optional user-defined version label for the model.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for the model.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the model.
        :type display_name: str | None
        """

        file_revision = self.create_revision(
            file_path=path,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )
        return self._create_model(
            file_revision=file_revision,
            source_job_id=source_job_id,
        )

    @log_method
    def update_model(
        self,
        model_id: str,
        path: PathLike,
        sources: list[NewSource | str] | None = None,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        source_job_id: str | None = None,
    ) -> Model:
        """
        Update an existing model with a new file and optional metadata.

        This method replaces the contents of a model by uploading a new file from the specified path.
        You can also update metadata such as description, version name, external identifier, and sources.

        :param model_id: Unique identifier of the model to update.
        :type model_id: str
        :param path: Filesystem path to the new model file.
        :type path: PathLike
        :param sources: Optional list of sources associated with the model. Each item may be a
                        NewSource instance or a string source name.
        :type sources: list[NewSource | str] | None
        :param description: Optional updated description of the model.
        :type description: str | None
        :param version_name: Optional user-defined version label for the model.
        :type version_name: str | None
        :param external_identifier: Optional external system identifier for the model.
        :type external_identifier: str | None
        :param display_name: Optional human-readable name for the model.
        :type display_name: str | None
        """

        salt = self.get_model(model_id=model_id).revision.content_token.salt

        file_revision = self.update_revision_content(
            file_path=path,
            salt=salt,
            sources=sources,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return self._update_model(
            model_id=model_id,
            file_revision=file_revision,
            source_job_id=source_job_id,
        )

    @log_method
    def add_function_auth_secret(
        self,
        function_auth_type: FunctionAuthType,
        path: PathLike,
        auth_integration_id: Optional[str] = None,
        expiration: Optional[datetime] = None,
    ) -> FunctionAuthSecret:
        """
        Create a new function authentication secret from a file.

        This method uploads a secret from a file and registers it as a function auth secret
        of the specified type. You may optionally associate it with an authentication
        integration and set an expiration date.

        :param function_auth_type: The type of function authentication (e.g., API key, OAuth).
        :type function_auth_type: FunctionAuthType
        :param path: Filesystem path to the file containing the secret.
        :type path: PathLike
        :param auth_integration_id: Optional identifier of the associated authentication integration.
        :type auth_integration_id: Optional[str]
        :param expiration: Optional expiration date/time of the secret.
        :type expiration: Optional[datetime]
        """

        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        file_revision = self.create_secret_revision(
            file_path=path,
        )

        # Generate content token for the secret
        # This is a different process than the file revision
        # because the secret is encrypted and we need to
        # generate a token for the plain secret content
        with open(path, "rb") as f:
            secret_content = f.read()
            token: Token = Token.from_bytes(secret_content)

        secret = NewFunctionAuthSecret(
            auth_integration_id=auth_integration_id,
            revision=file_revision,
            function_auth_type=function_auth_type,
            expiration=expiration,
            sha=token.sha,
            salt=token.salt,
        )

        return self._create_function_auth_secret(secret)

    def create_auth_integration(
        self,
        auth_integration_type: AuthIntegrationType,
        auth_type: FunctionAuthType,
        auth_registration_path: PathLike,
    ) -> AuthIntegration:
        path = Path(auth_registration_path)
        if not path.exists():
            raise FileNotFoundError(auth_registration_path)
        registration_revision = self.create_revision(file_path=path)
        new_auth_integration = NewAuthIntegration(
            auth_integration_type=auth_integration_type,
            auth_type=auth_type,
            revision=registration_revision,
        )
        return self._create_auth_integration(new_auth_integration)

    def update_auth_integration(
        self,
        auth_integration_id: UUID,
        auth_integration_type: AuthIntegrationType | None = None,
        function_auth_type: FunctionAuthType | None = None,
        auth_registration_path: PathLike | None = None,
    ):
        def make_revision():
            path = Path(auth_registration_path)
            if not path.exists():
                raise FileNotFoundError(path)
            auth_int: AuthIntegration = self.get_auth_integration(
                auth_integration_id=str(auth_integration_id)
            )
            salt = auth_int.file.revision.content_token.salt
            return self.update_revision_content(file_path=path, salt=salt)

        registration_revision = make_revision() if auth_registration_path else None

        update = AuthIntegrationUpdate(
            auth_integration_type=auth_integration_type,
            auth_type=function_auth_type,
            revision=registration_revision,
        )
        return self._update_auth_integration(auth_integration_id, update) # type: ignore[arg-type]

    @log_method
    def add_user_control_taggings(
        self,
        user_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[UserControlTagging]:
        """
        Assign one or more control tags to a user.

        When a control tag is applied to a user, the access is propagated to related resources
        (e.g., models and their child artifacts). The returned list of resource control taggings
        may exceed the number of control tags assigned due to this propagation.

        The calling user must be a customer admin of the tenant the target user belongs to;
        otherwise, the operation will fail with a permission denied error.

        :param user_id: Unique identifier of the user to whom control tag access will be assigned.
        :type user_id: str
        :param control_tag_ids: Identifiers of the control tags to assign.
        :type control_tag_ids: Iterable[str]
        :param reason: Optional reason for assigning the control tags.
        :type reason: Optional[str]
        """

        return self.patch_user_control_taggings(
            user_id, list(control_tag_ids), patch_op=PatchOp.SET, reason=reason
        )

    @log_method
    def remove_user_control_taggings(
        self,
        user_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[UserControlTagging]:
        """
        Remove (archive) one or more control tag access assignments from a user.

        This method revokes a user's access to the specified control tags. The calling user
        must be a customer admin on the tenant the target user belongs to; otherwise, the
        operation will fail with a permission denied error.

        :param user_id: Unique identifier of the user whose control tag access will be removed.
        :type user_id: str
        :param control_tag_ids: Identifiers of the control tags to revoke access from.
        :type control_tag_ids: Iterable[str]
        :param reason: Optional reason for removing the control tag access.
        :type reason: Optional[str]
        """

        return self.patch_user_control_taggings(
            user_id, list(control_tag_ids), patch_op=PatchOp.DELETE, reason=reason
        )

    @log_method
    def add_model_control_taggings(
        self,
        model_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """
        Assign one or more control tags to a model.

        When a control tag is applied to a model, the tagging is also applied to each of its
        child artifacts. As a result, the returned list of resource control taggings may include
        more entries than the number of control tags assigned.

        The caller must have owner or administrator access to the model in order to modify
        control tag assignments.

        :param model_id: Unique identifier of the model to which control tags will be assigned.
        :type model_id: str
        :param control_tag_ids: Identifiers of the control tags to assign.
        :type control_tag_ids: Iterable[str]
        :param reason: Optional reason for assigning the control tags.
        :type reason: Optional[str]
        """

        return self.patch_model_control_taggings(
            model_id, list(control_tag_ids), patch_op=PatchOp.SET, reason=reason
        )

    @log_method
    def remove_model_control_taggings(
        self,
        model_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """
        Remove (archive) one or more control tag assignments from a model.

        This method revokes control tag access from the specified model. Owner or administrator
        access to the model or its parent model is required to modify control tag assignments.

        :param model_id: Unique identifier of the model from which control tags will be removed.
        :type model_id: str
        :param control_tag_ids: Identifiers of the control tags to remove.
        :type control_tag_ids: Iterable[str]
        :param reason: Optional reason for removing the control tag assignments.
        :type reason: Optional[str]
        """

        return self.patch_model_control_taggings(
            model_id, list(control_tag_ids), patch_op=PatchOp.DELETE, reason=reason
        )

    @log_method
    def add_artifact_control_taggings(
        self,
        artifact_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """
        Assign one or more control tags to an artifact.

        This method applies control tags to the specified artifact. Owner or administrator
        access to the artifact’s parent model is required to modify control tag assignments.

        :param artifact_id: Unique identifier of the artifact to which control tags will be assigned.
        :type artifact_id: str
        :param control_tag_ids: Identifiers of the control tags to assign.
        :type control_tag_ids: Iterable[str]
        :param reason: Optional reason for assigning the control tags.
        :type reason: Optional[str]
        """

        return self.patch_artifact_control_taggings(
            artifact_id, list(control_tag_ids), patch_op=PatchOp.SET, reason=reason
        )

    @log_method
    def remove_artifact_control_taggings(
        self,
        artifact_id: StrictStr,
        control_tag_ids: Iterable[StrictStr],
        reason: Optional[StrictStr] = None,
    ) -> list[ResourceControlTagging]:
        """
        Remove (archive) one or more control tag assignments from an artifact.

        This method revokes control tag access from the specified artifact. Owner or administrator
        access to the artifact’s parent model is required to modify control tag assignments.

        :param artifact_id: Unique identifier of the artifact from which control tags will be removed.
        :type artifact_id: str
        :param control_tag_ids: Identifiers of the control tags to remove.
        :type control_tag_ids: Iterable[str]
        :param reason: Optional reason for removing the control tag assignments.
        :type reason: Optional[str]
        """

        return self.patch_artifact_control_taggings(
            artifact_id, list(control_tag_ids), patch_op=PatchOp.DELETE, reason=reason
        )

    @log_method
    def get_model_control_tags(self, model_id: StrictStr) -> list[ControlTag]:
        """
        Retrieve the list of control tags currently assigned to a model.

        This method returns all active control tags associated with the specified model.

        :param model_id: Unique identifier of the model to retrieve control tags for.
        :type model_id: str
        """

        return self.get_object_control_tags(ControlTaggingObjectType.MODEL, model_id)

    @log_method
    def get_artifact_control_tags(self, artifact_id: StrictStr) -> list[ControlTag]:
        """
        Retrieve the list of control tags currently assigned to an artifact.

        This method returns all active control tags associated with the specified artifact.

        :param artifact_id: Unique identifier of the artifact to retrieve control tags for.
        :type artifact_id: str
        """

        return self.get_object_control_tags(
            ControlTaggingObjectType.ARTIFACT, artifact_id
        )

    @log_method
    def get_user_control_tags(self, user_id: StrictStr) -> list[ControlTag]:
        """
        Retrieve the list of control tags a user has been assigned access to.

        This method returns all active control tags associated with the specified user.

        :param user_id: Unique identifier of the user to retrieve control tags for.
        :type user_id: str
        """

        return self.get_object_control_tags(ControlTaggingObjectType.USER, user_id)

    @log_method
    def get_user(self, user_id: StrictStr) -> User:
        """
        Retrieve a user from the registry.

        This is a convenience wrapper around `get_user_by_id`, provided for naming consistency
        with other `get_*` methods (e.g., `get_model`, `get_artifact`, etc.).

        :param user_id: Unique identifier of the user to retrieve.
        :type user_id: str
        """

        return self.get_user_by_id(user_id)
