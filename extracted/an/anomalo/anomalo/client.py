from __future__ import annotations

import json
import os
from collections.abc import Sequence
from datetime import datetime, timedelta
from time import sleep
from typing import Any, List, Union
from urllib.parse import urlparse

import requests
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from .result import BadRequestException, Result


class NotSet:
    pass


AUTHORIZATION_HEADER = "Authorization"
AUTHORIZATION_HEADER_ENV_VAR = "ANOMALO_AUTHORIZATION_HEADER"
NOT_SET = NotSet()

# Synthetic label id that matches tables with no labels. Pass it as label_id to
# tables()/filter_tables_by_label() to filter to unlabeled tables. Kept in sync
# with UNLABELED_LABEL_ID in the server (main.models.organization); a negative id
# cannot collide with a real label id.
UNLABELED_LABEL_ID = -1

OptionalStringList = Union[List[str], NotSet, None]


class Client:
    output_style = "json"

    def __init__(
        self,
        api_token=None,
        host=None,
        proto=None,
        ssl_cert_verify=None,
        output_style=None,
        legacy_auth: bool = True,
        headers: dict[str, str] | None = None,
    ):
        headers = headers or dict()
        if output_style:
            self.output_style = output_style
        self.host = host if host else os.environ.get("ANOMALO_INSTANCE_HOST")
        self.api_token = (
            api_token if api_token else os.environ.get("ANOMALO_API_SECRET_TOKEN")
        )
        if AUTHORIZATION_HEADER not in headers and (
            auth_header := os.environ.get(AUTHORIZATION_HEADER_ENV_VAR)
        ):
            headers[AUTHORIZATION_HEADER] = auth_header

        if not self.host:
            raise RuntimeError(
                "Please specify Anomalo instance host via ANOMALO_INSTANCE_HOST env var"
            )
        if not self.api_token and AUTHORIZATION_HEADER not in headers:
            raise RuntimeError(
                "Please specify Anomalo api token via ANOMALO_API_SECRET_TOKEN env var"
            )

        parsed_host_url = urlparse(self.host)
        host_scheme = parsed_host_url.scheme
        if host_scheme:
            self.proto = host_scheme
            self.host = parsed_host_url.netloc
        else:
            self.proto = proto if proto else "https"

        self.request_headers = dict()
        if self.api_token:
            self.request_headers.update(
                {"X-Anomalo-Token": self.api_token}
                if legacy_auth
                else {"Authorization": f"Bearer {self.api_token}"}
            )
        self.request_headers.update(headers)

        self.verify = ssl_cert_verify

        self._server_version: str | None = None

    @property
    def server_version(self) -> str:
        if self._server_version is None:
            url = f"{self.proto}://{self.host}/version.txt"
            response = requests.get(url)
            if not response.ok:
                raise RuntimeError("Could not determine server version")

            lines = [l for l in response.content.decode().splitlines() if l.strip()]

            if len(lines) == 2:
                # The semver (e.g. `v0.190.3`) if known.
                self._server_version = lines[1]
            elif len(lines) == 1:
                self._server_version = "test"
            else:
                self._server_version = "unknown"
        return self._server_version

    @retry(
        retry=retry_if_not_exception_type(BadRequestException),
        wait=wait_exponential_jitter(initial=1, max=10),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def _api_call(self, endpoint, method="GET", empty_response=False, **kwargs) -> Any:
        endpoint_url = f"{self.proto}://{self.host}/api/public/v1/{endpoint}"

        if method in ["PUT", "POST", "PATCH"]:
            request_args = dict(json=kwargs)
        else:
            request_args = dict(params=kwargs)

        response = requests.request(
            method,
            endpoint_url,
            headers=self.request_headers,
            verify=self.verify,
            allow_redirects=False,
            **request_args,
        )

        if not response.ok:
            if 400 <= response.status_code < 500:
                raise BadRequestException(response.text, response.status_code)
            else:
                raise RuntimeError(response.text)
        if empty_response:
            return response
        return Result.from_raw(response, self.output_style)

    def ping(self):
        return self._api_call("ping")

    def get_active_organization_id(self):
        res = self._api_call("organization")
        if self.output_style != "json":
            res = json.loads(res)
        return res.get("id")

    def set_active_organization_id(self, organization_id):
        res = self._api_call("organization", method="PUT", id=organization_id)
        if self.output_style != "json":
            res = json.loads(res)
        return res.get("id")

    def get_all_organizations(self):
        return self._api_call("organizations")

    def create_organization(self, name: str):
        return self._api_call("deployment/organization", method="POST", name=name)

    def list_warehouses(self):
        return self._api_call("list_warehouses")

    def get_warehouse(self, warehouse_id: int):
        return self._api_call(f"warehouse/{warehouse_id}")

    def _generate_schema_crawl_kwargs(
        self,
        schema_crawl_exclusion_list: OptionalStringList = NOT_SET,
        schema_crawl_inclusion_list: OptionalStringList = NOT_SET,
    ):
        extra_kwargs = {}
        if schema_crawl_exclusion_list is not NOT_SET:
            extra_kwargs["schema_crawl_exclusion_list"] = schema_crawl_exclusion_list
        if schema_crawl_inclusion_list is not NOT_SET:
            extra_kwargs["schema_crawl_inclusion_list"] = schema_crawl_inclusion_list
        return extra_kwargs

    def create_warehouse(
        self,
        name: str,
        warehouse_type: str,
        connection: dict[str, Any],
        schema_crawl_exclusion_list: OptionalStringList = NOT_SET,
        schema_crawl_inclusion_list: OptionalStringList = NOT_SET,
        schema_crawl_priority: str | None = None,
    ):
        return self._api_call(
            "warehouse",
            name=name,
            warehouse_type=warehouse_type,
            connection=connection,
            method="POST",
            schema_crawl_priority=schema_crawl_priority,
            **self._generate_schema_crawl_kwargs(
                schema_crawl_exclusion_list=schema_crawl_exclusion_list,
                schema_crawl_inclusion_list=schema_crawl_inclusion_list,
            ),
        )

    def update_warehouse(
        self,
        warehouse_id: int,
        name: str,
        connection: dict[str, Any],
        schema_crawl_exclusion_list: OptionalStringList = NOT_SET,
        schema_crawl_inclusion_list: OptionalStringList = NOT_SET,
        schema_crawl_priority: str | None = None,
    ):
        return self._api_call(
            f"warehouse/{warehouse_id}",
            name=name,
            connection=connection,
            method="PUT",
            schema_crawl_priority=schema_crawl_priority,
            **self._generate_schema_crawl_kwargs(
                schema_crawl_exclusion_list=schema_crawl_exclusion_list,
                schema_crawl_inclusion_list=schema_crawl_inclusion_list,
            ),
        )

    def delete_warehouse(self, warehouse_id: int):
        self._api_call(
            f"warehouse/{warehouse_id}", method="DELETE", empty_response=True
        )

    def refresh_warehouse(
        self, warehouse_id: int, schema_crawl_priority: str | None = None
    ):
        # If we pass schema_crawl_priority prior to v0.190.4 we will encounter
        # a 400 Bad Request error.
        data: dict[str, Any] = dict()
        if (
            schema_crawl_priority is not None
            and self.server_version not in ("test", "unknown")
            and self.server_version >= "v0.190.4"
        ):
            data |= dict(schema_crawl_priority=schema_crawl_priority)
        return self._api_call(f"warehouse/{warehouse_id}/refresh", method="PUT", **data)

    def refresh_warehouse_tables(
        self,
        warehouse_id: int,
        table_full_names: list[str],
        schema_crawl_priority: str | None = None,
    ):
        if not table_full_names:
            raise RuntimeError("Must specify a list of full table names to sync")
        return self._api_call(
            f"warehouse/{warehouse_id}/refresh",
            method="PUT",
            table_full_names=table_full_names,
            schema_crawl_priority=schema_crawl_priority,
        )

    def refresh_warehouse_new_tables(
        self, warehouse_id: int, schema_crawl_priority: str | None = None
    ):
        return self._api_call(
            f"warehouse/{warehouse_id}/refresh/new",
            method="PUT",
            schema_crawl_priority=schema_crawl_priority,
        )

    def list_notification_channels(self):
        return self._api_call("list_notification_channels")

    def configured_tables(
        self,
        check_cadence_type: str | None = None,
        warehouse_id: int | None = None,
        details: bool = True,
        limit: int = 0,
        offset: int = 0,
    ):
        return self._api_call(
            "configured_tables",
            check_cadence_type=check_cadence_type,
            warehouse_id=warehouse_id,
            details=details,
            limit=limit,
            offset=offset,
        )

    def tables(
        self,
        limit: int = 0,
        offset: int = 0,
        warehouse_id: int | None = None,
        # `label_id` is repeatable: a sequence matches tables carrying any of the ids
        label_id: int | Sequence[int] | None = None,
        without_access_groups: bool | None = None,
    ):
        """List tables. Pass label_id to filter by label; use UNLABELED_LABEL_ID
        to match tables with no labels."""
        params = {
            "limit": limit,
            "offset": offset,
            "warehouse_id": warehouse_id,
            "label_id": label_id,
            "without_access_groups": without_access_groups,
        }
        return self._api_call(
            "tables", **{k: v for k, v in params.items() if v is not None}
        )

    def filter_tables_by_label(self, label_id):
        return self._api_call(f"tables?label_id={label_id}")

    def get_table_information(self, warehouse_id=None, table_id=None, table_name=None):
        if (
            table_id
            or (  # Fully qualified with warehouse name
                table_name and table_name.count(".") >= 2
            )
            or (warehouse_id and table_name)
        ):
            return self._api_call(
                "get_table_information",
                warehouse_id=warehouse_id,
                table_id=table_id,
                table_name=table_name,
            )
        else:
            raise RuntimeError(
                "Must specify either table_id, a fully qualified table_name ('warehouse.schema.table'), or warehouse_id and table_name for get_table_information"
            )

    def create_table(
        self,
        name: str | None = None,
        *,
        anomalo_view_sql: str | None = None,
        warehouse_id: int,
        relation_type: str | None = None,
        schema: str | None = None,
        table: str | None = None,
    ):
        # Determine if we're using anomalo view parameters or table refresh parameters
        anomalo_view_params = name is not None or anomalo_view_sql is not None
        table_refresh_params = schema is not None or table is not None

        # Validation: Cannot mix anomalo view parameters with table refresh parameters
        if anomalo_view_params and table_refresh_params:
            raise ValueError(
                "schema and table parameters cannot be combined with name and anomalo_view_sql parameters"
            )

        # Validation: name and anomalo_view_sql are only allowed when relation_type is "anomalo_view" (if relation_type is specified)
        if (
            anomalo_view_params
            and relation_type is not None
            and relation_type.upper() != "ANOMALO_VIEW"
        ):
            raise ValueError(
                "name and anomalo_view_sql parameters are only allowed when relation_type is 'anomalo_view'"
            )

        # Auto-set relation_type to "ANOMALO_VIEW" if name or anomalo_view_sql is provided but relation_type is not set
        if anomalo_view_params and relation_type is None:
            relation_type = "ANOMALO_VIEW"

        # Build the API call parameters
        api_params = {"warehouse_id": warehouse_id}

        if name is not None:
            api_params["name"] = name
        if anomalo_view_sql is not None:
            api_params["anomalo_view_sql"] = anomalo_view_sql
        if relation_type is not None:
            api_params["relation_type"] = relation_type
        if schema is not None:
            api_params["schema"] = schema
        if table is not None:
            api_params["table"] = table

        return self._api_call(
            "tables",
            method="POST",
            **api_params,
        )

    def get_table_profile(
        self, warehouse_id=None, table_id=None, table_name=None, date=None
    ):
        if (
            table_id
            or (  # Fully qualified with warehouse name
                table_name and table_name.count(".") >= 2
            )
            or (warehouse_id and table_name)
        ):
            kwargs = {
                "warehouse_id": warehouse_id,
                "table_id": table_id,
                "table_name": table_name,
            }
            if date is not None:
                kwargs["date"] = date
            return self._api_call("get_table_profile", **kwargs)
        else:
            raise RuntimeError(
                "Must specify either table_id, a fully qualified table_name ('warehouse.schema.table'), or warehouse_id and table_name for get_table_profile"
            )

    def get_check_intervals(self, table_id=None, start=None, end=None):
        if not table_id:
            raise RuntimeError("Must specify a table_id for get_check_intervals")
        else:
            results = []
            page = 0
            paged_results = None
            while paged_results is None or len(paged_results) > 0:
                paged_results = self._api_call(
                    "get_check_intervals",
                    table_id=table_id,
                    start=start,
                    end=end,
                    page=page,
                )["intervals"]
                results.extend(paged_results)
                page = page + 1
            return results

    def get_checks_for_table(self, table_id, exclude_disabled=True):
        return self._api_call(
            "get_checks_for_table", table_id=table_id, exclude_disabled=exclude_disabled
        )

    def run_checks(
        self,
        table_id,
        interval_id=None,
        check_ids=None,
        force=False,
        respect_data_freshness_gate=False,
        execution_priority="high",
    ):
        if check_ids:
            if not isinstance(check_ids, list) and not isinstance(check_ids, tuple):
                check_ids = [check_ids]
            check_ids = list(check_ids)  # Convert from Tuple
            return self._api_call(
                "run_checks",
                method="POST",
                table_id=table_id,
                interval_id=interval_id,
                check_ids=check_ids,
                force=force,
                respect_data_freshness_gate=respect_data_freshness_gate,
                execution_priority=execution_priority,
            )
        else:
            return self._api_call(
                "run_checks",
                method="POST",
                table_id=table_id,
                interval_id=interval_id,
                force=force,
                respect_data_freshness_gate=respect_data_freshness_gate,
                execution_priority=execution_priority,
            )

    def get_run_result(self, job_id=None, check_run_id=None, include_mc_fields=False):
        if not job_id and not check_run_id:
            raise ValueError(
                "Must specify either run_checks_job_id or quality_check_run_id for get_run_result"
            )
        elif job_id and check_run_id:
            raise ValueError(
                "Only one of run_checks_job_id or quality_check_run_id should be provided"
            )
        else:
            return self._api_call(
                "get_run_result",
                run_checks_job_id=job_id,
                quality_check_run_id=check_run_id,
                include_mc_fields=include_mc_fields,
            )

    def get_run_result_triage_history(self, job_id):
        return self._api_call("get_run_result_triage_history", run_checks_job_id=job_id)

    def download_entity_time_series_csv_post(
        self,
        quality_check_run_id: int,
        entity_filter: dict,
        metric_name: str,
    ):
        return self._api_call(
            "download_entity_time_series_csv",
            method="POST",
            quality_check_run_id=quality_check_run_id,
            entity_filter=entity_filter,
            metric_name=metric_name,
        )

    def create_check(self, table_id, check_type, **params):
        return self._api_call(
            "create_check",
            table_id=table_id,
            check_type=check_type,
            method="POST",
            params=params,
        )

    def delete_check(self, table_id, check_id):
        return self._api_call(
            "delete_check",
            table_id=table_id,
            check_id=check_id,
            method="POST",
        )

    def clone_check(self, table_id, check_id, new_table_id):
        return self._api_call(
            "clone_check",
            table_id=table_id,
            check_id=check_id,
            new_table_id=new_table_id,
            method="POST",
        )

    def configure_table(
        self,
        table_id,
        *,
        check_cadence_type=None,
        definition=None,
        anomalo_view_sql=None,
        time_column_type=None,
        notify_after=None,
        time_columns=None,
        fresh_after=None,
        interval_skip_expr=None,
        notification_channel_id=None,
        notification_channel_ids=None,
        slack_users=None,
        check_cadence_run_at_duration=None,
        always_alert_on_errors=False,
        disabled_quality_check_ids=None,
        enable_data_quality=None,
        scope_of_data_to_check=None,
        use_auto_sla=None,
        enable_observability=None,
        custom_holidays=None,
    ):
        # Normalize time_columns: None or empty/blank strings -> []
        # Filter out blank strings and preserve valid columns
        if time_columns is not None and isinstance(time_columns, list):
            time_columns = [
                col for col in time_columns if col and str(col).strip()
            ] or []
        elif time_columns is None:
            time_columns = []
        slack_users = {} if slack_users is None else slack_users

        return self._api_call(
            "configure_table",
            table_id=table_id,
            method="POST",
            check_cadence_type=check_cadence_type,
            definition=definition,
            anomalo_view_sql=anomalo_view_sql,
            time_column_type=time_column_type,
            notify_after=notify_after,
            notification_channel_id=notification_channel_id,
            notification_channel_ids=notification_channel_ids,
            time_columns=time_columns,
            fresh_after=fresh_after,
            interval_skip_expr=interval_skip_expr,
            slack_users=slack_users,
            check_cadence_run_at_duration=check_cadence_run_at_duration,
            always_alert_on_errors=always_alert_on_errors,
            disabled_quality_check_ids=disabled_quality_check_ids,
            enable_data_quality=enable_data_quality,
            scope_of_data_to_check=scope_of_data_to_check,
            use_auto_sla=use_auto_sla,
            enable_observability=enable_observability,
            custom_holidays=custom_holidays,
        )

    # deprecated
    def create_table_label_for_organization(self, name):
        return self.create_label_for_organization(name)

    # deprecated
    def list_table_labels_for_organization(self):
        return self.list_labels_for_organization()

    # deprecated
    def update_table_label_name_for_organization(self, label_id, new_name):
        return self.update_label_name_for_organization(label_id, new_name)

    # deprecated
    def delete_table_label_for_organization(self, label_id):
        self.delete_label_for_organization(label_id)

    # deprecated
    def merge_table_labels_for_organization(
        self, source_label_id, destination_label_id
    ):
        return self.merge_labels_for_organization(source_label_id, destination_label_id)

    def create_label_for_organization(self, name, scope=None):
        if scope is None:
            scope = "everywhere"
        return self._api_call(
            "org_labels",
            method="POST",
            name=name,
            scope=scope,
        )

    def list_labels_for_organization(self, scope=None):
        if scope:
            return self._api_call(f"org_labels?scope={scope}")
        return self._api_call("org_labels")

    def update_label_name_for_organization(self, label_id, new_name):
        return self._api_call(
            f"org_labels/{label_id}",
            method="PATCH",
            name=new_name,
        )

    def update_label_scope_for_organization(self, label_id, new_scope):
        return self._api_call(
            f"org_labels/{label_id}",
            method="PATCH",
            scope=new_scope,
        )

    def delete_label_for_organization(self, label_id):
        self._api_call(
            f"org_labels/{label_id}",
            method="DELETE",
            empty_response=True,
        )

    def merge_labels_for_organization(self, source_label_id, destination_label_id):
        return self._api_call(
            f"org_labels/{destination_label_id}/merge",
            method="POST",
            source_label_id=source_label_id,
        )

    def replace_labels_for_check(self, check_id, labels, table_id=None):
        if not table_id:
            return self._api_call(
                f"checks/{check_id}/labels",
                method="PUT",
                empty_response=True,
                labels=labels,
            )
        return self._api_call(
            f"checks/{check_id}/labels",
            method="PUT",
            empty_response=True,
            labels=labels,
            table_id=table_id,
        )

    def add_new_labels_to_check(self, check_id, labels, table_id=None):
        if not table_id:
            return self._api_call(
                f"checks/{check_id}/labels",
                method="PATCH",
                empty_response=True,
                labels=labels,
            )
        return self._api_call(
            f"checks/{check_id}/labels",
            method="PATCH",
            empty_response=True,
            labels=labels,
            table_id=table_id,
        )

    def replace_labels_for_table(self, table_id, labels):
        return self._api_call(
            f"tables/{table_id}/labels",
            method="PUT",
            empty_response=True,
            labels=labels,
        )

    def add_new_labels_to_table(self, table_id, labels):
        return self._api_call(
            f"tables/{table_id}/labels",
            method="PATCH",
            empty_response=True,
            labels=labels,
        )

    def add_new_user(self, name, email, role, is_service_account=False):
        return self._api_call(
            "users",
            name=name,
            email=email,
            role=role,
            is_service_account=is_service_account,
            method="POST",
        )

    def list_users(self, limit=None, offset=None, without_access_groups=False):
        return self._api_call(
            "users",
            limit=limit,
            offset=offset,
            without_access_groups=without_access_groups,
            method="GET",
        )

    def get_user(self, user_id):
        return self._api_call(
            f"users/{user_id}",
            method="GET",
        )

    def list_user_access_groups(self, user_id, limit=None, offset=None):
        return self._api_call(
            f"users/{user_id}/access_groups",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def list_tables_from_user_access_groups(self, user_id, limit=None, offset=None):
        return self._api_call(
            f"users/{user_id}/access_groups/tables",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def list_user_api_keys(self, user_id, limit=None, offset=None):
        return self._api_call(
            f"users/{user_id}/api-keys",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def add_user_api_key(self, user_id, description, expires):
        return self._api_call(
            f"users/{user_id}/api-keys",
            description=description,
            expires=expires,
            method="POST",
        )

    def revoke_user_api_key(self, user_id, api_key_id):
        self._api_call(
            f"users/{user_id}/api-keys/{api_key_id}",
            method="DELETE",
            empty_response=True,
        )

    def list_api_keys_for_current_user(self, limit=None, offset=None):
        return self._api_call(
            "api-keys",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def create_api_key_for_current_user(self, description, expires):
        return self._api_call(
            "api-keys",
            description=description,
            expires=expires,
            method="POST",
        )

    def revoke_api_key_for_current_user(self, api_key_id):
        self._api_call(
            f"api-keys/{api_key_id}",
            method="DELETE",
            empty_response=True,
        )

    def add_table_lineage_edge(
        self,
        *,
        source_table_id=None,
        source_external_ref=None,
        source_display_name=None,
        source_data_source_name=None,
        source_description=None,
        source_url=None,
        destination_table_id=None,
        destination_external_ref=None,
        destination_display_name=None,
        destination_data_source_name=None,
        destination_description=None,
        destination_url=None,
    ):
        raw_source = dict(
            table_id=source_table_id,
            external_ref=source_external_ref,
            display_name=source_display_name,
            data_source_name=source_data_source_name,
            description=source_description,
            url=source_url,
        )
        pruned_source = {
            key: value for key, value in raw_source.items() if value is not None
        }

        raw_destination = dict(
            table_id=destination_table_id,
            external_ref=destination_external_ref,
            display_name=destination_display_name,
            data_source_name=destination_data_source_name,
            description=destination_description,
            url=destination_url,
        )
        pruned_destination = {
            key: value for key, value in raw_destination.items() if value is not None
        }

        return self._api_call(
            "table_lineage_edge",
            method="POST",
            empty_response=True,
            source=pruned_source,
            destination=pruned_destination,
        )

    def remove_table_lineage_edge(
        self,
        *,
        source_table_id=None,
        source_external_ref=None,
        destination_table_id=None,
        destination_external_ref=None,
    ):
        self._api_call(
            "table_lineage_edge",
            method="DELETE",
            empty_response=True,
            source_table_id=source_table_id,
            source_external_ref=source_external_ref,
            destination_table_id=destination_table_id,
            destination_external_ref=destination_external_ref,
        )

    def list_table_upstream_lineage(
        self, table_id, limit=None, offset=None, max_hops=None
    ):
        return self._api_call(
            f"tables/{table_id}/lineage/upstream",
            limit=limit,
            offset=offset,
            max_hops=max_hops,
            method="GET",
        )

    def list_table_downstream_lineage(
        self, table_id, limit=None, offset=None, max_hops=None
    ):
        return self._api_call(
            f"tables/{table_id}/lineage/downstream",
            limit=limit,
            offset=offset,
            max_hops=max_hops,
            method="GET",
        )

    def update_check(self, table_id, check_id=None, static_id=None, ref=None, **kwargs):
        if check_id is not None:
            return self._api_call(
                f"tables/{table_id}/checks/id/{check_id}",
                method="PATCH",
                empty_response=True,
                **kwargs,
            )
        elif static_id is not None:
            return self._api_call(
                f"tables/{table_id}/checks/static_id/{static_id}",
                method="PATCH",
                empty_response=True,
                **kwargs,
            )
        elif ref is not None:
            return self._api_call(
                f"tables/{table_id}/checks/ref/{ref}",
                method="PATCH",
                empty_response=True,
                **kwargs,
            )
        else:
            raise RuntimeError("Must specify check_id, static_id, or ref")

    def get_table_configuration(self, table_id):
        """Get the configuration for a specific table including custom_holidays."""
        return self._api_call(f"tables/{table_id}/config", method="GET")

    def update_table_configuration(self, table_id, **kwargs):
        return self._api_call(f"tables/{table_id}/config", method="PATCH", **kwargs)

    def bulk_update_table_configuration(self, filter, configuration, overwrite=False):
        return self._api_call(
            "tables/configure",
            method="POST",
            filter=filter,
            configuration=configuration,
            overwrite=overwrite,
        )

    def get_table_documentation(self, table_id):
        return self._api_call(
            f"tables/{table_id}/documentation",
            method="GET",
        )

    def replace_table_documentation(self, table_id, documentation):
        return self._api_call(
            f"tables/{table_id}/documentation",
            documentation=documentation,
            method="PUT",
            empty_response=True,
        )

    def get_sensitive_columns(self):
        return self._api_call("sensitive_columns")

    def add_sensitive_column(
        self,
        column_name: str,
        censor_for_all_tables: bool = False,
        table_id: int | None = None,
    ):
        return self._api_call(
            "sensitive_column",
            method="PUT",
            column_name=column_name,
            censor_for_all_tables=censor_for_all_tables,
            table_id=table_id,
        )

    def remove_sensitive_column(
        self,
        column_name: str,
        censor_for_all_tables: bool = False,
        table_id: int | None = None,
    ):
        return self._api_call(
            "sensitive_column",
            method="DELETE",
            column_name=column_name,
            censor_for_all_tables=censor_for_all_tables,
            table_id=table_id,
        )

    def create_access_group(self, name):
        return self._api_call("access_groups", name=name, method="POST")

    def get_access_group(self, access_group_id):
        return self._api_call(f"access_groups/{access_group_id}", method="GET")

    def delete_access_group(self, access_group_id):
        self._api_call(
            f"access_groups/{access_group_id}",
            method="DELETE",
            empty_response=True,
        )

    def update_access_group(self, access_group_id, name):
        return self._api_call(
            f"access_groups/{access_group_id}",
            name=name,
            method="PUT",
        )

    def create_access_group_policy(self, policy):
        return self._api_call("access_group_policies", method="POST", **policy)

    def get_access_group_policy(self, policy_id):
        return self._api_call(
            f"access_group_policies/{policy_id}",
            method="GET",
        )

    def list_access_group_policies(self, limit=None, offset=None):
        return self._api_call(
            "access_group_policies",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def update_access_group_policy(self, policy_id, policy):
        return self._api_call(
            f"access_group_policies/{policy_id}",
            method="PUT",
            **policy,
        )

    def delete_access_group_policy(self, policy_id):
        self._api_call(
            f"access_group_policies/{policy_id}", method="DELETE", empty_response=True
        )

    def attach_policy(self, access_group_id, policy_id):
        return self._api_call(
            f"access_groups/{access_group_id}/policies",
            method="POST",
            policy_id=policy_id,
        )

    def remove_policy(self, access_group_id, policy_id):
        return self._api_call(
            f"access_groups/{access_group_id}/policies/{policy_id}",
            method="DELETE",
            empty_response=True,
        )

    def add_users_to_access_group(self, access_group_id, *user_ids):
        return self._api_call(
            f"access_groups/{access_group_id}/users",
            method="POST",
            user_ids=user_ids,
            empty_response=True,
        )

    def remove_users_from_access_group(self, access_group_id, *user_ids):
        return self._api_call(
            f"access_groups/{access_group_id}/users",
            method="DELETE",
            user_id=user_ids,
            empty_response=True,
        )

    def list_access_groups(self, limit=None, offset=None):
        return self._api_call(
            "access_groups",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def list_access_group_tables(self, access_group_id, limit=None, offset=None):
        return self._api_call(
            f"access_groups/{access_group_id}/tables",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def add_tables_to_access_group(self, access_group_id, *table_ids):
        return self._api_call(
            f"access_groups/{access_group_id}/tables",
            method="POST",
            table_ids=table_ids,
            empty_response=True,
        )

    def remove_tables_from_access_group(self, access_group_id, *table_ids):
        return self._api_call(
            f"access_groups/{access_group_id}/tables",
            method="DELETE",
            table_id=table_ids,
            empty_response=True,
        )

    def add_table_to_access_group(self, access_group_id, table_id):
        return self._api_call(
            f"access_groups/{access_group_id}/tables/{table_id}",
            method="POST",
            empty_response=True,
        )

    def remove_table_from_access_group(self, access_group_id, table_id):
        self._api_call(
            f"access_groups/{access_group_id}/tables/{table_id}",
            method="DELETE",
            empty_response=True,
        )

    def list_access_group_users(self, access_group_id, limit=None, offset=None):
        return self._api_call(
            f"access_groups/{access_group_id}/users",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def add_user_to_access_group(self, access_group_id, user_id):
        return self._api_call(
            f"access_groups/{access_group_id}/users/{user_id}",
            method="POST",
            empty_response=True,
        )

    def remove_user_from_access_group(self, access_group_id, user_id):
        self._api_call(
            f"access_groups/{access_group_id}/users/{user_id}",
            method="DELETE",
            empty_response=True,
        )

    def list_table_access_groups(self, table_id, limit=None, offset=None):
        return self._api_call(
            f"tables/{table_id}/access_groups",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def list_table_access_group_users(self, table_id, limit=None, offset=None):
        return self._api_call(
            f"tables/{table_id}/access_groups/users",
            limit=limit,
            offset=offset,
            method="GET",
        )

    def get_task(self, task_id):
        return self._api_call(
            f"task/{task_id}",
            method="GET",
        )

    def poll_for_task_completion(self, task_id, *, timeout=30, interval=2):
        timeout_time = datetime.now() + timedelta(seconds=timeout)  # noqa: DTZ005 (call-datetime-now-without-tzinfo)
        while True:
            task_result = self.get_task(task_id=task_id)
            if task_result.get("state") in ["success", "failure"]:
                return task_result
            if datetime.now() > timeout_time:  # noqa: DTZ005 (call-datetime-now-without-tzinfo)
                raise Exception("Timeout exceeded")  # noqa: TRY002 (raise-vanilla-class)
            sleep(interval)

    def get_notification_channel(self, channel_id):
        return self._api_call(
            f"notification_channels/{channel_id}",
            method="GET",
        )

    def create_notification_channel(self, channel):
        return self._api_call(
            "notification_channels",
            method="POST",
            **channel,
        )

    def update_notification_channel(self, channel_id, channel):
        return self._api_call(
            f"notification_channels/{channel_id}",
            method="PATCH",
            **channel,
        )

    def delete_notification_channel(self, channel_id):
        self._api_call(
            f"notification_channels/{channel_id}",
            method="DELETE",
            empty_response=True,
        )
