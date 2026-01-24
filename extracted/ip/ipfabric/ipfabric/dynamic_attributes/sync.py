from collections import defaultdict
from pathlib import Path
from typing import Any, Union

from ipfabric import IPFClient
from ipfabric.settings.attributes import Attributes
from pandas import DataFrame
from pydantic import BaseModel, PrivateAttr, FilePath, Field

from ipfabric.dynamic_attributes.configs import Config, TableRule, ConfigRule, MultiConfig, InventoryRule, load_config
from ipfabric.dynamic_attributes.models import Attribute, MatchedRule, MatchedConfig, CONFIG_MAP


class AttributeSync(BaseModel):
    config: Union[MultiConfig, Config, FilePath, list[Union[Config, FilePath]]] = Field(
        title="Configuration File(s)",
        description="Path to the configuration file, Config object, or an ordered list of files or objects. "
        "Supports YAML, JSON, and TOML formats.",
    )
    _client: IPFClient = PrivateAttr(None)
    _attributes: dict[str, Attribute] = PrivateAttr(default_factory=dict)
    _endpoints_map: dict[str, str] = PrivateAttr(default_factory=dict)
    _endpoints: dict[str, set[str]] = PrivateAttr(default_factory=dict)
    _inventory: dict[int, set[str]] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        # If a single Config object is provided in a list, use it directly
        self.config = self.config[0] if isinstance(self.config, list) and len(self.config) == 1 else self.config
        if isinstance(self.config, MultiConfig):
            self.config = self.config.merge_configs()
        elif isinstance(self.config, list):
            # If a list of configs is provided, merge them into a single config
            multi = MultiConfig(configs=[_ if isinstance(_, Config) else load_config(_) for _ in self.config])
            self.config = multi.merge_configs()
        elif isinstance(self.config, Path):
            self.config = load_config(self.config)
        self._setup()

    def _validate(self, endpoints: dict[str, set[str]], dev_filters: Union[None, dict[str, set[str]]]) -> None:
        for url, columns in endpoints.items():
            if url not in self._client.oas:
                raise ValueError(f"API endpoint {url} not found in IP Fabric API.")
            if invalid := columns - set(self._client.oas[url].post.columns):
                raise ValueError(f"API endpoint '{url}' does not contain column(s): {invalid}.")
            if (
                dev_filters
                and hasattr(self._client.oas[url].post, "device_filters")
                and (invalid := dev_filters.get(url, set()) - set(self._client.oas[url].post.device_filters))
            ):
                # Added in SDK 7.2
                raise ValueError(f"API endpoint '{url}' does not contain device filter(s): {invalid}.")

    def _calculate_inventory(self, rule: Union[TableRule, ConfigRule, InventoryRule]) -> set[str]:
        # Get the filtered list of Inventory Devices for attribute calculation
        if rule.filter_hash in self._inventory:
            return self._inventory[rule.filter_hash]
        self._inventory[rule.filter_hash] = {
            _["sn"] for _ in self._client.inventory.devices.all(filters=rule.calc_filter, columns=["sn"])
        }
        return self._inventory[rule.filter_hash]

    def _setup(self) -> None:
        self._client = IPFClient(**self.config.ipfabric.model_dump())
        self._endpoints, dev_filters = defaultdict(set), defaultdict(set)

        # Validate the inventory filters
        self._validate(
            {
                "tables/inventory/devices": {
                    *{_.column for _ in self.config.inventory.filters},
                    *self.config.inventory.calc_columns,
                }
            },
            None,
        )

        # Validate the endpoints and device filters
        for rule in self.config.merged_rules:
            if isinstance(rule, ConfigRule):
                continue
            # Get all API endpoints from the rules and the columns required for each endpoint
            url = self._client._check_url(rule.value.api_endpoint)
            self._endpoints_map[rule.value.api_endpoint] = url
            endpoint = self._endpoints[url]
            endpoint.add(rule.value.sn)  # Add the serial number column
            if rule.value.column:
                endpoint.add(rule.value.column)
            if rule.value.sort:
                endpoint.add(rule.value.sort.column)
            for _ in rule.filters:
                endpoint.add(_.column)
            for _ in rule.device_filters:
                # If the filter is a device filter, add it to the dev_filters
                dev_filters[url].add(f"device.{_.column}")
        self._validate(self._endpoints, dev_filters)

        # Verify Attribute Names are formatted correctly
        attribute_names = {r.attribute for r in self.config.merged_rules}
        self._client.settings.global_attributes.check_attribute_name(attribute_names)

        # Get the filtered list of Inventory Devices for attribute calculation
        inventory = self._calculate_inventory(self.config.inventory)
        self._attributes = {_.sn: Attribute(device=_) for _ in self._client.devices.all if _.sn in inventory}

    def run(self) -> DataFrame:
        """Run the attribute sync process and return the report DataFrame."""
        self.calculate_attribute()
        report = self.report()
        return report if self.config.dry_run else self.apply_attributes(report)

    def _delete_attributes(self, report: DataFrame) -> list[str]:
        # Fetch only relevant attributes for deletion to reduce memory usage
        report_index = set(report.set_index(["sn", "attribute"]).index)
        attributes = self._client.fetch_all(
            url="tables/global-attributes",
            export="df",
            columns=["id", "sn", "name", "value"],
            snapshot=False,
        )
        attributes["delete"] = attributes.set_index(["sn", "name"]).index.isin(report_index)
        # Use list comprehension directly on the DataFrame for better performance
        if payload := attributes.loc[attributes["delete"], "id"].tolist():
            self._client.settings.global_attributes.delete_attribute_by_id(*payload)
        return payload

    def apply_attributes(self, report) -> DataFrame:
        result = {"applied": [], "deleted": []}
        payload = (
            report.query("update == True | create == True")[["sn", "attribute", "new_value"]]
            .rename(columns={"attribute": "name", "new_value": "value"})
            .to_dict("records")
        )
        if payload:
            # Submit the payload to the API
            result["applied"] = self._client.settings.global_attributes.set_attributes_by_sn(payload)

        if not (deletion := report[["sn", "attribute", "delete"]].query("delete == True")).empty:
            result["deleted"] = self._delete_attributes(deletion)

        if self.config.update_snapshot:
            # Update the snapshot with the new attributes
            Attributes(client=self._client, snapshot_id=self._client.snapshot_id).update_local_attr_from_global(
                wait_for_load=False
            )
        return report

    def _process_deletions(self, rule: Union[TableRule, ConfigRule]) -> None:
        """Process deletions for the given rule on the remaining inventory if no match was found."""
        for dev in self._attributes.values():
            current_value = dev.global_attribute(rule.attribute)
            matched_rule = dev.matched_rule.get(rule.attribute)
            if current_value and (not matched_rule or matched_rule.marked_for_deletion):
                # If a match is found, then mark for deletion
                dev.matched_rule[rule.attribute] = MatchedRule(
                    name=rule.name,
                    attribute=rule.attribute,
                    current_value=current_value,
                    delete=True,
                    overwrite=True,
                    api_endpoint=self._endpoints_map[rule.value.api_endpoint],
                    **rule.value.model_dump(exclude={"api_endpoint"}),
                )

    def _filter_device_inventory(self, rule: Union[TableRule, ConfigRule]) -> dict[str, Attribute]:
        """Filter the device inventory based on the rule's filters."""
        devices = self._attributes
        if rule.inventory and rule.inventory.calc_filter:
            # Filter inventory if multiple configurations are merged
            filtered = self._calculate_inventory(rule.inventory)
            devices = {k: v for k, v in devices.items() if k in filtered}
        if isinstance(rule, ConfigRule) and rule.calc_filter:
            filtered = self._calculate_inventory(rule)
            devices = {k: v for k, v in devices.items() if k in filtered}
        [
            dev.matched_rule.update({rule.attribute: None})
            for dev in devices.values()
            if rule.attribute not in dev.matched_rule
        ]
        return devices

    def _process_table_rule(self, rule: TableRule) -> None:
        """Process Table Rules if a match/new_value has not been applied."""

        # Filter the device inventory based on the rule's filters
        inventory = self._filter_device_inventory(rule)

        url = self._endpoints_map[rule.value.api_endpoint]
        for data in self._client.fetch_all(
            url,
            filters=rule.calc_filter,
            columns=list(self._endpoints[url]),
            sort=rule.value.sort.model_dump() if rule.value.sort else None,
        ):
            dev = inventory.get(data[rule.value.sn])
            if not dev:
                continue
            matched_rule = dev.matched_rule.get(rule.attribute)
            if matched_rule and matched_rule.marked_for_deletion is False:
                continue
            value, regex_match, map_dict = rule.value.calc_value(data)
            if value:
                # If a match is found, assign the value to the device's attribute
                dev.matched_rule[rule.attribute] = MatchedRule(
                    name=rule.name,
                    attribute=rule.attribute,
                    delete=False,
                    overwrite=bool(rule.overwrite),
                    api_endpoint=url,
                    current_value=dev.global_attribute(rule.attribute),
                    new_value=value,
                    regex_match=regex_match,
                    column_value=data.get(rule.value.column) if rule.value.column else None,
                    mapping_match=map_dict,
                    **rule.value.model_dump(exclude={"api_endpoint"}),
                )

    @staticmethod
    def _get_config_or_log(dev: Attribute, rule: ConfigRule, match: MatchedConfig) -> Union[None, str]:
        if rule.value.config == "log":
            config = dev.device.get_log_file()
            if not config:
                match.new_value = rule.value.no_log_value
                dev.no_log_file = True
                dev.matched_rule[rule.attribute] = match
                return None
            setattr(dev, CONFIG_MAP[rule.value.config]["config"], config)
            return config

        config = dev.device.get_config()
        if not config:
            if (rule.overwrite_unsupported and match.current_value) or not match.current_value:
                match.new_value = rule.value.no_config_value
            else:
                match.new_value = match.current_value
            dev.no_start_config, dev.no_current_config = True, True
            dev.matched_rule[rule.attribute] = match
            return None

        config_string = getattr(config, CONFIG_MAP[rule.value.config]["name"], None)
        if not config_string:
            match.new_value = rule.value.no_config_value
            setattr(dev, CONFIG_MAP[rule.value.config]["no"], True)
            dev.matched_rule[rule.attribute] = match
            return None
        setattr(dev, CONFIG_MAP[rule.value.config]["config"], config_string)
        return config_string

    def _get_config(self, dev: Attribute, rule: ConfigRule) -> Union[None, str]:
        if config_string := getattr(dev, CONFIG_MAP[rule.value.config]["config"], None):
            return config_string

        match = MatchedConfig(
            name=rule.name,
            attribute=rule.attribute,
            current_value=dev.global_attribute(rule.attribute),
            delete=False,
            no_config_match=True,
            **rule.value.model_dump(),
        )
        return self._get_config_or_log(dev, rule, match)

    def _process_config_rule(self, rule: ConfigRule) -> None:
        """Process config rules if a match/new_value has not been applied."""

        # Filter the device inventory based on the rule's filters
        inventory = self._filter_device_inventory(rule)

        for dev in inventory.values():
            if dev.config_skip(rule) or (not (config_string := self._get_config(dev, rule))):
                continue
            new_value, regex_match, mapping_match = rule.value.calc_value(config_string)
            if new_value:
                dev.matched_rule[rule.attribute] = MatchedConfig(
                    name=rule.name,
                    attribute=rule.attribute,
                    current_value=dev.global_attribute(rule.attribute),
                    delete=False,
                    overwrite=bool(rule.overwrite),
                    no_config_match=False,
                    new_value=new_value,
                    regex_match=regex_match,
                    mapping_match=mapping_match,
                    **rule.value.model_dump(),
                )

    def calculate_attribute(self) -> dict[str, Attribute]:
        for rule in self.config.merged_rules:
            if isinstance(rule, TableRule):
                self._process_table_rule(rule)
            else:
                self._process_config_rule(rule)
            if rule.delete_attribute:
                self._process_deletions(rule)
        return self._attributes

    def report(self) -> DataFrame:
        df = DataFrame(
            [_ for dev in self._attributes.values() for _ in dev.export(self.config.inventory.calc_columns)],
            columns=self.config.inventory.df_columns,
        )
        df["correct"] = df["new_value"] == df["global_value"]
        df["update"] = df["new_value"].notnull() & (df["new_value"] != df["global_value"]) & df["overwrite"]
        df["create"] = df["new_value"].notnull() & df["global_value"].isnull()
        return df
