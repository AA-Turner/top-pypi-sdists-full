# mypy: disable-error-code="override"

from typing import Optional, Union
import os
from pathlib import Path
from typing_extensions import override

from istari_digital_client.legacy.configuration import Configuration
from istari_digital_client.legacy.key_management import KeyManagementMixin
from istari_digital_client.legacy.api_client import ApiClient
from istari_digital_client.sdk._auth_deprecation import AuthDeprecationResult
from istari_digital_client.legacy.storage.api.storage_api import StorageApi
from istari_digital_client.legacy.v2.models.token import Token
from istari_digital_client.legacy.v3.api.v3_api import V3Api
from istari_digital_client.legacy.v3.models.comment_dto import CommentDto
from istari_digital_client.legacy.v3.models.new_comment_create_dto import NewCommentCreateDto
from istari_digital_client.legacy.v3.models.resource_dto import ResourceDto
from istari_digital_client.legacy.v3.models.resource_type_dto import ResourceTypeDto
from istari_digital_client.legacy.v3.models.resource_create_dto import ResourceCreateDto
from istari_digital_client.legacy.v3.models.token_create_dto import TokenCreateDto
from istari_digital_client.legacy.v3.models.token_dto import TokenDto
from istari_digital_client.legacy.v3.models.resource_revision_create_dto import ResourceRevisionCreateDto
from istari_digital_client.legacy.v3.models.resource_revision_dto import ResourceRevisionDto
from istari_digital_client.legacy.v3.models.update_comment_dto import UpdateCommentDto
from istari_digital_client.legacy.v3.models.upstream_info_create_dto import UpstreamInfoCreateDto
from istari_digital_client.legacy.v3.models.upstream_revision_info_create_dto import UpstreamRevisionInfoCreateDto
from istari_digital_client.legacy.v3.models.workflow_output_create_dto import WorkflowOutputCreateDto
from istari_digital_client.legacy.v3.models.workflow_output_dto import WorkflowOutputDto


PathLike = Union[str, os.PathLike, Path]


def _token_dto_to_token(token_dto: TokenDto) -> Token:
    """Convert TokenDto to v2 Token for StorageApi."""
    return Token(
        id=token_dto.id,
        sha=token_dto.sha,
        salt=token_dto.salt,
        created=token_dto.created,
    )

