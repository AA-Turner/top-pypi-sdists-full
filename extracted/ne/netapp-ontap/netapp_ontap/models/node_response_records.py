r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NodeResponseRecords", "NodeResponseRecordsSchema"]
__pdoc__ = {
    "NodeResponseRecordsSchema.resource": False,
    "NodeResponseRecordsSchema.opts": False,
    "NodeResponseRecords": False,
}


class NodeResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NodeResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the node_response_records. """

    anti_ransomware_version = marshmallow_fields.Str(data_key="anti_ransomware_version", allow_none=True)
    r""" Anti ransomware version.

Example: 1.0 """

    cluster_interface = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_cluster_interface.ClusterNodesClusterInterfaceSchema", unknown=EXCLUDE, data_key="cluster_interface", allow_none=True)
    r""" The cluster network IP address of the node to be added. """

    cluster_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.node_management_interfaces.NodeManagementInterfacesSchema", unknown=EXCLUDE, allow_none=True), data_key="cluster_interfaces", allow_none=True)
    r""" Network interface """

    controller = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller.ClusterNodesControllerSchema", unknown=EXCLUDE, data_key="controller", allow_none=True)
    r""" Controller information """

    date = ImpreciseDateTime(data_key="date", allow_none=True)
    r""" The current or "wall clock" time of the node in ISO-8601 date, time, and time zone format.
The ISO-8601 date and time are localized based on the ONTAP cluster's timezone setting.


Example: 2019-04-17T15:49:26.000+0000 """

    external_cache = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_external_cache.ClusterNodesExternalCacheSchema", unknown=EXCLUDE, data_key="external_cache", allow_none=True)
    r""" Cache used for buffer management. """

    ha = marshmallow_fields.Nested("netapp_ontap.models.node_response_records_ha.NodeResponseRecordsHaSchema", unknown=EXCLUDE, data_key="ha", allow_none=True)
    r""" The ha field of the node_response_records. """

    hw_assist = marshmallow_fields.Nested("netapp_ontap.models.hw_assist.HwAssistSchema", unknown=EXCLUDE, data_key="hw_assist", allow_none=True)
    r""" The hardware assist information. """

    is_spares_low = marshmallow_fields.Boolean(data_key="is_spares_low", allow_none=True)
    r""" Specifies whether or not the node is in spares low condition. """

    location = marshmallow_fields.Str(data_key="location", allow_none=True)
    r""" The location field of the node_response_records.

Example: rack 2 row 5 """

    management_interface = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_management_interface.ClusterNodesManagementInterfaceSchema", unknown=EXCLUDE, data_key="management_interface", allow_none=True)
    r""" The management interface of the node to be added. The subnet mask is set based on the management interface of the cluster or the management interfaces of other nodes. """

    management_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.node_management_interfaces.NodeManagementInterfacesSchema", unknown=EXCLUDE, allow_none=True), data_key="management_interfaces", allow_none=True)
    r""" Network interface """

    membership = marshmallow_fields.Str(data_key="membership", allow_none=True)
    r""" Possible values:

* <i>available</i> - A node is detected on the internal cluster network and can be added to the cluster.  Nodes that have a membership of "available" are not returned when a GET request is called when the cluster exists. Provide a query on the "membership" property for <i>available</i> to scan for nodes on the cluster network. Nodes that have a membership of "available" are returned automatically before a cluster is created.
* <i>joining</i> - Joining nodes are in the process of being added to the cluster. The node might be progressing through the steps to become a member or might have failed. The job to add the node or create the cluster provides details on the current progress of the node.
* <i>member</i> - Nodes that are members have successfully joined the cluster.


Valid choices:

* available
* joining
* member """

    metric = marshmallow_fields.Nested("netapp_ontap.resources.node_metrics.NodeMetricsSchema", unknown=EXCLUDE, data_key="metric", allow_none=True)
    r""" CPU performance for the nodes. """

    metrocluster = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_metrocluster.ClusterNodesMetroclusterSchema", unknown=EXCLUDE, data_key="metrocluster", allow_none=True)
    r""" Metrocluster """

    model = marshmallow_fields.Str(data_key="model", allow_none=True)
    r""" The model field of the node_response_records.

Example: FAS3070 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the node_response_records.

Example: node-01 """

    nvram = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_nvram.ClusterNodesNvramSchema", unknown=EXCLUDE, data_key="nvram", allow_none=True)
    r""" The nvram field of the node_response_records. """

    owner = marshmallow_fields.Str(data_key="owner", allow_none=True)
    r""" Owner of the node.

