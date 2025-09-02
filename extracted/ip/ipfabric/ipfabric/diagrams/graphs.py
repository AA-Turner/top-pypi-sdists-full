import json
import logging
from typing import Union, Optional, Literal, Any

from pydantic import BaseModel

from ipfabric.models import Device
from ipfabric.models.security import DefaultAction
from ipfabric.tools.shared import raise_for_status
from .input_models import (
    Unicast,
    Multicast,
    Host2GW,
    Network,
    NetworkSettings,
    PathLookupSettings,
    Overlay,
    SharedView,
    GroupSettings,
)
from .output_models.graph_result import (
    GraphResult,
    Position,
    PathLookupResult,
    TopologyResult,
)

logger = logging.getLogger("ipfabric")
GRAPHS_URL = "graphs/"
GRAPH_TYPES = Union[Unicast, Multicast, Host2GW, Network]
GRAPH_SETTINGS = Optional[Union[NetworkSettings, PathLookupSettings]]
OVERLAY_SETTINGS = Optional[Union[Overlay, dict]]
ATTRIBUTE_FILTERS = Optional[dict[str, list[str]]]
POSITION_SETTINGS = Optional[dict[str, Union[Position, dict]]]
GRAPH_RESULTS = Union[PathLookupResult, TopologyResult]


class GraphDevice(BaseModel):
    device: Device
    decidingPolicyName: Optional[str] = None
    decidingRule: Optional[list] = None
    securityType: Optional[str] = None
    securityModelRule: Optional[Union[list, DefaultAction]] = None