class V3Client(KeyManagementMixin, V3Api):
    def __init__(self, config: Configuration) -> None:
        self._api_client = ApiClient(config, spec_ids=(V3Api._SPEC_ID, StorageApi._SPEC_ID))
        self._storage_api = StorageApi(config=config, api_client=self._api_client)
        super().__init__(config=config, api_client=self._api_client)

    @property
    def _identity_service_config(self) -> Configuration:
        return self.config

    @property
    def auth_deprecation(self) -> Optional[AuthDeprecationResult]:
        """Return the latest auth-deprecation advisory from the server, or None.

        Set when authenticating with a legacy personal access token against an
        Identity-Service-enabled registry. Migrate via `client.keys.exchange_pat()`.
        """
        return self._api_client.auth_deprecation_checker.last_result


    @override
    def create_resource(
        self,
        path: PathLike,
        resource_type: ResourceTypeDto,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        upstream_remote_info: UpstreamInfoCreateDto | None = None,
    ) -> ResourceDto:
        file_revision = self._storage_api.create_revision(
            file_path=path,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return super().create_resource(
            resource_create_dto=ResourceCreateDto(
                name=file_revision.name, # type: ignore[arg-type]
                extension=file_revision.extension,
                size=file_revision.size,
                mime=file_revision.mime,
                description=file_revision.description,
                version_name=file_revision.version_name,
                external_identifier=file_revision.external_identifier,
                display_name=file_revision.display_name,
                content_token=TokenCreateDto(
                    sha=file_revision.content_token.sha,
                    salt=file_revision.content_token.salt,
                ),
                properties_token=TokenCreateDto(
                    sha=file_revision.properties_token.sha,
                    salt=file_revision.properties_token.salt,
                ),
                resource_type=resource_type,
                upstream_remote_info=upstream_remote_info,
            )
        )

    @override
    def create_resource_revision(
        self,
        resource_id: str,
        path: PathLike,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        upstream_revision_info: UpstreamRevisionInfoCreateDto | None = None,
    ) -> ResourceRevisionDto:
        file_revision = self._storage_api.create_revision(
            file_path=path,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )

        return super().create_resource_revision(
            resource_id=resource_id,
            resource_revision_create_dto=ResourceRevisionCreateDto(
                name=file_revision.name, # type: ignore[arg-type]
                extension=file_revision.extension,
                size=file_revision.size,
                mime=file_revision.mime,
                description=file_revision.description,
                version_name=file_revision.version_name,
                external_identifier=file_revision.external_identifier,
                display_name=file_revision.display_name,
                content_token=TokenCreateDto(
                    sha=file_revision.content_token.sha,
                    salt=file_revision.content_token.salt,
                ),
                properties_token=TokenCreateDto(
                    sha=file_revision.properties_token.sha,
                    salt=file_revision.properties_token.salt,
                ),
                upstream_revision_info=upstream_revision_info,
            )
        )


    @override
    def create_comment(
        self,
        resource_id: str,
        path: PathLike,
        parent_comment_id: str | None = None,
    ) -> CommentDto:
        file_revision = self._storage_api.create_revision(
            file_path=path,
        )
        return super().create_comment(
            resource_id=resource_id,
            new_comment_create_dto=NewCommentCreateDto(
                content_token=TokenCreateDto(
                    sha=file_revision.content_token.sha,
                    salt=file_revision.content_token.salt,
                ),
                properties_token=TokenCreateDto(
                    sha=file_revision.properties_token.sha,
                    salt=file_revision.properties_token.salt,
                ),
                parent_comment_id=parent_comment_id,
            ),
        )

    @override
    def update_comment(
        self,
        resource_id: str,
        comment_id: str,
        path: PathLike,
    ) -> CommentDto:
        file_revision = self._storage_api.create_revision(
            file_path=path,
        )
        return super().update_comment(
            resource_id=resource_id,
            comment_id=comment_id,
            update_comment_dto=UpdateCommentDto(
                content_token=TokenCreateDto(
                    sha=file_revision.content_token.sha,
                    salt=file_revision.content_token.salt,
                ),
                properties_token=TokenCreateDto(
                    sha=file_revision.properties_token.sha,
                    salt=file_revision.properties_token.salt,
                ),
            ),
        )

    @override
    def create_workflow_output(
        self,
        system_id: str,
        path: PathLike,
        *,
        description: str | None = None,
        display_name: str | None = None,
        external_identifier: str | None = None,
    ) -> WorkflowOutputDto:
        file_revision = self._storage_api.create_revision(
            file_path=path,
            display_name=display_name,
            description=description,
            external_identifier=external_identifier,
        )

        return super().create_workflow_output(
            system_id=system_id,
            workflow_output_create_dto=WorkflowOutputCreateDto(
                name=file_revision.name,  # type: ignore[arg-type]
                extension=file_revision.extension,
                size=file_revision.size,
                mime=file_revision.mime,
                description=file_revision.description,
                display_name=file_revision.display_name,
                external_identifier=file_revision.external_identifier,
                content_token=TokenCreateDto(
                    sha=file_revision.content_token.sha,
                    salt=file_revision.content_token.salt,
                ),
                properties_token=TokenCreateDto(
                    sha=file_revision.properties_token.sha,
                    salt=file_revision.properties_token.salt,
                ),
            ),
        )

    def get_content(
        self,
        resource: ResourceDto | ResourceRevisionDto | CommentDto,
    ) -> bytes:
        """
        Fetch and return the raw content bytes for a resource, resource revision, or comment.

        :param resource: A ResourceDto, ResourceRevisionDto, or CommentDto instance with a content_token.
        :return: Raw file content as bytes.
        :raises ValueError: If the resource has no content_token (e.g. ResourceRevisionDto with None).
        """
        content_token = getattr(resource, "content_token", None)
        if content_token is None:
            raise ValueError(
                f"`content_token` is not set for instance of {type(resource).__name__}"
            )
        return self._storage_api.read_contents(token=_token_dto_to_token(content_token))
