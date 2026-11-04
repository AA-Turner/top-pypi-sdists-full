# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Stainless-named aliases over the generated pydantic models.

``@hey-api/openapi-python`` derives model names from the HTTP method and path
(``PostV31ToolRouterSessionResponse``), which are stable against the pinned
spec snapshot but not ergonomic. These aliases are the Stainless-shaped names
the resource methods use, and they are derived from the same operation plan
the resource classes are.

Types are *relaxed* relative to Stainless: these are hey-api pydantic models,
not Stainless-identical TypedDicts. ``*Body`` / ``*Query`` are the request
models, ``*Response`` the parsed response models. Some list responses are
pydantic ``RootModel`` — reach their payload through ``.root`` (MIGRATION.md).
"""

from __future__ import annotations

from ._generated import pydantic_gen as _g

# ---- tool_router.session responses (13) ----
SessionCreateResponse = _g.PostV31ToolRouterSessionResponse
SessionRetrieveResponse = _g.GetV31ToolRouterSessionBySessionIdResponse
SessionDeleteResponse = _g.DeleteV31ToolRouterSessionBySessionIdResponse
SessionAttachResponse = _g.PostV31ToolRouterSessionBySessionIdAttachResponse
SessionConfigHistoryResponse = _g.GetV31ToolRouterSessionBySessionIdConfigHistoryResponse
SessionExecuteResponse = _g.PostV31ToolRouterSessionBySessionIdExecuteResponse
SessionExecuteMetaResponse = _g.PostV31ToolRouterSessionBySessionIdExecuteMetaResponse
SessionLinkResponse = _g.PostV31ToolRouterSessionBySessionIdLinkResponse
SessionPatchResponse = _g.PatchV31ToolRouterSessionBySessionIdResponse
SessionProxyExecuteResponse = _g.PostV31ToolRouterSessionBySessionIdProxyExecuteResponse
SessionSearchResponse = _g.PostV31ToolRouterSessionBySessionIdSearchResponse
SessionToolkitsResponse = _g.GetV31ToolRouterSessionBySessionIdToolkitsResponse
SessionToolsResponse = _g.GetV31ToolRouterSessionBySessionIdToolsResponse

# ---- tool_router.session request models (11) ----
SessionCreateBody = _g.PostV31ToolRouterSessionBody
SessionAttachBody = _g.PostV31ToolRouterSessionBySessionIdAttachBody
SessionConfigHistoryQuery = _g.GetV31ToolRouterSessionBySessionIdConfigHistoryQuery
SessionExecuteBody = _g.PostV31ToolRouterSessionBySessionIdExecuteBody
SessionExecuteMetaBody = _g.PostV31ToolRouterSessionBySessionIdExecuteMetaBody
SessionLinkBody = _g.PostV31ToolRouterSessionBySessionIdLinkBody
SessionPatchBody = _g.PatchV31ToolRouterSessionBySessionIdBody
SessionProxyExecuteBody = _g.PostV31ToolRouterSessionBySessionIdProxyExecuteBody
SessionSearchBody = _g.PostV31ToolRouterSessionBySessionIdSearchBody
SessionToolkitsQuery = _g.GetV31ToolRouterSessionBySessionIdToolkitsQuery
SessionToolsQuery = _g.GetV31ToolRouterSessionBySessionIdToolsQuery

# ---- tool_router.session.files responses (4) ----
ToolRouterSessionFileListResponse = _g.GetV31ToolRouterSessionBySessionIdMountsByMountIdItemsResponse
FileDeleteResponse = _g.PostV31ToolRouterSessionBySessionIdMountsByMountIdDeleteResponse
FileCreateDownloadURLResponse = _g.PostV31ToolRouterSessionBySessionIdMountsByMountIdDownloadUrlResponse
FileCreateUploadURLResponse = _g.PostV31ToolRouterSessionBySessionIdMountsByMountIdUploadUrlResponse

# ---- tool_router.session.files request models (4) ----
ToolRouterSessionFileListQuery = _g.GetV31ToolRouterSessionBySessionIdMountsByMountIdItemsQuery
FileDeleteBody = _g.PostV31ToolRouterSessionBySessionIdMountsByMountIdDeleteBody
FileCreateDownloadURLBody = _g.PostV31ToolRouterSessionBySessionIdMountsByMountIdDownloadUrlBody
FileCreateUploadURLBody = _g.PostV31ToolRouterSessionBySessionIdMountsByMountIdUploadUrlBody

# ---- tools responses (7) ----
ToolRetrieveResponse = _g.GetV31ToolsByToolSlugResponse
ToolListResponse = _g.GetV31ToolsResponse
ToolExecuteResponse = _g.PostV31ToolsExecuteByToolSlugResponse
ToolGetInputResponse = _g.PostV31ToolsExecuteByToolSlugInputResponse
ToolProxyResponse = _g.PostV31ToolsExecuteProxyResponse
ToolRetrieveEnumResponse = _g.GetV31ToolsEnumResponse
ToolRetrieveRequiredScopesResponse = _g.PostV31ToolsScopesRequiredResponse

# ---- tools request models (6) ----
ToolRetrieveQuery = _g.GetV31ToolsByToolSlugQuery
ToolListQuery = _g.GetV31ToolsQuery
ToolExecuteBody = _g.PostV31ToolsExecuteByToolSlugBody
ToolGetInputBody = _g.PostV31ToolsExecuteByToolSlugInputBody
ToolProxyBody = _g.PostV31ToolsExecuteProxyBody
ToolRetrieveRequiredScopesBody = _g.PostV31ToolsScopesRequiredBody

# ---- files responses (2) ----
FileListResponse = _g.GetV31FilesListResponse
FileCreatePresignedURLResponse = _g.PostV31FilesUploadRequestResponse

# ---- files request models (2) ----
FileListQuery = _g.GetV31FilesListQuery
FileCreatePresignedURLBody = _g.PostV31FilesUploadRequestBody

# ---- connected_accounts responses (9) ----
ConnectedAccountCreateResponse = _g.PostV31ConnectedAccountsResponse
ConnectedAccountRetrieveResponse = _g.GetV31ConnectedAccountsByNanoidResponse
ConnectedAccountListResponse = _g.GetV31ConnectedAccountsResponse
ConnectedAccountDeleteResponse = _g.DeleteV31ConnectedAccountsByNanoidResponse
ConnectedAccountCompleteAuthResponse = _g.PostV31ConnectedAccountsCompleteAuthResponse
ConnectedAccountPatchResponse = _g.PatchV31ConnectedAccountsByNanoidResponse
ConnectedAccountRefreshResponse = _g.PostV31ConnectedAccountsByNanoidRefreshResponse
ConnectedAccountRevokeResponse = _g.PostV31ConnectedAccountsByNanoidRevokeResponse
ConnectedAccountUpdateStatusResponse = _g.PatchV31ConnectedAccountsByNanoIdStatusResponse

# ---- connected_accounts request models (8) ----
ConnectedAccountCreateBody = _g.PostV31ConnectedAccountsBody
ConnectedAccountListQuery = _g.GetV31ConnectedAccountsQuery
ConnectedAccountDeleteQuery = _g.DeleteV31ConnectedAccountsByNanoidQuery
ConnectedAccountCompleteAuthBody = _g.PostV31ConnectedAccountsCompleteAuthBody
ConnectedAccountPatchBody = _g.PatchV31ConnectedAccountsByNanoidBody
ConnectedAccountRefreshBody = _g.PostV31ConnectedAccountsByNanoidRefreshBody
ConnectedAccountRefreshQuery = _g.PostV31ConnectedAccountsByNanoidRefreshQuery
ConnectedAccountUpdateStatusBody = _g.PatchV31ConnectedAccountsByNanoIdStatusBody

# ---- link responses (1) ----
LinkCreateResponse = _g.PostV31ConnectedAccountsLinkResponse

# ---- link request models (1) ----
LinkCreateBody = _g.PostV31ConnectedAccountsLinkBody

# ---- toolkits responses (7) ----
ToolkitRetrieveResponse = _g.GetV31ToolkitsBySlugResponse
ToolkitListResponse = _g.GetV31ToolkitsResponse
ToolkitRecommendScopesResponse = _g.RecommendToolkitScopesResponse
ToolkitRetrieveCategoriesResponse = _g.GetV31ToolkitsCategoriesResponse
ToolkitRetrieveChangelogResponse = _g.GetV31ToolkitsChangelogResponse
ToolkitRetrieveMultiResponse = _g.PostV31ToolkitsMultiResponse
ToolkitRetrieveScopesGrantContextResponse = _g.RecommendToolkitScopesGrantContextResponse

# ---- toolkits request models (6) ----
ToolkitRetrieveQuery = _g.GetV31ToolkitsBySlugQuery
ToolkitListQuery = _g.GetV31ToolkitsQuery
ToolkitRecommendScopesBody = _g.RecommendToolkitScopesBody
ToolkitRetrieveChangelogQuery = _g.GetV31ToolkitsChangelogQuery
ToolkitRetrieveMultiBody = _g.PostV31ToolkitsMultiBody
ToolkitRetrieveScopesGrantContextQuery = _g.RecommendToolkitScopesGrantContextQuery

# ---- auth_configs responses (6) ----
AuthConfigCreateResponse = _g.PostV31AuthConfigsResponse
AuthConfigRetrieveResponse = _g.GetV31AuthConfigsByNanoidResponse
AuthConfigUpdateResponse = _g.PatchV31AuthConfigsByNanoidResponse
AuthConfigListResponse = _g.GetV31AuthConfigsResponse
AuthConfigDeleteResponse = _g.DeleteV31AuthConfigsByNanoidResponse
AuthConfigUpdateStatusResponse = _g.PatchV31AuthConfigsByNanoidByStatusResponse

# ---- auth_configs request models (4) ----
AuthConfigCreateBody = _g.PostV31AuthConfigsBody
AuthConfigUpdateBody = _g.PatchV31AuthConfigsByNanoidBody
AuthConfigListQuery = _g.GetV31AuthConfigsQuery
AuthConfigDeleteQuery = _g.DeleteV31AuthConfigsByNanoidQuery

# ---- triggers_types responses (3) ----
TriggersTypeRetrieveResponse = _g.GetV31TriggersTypesBySlugResponse
TriggersTypeListResponse = _g.GetV31TriggersTypesResponse
TriggersTypeRetrieveEnumResponse = _g.GetV31TriggersTypesListEnumResponse

# ---- triggers_types request models (2) ----
TriggersTypeRetrieveQuery = _g.GetV31TriggersTypesBySlugQuery
TriggersTypeListQuery = _g.GetV31TriggersTypesQuery

# ---- trigger_instances responses (2) ----
TriggerInstanceListActiveResponse = _g.GetV31TriggerInstancesActiveResponse
TriggerInstanceUpsertResponse = _g.PostV31TriggerInstancesBySlugUpsertResponse

# ---- trigger_instances request models (2) ----
TriggerInstanceListActiveQuery = _g.GetV31TriggerInstancesActiveQuery
TriggerInstanceUpsertBody = _g.PostV31TriggerInstancesBySlugUpsertBody

# ---- trigger_instances.manage responses (2) ----
ManageUpdateResponse = _g.PatchV31TriggerInstancesManageByTriggerIdResponse
ManageDeleteResponse = _g.DeleteV31TriggerInstancesManageByTriggerIdResponse

# ---- trigger_instances.manage request models (1) ----
ManageUpdateBody = _g.PatchV31TriggerInstancesManageByTriggerIdBody

# ---- mcp responses (9) ----
McpCreateResponse = _g.PostV31McpServersResponse
McpRetrieveResponse = _g.GetV31McpByIdResponse
McpUpdateResponse = _g.PatchV31McpByIdResponse
McpListResponse = _g.GetV31McpServersResponse
McpDeleteResponse = _g.DeleteV31McpByIdResponse
McpCreateInstanceResponse = _g.PostV31McpServersByServerIdInstancesResponse
McpDeleteInstanceResponse = _g.DeleteV31McpServersByServerIdInstancesByInstanceIdResponse
McpListInstancesResponse = _g.GetV31McpServersByServerIdInstancesResponse
McpRetrieveAppResponse = _g.GetV31McpAppByAppKeyResponse

# ---- mcp request models (6) ----
McpCreateBody = _g.PostV31McpServersBody
McpUpdateBody = _g.PatchV31McpByIdBody
McpListQuery = _g.GetV31McpServersQuery
McpCreateInstanceBody = _g.PostV31McpServersByServerIdInstancesBody
McpListInstancesQuery = _g.GetV31McpServersByServerIdInstancesQuery
McpRetrieveAppQuery = _g.GetV31McpAppByAppKeyQuery

# ---- mcp.custom responses (1) ----
CustomCreateResponse = _g.PostV31McpServersCustomResponse

# ---- mcp.custom request models (1) ----
CustomCreateBody = _g.PostV31McpServersCustomBody

# ---- mcp.generate responses (1) ----
GenerateURLResponse = _g.PostV31McpServersGenerateResponse

# ---- mcp.generate request models (1) ----
GenerateURLBody = _g.PostV31McpServersGenerateBody

# ---- logs responses (2) ----
LogCreateToolExecutionResponse = _g.PostV31LogsToolExecutionResponse
LogRetrieveToolExecutionResponse = _g.GetV31LogsToolExecutionByIdResponse

# ---- logs request models (1) ----
LogCreateToolExecutionBody = _g.PostV31LogsToolExecutionBody

# ---- project.usage responses (2) ----
ProjectUsageRetrieveResponse = _g.PostV31ProjectUsageByEntityTypeResponse
ProjectUsageRetrieveSummaryResponse = _g.PostV31ProjectUsageSummaryResponse

# ---- project.usage request models (2) ----
ProjectUsageRetrieveBody = _g.PostV31ProjectUsageByEntityTypeBody
ProjectUsageRetrieveSummaryBody = _g.PostV31ProjectUsageSummaryBody

# ---- webhook_subscriptions responses (7) ----
WebhookSubscriptionCreateResponse = _g.PostV31WebhookSubscriptionsResponse
WebhookSubscriptionRetrieveResponse = _g.GetV31WebhookSubscriptionsByIdResponse
WebhookSubscriptionUpdateResponse = _g.PatchV31WebhookSubscriptionsByIdResponse
WebhookSubscriptionListResponse = _g.GetV31WebhookSubscriptionsResponse
WebhookSubscriptionDeleteResponse = _g.DeleteV31WebhookSubscriptionsByIdResponse
WebhookSubscriptionListEventTypesResponse = _g.GetV31WebhookSubscriptionsEventTypesResponse
WebhookSubscriptionRotateSecretResponse = _g.PostV31WebhookSubscriptionsByIdRotateSecretResponse

# ---- webhook_subscriptions request models (3) ----
WebhookSubscriptionCreateBody = _g.PostV31WebhookSubscriptionsBody
WebhookSubscriptionUpdateBody = _g.PatchV31WebhookSubscriptionsByIdBody
WebhookSubscriptionListQuery = _g.GetV31WebhookSubscriptionsQuery

# ---- webhook_endpoints responses (5) ----
WebhookEndpointCreateResponse = _g.PostV31WebhookEndpointsResponse
WebhookEndpointRetrieveResponse = _g.GetV31WebhookEndpointsByNanoIdResponse
WebhookEndpointUpdateResponse = _g.PatchV31WebhookEndpointsByNanoIdResponse
WebhookEndpointListResponse = _g.GetV31WebhookEndpointsResponse
WebhookEndpointReplaceResponse = _g.PostV31WebhookEndpointsByNanoIdResponse

# ---- webhook_endpoints request models (4) ----
WebhookEndpointCreateBody = _g.PostV31WebhookEndpointsBody
WebhookEndpointUpdateBody = _g.PatchV31WebhookEndpointsByNanoIdBody
WebhookEndpointListQuery = _g.GetV31WebhookEndpointsQuery
WebhookEndpointReplaceBody = _g.PostV31WebhookEndpointsByNanoIdBody

# ---- org responses (1) ----
OrgListResponse = _g.GetV31OrgListResponse

# ---- org request models (1) ----
OrgListQuery = _g.GetV31OrgListQuery

# ---- org.owner.project responses (5) ----
ProjectCreateResponse = _g.PostV31OrgOwnerProjectNewResponse
ProjectRetrieveResponse = _g.GetV31OrgOwnerProjectByNanoIdResponse
OrgOwnerProjectListResponse = _g.GetV31OrgOwnerProjectListResponse
ProjectDeleteResponse = _g.DeleteV31OrgOwnerProjectByNanoIdResponse
ProjectRegenerateAPIKeyResponse = _g.PostV31OrgOwnerProjectByNanoIdRegenerateApiKeyResponse

# ---- org.owner.project request models (3) ----
ProjectCreateBody = _g.PostV31OrgOwnerProjectNewBody
OrgOwnerProjectListQuery = _g.GetV31OrgOwnerProjectListQuery
ProjectDeleteQuery = _g.DeleteV31OrgOwnerProjectByNanoIdQuery

# ---- org.project responses (1) ----
OrgProjectListResponse = _g.GetV31OrgProjectListResponse

# ---- org.project request models (1) ----
OrgProjectListQuery = _g.GetV31OrgProjectListQuery

# ---- org.usage responses (2) ----
OrgUsageRetrieveResponse = _g.PostV31OrgUsageByEntityTypeResponse
OrgUsageRetrieveSummaryResponse = _g.PostV31OrgUsageSummaryResponse

# ---- org.usage request models (2) ----
OrgUsageRetrieveBody = _g.PostV31OrgUsageByEntityTypeBody
OrgUsageRetrieveSummaryBody = _g.PostV31OrgUsageSummaryBody

# ---- auth.session responses (1) ----
SessionRetrieveInfoResponse = _g.GetV31AuthSessionInfoResponse

# ---- api_key_revocation responses (1) ----
ApiKeyRevocationCreateResponse = _g.PostV31ApiKeyRevocationResponse

# ---- api_key_revocation request models (1) ----
ApiKeyRevocationCreateBody = _g.PostV31ApiKeyRevocationBody

# ---- _internal.cli responses (3) ----
CliCreateCodactFailureResponse = _g.PostV31CliCodactFailuresResponse
CliCreateSessionResponse = _g.PostV31CliCreateSessionResponse
CliGetSessionResponse = _g.GetV31CliGetSessionResponse

# ---- _internal.cli request models (3) ----
CliCreateCodactFailureBody = _g.PostV31CliCodactFailuresBody
CliCreateSessionBody = _g.PostV31CliCreateSessionBody
CliGetSessionQuery = _g.GetV31CliGetSessionQuery

# ---- _internal.cli.realtime responses (2) ----
RealtimeAuthResponse = _g.PostV31CliRealtimeAuthResponse
RealtimeCredentialsResponse = _g.GetV31CliRealtimeCredentialsResponse

# ---- _internal.cli.realtime request models (1) ----
RealtimeAuthBody = _g.PostV31CliRealtimeAuthBody

# ---- _internal.consumer.permissions responses (1) ----
PermissionsResolveResponse = _g.PostV31ConsumerPermissionsResolveResponse

# ---- _internal.consumer.permissions request models (1) ----
PermissionsResolveBody = _g.PostV31ConsumerPermissionsResolveBody

# ---- _internal.logs.triggers responses (2) ----
TriggerRetrieveResponse = _g.GetV31InternalTriggerLogByIdResponse
TriggerListResponse = _g.PostV31InternalTriggerLogsResponse

# ---- _internal.logs.triggers request models (1) ----
TriggerListBody = _g.PostV31InternalTriggerLogsBody

# ---- _internal.logs.tools responses (3) ----
LogsToolRetrieveResponse = _g.GetV31InternalActionExecutionLogByIdResponse
LogsToolListResponse = _g.PostV31InternalActionExecutionLogsResponse
ToolListFieldsResponse = _g.GetV31InternalActionExecutionFieldsResponse

# ---- _internal.logs.tools request models (1) ----
LogsToolListBody = _g.PostV31InternalActionExecutionLogsBody

# ---- _internal.org.consumer responses (2) ----
ConsumerListConnectedToolkitsResponse = _g.GetV31OrgConsumerConnectedToolkitsResponse
ConsumerRetrieveConfigResponse = _g.GetV31OrgConsumerConfigResponse

# ---- _internal.org.consumer request models (1) ----
ConsumerListConnectedToolkitsQuery = _g.GetV31OrgConsumerConnectedToolkitsQuery

# ---- _internal.org.consumer.project responses (1) ----
ProjectResolveResponse = _g.PostV31OrgConsumerProjectResolveResponse

# ---- custom responses (5) ----
CustomCreateToolkitResponse = _g.PostV31CustomToolkitsResponse
CustomDeleteToolkitResponse = _g.DeleteV31CustomToolkitsBySlugResponse
CustomSyncResponse = _g.PostV31CustomToolkitsSyncResponse
CustomUpdateToolkitsResponse = _g.PatchV31CustomToolkitsBySlugResponse
CustomUpsertResponse = _g.PostV31CustomToolkitsUpsertResponse

# ---- custom request models (5) ----
CustomCreateToolkitBody = _g.PostV31CustomToolkitsBody
CustomDeleteToolkitQuery = _g.DeleteV31CustomToolkitsBySlugQuery
CustomSyncBody = _g.PostV31CustomToolkitsSyncBody
CustomUpdateToolkitsBody = _g.PatchV31CustomToolkitsBySlugBody
CustomUpsertBody = _g.PostV31CustomToolkitsUpsertBody

# ---- keyring responses (1) ----
KeyringListTransferKeysResponse = _g.GetV31KeyringTransferKeysResponse

# ---- session_configs responses (2) ----
SessionConfigsRetrieveResponse = _g.GetV31SessionConfigsBySessionConfigIdResponse
SessionConfigsListResponse = _g.GetV31SessionConfigsResponse

# ---- session_configs request models (1) ----
SessionConfigsListQuery = _g.GetV31SessionConfigsQuery

__all__ = [
    "SessionCreateResponse",
    "SessionRetrieveResponse",
    "SessionDeleteResponse",
    "SessionAttachResponse",
    "SessionConfigHistoryResponse",
    "SessionExecuteResponse",
    "SessionExecuteMetaResponse",
    "SessionLinkResponse",
    "SessionPatchResponse",
    "SessionProxyExecuteResponse",
    "SessionSearchResponse",
    "SessionToolkitsResponse",
    "SessionToolsResponse",
    "SessionCreateBody",
    "SessionAttachBody",
    "SessionConfigHistoryQuery",
    "SessionExecuteBody",
    "SessionExecuteMetaBody",
    "SessionLinkBody",
    "SessionPatchBody",
    "SessionProxyExecuteBody",
    "SessionSearchBody",
    "SessionToolkitsQuery",
    "SessionToolsQuery",
    "ToolRouterSessionFileListResponse",
    "FileDeleteResponse",
    "FileCreateDownloadURLResponse",
    "FileCreateUploadURLResponse",
    "ToolRouterSessionFileListQuery",
    "FileDeleteBody",
    "FileCreateDownloadURLBody",
    "FileCreateUploadURLBody",
    "ToolRetrieveResponse",
    "ToolListResponse",
    "ToolExecuteResponse",
    "ToolGetInputResponse",
    "ToolProxyResponse",
    "ToolRetrieveEnumResponse",
    "ToolRetrieveRequiredScopesResponse",
    "ToolRetrieveQuery",
    "ToolListQuery",
    "ToolExecuteBody",
    "ToolGetInputBody",
    "ToolProxyBody",
    "ToolRetrieveRequiredScopesBody",
    "FileListResponse",
    "FileCreatePresignedURLResponse",
    "FileListQuery",
    "FileCreatePresignedURLBody",
    "ConnectedAccountCreateResponse",
    "ConnectedAccountRetrieveResponse",
    "ConnectedAccountListResponse",
    "ConnectedAccountDeleteResponse",
    "ConnectedAccountCompleteAuthResponse",
    "ConnectedAccountPatchResponse",
    "ConnectedAccountRefreshResponse",
    "ConnectedAccountRevokeResponse",
    "ConnectedAccountUpdateStatusResponse",
    "ConnectedAccountCreateBody",
    "ConnectedAccountListQuery",
    "ConnectedAccountDeleteQuery",
    "ConnectedAccountCompleteAuthBody",
    "ConnectedAccountPatchBody",
    "ConnectedAccountRefreshBody",
    "ConnectedAccountRefreshQuery",
    "ConnectedAccountUpdateStatusBody",
    "LinkCreateResponse",
    "LinkCreateBody",
    "ToolkitRetrieveResponse",
    "ToolkitListResponse",
    "ToolkitRecommendScopesResponse",
    "ToolkitRetrieveCategoriesResponse",
    "ToolkitRetrieveChangelogResponse",
    "ToolkitRetrieveMultiResponse",
    "ToolkitRetrieveScopesGrantContextResponse",
    "ToolkitRetrieveQuery",
    "ToolkitListQuery",
    "ToolkitRecommendScopesBody",
    "ToolkitRetrieveChangelogQuery",
    "ToolkitRetrieveMultiBody",
    "ToolkitRetrieveScopesGrantContextQuery",
    "AuthConfigCreateResponse",
    "AuthConfigRetrieveResponse",
    "AuthConfigUpdateResponse",
    "AuthConfigListResponse",
    "AuthConfigDeleteResponse",
    "AuthConfigUpdateStatusResponse",
    "AuthConfigCreateBody",
    "AuthConfigUpdateBody",
    "AuthConfigListQuery",
    "AuthConfigDeleteQuery",
    "TriggersTypeRetrieveResponse",
    "TriggersTypeListResponse",
    "TriggersTypeRetrieveEnumResponse",
    "TriggersTypeRetrieveQuery",
    "TriggersTypeListQuery",
    "TriggerInstanceListActiveResponse",
    "TriggerInstanceUpsertResponse",
    "TriggerInstanceListActiveQuery",
    "TriggerInstanceUpsertBody",
    "ManageUpdateResponse",
    "ManageDeleteResponse",
    "ManageUpdateBody",
    "McpCreateResponse",
    "McpRetrieveResponse",
    "McpUpdateResponse",
    "McpListResponse",
    "McpDeleteResponse",
    "McpCreateInstanceResponse",
    "McpDeleteInstanceResponse",
    "McpListInstancesResponse",
    "McpRetrieveAppResponse",
    "McpCreateBody",
    "McpUpdateBody",
    "McpListQuery",
    "McpCreateInstanceBody",
    "McpListInstancesQuery",
    "McpRetrieveAppQuery",
    "CustomCreateResponse",
    "CustomCreateBody",
    "GenerateURLResponse",
    "GenerateURLBody",
    "LogCreateToolExecutionResponse",
    "LogRetrieveToolExecutionResponse",
    "LogCreateToolExecutionBody",
    "ProjectUsageRetrieveResponse",
    "ProjectUsageRetrieveSummaryResponse",
    "ProjectUsageRetrieveBody",
    "ProjectUsageRetrieveSummaryBody",
    "WebhookSubscriptionCreateResponse",
    "WebhookSubscriptionRetrieveResponse",
    "WebhookSubscriptionUpdateResponse",
    "WebhookSubscriptionListResponse",
    "WebhookSubscriptionDeleteResponse",
    "WebhookSubscriptionListEventTypesResponse",
    "WebhookSubscriptionRotateSecretResponse",
    "WebhookSubscriptionCreateBody",
    "WebhookSubscriptionUpdateBody",
    "WebhookSubscriptionListQuery",
    "WebhookEndpointCreateResponse",
    "WebhookEndpointRetrieveResponse",
    "WebhookEndpointUpdateResponse",
    "WebhookEndpointListResponse",
    "WebhookEndpointReplaceResponse",
    "WebhookEndpointCreateBody",
    "WebhookEndpointUpdateBody",
    "WebhookEndpointListQuery",
    "WebhookEndpointReplaceBody",
    "OrgListResponse",
    "OrgListQuery",
    "ProjectCreateResponse",
    "ProjectRetrieveResponse",
    "OrgOwnerProjectListResponse",
    "ProjectDeleteResponse",
    "ProjectRegenerateAPIKeyResponse",
    "ProjectCreateBody",
    "OrgOwnerProjectListQuery",
    "ProjectDeleteQuery",
    "OrgProjectListResponse",
    "OrgProjectListQuery",
    "OrgUsageRetrieveResponse",
    "OrgUsageRetrieveSummaryResponse",
    "OrgUsageRetrieveBody",
    "OrgUsageRetrieveSummaryBody",
    "SessionRetrieveInfoResponse",
    "ApiKeyRevocationCreateResponse",
    "ApiKeyRevocationCreateBody",
    "CliCreateCodactFailureResponse",
    "CliCreateSessionResponse",
    "CliGetSessionResponse",
    "CliCreateCodactFailureBody",
    "CliCreateSessionBody",
    "CliGetSessionQuery",
    "RealtimeAuthResponse",
    "RealtimeCredentialsResponse",
    "RealtimeAuthBody",
    "PermissionsResolveResponse",
    "PermissionsResolveBody",
    "TriggerRetrieveResponse",
    "TriggerListResponse",
    "TriggerListBody",
    "LogsToolRetrieveResponse",
    "LogsToolListResponse",
    "ToolListFieldsResponse",
    "LogsToolListBody",
    "ConsumerListConnectedToolkitsResponse",
    "ConsumerRetrieveConfigResponse",
    "ConsumerListConnectedToolkitsQuery",
    "ProjectResolveResponse",
    "CustomCreateToolkitResponse",
    "CustomDeleteToolkitResponse",
    "CustomSyncResponse",
    "CustomUpdateToolkitsResponse",
    "CustomUpsertResponse",
    "CustomCreateToolkitBody",
    "CustomDeleteToolkitQuery",
    "CustomSyncBody",
    "CustomUpdateToolkitsBody",
    "CustomUpsertBody",
    "KeyringListTransferKeysResponse",
    "SessionConfigsRetrieveResponse",
    "SessionConfigsListResponse",
    "SessionConfigsListQuery",
]
