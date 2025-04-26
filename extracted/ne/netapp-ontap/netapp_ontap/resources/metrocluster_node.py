r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Retrieves the configuration information for the nodes in the MetroCluster configuration.
####
---
### Example
```
GET https://<mgmt-ip>/api/cluster/metrocluster/nodes
{
    "records": [
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster1",
                "uuid": "8f77de32-9857-11e9-9a55-005056828eb9",
                "_links": {
                    "self": {
                        "href": "/api/cluster"
                    }
                }
            },
            "node": {
                "name": "cluster1_01",
                "uuid": "46147363-9857-11e9-9a55-005056828eb9",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/46147363-9857-11e9-9a55-005056828eb9"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/46147363-9857-11e9-9a55-005056828eb9"
                }
            }
        },
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster1",
                "uuid": "8f77de32-9857-11e9-9a55-005056828eb9",
                "_links": {
                    "self": {
                        "href": "/api/cluster"
                    }
                }
            },
            "node": {
                "name": "cluster1_02",
                "uuid": "cf1dc67f-9857-11e9-bf80-005056829db6",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/cf1dc67f-9857-11e9-bf80-005056829db6"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/cf1dc67f-9857-11e9-bf80-005056829db6"
                }
            }
        },
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster3",
                "uuid": "aa8aa15a-9857-11e9-80c9-00505682e684",
                "_links": {
                    "self": {
                        "href": "/api/cluster/peers/aa8aa15a-9857-11e9-80c9-00505682e684/cluster"
                    }
                }
            },
            "node": {
                "name": "cluster3_01",
                "uuid": "5b3b983b-9857-11e9-80c9-00505682e684",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/5b3b983b-9857-11e9-80c9-00505682e684"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/5b3b983b-9857-11e9-80c9-00505682e684"
                }
            }
        },
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster3",
                "uuid": "aa8aa15a-9857-11e9-80c9-00505682e684",
                "_links": {
                    "self": {
                        "href": "/api/cluster/peers/aa8aa15a-9857-11e9-80c9-00505682e684/cluster"
                    }
                }
            },
            "node": {
                "name": "cluster3_02",
                "uuid": "45bff538-9858-11e9-a624-005056820377",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/45bff538-9858-11e9-a624-005056820377"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/45bff538-9858-11e9-a624-005056820377"
                }
            }
        }
    ],
    "num_records": 4,
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster/nodes?fields=%2A"
        }
    }
}
```
---"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["MetroclusterNode", "MetroclusterNodeSchema"]
__pdoc__ = {
    "MetroclusterNodeSchema.resource": False,
    "MetroclusterNodeSchema.opts": False,
}


class MetroclusterNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterNode object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the metrocluster_node."""

    automatic_uso = marshmallow_fields.Boolean(
        data_key="automatic_uso",
        allow_none=True,
    )
    r""" Specifies if automatic unplanned switchover is enabled."""

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="cluster", unknown=EXCLUDE, allow_none=True)
    r""" The cluster field of the metrocluster_node."""

    configuration_state = marshmallow_fields.Str(
        data_key="configuration_state",
        validate=enum_validation(['unreachable', 'configured']),
        allow_none=True,
    )
    r""" Configuration state of the node.

Valid choices:

* unreachable
* configured"""

    dr_auxiliary_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="dr_auxiliary_cluster", unknown=EXCLUDE, allow_none=True)
    r""" The dr_auxiliary_cluster field of the metrocluster_node."""

    dr_auxiliary_partner = marshmallow_fields.Nested("netapp_ontap.models.mcc_node.MccNodeSchema", data_key="dr_auxiliary_partner", unknown=EXCLUDE, allow_none=True)
    r""" The dr_auxiliary_partner field of the metrocluster_node."""

    dr_group_id = Size(
        data_key="dr_group_id",
        allow_none=True,
    )
    r""" DR Group ID."""

    dr_mirroring_state = marshmallow_fields.Str(
        data_key="dr_mirroring_state",
        validate=enum_validation(['enabled', 'disabled', 'unreachable', 'configured']),
        allow_none=True,
    )
    r""" State of the DR mirroring configuration.

Valid choices:

