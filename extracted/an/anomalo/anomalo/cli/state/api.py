from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Sequence
from contextlib import suppress
from functools import cached_property, lru_cache
from time import sleep
from typing import Any, List

from ...client import Client
from ...result import BadRequestException
from ..state.system_check import check_type_to_ref
from .errors import CheckNotFound, InvalidTableRef, TableNotFound
from .models import (
    Action,
    Check,
    CheckAction,
    LabelAction,
    NotificationChannelAction,
    State,
    TableConfigAction,
)


def _normalize_time_columns_for_pull(time_columns):
    """Normalize time_columns for pull operations (API -> YAML).

    Returns None if time_columns is empty, has only blank strings, or is already None.
    Otherwise returns a list of non-empty strings.
    """
    if time_columns is None:
        return None
    non_empty = [col for col in time_columns if col and str(col).strip()]
    return non_empty if non_empty else None


def retry_requests(f):
    try_times = 3

    def wrapper(*args, **kwargs):
        for i in range(try_times):
            try:
                return f(*args, **kwargs)
            except BadRequestException:
                raise
            except RuntimeError:
                if i >= try_times - 1:
                    # Last retry, re-raise exception
                    raise
                amount = 2 * (i + 1)
                sleep(amount)

    return wrapper


class APIDriver:
    def __init__(self, client: Client):
        self.client = client
        self.state = State()

    def load_table(self, table_ref: str) -> None:
        if self.state.tables[table_ref].config:
            return
        table_info = self._table_raw(table_ref)
        config = (
            self._filter_table_config_response(table_info.get("config") or {}) or {}
        )

        # Normalize time_columns to None if empty or contains only blank strings
        if "time_columns" in config:
            config["time_columns"] = _normalize_time_columns_for_pull(
                config["time_columns"]
            )

        # Include anomalo_view_sql from top level API response if present
        anomalo_view_sql = table_info.get("anomalo_view_sql")
        if anomalo_view_sql is not None:
            config["anomalo_view_sql"] = anomalo_view_sql

        self.state.tables[table_ref].config = config
        self.state.tables[table_ref].labels = [
            label.get("name") for label in table_info.get("labels", [])
        ]

        notification_channels = table_info.get("notification_channels")
        if len(notification_channels) == 1 and notification_channels[0]["is_default"]:
            notification_channels = []

        self.state.tables[table_ref].notification_channels = [
            notification_channel["ref"]
            for notification_channel in notification_channels
        ]

    def load_non_system_checks(self, table_ref: str) -> None:
        for check_ref, raw_check in self._checks_for_table_by_ref(table_ref).items():
            check = self.load_raw_check(raw_check)
            self.state.tables[table_ref].checks[check_ref] = check

    def load_system_checks(self, table_ref: str) -> None:
        for check_ref, raw_check in self._checks_for_table_by_ref(
            table_ref, system=True
        ).items():
            check = self.load_raw_check(raw_check)
            self.state.tables[table_ref].system_checks[check_ref] = check

    def load_single_check(self, table_ref: str, check_ref: str) -> None:
        non_system = self._checks_for_table_by_ref(table_ref)
        system = self._checks_for_table_by_ref(table_ref, system=True)
        raw_check = non_system.get(check_ref) or system.get(check_ref)

        if raw_check is None:
            raise CheckNotFound(table_ref, check_ref)

        check = self.load_raw_check(raw_check)

        if check_ref in non_system:
            self.state.tables[table_ref].checks[check_ref] = check
        else:
            self.state.tables[table_ref].system_checks[check_ref] = check

    def load_raw_check(self, raw_check: dict[str, Any]) -> Check:
        params = {
            **(raw_check["config"].get("params") or {}),
        }
        if "notification_channel" in params:
            # Remove the default notification channel, as it is not used in the state
            del params["notification_channel"]

        notification_channel_ids = raw_check.get(
            "additional_notification_channel_ids", []
        )
        notification_channels = [
            self._notification_channels_by_id[id]
            for id in notification_channel_ids
            if id in self._notification_channels_by_id
        ]

        return Check(
            check_type=raw_check["check_type"],
            params=params,
            labels=[label.get("name") for label in raw_check.get("labels", [])],
            notification_channels=[
                notification_channel["ref"]
                for notification_channel in notification_channels
            ],
        )

    def load_from_state(self, other_state: State) -> None:
        for table_ref, table in other_state.tables.items():
            if table.config:
                self.load_table(table_ref)
            for check_ref in table.checks.keys():
                with suppress(CheckNotFound):
                    self.load_single_check(table_ref, check_ref)

            # Unlike with non-system checks, we always load system checks
            # since they can't be maintained specially by the user
            self.load_system_checks(table_ref)

    def apply_action(self, action: Action) -> None:
        if isinstance(action, TableConfigAction):
            if action.new:
                self.client.configure_table(
                    table_id=self._table_id(action.table_ref), **action.new
                )
                self._table_raw.cache_clear()  # pragma: no cover
                self._checks_for_table.cache_clear()  # pragma: no cover
        elif isinstance(action, CheckAction):
            if action.new and action.check_id:  # Update a system check
                self.client.update_check(
                    table_id=self._table_id(action.table_ref),
                    check_id=action.check_id,
                    config={
                        "params": action.new.params,
                    },
                )
            elif (
                action.new and action.check_ref
            ):  # Update or create a user created check
                params = {**action.new.params, **{"ref": action.check_ref}}
                self.client.create_check(
                    self._table_id(action.table_ref),
                    action.new.check_type,
                    **params,
                )
                # Clear the cache so subsequent actions can find the newly created check
                self._checks_for_table.cache_clear()
            elif not action.check_id:  # System checks cannot be destroyed
                check_id = self._checks_for_table_by_ref(action.table_ref)[
                    action.check_ref
                ]["check_id"]
                self.client.delete_check(
                    self._table_id(action.table_ref),
                    # Current check ID for this check
                    self._checks_for_table_by_ref(action.table_ref)[action.check_ref][
                        "check_id"
                    ],
                )
        elif isinstance(action, LabelAction):
            labels = action.new or []
            labels_being_added = set(labels) - set(action.prev or [])
            labels_by_name = self._org_labels_by_name

            # For each label being added, we need to create it if it doesn't exist
            for label in labels_being_added:
                if not labels_by_name.get(label):
                    labels_by_name[label] = self.client.create_label_for_organization(
                        label, "everywhere"
                    )
                else:
                    # We need to check that the scope is correct
                    scope = labels_by_name[label].get("scope")
                    label_id = labels_by_name[label]["id"]

                    wrong_scope = (
                        action.check_ref is None
                        and scope != "table"
                        and scope != "everywhere"
                    ) or (
                        action.check_ref and scope != "check" and scope != "everywhere"
                    )
                    if wrong_scope:
                        self.client.update_label_scope_for_organization(
                            label_id, "everywhere"
                        )

            table_id = self._table_id(action.table_ref)
            if action.check_id or action.check_ref:
                check_id = (
                    action.check_id
                    or self._checks_for_table_by_ref(action.table_ref)
                    .get(action.check_ref, {})
                    .get("check_id")
                    or self.get_system_check_id(action.table_ref, action.check_ref)
                )
                if not check_id:
                    print(
                        f"Warning: Skipping labels for {action.check_ref} on "
                        f"{action.table_ref} (check does not exist)",
                        file=sys.stderr,
                    )
                    return
                self.client.replace_labels_for_check(
                    table_id=table_id,
                    check_id=check_id,
                    labels=[labels_by_name[label]["id"] for label in labels],
                )
            else:
                self.client.replace_labels_for_table(
                    table_id=table_id,
                    labels=[labels_by_name[label]["id"] for label in labels],
                )
        elif isinstance(action, NotificationChannelAction):
            invalid_refs = []
            valid_channels = []

            for channel_ref_or_id in action.new or []:
                channel = self._notification_channels_by_ref.get(
                    channel_ref_or_id
                ) or self._notification_channels_by_id.get(channel_ref_or_id)
                if channel is None:
                    invalid_refs.append(channel_ref_or_id)
                else:
                    valid_channels.append(channel)

            if invalid_refs:
                refs_str = ", ".join(f'"{ref}"' for ref in invalid_refs)
                print(
                    f"Warning: The following notification channel refs do not exist: {refs_str}",
                    file=sys.stderr,
                )

            notification_channel_ids = [channel["id"] for channel in valid_channels]

            if (action.check_id or action.check_ref) and action.table_ref:
                check_id = (
                    action.check_id
                    or self._checks_for_table_by_ref(action.table_ref)
                    .get(action.check_ref, {})
                    .get("check_id")
                    or self.get_system_check_id(action.table_ref, action.check_ref)
                )
                if not check_id:
                    print(
                        f"Warning: Skipping notification channels for "
                        f"{action.check_ref} on {action.table_ref} "
                        f"(check does not exist)",
                        file=sys.stderr,
                    )
                    return
                self.client.update_check(
                    table_id=self._table_id(action.table_ref),
                    check_id=check_id,
                    additional_notification_channel_ids=notification_channel_ids,
                )
            elif action.table_ref:
                # Get existing table config to preserve time column settings
                table_info = self._table_raw(action.table_ref)
                config = table_info.get("config") or {}  # pragma: no cover

                self.client.configure_table(
                    table_id=self._table_id(action.table_ref),
                    notification_channel_ids=notification_channel_ids,
                    time_columns=config.get("time_columns"),
                    time_column_type=config.get("time_column_type"),
                )

    def get_system_check_id(self, table_ref: str, check_ref: List[str]) -> int | None:
        raw_check = self._checks_for_table_by_ref(table_ref, system=True).get(check_ref)
        if not raw_check:
            return None
        return raw_check["check_id"]

    @cached_property
    def table_refs(self) -> set[str]:
        return set(self._tables.keys())

    @cached_property
    @retry_requests
    def _warehouses_raw(self) -> Sequence[tuple[int, str]]:
        return [
            (w["id"], w["name"]) for w in self.client.list_warehouses()["warehouses"]
        ]

    @cached_property
    def _warehouses(self) -> dict[str, int]:
        warehouse_counts = defaultdict(int)
        for _, wh_name in self._warehouses_raw:
            warehouse_counts[wh_name] += 1
        # Exclude non-unique warehouse names
        duplicates = {
            wh_name for wh_name, count in warehouse_counts.items() if count > 1
        }
        ret = {
            wh_name: wh_id
            for wh_id, wh_name in self._warehouses_raw
            if wh_name not in duplicates
        }
        return ret

    @cached_property
    def _warehouse_names(self) -> set[str]:
        return set(self._warehouses.keys())

    @cached_property
    @retry_requests
    def _tables(self) -> dict[str, int]:
        request_kwargs: dict[str, int] = {}
        all_tables: dict[str, int] = {}
        while True:
            result = self.client.tables(**request_kwargs)
            all_tables |= {
                f"{table['warehouse']['name']}.{table['full_name']}": table["id"]
                for table in result
                if table["warehouse"]["name"] in self._warehouse_names
            }
            if "next" not in result.pages:
                break
            request_kwargs = result.pages["next"]
        return all_tables

    def _table_id(self, table_ref: str) -> int:
        return self._table_raw(table_ref)["id"]

    @lru_cache(maxsize=None)
    @retry_requests
    def _table_raw(self, table_ref: str) -> dict[str, Any]:
        warehouse_name, table_name = self._table_ref_parts(table_ref)
        try:
            return self.client.get_table_information(
                warehouse_id=self._warehouses[warehouse_name], table_name=table_name
            )
        except KeyError as e:
            raise TableNotFound(table_ref) from e

    def _table_ref_parts(self, table_ref: str) -> tuple[str, str]:
        try:
            warehouse, schema, table = table_ref.rsplit(".", 2)
        except ValueError as e:
            raise InvalidTableRef(table_ref) from e
        return (warehouse, f"{schema}.{table}")

    def _filter_table_config_response(self, response: dict[str, Any]) -> dict[str, Any]:
        return {
            k: v
            for k, v in response.items()
            if k
            not in {
                "table_id",
                "last_edited_at",
                "last_edited_by",
                "created",
                "created_by",
                "slack_users",
                "notification_channel_id",
                "notification_channel_ids",
            }
        }

    def _checks_for_table_by_ref(self, table_ref: str, system=False) -> dict[str, Any]:
        checks = self._checks_for_table(table_ref)

        if not system:
            return {check["ref"]: check for check in checks if check["ref"]}

        return {
            check_type_to_ref(check["check_type"]): check
            for check in checks
            if not check["ref"]
        }

    @lru_cache(maxsize=None)
    @retry_requests
    def _checks_for_table(self, table_ref: str) -> List[dict[str, Any]]:
        return self.client.get_checks_for_table(
            table_id=self._table_id(table_ref), exclude_disabled=False
        )["checks"]

    @cached_property
    @retry_requests
    def _org_labels(self) -> List[Any]:
        return self.client.list_labels_for_organization()

    @cached_property
    def _org_labels_by_name(self) -> dict[str, Any]:
        return {label["name"]: label for label in self._org_labels}

    @cached_property
    @retry_requests
    def _notification_channels(self) -> List[dict[str, Any]]:
        return self.client.list_notification_channels()["notification_channels"]

    @cached_property
    def _notification_channels_by_id(self) -> dict[str, dict[str, Any]]:
        return {channel["id"]: channel for channel in self._notification_channels}

    @cached_property
    def _notification_channels_by_ref(self) -> dict[str, dict[str, Any]]:
        return {channel["ref"]: channel for channel in self._notification_channels}
