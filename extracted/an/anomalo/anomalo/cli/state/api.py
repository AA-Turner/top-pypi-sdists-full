from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Sequence
from contextlib import suppress
from functools import cached_property
from time import sleep
from typing import Any, List

from ...client import Client
from ...result import BadRequestException
from ..state.system_check import check_type_to_ref
from .errors import (
    CheckNotFound,
    InvalidTableRef,
    TableNotFound,
    UnknownTableLabels,
)
from .filters import TableFilters
from .models import (
    Action,
    Check,
    CheckAction,
    LabelAction,
    NotificationChannelAction,
    State,
    TableConfigAction,
)
from .plan import ResourceKey


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
        # Server reads, cached per table ref so a write can invalidate just the
        # table it wrote. These were `lru_cache` on the methods, which keys on
        # `self` — so `cache_clear()` wiped every table of every driver in the
        # process, and the cache kept drivers alive for the life of the process.
        self._table_cache: dict[str, dict[str, Any]] = {}
        self._checks_cache: dict[str, List[dict[str, Any]]] = {}

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
        # Remove the default notification channel, as it is not used in the state
        params.pop("notification_channel", None)

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
        self._dispatch_action(action)
        # Any write can change the table's configuration or its set of checks, and
        # a later action in the same apply has to see it. Invalidating here — once,
        # in the one place that knows a write happened — is what removes the class
        # of bug where a new dispatch branch forgets its own cache_clear().
        if action.table_ref:
            self._invalidate_table(action.table_ref)

    def _dispatch_action(self, action: Action) -> None:
        if isinstance(action, TableConfigAction):
            if action.new:
                self.client.configure_table(
                    table_id=self._table_id(action.table_ref), **action.new
                )
        elif isinstance(action, CheckAction):
            if action.new and action.is_system_check:
                # Falling through to create_check when the id is missing is what
                # the API rejects with "'DataFreshness' is not a valid check type".
                check_id = self._resolve_check_id(action)
                if not check_id:
                    print(
                        f"Warning: Skipping {action.check_ref} on "
                        f"{action.table_ref} (check does not exist)",
                        file=sys.stderr,
                    )
                    return
                self.client.update_check(
                    table_id=self._table_id(action.table_ref),
                    check_id=check_id,
                    config={
                        "params": action.new.params,
                    },
                )
            elif (
                action.new and action.check_ref
            ):  # Update or create a user created check
                params = {**action.new.params, "ref": action.check_ref}
                self.client.create_check(
                    self._table_id(action.table_ref),
                    action.new.check_type,
                    **params,
                )
            elif not action.is_system_check:  # System checks cannot be destroyed
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
            if action.check_ref:
                check_id = self._resolve_check_id(action)
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

            if action.check_ref and action.table_ref:
                check_id = self._resolve_check_id(action)
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
                # PATCH, not POST configure_table: the latter is a full replace, so
                # sending only the channels here would blank every field the table
                # config action just wrote — silently deconfiguring the table.
                self.client.update_table_configuration(
                    table_id=self._table_id(action.table_ref),
                    notification_channel_ids=notification_channel_ids,
                )

    def is_resource_present(self, key: ResourceKey) -> bool:
        """Whether the server already holds the state a `ResourceKey` names.

        The planner calls this only for prerequisites a plan does not itself create,
        so the cost is one (cached) lookup per prerequisite that would otherwise
        have been assumed to exist.
        """
        if key[0] not in ("check", "system_check"):
            return True  # pragma: no cover - only check keys are prerequisites
        table_ref, check_ref = key[1], key[2]
        # Either variant counts. `_resolve_check_id` falls back across both, so
        # anything the executor could resolve must not be called unsatisfiable.
        return (
            self._checks_for_table_by_ref(table_ref).get(check_ref) is not None
            or self.get_system_check_id(table_ref, check_ref) is not None
        )

    def _resolve_check_id(
        self, action: CheckAction | LabelAction | NotificationChannelAction
    ) -> int | None:
        """Resolve a check's id from live server state, never from the plan.

        Ids are unresolvable while planning for anything created during the same
        apply — the server materializes a table's system checks as a side effect of
        configuring it — so every id comes from a fresh (cached) lookup here.

        The variant the action targets decides which namespace is searched first.
        System and user checks share a ref namespace, so searching user checks
        first would resolve a system-check action to a colliding user check. The
        other namespace stays as a fallback for refs the file classified wrongly.
        """
        user_check_id = (
            self._checks_for_table_by_ref(action.table_ref)
            .get(action.check_ref, {})
            .get("check_id")
        )
        system_check_id = self.get_system_check_id(action.table_ref, action.check_ref)
        if action.is_system_check:
            return system_check_id or user_check_id
        return user_check_id or system_check_id

    def get_system_check_id(self, table_ref: str, check_ref: str) -> int | None:
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
    def _warehouse_names_by_id(self) -> dict[int, str]:
        return {wh_id: wh_name for wh_name, wh_id in self._warehouses.items()}

    @cached_property
    def _tables(self) -> dict[str, int]:
        return self._fetch_tables()

    def pull_table_refs(self, filters: TableFilters) -> set[str]:
        """Table refs to pull when none are given explicitly on the command line."""
        label_ids = self._table_label_ids(filters.table_labels)
        # Each filter that the server can answer contributes a set of refs, and the
        # result is their intersection; the rest are predicates on the ref itself.
        refs: set[str] | None = None
        if filters.configured_only:
            refs = self._fetch_configured_table_refs(filters.warehouse_id)
        if label_ids:
            labeled = set(self._fetch_tables(filters.warehouse_id, label_ids=label_ids))
            refs = labeled if refs is None else refs & labeled
        if refs is None:
            refs = (
                self.table_refs
                if filters.warehouse_id is None
                else set(self._fetch_tables(filters.warehouse_id))
            )
        return {ref for ref in refs if filters.matches_ref(ref)}

    def _table_label_ids(self, label_names: Sequence[str]) -> list[int]:
        if not label_names:
            # Resolving nothing would still pay for a `list_labels_for_organization`
            # call on every unfiltered pull.
            return []
        labels_by_name = self._org_labels_by_name
        unknown = [name for name in label_names if name not in labels_by_name]
        if unknown:
            raise UnknownTableLabels(unknown)
        return [labels_by_name[name]["id"] for name in label_names]

    @retry_requests
    def _fetch_tables(
        self,
        warehouse_id: int | None = None,
        label_ids: Sequence[int] | None = None,
    ) -> dict[str, int]:
        base_kwargs: dict[str, Any] = {}
        if warehouse_id is not None:
            base_kwargs["warehouse_id"] = warehouse_id
        if label_ids:
            # `label_id` is repeatable on the endpoint and matches any of the ids
            base_kwargs["label_id"] = list(label_ids)
        request_kwargs = dict(base_kwargs)
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
            # Page links only carry limit/offset, so any filter must be re-applied
            request_kwargs = base_kwargs | result.pages["next"]
        return all_tables

    @retry_requests
    def _fetch_configured_table_refs(self, warehouse_id: int | None = None) -> set[str]:
        base_kwargs: dict[str, Any] = {"details": False}
        if warehouse_id is not None:
            base_kwargs["warehouse_id"] = warehouse_id
        request_kwargs = dict(base_kwargs)
        table_refs: set[str] = set()
        while True:
            result = self.client.configured_tables(**request_kwargs)
            for row in result:
                table = row["table"]
                # Unknown ids are warehouses with non-unique names, excluded above
                warehouse_name = self._warehouse_names_by_id.get(table["warehouse_id"])
                if warehouse_name:
                    table_refs.add(f"{warehouse_name}.{table['full_name']}")
            if "next" not in result.pages:
                break
            request_kwargs = base_kwargs | result.pages["next"]
        return table_refs

    def _table_id(self, table_ref: str) -> int:
        return self._table_raw(table_ref)["id"]

    def _table_raw(self, table_ref: str) -> dict[str, Any]:
        if table_ref not in self._table_cache:
            self._table_cache[table_ref] = self._fetch_table_raw(table_ref)
        return self._table_cache[table_ref]

    @retry_requests
    def _fetch_table_raw(self, table_ref: str) -> dict[str, Any]:
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

    def _checks_for_table(self, table_ref: str) -> List[dict[str, Any]]:
        if table_ref not in self._checks_cache:
            self._checks_cache[table_ref] = self._fetch_checks_for_table(table_ref)
        return self._checks_cache[table_ref]

    @retry_requests
    def _fetch_checks_for_table(self, table_ref: str) -> List[dict[str, Any]]:
        return self.client.get_checks_for_table(
            table_id=self._table_id(table_ref), exclude_disabled=False
        )["checks"]

    def _invalidate_table(self, table_ref: str) -> None:
        """Forget cached server state for one table, after writing to it."""
        self._table_cache.pop(table_ref, None)
        self._checks_cache.pop(table_ref, None)

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