* enabled
* disabled
* unreachable
* configured"""

    dr_operation_state = marshmallow_fields.Str(
        data_key="dr_operation_state",
        validate=enum_validation(['normal', 'switchover_bypassed', 'switchover_in_progress', 'switchover_completed', 'switchover_failed', 'switched_over', 'heal_aggrs_in_progress', 'heal_aggrs_completed', 'heal_aggrs_failed', 'heal_roots_in_progress', 'heal_roots_completed', 'heal_roots_failed', 'switchback_vetoed', 'switchback_vetocheck_locked', 'switchback_pre_commit_completed', 'switchback_in_progress', 'switchback_completed', 'switchback_failed', 'negotiated_switchover_vetoed', 'negotiated_switchover_vetocheck_locked', 'negotiated_switchover_pre_commit_completed', 'negotiated_switchover_in_progress', 'negotiated_switchover_completed', 'negotiated_switchover_in_progress_waiting_for_DR_partner', 'negotiated_switchover_incomplete', 'negotiated_switchover_failed', 'negotiated_switchover_failed_on_DR_partner', 'switchback_recovery_in_progress', 'switchback_recovery_complete', 'waiting_for_switchback_recovery', 'unknown']),
        allow_none=True,
    )
    r""" State of the DR operation.

Valid choices:

* normal
* switchover_bypassed
* switchover_in_progress
* switchover_completed
* switchover_failed
* switched_over
* heal_aggrs_in_progress
* heal_aggrs_completed
* heal_aggrs_failed
* heal_roots_in_progress
* heal_roots_completed
* heal_roots_failed
* switchback_vetoed
* switchback_vetocheck_locked
* switchback_pre_commit_completed
* switchback_in_progress
* switchback_completed
* switchback_failed
* negotiated_switchover_vetoed
* negotiated_switchover_vetocheck_locked
* negotiated_switchover_pre_commit_completed
* negotiated_switchover_in_progress
* negotiated_switchover_completed
* negotiated_switchover_in_progress_waiting_for_DR_partner
* negotiated_switchover_incomplete
* negotiated_switchover_failed
* negotiated_switchover_failed_on_DR_partner
* switchback_recovery_in_progress
* switchback_recovery_complete
* waiting_for_switchback_recovery
* unknown"""

    dr_partner = marshmallow_fields.Nested("netapp_ontap.models.mcc_node.MccNodeSchema", data_key="dr_partner", unknown=EXCLUDE, allow_none=True)
    r""" The dr_partner field of the metrocluster_node."""

    dr_partner_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="dr_partner_cluster", unknown=EXCLUDE, allow_none=True)
    r""" The dr_partner_cluster field of the metrocluster_node."""

    encryption_enabled = marshmallow_fields.Boolean(
        data_key="encryption_enabled",
        allow_none=True,
    )
    r""" Indicates if the encryption for NVLog and storage traffic is enabled."""

    ha_partner = marshmallow_fields.Nested("netapp_ontap.models.mcc_node.MccNodeSchema", data_key="ha_partner", unknown=EXCLUDE, allow_none=True)
    r""" The ha_partner field of the metrocluster_node."""

    ha_partner_cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="ha_partner_cluster", unknown=EXCLUDE, allow_none=True)
    r""" The ha_partner_cluster field of the metrocluster_node."""

    is_mccip = marshmallow_fields.Boolean(
        data_key="is_mccip",
        allow_none=True,
    )
    r""" Indicates whether the configuration type is MCC-IP."""

    limit_enforcement = marshmallow_fields.Str(
        data_key="limit_enforcement",
        validate=enum_validation(['enabled', 'disabled']),
        allow_none=True,
    )
    r""" Indicates if the node object limits are enforced.

Valid choices:

