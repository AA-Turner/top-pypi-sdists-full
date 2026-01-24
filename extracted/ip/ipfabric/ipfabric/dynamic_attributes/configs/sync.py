import json
from functools import cached_property
from typing import Optional, Literal, Any, Union, Callable, ForwardRef

import yaml
import yaml_include
from pydantic import BaseModel, Field, model_validator, ConfigDict, FilePath

from ipfabric.dynamic_attributes.configs.rules import (
    InventoryRule,
    DefaultRule,
    ConfigRule,
    TableRule,
    DefaultConfigRule,
)

try:
    import tomllib
except ImportError:
    import tomli as tomllib

Config = ForwardRef("Config")


class IPFabric(BaseModel):
    base_url: Optional[str] = Field(
        None,
        description="The IP Fabric Base URL to fetch data from (env: 'IPF_URL').",
        title="IP Fabric URL",
        examples=["https://demo.ipfabric.com"],
    )
    auth: Optional[str] = Field(
        None,
        description="The IP Fabric API token to use for authentication (env: 'IPF_TOKEN'). "
        "Username and password can be used by setting Environment Variables (IPF_USERNAME, IPF_PASSWORD).",
        title="IP Fabric API Token",
    )
    timeout: Optional[Union[int, tuple, float, None]] = Field(
        5,
        description="The timeout for the API requests; default 5 seconds (env: 'IPF_TIMEOUT').",
        title="IP Fabric Timeout",
    )
    verify: Union[bool, str] = Field(
        True, description="Verify SSL Certificates; default True (env: 'IPF_VERIFY').", title="SSL Verification"
    )
    snapshot_id: str = Field(
        "$last",
        description="The snapshot ID to use for the API endpoint; defaults to '$last'.",
        title="Snapshot ID",
        examples=["$last", "$prev", "$lastLocked", "d03a89d3-911b-4e2d-868b-8b8103771801"],
    )


