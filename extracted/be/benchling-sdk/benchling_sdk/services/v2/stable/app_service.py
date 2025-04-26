from datetime import datetime
from typing import Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.apps import (
    archive_app_canvases,
    archive_benchling_apps,
    bulk_create_app_configuration_items,
    bulk_update_app_configuration_items,
    create_app_canvas,
    create_app_configuration_item,
    create_app_session,
    create_benchling_app,
    get_app_canvas,
    get_app_configuration_item_by_id,
    get_app_session_by_id,
    get_benchling_app_by_id,
    list_app_canvases,
    list_app_configuration_items,
    list_app_sessions,
    list_benchling_apps,
    patch_benchling_app,
    unarchive_app_canvases,
    unarchive_benchling_apps,
    update_app_canvas,
    update_app_configuration_item,
    update_app_session,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import AppSessionClosedError, raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.logging_helpers import log_deprecation
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import (
    AppCanvas,
    AppCanvasCreate,
    AppCanvasesArchivalChange,
    AppCanvasesArchive,
    AppCanvasesArchiveReason,
    AppCanvasesPaginatedList,
    AppCanvasesUnarchive,
    AppCanvasUpdate,
    AppConfigItem,
    AppConfigItemBulkUpdate,
    AppConfigItemCreate,
    AppConfigItemsBulkCreateRequest,
    AppConfigItemsBulkUpdateRequest,
    AppConfigItemUpdate,
    AppConfigurationPaginatedList,
    AppSession,
    AppSessionCreate,
    AppSessionsPaginatedList,
    AppSessionUpdate,
    AsyncTaskLink,
    BenchlingApp,
    BenchlingAppCreate,
    BenchlingAppsArchivalChange,
    BenchlingAppsArchive,
    BenchlingAppsArchiveReason,
    BenchlingAppsPaginatedList,
    BenchlingAppsUnarchive,
    BenchlingAppUpdate,
    ListAppCanvasesEnabled,
    ListAppCanvasesSort,
    ListAppConfigurationItemsSort,
    ListAppSessionsSort,
    ListBenchlingAppsSort,
)
from benchling_sdk.services.v2.base_service import BaseService


class AppService(BaseService):
    """
    Apps.

    Create and manage Apps on your tenant.

    See https://benchling.com/api/reference#/Apps
    """

    @api_method
    def _apps_page(
        self,
        *,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[ListBenchlingAppsSort] = None,
        ids: Optional[Iterable[str]] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        namesany_of: Optional[Iterable[str]] = None,
        namesany_ofcase_sensitive: Optional[Iterable[str]] = None,
        creator_ids: Optional[Iterable[str]] = None,
        member_of: Optional[Iterable[str]] = None,
        admin_of: Optional[Iterable[str]] = None,
    ) -> Response[BenchlingAppsPaginatedList]:
        response = list_benchling_apps.sync_detailed(
            client=self.client,
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            sort=none_as_unset(sort),
            ids=none_as_unset(optional_array_query_param(ids)),
            modified_at=none_as_unset(modified_at),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            namesany_of=none_as_unset(optional_array_query_param(namesany_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(namesany_ofcase_sensitive)),
            creator_ids=none_as_unset(optional_array_query_param(creator_ids)),
            member_of=none_as_unset(optional_array_query_param(member_of)),
            admin_of=none_as_unset(optional_array_query_param(admin_of)),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list_apps(
        self,
        *,
        page_size: Optional[int] = 50,
        sort: Optional[Union[str, ListBenchlingAppsSort]] = None,
        ids: Optional[Iterable[str]] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        namesany_of: Optional[Iterable[str]] = None,
        namesany_ofcase_sensitive: Optional[Iterable[str]] = None,
        creator_ids: Optional[str] = None,
        member_of: Optional[str] = None,
        admin_of: Optional[str] = None,
    ) -> PageIterator[BenchlingApp]:
        """
        List Apps.

        See https://benchling.com/api/reference#/Apps/listBenchlingApps
        """

        def api_call(next_token: NextToken) -> Response[BenchlingAppsPaginatedList]:
            return self._apps_page(
                page_size=page_size,
                sort=_translate_to_string_enum(ListBenchlingAppsSort, sort),
                ids=ids,
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                namesany_of=namesany_of,
                namesany_ofcase_sensitive=namesany_ofcase_sensitive,
                creator_ids=creator_ids,
                member_of=member_of,
                admin_of=admin_of,
                next_token=next_token,
            )

        def results_extractor(body: BenchlingAppsPaginatedList) -> Optional[List[BenchlingApp]]:
            return body.apps

        return PageIterator(api_call, results_extractor)

    @api_method
    def get_by_id(self, app_id: str) -> BenchlingApp:
        """
        Get an App by ID.

        See https://benchling.com/api/reference#/Apps/getBenchlingAppByID
        """
        response = get_benchling_app_by_id.sync_detailed(client=self.client, app_id=app_id)
        return model_from_detailed(response)

    @api_method
    def create(self, app: BenchlingAppCreate) -> BenchlingApp:
        """
        Create an App (Deprecated).

        .. deprecated:: 1.8.0

        See https://benchling.com/api/reference#/Apps/createBenchlingApp
        """
        log_deprecation("apps.create")
        response = create_benchling_app.sync_detailed(client=self.client, json_body=app)
        return model_from_detailed(response)

    @api_method
    def update(self, app_id: str, app: BenchlingAppUpdate) -> BenchlingApp:
        """
        Update an App's metadata (Deprecated).

        .. deprecated:: 1.8.0

        See https://benchling.com/api/reference#/Apps/patchBenchlingApp
        """
        log_deprecation("apps.update")
        response = patch_benchling_app.sync_detailed(client=self.client, app_id=app_id, json_body=app)
        return model_from_detailed(response)

    @api_method
    def archive(
        self, app_ids: Iterable[str], reason: BenchlingAppsArchiveReason
    ) -> BenchlingAppsArchivalChange:
        """
        Archive Apps (Deprecated).

        .. deprecated:: 1.8.0

        See https://benchling.com/api/reference#/Apps/archiveBenchlingApps
        """
        log_deprecation("apps.archive")
        archive_request = BenchlingAppsArchive(app_ids=list(app_ids), reason=reason)
        response = archive_benchling_apps.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, app_ids: Iterable[str]) -> BenchlingAppsArchivalChange:
        """
        Unarchive Apps (Deprecated).

        .. deprecated:: 1.8.0

        See https://benchling.com/api/reference#/Apps/unarchiveBenchlingApps
        """
        log_deprecation("apps.unarchive")
        unarchive_request = BenchlingAppsUnarchive(app_ids=list(app_ids))
        response = unarchive_benchling_apps.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def _list_app_configuration_items_page(
        self,
        *,
        app_id: Optional[str] = None,
        ids: Optional[Iterable[str]] = None,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        modified_at: Optional[str] = None,
        sort: Optional[ListAppConfigurationItemsSort] = None,
    ) -> Response[AppConfigurationPaginatedList]:
        return list_app_configuration_items.sync_detailed(  # type: ignore
            client=self.client,
            app_id=none_as_unset(app_id),
            ids=none_as_unset(optional_array_query_param(ids)),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            modified_at=none_as_unset(modified_at),
            sort=none_as_unset(sort),
        )

    def list_app_configuration_items(
        self,
        *,
        app_id: Optional[str] = None,
        ids: Optional[Iterable[str]] = None,
        page_size: Optional[int] = 50,
        modified_at: Optional[str] = None,
        sort: Optional[Union[str, ListAppConfigurationItemsSort]] = None,
    ) -> PageIterator[AppConfigItem]:
        """
        Get app configuration items.

        See https://benchling.com/api/reference#/Apps/listAppConfigurationItems
        """

        def api_call(next_token: NextToken) -> Response[AppConfigurationPaginatedList]:
            return self._list_app_configuration_items_page(
                app_id=app_id,
                ids=ids,
                page_size=page_size,
                modified_at=modified_at,
                sort=_translate_to_string_enum(ListAppConfigurationItemsSort, sort),
                next_token=next_token,
            )

        def results_extractor(
            body: AppConfigurationPaginatedList,
        ) -> Optional[List[AppConfigItem]]:
            return body.app_configuration_items

        return PageIterator(api_call, results_extractor)

    @api_method
    def get_app_configuration_item_by_id(self, item_id: str) -> AppConfigItem:
        """
        Get app configuration.

        See https://benchling.com/api/reference#/Apps/getAppConfigurationItemById
        """
        response = get_app_configuration_item_by_id.sync_detailed(client=self.client, item_id=item_id)
        return model_from_detailed(response)

    @api_method
    def create_app_configuration_item(self, configuration_item: AppConfigItemCreate) -> AppConfigItem:
        """
        Create app configuration item.

        See https://benchling.com/api/reference#/Apps/createAppConfigurationItem
        """
        response = create_app_configuration_item.sync_detailed(
            client=self.client, json_body=configuration_item
        )
        return model_from_detailed(response)

    @api_method
    def update_app_configuration_item(
        self, item_id: str, configuration_item: AppConfigItemUpdate
    ) -> AppConfigItem:
        """
        Update app configuration item.

        See https://benchling.com/api/reference#/Apps/updateAppConfigurationItem
        """
        response = update_app_configuration_item.sync_detailed(
            client=self.client, item_id=item_id, json_body=configuration_item
        )
        return model_from_detailed(response)

    # TODO BNCH-52599 Add tests once platform supports archive
    # @api_method
    # def archive_app_configuration_items(
    #     self, item_ids: Iterable[str], reason: AppConfigItemsArchiveReason
    # ) -> AppConfigItemsArchivalChange:
    #     """
    #     Archive app configuration items.
    #
    #     See https://benchling.com/api/reference#/Apps/archiveAppConfigurationItems
    #     """
    #     archive_request = AppConfigItemsArchive(reason=reason, item_ids=list(item_ids))
    #     response = archive_app_configuration_items.sync_detailed(
    #         client=self.client, json_body=archive_request
    #     )
    #     return model_from_detailed(response)

    # TODO BNCH-52599 Add tests once platform supports archive
    # @api_method
    # def unarchive_app_configuration_items(self, item_ids: Iterable[str]) -> AppConfigItemsArchivalChange:
    #     """
    #     Unarchive app configuration items.
    #
    #     See https://benchling.com/api/reference#/Apps/unarchiveAppConfigurationItems
    #     """
    #     unarchive_request = AppConfigItemsUnarchive(item_ids=list(item_ids))
    #     response = unarchive_app_configuration_items.sync_detailed(
    #         client=self.client, json_body=unarchive_request
    #     )
    #     return model_from_detailed(response)

    @api_method
    def bulk_create_app_configuration_items(self, items: Iterable[AppConfigItemCreate]) -> AsyncTaskLink:
        """
        Bulk create app configuration items.

        See https://benchling.com/api/reference#/Apps/bulkCreateAppConfigurationItems
        """
        body = AppConfigItemsBulkCreateRequest(list(items))
        response = bulk_create_app_configuration_items.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_update_app_configuration_items(self, items: Iterable[AppConfigItemBulkUpdate]) -> AsyncTaskLink:
        """
        Bulk update app configuration items.

        See https://benchling.com/api/reference#/Apps/bulkUpdateAppConfigurationItems
        """
        body = AppConfigItemsBulkUpdateRequest(list(items))
        response = bulk_update_app_configuration_items.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    # Canvases

    @api_method
    def create_canvas(self, canvas: AppCanvasCreate) -> AppCanvas:
        """
        Create an App Canvas that a Benchling App can write to and read user interaction from.

        See https://benchling.com/api/reference#/Apps/createAppCanvas
        """
        response = create_app_canvas.sync_detailed(
            client=self.client,
            json_body=canvas,
        )
        return model_from_detailed(response)

    @api_method
    def _canvases_page(
        self,
        app_id: Optional[str] = None,
        feature_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        enabled: Optional[ListAppCanvasesEnabled] = None,
        archive_reason: Optional[str] = None,
        sort: Optional[Union[str, ListAppCanvasesSort]] = None,
        next_token: Optional[NextToken] = None,
        page_size: Optional[int] = None,
    ) -> Response[AppCanvasesPaginatedList]:
        response = list_app_canvases.sync_detailed(
            client=self.client,
            app_id=none_as_unset(app_id),
            feature_id=none_as_unset(feature_id),
            resource_id=none_as_unset(resource_id),
            enabled=none_as_unset(enabled),
            archive_reason=none_as_unset(archive_reason),
            sort=none_as_unset(_translate_to_string_enum(ListAppCanvasesSort, sort)),
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
        )
        raise_for_status(response)
        return response  # type: ignore

    # Removed until the API endpoints are released to GA (currently LA)

    # def list_canvases(
    #     self,
    #     app_id: Optional[str] = None,
    #     feature_id: Optional[str] = None,
    #     resource_id: Optional[str] = None,
    #     enabled: Optional[ListAppCanvasesEnabled] = None,
    #     archive_reason: Optional[str] = None,
    #     sort: Optional[Union[str, ListAppCanvasesSort]] = None,
    #     page_size: Optional[int] = None,
    # ) -> PageIterator[AppCanvas]:
    #     """
    #     List canvases.

    #     See https://benchling.com/api/reference#/Apps/listAppCanvases
    #     """

    #     def api_call(next_token: NextToken) -> Response[AppCanvasesPaginatedList]:
    #         return self._canvases_page(
    #             app_id=app_id,
    #             feature_id=feature_id,
    #             resource_id=resource_id,
    #             enabled=enabled,
    #             archive_reason=archive_reason,
    #             sort=sort,
    #             next_token=next_token,
    #             page_size=page_size,
    #         )

    #     def results_extractor(body: AppCanvasesPaginatedList) -> Optional[List[AppCanvas]]:
    #         return body.app_canvases

    #     return PageIterator(api_call, results_extractor)

    @api_method
    def get_canvas_by_id(self, canvas_id: str, returning: Optional[List[str]] = None) -> AppCanvas:
        """
        Get the current state of the App Canvas, including user input elements.

        See https://benchling.com/api/reference#/Apps/getAppCanvas
        """
        response = get_app_canvas.sync_detailed(
            client=self.client,
            canvas_id=canvas_id,
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return model_from_detailed(response)

    @api_method
    def update_canvas(self, canvas_id: str, canvas: AppCanvasUpdate) -> AppCanvas:
        """
        Update App Canvas.

        See https://benchling.com/api/reference#/Apps/updateAppCanvas
        """
        response = update_app_canvas.sync_detailed(
            client=self.client,
            canvas_id=canvas_id,
            json_body=canvas,
        )
        return model_from_detailed(response)

    @api_method
    def archive_canvases(
        self, canvas_ids: Iterable[str], reason: AppCanvasesArchiveReason
    ) -> AppCanvasesArchivalChange:
        """
        Archive App Canvases.

        See https://benchling.com/api/reference#/Apps/archiveAppCanvases
        """
        archive_request = AppCanvasesArchive(reason=reason, canvas_ids=list(canvas_ids))
        response = archive_app_canvases.sync_detailed(
            client=self.client,
            json_body=archive_request,
        )
        return model_from_detailed(response)

    @api_method
    def unarchive_canvases(self, canvas_ids: Iterable[str]) -> AppCanvasesArchivalChange:
        """
        Unarchive App Canvases.

        See https://benchling.com/api/reference#/Apps/unarchiveAppCanvases
        """
        unarchive_request = AppCanvasesUnarchive(canvas_ids=list(canvas_ids))
        response = unarchive_app_canvases.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    # Sessions

    @api_method
    def create_session(self, session: AppSessionCreate) -> AppSession:
        """
        Create a new Benchling App session. Sessions cannot be archived once created.

        See https://benchling.com/api/v2/reference#/Apps/createAppSessions
        """
        response = create_app_session.sync_detailed(
            client=self.client,
            json_body=session,
        )
        return model_from_detailed(response)

    @api_method
    def get_session_by_id(self, session_id: str, returning: Optional[List[str]] = None) -> AppSession:
        """
        Get a Benchling App session.

        See https://benchling.com/api/v2/reference#/Apps/getAppSessionById
        """
        response = get_app_session_by_id.sync_detailed(
            client=self.client,
            id=session_id,
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return model_from_detailed(response)

    @api_method
    def update_session(self, session_id: str, session: AppSessionUpdate) -> AppSession:
        """
        Update Benchling App session.

        Raises AppSessionClosedError if trying to update a Session that has already been closed.

        See https://benchling.com/api/v2/reference#/Apps/updateAppSession
        """
        response = update_app_session.sync_detailed(
            client=self.client,
            id=session_id,
            json_body=session,
        )
        return model_from_detailed(response, error_types=[AppSessionClosedError])

    @api_method
    def _sessions_page(
        self,
        app_id: Optional[str] = None,
        created_at_lt: Optional[datetime] = None,
        created_at_gt: Optional[datetime] = None,
        created_at_lte: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        modified_at_lt: Optional[datetime] = None,
        modified_at_gt: Optional[datetime] = None,
        modified_at_lte: Optional[datetime] = None,
        modified_at_gte: Optional[datetime] = None,
        sort: Optional[ListAppSessionsSort] = None,
        returning: Optional[Iterable[str]] = None,
        next_token: Optional[NextToken] = None,
        page_size: Optional[int] = None,
    ) -> Response[AppSessionsPaginatedList]:
        response = list_app_sessions.sync_detailed(
            client=self.client,
            app_id=none_as_unset(app_id),
            # TODO BNCH-70665 These should all be strings to be consistent with the rest of our API
            created_atlt=none_as_unset(created_at_lt),
            created_atgt=none_as_unset(created_at_gt),
            created_atlte=none_as_unset(created_at_lte),
            created_atgte=none_as_unset(created_at_gte),
            modified_atlt=none_as_unset(modified_at_lt),
            modified_atgt=none_as_unset(modified_at_gt),
            modified_atlte=none_as_unset(modified_at_lte),
            modified_atgte=none_as_unset(modified_at_gte),
            sort=none_as_unset(sort),
            returning=none_as_unset(optional_array_query_param(returning)),
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
        )
        raise_for_status(response)
        return response  # type: ignore

    # Removed until the API endpoints are released to GA (currently LA)

    # def list_sessions(
    #     self,
    #     app_id: Optional[str] = None,
    #     created_at_lt: Optional[datetime] = None,
    #     created_at_gt: Optional[datetime] = None,
    #     created_at_lte: Optional[datetime] = None,
    #     created_at_gte: Optional[datetime] = None,
    #     modified_at_lt: Optional[datetime] = None,
    #     modified_at_gt: Optional[datetime] = None,
    #     modified_at_lte: Optional[datetime] = None,
    #     modified_at_gte: Optional[datetime] = None,
    #     sort: Optional[ListAppSessionsSort] = None,
    #     returning: Optional[Iterable[str]] = None,
    #     page_size: Optional[int] = None,
    # ) -> PageIterator[AppSession]:
    #     """
    #     List all Benchling App sessions.

    #     See https://benchling.com/api/v2/reference#/Apps/listAppSessions
    #     """

    #     def api_call(next_token: NextToken) -> Response[AppSessionsPaginatedList]:
    #         return self._sessions_page(
    #             app_id=app_id,
    #             created_at_lt=created_at_lt,
    #             created_at_gt=created_at_gt,
    #             created_at_lte=created_at_lte,
    #             created_at_gte=created_at_gte,
    #             modified_at_lt=modified_at_lt,
    #             modified_at_gt=modified_at_gt,
    #             modified_at_lte=modified_at_lte,
    #             modified_at_gte=modified_at_gte,
    #             sort=sort,
    #             returning=returning,
    #             next_token=next_token,
    #             page_size=page_size,
    #         )

    #     def results_extractor(body: AppSessionsPaginatedList) -> Optional[List[AppSession]]:
    #         return body.app_sessions

    #     return PageIterator(api_call, results_extractor)