* enabled
* disabled"""

    node = marshmallow_fields.Nested("netapp_ontap.models.mcc_node.MccNodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the metrocluster_node."""

    @property
    def resource(self):
        return MetroclusterNode

    gettable_fields = [
        "links",
        "automatic_uso",
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "configuration_state",
        "dr_auxiliary_cluster.links",
        "dr_auxiliary_cluster.name",
        "dr_auxiliary_cluster.uuid",
        "dr_auxiliary_partner.links",
        "dr_auxiliary_partner.name",
        "dr_auxiliary_partner.system_id",
        "dr_auxiliary_partner.uuid",
        "dr_group_id",
        "dr_mirroring_state",
        "dr_operation_state",
        "dr_partner.links",
        "dr_partner.name",
        "dr_partner.system_id",
        "dr_partner.uuid",
        "dr_partner_cluster.links",
        "dr_partner_cluster.name",
        "dr_partner_cluster.uuid",
        "encryption_enabled",
        "ha_partner.links",
        "ha_partner.name",
        "ha_partner.system_id",
        "ha_partner.uuid",
        "ha_partner_cluster.links",
        "ha_partner_cluster.name",
        "ha_partner_cluster.uuid",
        "is_mccip",
        "limit_enforcement",
        "node.links",
        "node.name",
        "node.system_id",
        "node.uuid",
    ]
    """links,automatic_uso,cluster.links,cluster.name,cluster.uuid,configuration_state,dr_auxiliary_cluster.links,dr_auxiliary_cluster.name,dr_auxiliary_cluster.uuid,dr_auxiliary_partner.links,dr_auxiliary_partner.name,dr_auxiliary_partner.system_id,dr_auxiliary_partner.uuid,dr_group_id,dr_mirroring_state,dr_operation_state,dr_partner.links,dr_partner.name,dr_partner.system_id,dr_partner.uuid,dr_partner_cluster.links,dr_partner_cluster.name,dr_partner_cluster.uuid,encryption_enabled,ha_partner.links,ha_partner.name,ha_partner.system_id,ha_partner.uuid,ha_partner_cluster.links,ha_partner_cluster.name,ha_partner_cluster.uuid,is_mccip,limit_enforcement,node.links,node.name,node.system_id,node.uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "dr_auxiliary_cluster.name",
        "dr_auxiliary_cluster.uuid",
        "dr_auxiliary_partner.links",
        "dr_auxiliary_partner.name",
        "dr_auxiliary_partner.uuid",
        "dr_partner.links",
        "dr_partner.name",
        "dr_partner.uuid",
        "dr_partner_cluster.name",
        "dr_partner_cluster.uuid",
        "encryption_enabled",
        "ha_partner.links",
        "ha_partner.name",
        "ha_partner.uuid",
        "ha_partner_cluster.name",
        "ha_partner_cluster.uuid",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """cluster.name,cluster.uuid,dr_auxiliary_cluster.name,dr_auxiliary_cluster.uuid,dr_auxiliary_partner.links,dr_auxiliary_partner.name,dr_auxiliary_partner.uuid,dr_partner.links,dr_partner.name,dr_partner.uuid,dr_partner_cluster.name,dr_partner_cluster.uuid,encryption_enabled,ha_partner.links,ha_partner.name,ha_partner.uuid,ha_partner_cluster.name,ha_partner_cluster.uuid,node.links,node.name,node.uuid,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "dr_auxiliary_cluster.name",
        "dr_auxiliary_cluster.uuid",
        "dr_auxiliary_partner.links",
        "dr_auxiliary_partner.name",
        "dr_auxiliary_partner.uuid",
        "dr_partner.links",
        "dr_partner.name",
        "dr_partner.uuid",
        "dr_partner_cluster.name",
        "dr_partner_cluster.uuid",
        "encryption_enabled",
        "ha_partner.links",
        "ha_partner.name",
        "ha_partner.uuid",
        "ha_partner_cluster.name",
        "ha_partner_cluster.uuid",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """cluster.name,cluster.uuid,dr_auxiliary_cluster.name,dr_auxiliary_cluster.uuid,dr_auxiliary_partner.links,dr_auxiliary_partner.name,dr_auxiliary_partner.uuid,dr_partner.links,dr_partner.name,dr_partner.uuid,dr_partner_cluster.name,dr_partner_cluster.uuid,encryption_enabled,ha_partner.links,ha_partner.name,ha_partner.uuid,ha_partner_cluster.name,ha_partner_cluster.uuid,node.links,node.name,node.uuid,"""

class MetroclusterNode(Resource):
    r""" Data for a node in a MetroCluster. REST: /api/cluster/metrocluster/nodes """

    _schema = MetroclusterNodeSchema
    _path = "/api/cluster/metrocluster/nodes"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves MetroCluster nodes and their configurations.
### Related ONTAP Commands
* `metrocluster node show`
### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all MetroclusterNode resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent MetroclusterNode resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves MetroCluster nodes and their configurations.
### Related ONTAP Commands
* `metrocluster node show`
### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the node configuration in the MetroCluster.
### Related ONTAP Commands
* `metrocluster node show`

### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