class Diagram(BaseModel):
    ipf: Any

    def _check_snapshot_id(self, snapshot_id):
        snapshot_id = snapshot_id or self.ipf.snapshot_id
        if snapshot_id not in self.ipf.loaded_snapshots:
            raise ValueError(f"Snapshot {snapshot_id} is not loaded or not found in IP Fabric.")
        return snapshot_id

    def _intent_overlay(self, overlay: Overlay) -> dict:
        try:
            Overlay.valid_intent_rule(overlay.intentRuleId)
        except ValueError:
            if not self.ipf.intent.loaded:
                self.ipf.intent.load_intent()
            intents = self.ipf.intent.intents_by_name[overlay.intentRuleId]
            if len(intents) > 1:
                raise ValueError(f"Multiple Intents found with name `{overlay.intentRuleId}`.")
            else:
                overlay.intentRuleId = intents[0].intent_id
        return overlay.model_dump()

    def _snapshot_overlay(self, overlay: Overlay, snapshot_id: str = None) -> dict:
        if overlay.snapshotToCompare not in self.ipf.loaded_snapshots:
            raise ValueError(f"Snapshot `{overlay.snapshotToCompare}` is not loaded.")
        overlay.snapshotToCompare = self.ipf.snapshots[overlay.snapshotToCompare].snapshot_id
        if snapshot_id or self.ipf.snapshot_id == overlay.snapshotToCompare:
            raise ValueError(f"Cannot compare snapshot `{overlay.snapshotToCompare}` to itself.")
        self._check_snapshot_id(overlay.snapshotToCompare)
        return overlay.model_dump()

    def _format_overlay(self, overlay: Union[Overlay, dict], snapshot_id: str = None) -> dict:
        if isinstance(overlay, dict):
            overlay = Overlay(**overlay)
        if overlay.intentRuleId:
            return self._intent_overlay(overlay)
        return self._snapshot_overlay(overlay, snapshot_id)

    def _query(
        self,
        parameters: Union[GRAPH_TYPES, dict],
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        image: Literal["png", "svg", "json", "vsdx"] = "json",
        graph_settings: Union[GRAPH_SETTINGS, dict] = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        positions: POSITION_SETTINGS = None,
    ) -> Union[dict, bytes]:
        """
        Submits a query, does no formatting on the parameters.  Use for copy/pasting from the webpage.
        :param parameters: dict: Dictionary to submit in POST.
        :return: list: List of Dictionary objects.
        """
        url = GRAPHS_URL
        if image in ["svg", "png", "vsdx"]:
            url += image
        payload = dict(
            parameters=parameters if isinstance(parameters, dict) else parameters.model_dump(),
            snapshot=self._check_snapshot_id(snapshot_id),
        )
        if overlay:
            payload["overlay"] = self._format_overlay(overlay, snapshot_id)
        if graph_settings:
            payload["settings"] = graph_settings if isinstance(graph_settings, dict) else graph_settings.model_dump()
        if attr_filters or self.ipf.attribute_filters:
            payload["attributeFilters"] = attr_filters or self.ipf.attribute_filters
        payload["positions"] = {k: dict(v) for k, v in positions.items()} if positions else {}
        if image == "vsdx":
            if payload.get("overlay", None):
                logger.warning("Overlay is not supported for Visio diagrams.")
            json_graph = raise_for_status(self.ipf.post(GRAPHS_URL, json=payload)).json()["graphResult"]
            files = {
                "graph": (
                    "graph.json",
                    json.dumps(
                        {
                            "graph": {
                                "boxLabels": json_graph["boxLabels"],
                                "edges": json_graph["graphData"]["edges"],
                                "nodes": json_graph["graphData"]["nodes"],
                            }
                        }
                    ),
                    "application/json",
                )
            }
            res = raise_for_status(self.ipf.post(url, files=files))
        else:
            res = raise_for_status(self.ipf.post(url, json=payload))
        return res.json() if image == "json" else res.content

    @staticmethod
    def _swap_src_dst(p: GRAPH_TYPES, unicast_swap_src_dst: bool = False) -> GRAPH_TYPES:
        return p.swap_src_dst if unicast_swap_src_dst and isinstance(p, Unicast) else p

    def json(
        self,
        parameters: GRAPH_TYPES,
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        graph_settings: GRAPH_SETTINGS = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        unicast_swap_src_dst: bool = False,
        positions: POSITION_SETTINGS = None,
    ) -> dict:
        return self._query(
            self._swap_src_dst(parameters, unicast_swap_src_dst),
            snapshot_id=snapshot_id,
            image="json",
            overlay=overlay,
            attr_filters=attr_filters,
            graph_settings=graph_settings.model_dump() if graph_settings else None,
            positions=positions,
        )

    def svg(
        self,
        parameters: GRAPH_TYPES,
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        graph_settings: GRAPH_SETTINGS = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        unicast_swap_src_dst: bool = False,
        positions: POSITION_SETTINGS = None,
    ) -> bytes:
        return self._query(
            self._swap_src_dst(parameters, unicast_swap_src_dst),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="svg",
            graph_settings=graph_settings.model_dump() if graph_settings else None,
            positions=positions,
        )

    def png(
        self,
        parameters: GRAPH_TYPES,
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        graph_settings: GRAPH_SETTINGS = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        unicast_swap_src_dst: bool = False,
        positions: POSITION_SETTINGS = None,
    ) -> bytes:
        return self._query(
            self._swap_src_dst(parameters, unicast_swap_src_dst),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="png",
            graph_settings=graph_settings.model_dump() if graph_settings else None,
            positions=positions,
        )

    def visio(
        self,
        parameters: GRAPH_TYPES,
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        graph_settings: GRAPH_SETTINGS = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        unicast_swap_src_dst: bool = False,
        positions: POSITION_SETTINGS = None,
    ) -> bytes:
        return self._query(
            self._swap_src_dst(parameters, unicast_swap_src_dst),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="vsdx",
            graph_settings=graph_settings.model_dump() if graph_settings else None,
            positions=positions,
        )

    def share_link(
        self,
        parameters: GRAPH_TYPES,
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        graph_settings: GRAPH_SETTINGS = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        unicast_swap_src_dst: bool = False,
        positions: POSITION_SETTINGS = None,
    ) -> str:
        parameters = self._swap_src_dst(parameters, unicast_swap_src_dst)
        resp = self._query(
            parameters,
            snapshot_id=snapshot_id,
            overlay=overlay,
            image="json",
            attr_filters=attr_filters,
            graph_settings=graph_settings.model_dump() if graph_settings else None,
            positions=positions,
        )

        input_model = parameters.model_dump()
        input_model.pop("layouts", None)
        payload = {
            "graphView": {
                "name": "Shared view",
                "parameters": input_model,
                "collapsedNodeGroups": [],
                "hiddenNodes": [],
                "positions": {k: v["position"] for k, v in resp["graphResult"]["graphData"]["nodes"].items()},
                "settings": resp["graphResult"]["settings"],
            },
            "snapshot": self._check_snapshot_id(snapshot_id),
        }
        if overlay:
            payload["graphView"]["overlay"] = self._format_overlay(overlay, snapshot_id)
        res = raise_for_status(self.ipf.post("graphs/urls", json=payload))
        return str(self.ipf.base_url.join(f"/diagrams/share/{res.json()['id']}"))

    def model(
        self,
        parameters: GRAPH_TYPES,
        snapshot_id: Optional[str] = None,
        overlay: OVERLAY_SETTINGS = None,
        graph_settings: GRAPH_SETTINGS = None,
        attr_filters: ATTRIBUTE_FILTERS = None,
        unicast_swap_src_dst: bool = False,
        positions: POSITION_SETTINGS = None,
    ) -> GRAPH_RESULTS:
        json_data = self.json(
            parameters, snapshot_id, overlay, graph_settings, attr_filters, unicast_swap_src_dst, positions
        )
        graph_result = TopologyResult(**json_data) if "topology" in json_data else PathLookupResult(**json_data)
        e_setting = self._diagram_edge_settings(graph_result.graphResult.settings)

        edges = {edge_id: edge for edge_id, edge in graph_result.edges.items()}
        for edge_id, edge in edges.items():
            edge.protocol = e_setting[edge.edgeSettingsId].name if edge.edgeSettingsId in e_setting else None
            if edge.source:
                edge.source = graph_result.nodes[edge.source]
            if edge.target:
                edge.target = graph_result.nodes[edge.target]

        graph_result.graphResult.graphData.edges = edges
        return graph_result if isinstance(graph_result, TopologyResult) else self._diagram_pathlookup(graph_result)

    @staticmethod
    def _diagram_pathlookup(graph_result: PathLookupResult) -> PathLookupResult:
        for edge_id, edge in graph_result.edges.items():
            for prev_id in edge.prevEdgeIds:
                edge.prevEdge.append(graph_result.edges[prev_id])
            for next_id in edge.nextEdgeIds:
                edge.nextEdge.append(graph_result.edges[next_id] if next_id in graph_result.edges else next_id)
        return graph_result

    @staticmethod
    def _diagram_edge_settings(graph_settings: Union[NetworkSettings, PathLookupSettings]) -> dict:
        edge_setting_dict = dict()
        for edge in graph_settings.edges:
            edge_setting_dict[edge.id] = edge
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    edge_setting_dict[child.id] = child
        return edge_setting_dict

    def shared_view(
        self,
        url: Union[int, str],
        image: Literal["json", "code", "model", "svg", "png"] = "json",
        positions: bool = False,
    ):
        """Takes a shared graph link and returns the data or the code to implement in python.

        Args:
            url: Id of the shared view (1453653298) or full/partial URL (`/diagrams/share/1453626097`)
            image: Defaults to return the data instead of printing the code
            positions: If returning code then include positions of nodes in example; Default False

        Returns: The graph data or string representing the code to produce it.
        """
        query, _ = self.ipf._shared_url(url, False)
        if query["snapshot"] not in self.ipf.loaded_snapshots:
            logger.warning(f'Snapshot {query["snapshot"]} is not loaded, switching to {self.ipf.snapshot_id}.')
            query["snapshot"] = self.ipf.snapshot_id
        overlay = query["graphView"].get("overlay", {})
        if (
            overlay
            and overlay.get("snapshotToCompare", None)
            and overlay["snapshotToCompare"] not in self.ipf.loaded_snapshots
        ):
            logger.error(f"Snapshot `{overlay['snapshotToCompare']}` is not loaded to compare, removing overlay.")
            overlay = {}

        view = SharedView(
            snapshot_id=query["snapshot"],
            client_snapshot_id=self.ipf.snapshot_id,
            hidden_nodes=query["graphView"]["hiddenNodes"],
            collapsed_node_groups=query["graphView"]["collapsedNodeGroups"],
            positions=query["graphView"]["positions"],
            settings=query["graphView"]["settings"]["edges"],
            params=query["graphView"]["parameters"],
            hidden_devs=query["graphView"]["settings"].get("hiddenDeviceTypes", []),
            path_lookup=query["graphView"]["settings"].get("pathLookup", None),
            overlay=overlay,
        )
        if view.hidden_nodes or view.collapsed_node_groups:
            logger.warning("Hidden Nodes and Collapsed Node Groups are only available via the UI.")

        if image in ["json", "svg", "png"]:
            return self._query(
                parameters=query["graphView"]["parameters"],
                snapshot_id=query["snapshot"],
                overlay=overlay,
                image=image,
                graph_settings=query["graphView"]["settings"],
                positions=query["graphView"]["positions"],
            )

        if image == "code":
            return "\n".join(view.create_code(positions))
        if image == "model":
            return self.model(
                parameters=view.graph_model(),
                snapshot_id=query["snapshot"],
                overlay=overlay,
                graph_settings=view.graph_settings(),
                positions=query["graphView"]["positions"],
            )
        return None

    def _process_path(
        self, path: Union[GRAPH_RESULTS, GRAPH_TYPES], snapshot_id: Optional[str] = None
    ) -> GRAPH_RESULTS:
        """Helper method to process model or return a GraphResult.

        Args:
            path: PathLookupResult or TopologyResult or Unicast, Multicast, Host2GW, Network object
            snapshot_id: Optional snapshot_id to use

        Returns:
            GraphResult: Processed result
        """
        if isinstance(path, (PathLookupResult, TopologyResult)):
            return path
        return self.model(path, snapshot_id=snapshot_id)

    def nodes_in_diagram(
        self,
        path: Union[GRAPH_RESULTS, GRAPH_TYPES],
        dev_types: Optional[list[str]] = None,
        inventory_columns: Optional[Union[list[str], set[str]]] = None,
        snapshot_id: Optional[str] = None,
    ) -> list[Device]:
        """Fetches the device inventory for devices in the path.

        Args:
            path: PathLookupResult or TopologyResult or Unicast, Multicast, Host2GW, Network object
            dev_types: Optional list of device types to fetch, default ["l3switch", "fw", "switch", "router", "lb"]
            inventory_columns: Optional list of columns to fetch, default
                               ["sn", "version", "hostname", "model", "vendor", "siteName"]
            snapshot_id: Optional snapshot_id to use
        Returns:
            list[dict]: Device inventory
        """
        list_of_device_objects = list()
        dev_types = NetworkSettings._valid_dev_types(dev_types or ["l3switch", "fw", "switch", "router", "lb"])
        inventory_columns = list(inventory_columns) or ["sn", "version", "hostname", "model", "vendor", "siteName"]
        if not all(_ in self.ipf.oas["tables/inventory/devices"].post.columns for _ in inventory_columns):
            raise ValueError(
                f"Inventory Columns '{inventory_columns}' must be in "
                f"{self.ipf.oas['tables/inventory/devices'].post.columns}."
            )

        path = self._process_path(path, snapshot_id)
        device_sn_to_fetch = [node.sn for node in path.nodes.values() if node.type in dev_types]
        for sn in device_sn_to_fetch:
            list_of_device_objects.append(self.ipf.devices.by_sn[sn])
        return list_of_device_objects

    def security_event_rules(  # NOSONAR
        self,
        path: Union[GraphResult, Unicast, Multicast, Host2GW],
        snapshot_id: Optional[str] = None,
    ) -> list[GraphDevice]:  # noqa: C901
        """Fetches the security events for devices in the path.

        Args:
            path: PathLookupResult or TopologyResult or Unicast, Multicast, Host2GW
            snapshot_id: Optional snapshot_id to use

        Returns:
            list[dict]: Device Inventory Information and Security Event
        """
        logger.warning("This method is experimental and may not work as expected.")
        path = self._process_path(path, snapshot_id)
        app_graph_nodes_dict = {node.id: node for node in path.nodes.values() if node.style}
        path_inventory_dict = {device.sn: device for device in self.nodes_in_diagram(path, snapshot_id)}
        list_for_return = list()

        for vdevice, decisions in path.pathlookup.decisions.items():
            node = app_graph_nodes_dict.get(vdevice, None)
            if not node or not path_inventory_dict.get(node.sn, None):
                continue

            for trace in decisions.traces:
                for chain in trace.trace:
                    for event in chain.events:
                        if event.type in ["security check", "security check ignored"]:
                            device_data = path_inventory_dict[node.sn]
                            graph_device = GraphDevice(
                                device=device_data,
                                decidingPolicyName=event.decidingPolicyName,
                                decidingRule=event.decidingRule,
                                securityType=event.securityType,
                            )
                            if event.securityType == "zoneFw":
                                sec_model = graph_device.device.get_security_model()
                                machine_zones = sec_model.security.machineZones
                                rule_sequence = event.decidingRule[1]
                                zone_firewall_rules = (
                                    graph_device.device.technology.security.zone_firewall_policies.all(
                                        filters={
                                            "policyName": ["like", event.decidingPolicyName],
                                            "ruleNameNumeric": ["eq", (rule_sequence + 1)],
                                        }
                                    )
                                )
                                if zone_firewall_rules:
                                    graph_device.securityModelRule = zone_firewall_rules[0]
                                else:
                                    graph_device.securityModelRule = machine_zones.ruleChains.get(
                                        event.decidingPolicyName
                                    )
                            list_for_return.append(graph_device)
        return list_for_return

    def stp_instances(self, sites: Union[list[str], str], vlan_id: int) -> list[dict]:
        """Get the STP instances for the given sites and VLAN ID.

        Args:
            sites: Site name or list of site names to search for.
            vlan_id: VLAN ID to search for.

        Returns:

        """
        sites = [sites] if isinstance(sites, str) else sites
        filters = {"or": [{"siteName": ["eq", _]} for _ in sites]}
        devs = [_["sn"] for _ in self.ipf.inventory.devices.all(filters=filters, columns=["sn"])]
        roots = self.ipf.technology.stp.instance_members.all(
            filters={
                "and": [
                    {"members": ["containsAny", devs]},
                    {"rootHostname": ["empty", False]},
                    {"vlanId": ["eq", vlan_id]},
                ]
            },
            columns=["rootHostname", "rootId", "vlanId", "vlanName"],
        )
        return roots