class Config(BaseModel):  # noqa: F811
    model_config = ConfigDict(extra="allow")

    ipfabric: Optional[IPFabric] = Field(
        default_factory=IPFabric, description="IP Fabric connection configuration.", title="IP Fabric Connection"
    )
    dry_run: bool = Field(
        True, description="Defaults to run in dry-run mode and not apply any updates.", title="Dry Run"
    )
    update_snapshot: bool = Field(
        True,
        description="Update Local Attributes on the selected snapshot; default True.",
        title="Update Snapshot Attributes",
    )
    inventory: InventoryRule = Field(
        default_factory=InventoryRule,
        description="Optional: Filters to limit the inventory of devices based on Inventory > Devices table.",
        title="Inventory Filters",
    )
    default: Optional[DefaultRule] = Field(
        None,
        description="Optional: Default configuration to merge into all other Table Rules.",
        title="Default Table TableRule",
    )
    default_config: Optional[DefaultConfigRule] = Field(
        None,
        description="Optional: Default configuration to merge into all other Configuration Rules.",
        title="Default Configuration TableRule",
    )
    rules: list[Union[ConfigRule, TableRule]] = Field(
        description="List of Table or Configuration Rules which are processed in order; at least 1 rule is required.",
        title="Dynamic Attribute Rules",
    )

    @model_validator(mode="after")
    def _validate(self):
        if not self.rules:
            raise ValueError("At least one rule must be provided.")
        if len({_.name for _ in self.rules}) != len(self.rules):
            raise ValueError("Duplicate TableRule Names found.")
        if False in {bool(_.value) for _ in self.rules} and not self.default.value:
            raise ValueError("All Rules must have a value set or 'default[value]' can be used for Table Rules.")
        if False in {bool(_.attribute) for _ in self.rules if isinstance(_, TableRule)} and not self.default.attribute:
            raise ValueError(
                "An Attribute Name must be set in 'default[attribute]' or all Table rules must have it defined."
            )
        if (
            False in {bool(_.attribute) for _ in self.rules if isinstance(_, ConfigRule)}
            and not self.default_config.attribute
        ):
            raise ValueError(
                "An Attribute Name must be set in 'default_config[attribute]' "
                "or all Configuration Rules must have it defined."
            )
        return self

    @cached_property
    def merged_rules(self) -> list[Union[ConfigRule, TableRule]]:
        """Copy Defaults to rules"""
        return [
            rule.merge_default(self.default if isinstance(rule, TableRule) else self.default_config)
            for rule in self.rules
        ]

    def model_dump_merged(
        self,
        *,
        mode: Literal["json", "python"] = "python",
        context: Optional[Any] = None,
        by_alias: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: Union[bool, Literal["none", "warn", "error"]] = True,
        fallback: Optional[Callable[[Any], Any]] = None,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        """Dump the full config with all default rules merged."""
        config = self.model_copy(deep=True)
        config.rules = self.merged_rules
        return config.model_dump(
            mode=mode,
            exclude={"default", "default_config"},
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )

    def model_merged(self) -> "Config":
        """Return a copy of the merged config with all default rules merged."""
        config = self.model_copy(deep=True)
        config.rules = self.merged_rules
        config.default, config.default_config = None, None
        return config


Config.model_rebuild()


def my_loader(urlpath, file, Loader):
    if urlpath.lower().endswith(".json"):
        return json.load(file)
    if urlpath.lower().endswith(".toml"):
        return tomllib.load(file)
    if urlpath.lower().endswith((".yaml", ".yml")):
        return yaml.load(file, Loader)
    raise ValueError("Unsupported config file format. Use .yaml, .yml, .json, or .toml.")


def load_config(file: FilePath) -> Config:
    try:
        if (suffix := file.suffix.lower()) in (".yaml", ".yml"):
            yaml.add_constructor("!inc", yaml_include.Constructor(custom_loader=my_loader), Loader=yaml.SafeLoader)
            with open(file, "r", encoding="utf8") as f:
                return Config(**yaml.safe_load(f), filename=file.name)
        elif suffix == ".json":
            with open(file, "r", encoding="utf8") as f:
                return Config(**json.load(f), filename=file.name)
        elif suffix == ".toml":
            with open(file, "rb") as f:
                return Config(**tomllib.load(f), filename=file.name)
        else:
            raise ValueError("Unsupported config file format. Use .yaml, .yml, .json, or .toml.")
    except (yaml.YAMLError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        raise type(exc)(f"Error parsing {str(file)} file: {exc}")


class MultiConfig(BaseModel):
    """Model to handle multiple configurations."""

    configs: list[Union[Config, FilePath]] = Field(
        title="IP Fabric Dynamic Attribute Configurations",
        description="Ordered list of Configurations to process; at least one configuration is required. "
        "IPFabric ['base_url', 'auth', 'verify', 'snapshot_id'] values must be the same in all config files; "
        "recommended to leave empty and use environment variables.",
    )
    dry_run_override: Optional[bool] = Field(
        None,
        description="Defaults to use the 'dry_run' value from the configs; values in all the configs must be the same. "
        "If set to a boolean value then it will override the config values.",
        title="Override Dry Run",
    )
    update_snapshot_override: Optional[bool] = Field(
        None,
        description="Defaults to use the 'update_snapshot' value from the configs; "
        "values in all the configs must be the same. "
        "If set to a boolean value then it will override the config values.",
        title="Update Snapshot Attributes",
    )
    ipfabric_override: Optional[IPFabric] = Field(
        None,
        description="Defaults to use the 'ipfabric' value from the configs; "
        "values in all the configs must be the same. "
        "If an IP Fabric configuration is passed in then the value will ignore the individual the configs.",
        title="IP Fabric Connection",
    )

    def _get_ipfabric_config(self, attr: str) -> list[Any]:
        """Get a unique attribute from all configurations."""
        return list(
            {getattr(_.ipfabric, attr) for _ in self.configs if _.ipfabric and getattr(_.ipfabric, attr) is not None}
        )

    @model_validator(mode="after")
    def _validate(self):
        if not self.configs:
            raise ValueError("At least one configuration must be provided.")
        self.configs = [_ if isinstance(_, Config) else load_config(_) for _ in self.configs]
        if not self.ipfabric_override:
            for attr in ["base_url", "auth", "verify", "snapshot_id"]:
                if len(self._get_ipfabric_config(attr)) > 1:
                    raise ValueError(
                        "All IPFabric settings must have the same ['base_url', 'auth', 'verify', 'snapshot_id'] values."
                        " Alternatively, you can set 'ipfabric_override' to a single IPFabric configuration."
                    )
        if self.dry_run_override is None and len({_.dry_run for _ in self.configs}) > 1:
            raise ValueError(
                "All configurations must have the same 'dry_run' value. "
                "Alternatively, you can set 'dry_run_override' to a boolean value."
            )
        if self.update_snapshot_override is None and len({_.update_snapshot for _ in self.configs}) > 1:
            raise ValueError(
                "All configurations must have the same 'update_snapshot' value. "
                "Alternatively, you can set 'update_snapshot_override' to a boolean value."
            )
        return self

    @staticmethod
    def _merge_timeout(timeouts: set) -> Union[int, tuple, float, None]:
        """Merge timeouts from a set of timeouts using the largest value or None."""
        if None in timeouts or 0 in timeouts:
            return None
        elif t := {_ for _ in timeouts if isinstance(_, (int, float))}:
            return sorted(t, reverse=True)[0]
        return sorted(timeouts)[0]

    def _merge_ipf_settings(self) -> IPFabric:
        """Merge IPFabric settings."""
        base_url = self._get_ipfabric_config("base_url")
        auth = self._get_ipfabric_config("auth")
        verify = self._get_ipfabric_config("verify")
        snapshot_id = self._get_ipfabric_config("snapshot_id")
        return IPFabric(
            base_url=base_url[0] if base_url else None,
            auth=auth[0] if auth else None,
            verify=verify[0] if verify else None,
            timeout=self._merge_timeout(set(self._get_ipfabric_config("timeout"))),
            snapshot_id=snapshot_id[0] if snapshot_id else None,
        )

    def merge_configs(self) -> Config:
        """Merge all configurations into a single config file."""
        rules = []
        reports = set()
        for idx, config in enumerate(self.configs):
            prefix = config.model_extra.get("filename", f"config_{idx}")
            merged = config.model_merged()
            reports.update(set(merged.inventory.report_columns))
            for rule in merged.rules:
                rule.name = f"{prefix}: {rule.name}"
                rule.inventory = merged.inventory
            rules.extend(merged.rules)

        return Config(
            ipfabric=self.ipfabric_override or self._merge_ipf_settings(),
            dry_run=self.configs[0].dry_run if self.dry_run_override is None else self.dry_run_override,
            update_snapshot=(
                self.configs[0].update_snapshot
                if self.update_snapshot_override is None
                else self.update_snapshot_override
            ),
            inventory=InventoryRule(report_columns=list(reports)),
            rules=rules,
        )