Example: Example Corp """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" The serial_number field of the node_response_records.

Example: 4048820-60-9 """

    service_processor = marshmallow_fields.Nested("netapp_ontap.models.service_processor.ServiceProcessorSchema", unknown=EXCLUDE, data_key="service_processor", allow_none=True)
    r""" The service_processor field of the node_response_records. """

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_snaplock.ClusterNodesSnaplockSchema", unknown=EXCLUDE, data_key="snaplock", allow_none=True)
    r""" SnapLock-related properties. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the node:

* <i>up</i> - Node is up and operational.
* <i>booting</i> - Node is booting up.
* <i>down</i> - Node has stopped or is dumping core.
* <i>taken_over</i> - Node has been taken over by its HA partner and is not yet waiting for giveback.
* <i>waiting_for_giveback</i> - Node has been taken over by its HA partner and is waiting for the HA partner to giveback disks.
* <i>degraded</i> - Node has one or more critical services offline.
* <i>unknown</i> - Node or its HA partner cannot be contacted and there is no information on the node's state.


Valid choices:

* up
* booting
* down
* taken_over
* waiting_for_giveback
* degraded
* unknown """

    statistics = marshmallow_fields.Nested("netapp_ontap.models.node_statistics.NodeStatisticsSchema", unknown=EXCLUDE, data_key="statistics", allow_none=True)
    r""" Raw CPU performance for the nodes. """

    storage_availability_zones = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.node_storage_availability_zones.NodeStorageAvailabilityZonesSchema", unknown=EXCLUDE, allow_none=True), data_key="storage_availability_zones", allow_none=True)
    r""" Storage availability zones associated with the node. """

    storage_configuration = marshmallow_fields.Str(data_key="storage_configuration", allow_none=True)
    r""" The storage configuration in the system. Possible values:

* <i>mixed_path</i>
* <i>single_path</i>
* <i>multi_path</i>
* <i>tri_path</i>
* <i>quad_path</i>
* <i>mixed_path_ha</i>
* <i>single_path_ha</i>
* <i>multi_path_ha</i>
* <i>tri_path_ha</i>
* <i>quad_path_ha</i>
* <i>unknown</i>
* <i>virtual</i>


Valid choices:

* unknown
* single_path
* multi_path
* mixed_path
* quad_path
* single_path_ha
* multi_path_ha
* mixed_path_ha
* quad_path_ha
* tri_path
* tri_path_ha
* virtual """

    system_aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="system_aggregate", allow_none=True)
    r""" The system_aggregate field of the node_response_records. """

    system_id = marshmallow_fields.Str(data_key="system_id", allow_none=True)
    r""" The system_id field of the node_response_records.

Example: 92027651 """

    system_machine_type = marshmallow_fields.Str(data_key="system_machine_type", allow_none=True)
    r""" OEM system machine type.

Example: 7Y56-CTOWW1 """

    uptime = Size(data_key="uptime", allow_none=True)
    r""" The total time, in seconds, that the node has been up.

Example: 300536 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the node_response_records.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    vendor_serial_number = marshmallow_fields.Str(data_key="vendor_serial_number", allow_none=True)
    r""" OEM vendor serial number.

Example: 791603000068 """

    version = marshmallow_fields.Nested("netapp_ontap.models.version.VersionSchema", unknown=EXCLUDE, data_key="version", allow_none=True)
    r""" This returns the cluster version information.  When the cluster has more than one node, the cluster version is equivalent to the lowest of generation, major, and minor versions on all nodes. """

    vm = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_vm.ClusterNodesVmSchema", unknown=EXCLUDE, data_key="vm", allow_none=True)
    r""" The vm field of the node_response_records. """

    @property
    def resource(self):
        return NodeResponseRecords

    gettable_fields = [
        "links",
        "anti_ransomware_version",
        "cluster_interfaces.links",
        "cluster_interfaces.ip",
        "cluster_interfaces.name",
        "cluster_interfaces.uuid",
        "controller",
        "date",
        "external_cache",
        "ha",
        "hw_assist",
        "is_spares_low",
        "location",
        "management_interfaces.links",
        "management_interfaces.ip",
        "management_interfaces.name",
        "management_interfaces.uuid",
        "membership",
        "metric",
        "metrocluster",
        "model",
        "name",
        "nvram",
        "owner",
        "serial_number",
        "service_processor",
        "snaplock",
        "state",
        "statistics",
        "storage_availability_zones.links",
        "storage_availability_zones.name",
        "storage_availability_zones.uuid",
        "storage_configuration",
        "system_aggregate.links",
        "system_aggregate.name",
        "system_aggregate.uuid",
        "system_id",
        "system_machine_type",
        "uptime",
        "uuid",
        "vendor_serial_number",
        "version",
        "vm",
    ]
    """links,anti_ransomware_version,cluster_interfaces.links,cluster_interfaces.ip,cluster_interfaces.name,cluster_interfaces.uuid,controller,date,external_cache,ha,hw_assist,is_spares_low,location,management_interfaces.links,management_interfaces.ip,management_interfaces.name,management_interfaces.uuid,membership,metric,metrocluster,model,name,nvram,owner,serial_number,service_processor,snaplock,state,statistics,storage_availability_zones.links,storage_availability_zones.name,storage_availability_zones.uuid,storage_configuration,system_aggregate.links,system_aggregate.name,system_aggregate.uuid,system_id,system_machine_type,uptime,uuid,vendor_serial_number,version,vm,"""

    patchable_fields = [
        "ha",
        "location",
        "name",
        "owner",
        "service_processor",
        "system_aggregate.name",
        "system_aggregate.uuid",
    ]
    """ha,location,name,owner,service_processor,system_aggregate.name,system_aggregate.uuid,"""

    postable_fields = [
        "cluster_interface",
        "ha",
        "location",
        "management_interface",
        "name",
        "owner",
        "service_processor",
        "system_aggregate.name",
        "system_aggregate.uuid",
    ]
    """cluster_interface,ha,location,management_interface,name,owner,service_processor,system_aggregate.name,system_aggregate.uuid,"""


class NodeResponseRecords(Resource):

    _schema = NodeResponseRecordsSchema
