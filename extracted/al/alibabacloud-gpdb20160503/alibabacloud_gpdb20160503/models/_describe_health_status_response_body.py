# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from alibabacloud_gpdb20160503 import models as main_models
from darabonba.model import DaraModel

class DescribeHealthStatusResponseBody(DaraModel):
    def __init__(
        self,
        dbcluster_id: str = None,
        request_id: str = None,
        status: main_models.DescribeHealthStatusResponseBodyStatus = None,
    ):
        # The instance ID.
        self.dbcluster_id = dbcluster_id
        # The request ID.
        self.request_id = request_id
        # The detailed performance monitoring information, which consists of the metric name, status, and metric value. Monitoring information is returned only for the metrics specified in the **Key** request parameter. For example, if the **Key** parameter contains only **adbpg_status**, only the monitoring information for **adbpg_status** is returned.
        # 
        # For more information about performance metrics, see [Performance metrics](https://help.aliyun.com/document_detail/86943.html).
        self.status = status

    def validate(self):
        if self.status:
            self.status.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.dbcluster_id is not None:
            result['DBClusterId'] = self.dbcluster_id

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        if self.status is not None:
            result['Status'] = self.status.to_map()

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBClusterId') is not None:
            self.dbcluster_id = m.get('DBClusterId')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        if m.get('Status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatus()
            self.status = temp_model.from_map(m.get('Status'))

        return self

class DescribeHealthStatusResponseBodyStatus(DaraModel):
    def __init__(
        self,
        adbgp_segment_disk_usage_percent_max: main_models.DescribeHealthStatusResponseBodyStatusAdbgpSegmentDiskUsagePercentMax = None,
        adbpg_connection_status: main_models.DescribeHealthStatusResponseBodyStatusAdbpgConnectionStatus = None,
        adbpg_disk_status: main_models.DescribeHealthStatusResponseBodyStatusAdbpgDiskStatus = None,
        adbpg_disk_usage_percent: main_models.DescribeHealthStatusResponseBodyStatusAdbpgDiskUsagePercent = None,
        adbpg_instance_cold_data_gb: main_models.DescribeHealthStatusResponseBodyStatusAdbpgInstanceColdDataGb = None,
        adbpg_instance_hot_data_gb: main_models.DescribeHealthStatusResponseBodyStatusAdbpgInstanceHotDataGb = None,
        adbpg_instance_total_data_gb: main_models.DescribeHealthStatusResponseBodyStatusAdbpgInstanceTotalDataGb = None,
        adbpg_master_disk_usage_percent_max: main_models.DescribeHealthStatusResponseBodyStatusAdbpgMasterDiskUsagePercentMax = None,
        adbpg_master_status: main_models.DescribeHealthStatusResponseBodyStatusAdbpgMasterStatus = None,
        adbpg_segment_status: main_models.DescribeHealthStatusResponseBodyStatusAdbpgSegmentStatus = None,
        adbpg_status: main_models.DescribeHealthStatusResponseBodyStatusAdbpgStatus = None,
        node_master_connection_status: main_models.DescribeHealthStatusResponseBodyStatusNodeMasterConnectionStatus = None,
        node_master_status: main_models.DescribeHealthStatusResponseBodyStatusNodeMasterStatus = None,
        node_segment_connection_status: main_models.DescribeHealthStatusResponseBodyStatusNodeSegmentConnectionStatus = None,
        node_segment_disk_status: main_models.DescribeHealthStatusResponseBodyStatusNodeSegmentDiskStatus = None,
    ):
        # The maximum storage usage of compute nodes in the instance, which is the maximum storage usage among all segment nodes in the instance.
        # 
        # > This value is returned only for instances in elastic storage mode.
        self.adbgp_segment_disk_usage_percent_max = adbgp_segment_disk_usage_percent_max
        # The connection status of the instance.
        self.adbpg_connection_status = adbpg_connection_status
        # The instance storage status.
        # 
        # > This value is returned only for instances in the elastic storage pattern.
        self.adbpg_disk_status = adbpg_disk_status
        # The instance storage usage.
        # 
        # > This value is returned only for instances in the elastic storage pattern.
        self.adbpg_disk_usage_percent = adbpg_disk_usage_percent
        # The total amount of cold data stored.
        self.adbpg_instance_cold_data_gb = adbpg_instance_cold_data_gb
        # The total amount of hot data stored.
        self.adbpg_instance_hot_data_gb = adbpg_instance_hot_data_gb
        # The total amount of instance storage data.
        self.adbpg_instance_total_data_gb = adbpg_instance_total_data_gb
        # The maximum storage usage of coordinator nodes in the instance, which is the maximum storage usage among all master nodes in the instance.
        # 
        # > This value is returned only for instances in elastic storage mode.
        self.adbpg_master_disk_usage_percent_max = adbpg_master_disk_usage_percent_max
        # The status of coordinator nodes, namely the availability status of master nodes.
        self.adbpg_master_status = adbpg_master_status
        # The status of compute nodes, namely the availability status of segment nodes.
        self.adbpg_segment_status = adbpg_segment_status
        # The health status of the instance.
        self.adbpg_status = adbpg_status
        # The connection health status of coordinator nodes, namely master nodes.
        self.node_master_connection_status = node_master_connection_status
        # The health status of coordinator nodes, namely master nodes.
        self.node_master_status = node_master_status
        # The connection health status of compute nodes, namely segment nodes.
        self.node_segment_connection_status = node_segment_connection_status
        # The storage status of compute nodes, namely segment nodes.
        # 
        # > This value is returned only for instances in elastic storage mode.
        self.node_segment_disk_status = node_segment_disk_status

    def validate(self):
        if self.adbgp_segment_disk_usage_percent_max:
            self.adbgp_segment_disk_usage_percent_max.validate()
        if self.adbpg_connection_status:
            self.adbpg_connection_status.validate()
        if self.adbpg_disk_status:
            self.adbpg_disk_status.validate()
        if self.adbpg_disk_usage_percent:
            self.adbpg_disk_usage_percent.validate()
        if self.adbpg_instance_cold_data_gb:
            self.adbpg_instance_cold_data_gb.validate()
        if self.adbpg_instance_hot_data_gb:
            self.adbpg_instance_hot_data_gb.validate()
        if self.adbpg_instance_total_data_gb:
            self.adbpg_instance_total_data_gb.validate()
        if self.adbpg_master_disk_usage_percent_max:
            self.adbpg_master_disk_usage_percent_max.validate()
        if self.adbpg_master_status:
            self.adbpg_master_status.validate()
        if self.adbpg_segment_status:
            self.adbpg_segment_status.validate()
        if self.adbpg_status:
            self.adbpg_status.validate()
        if self.node_master_connection_status:
            self.node_master_connection_status.validate()
        if self.node_master_status:
            self.node_master_status.validate()
        if self.node_segment_connection_status:
            self.node_segment_connection_status.validate()
        if self.node_segment_disk_status:
            self.node_segment_disk_status.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.adbgp_segment_disk_usage_percent_max is not None:
            result['adbgp_segment_disk_usage_percent_max'] = self.adbgp_segment_disk_usage_percent_max.to_map()

        if self.adbpg_connection_status is not None:
            result['adbpg_connection_status'] = self.adbpg_connection_status.to_map()

        if self.adbpg_disk_status is not None:
            result['adbpg_disk_status'] = self.adbpg_disk_status.to_map()

        if self.adbpg_disk_usage_percent is not None:
            result['adbpg_disk_usage_percent'] = self.adbpg_disk_usage_percent.to_map()

        if self.adbpg_instance_cold_data_gb is not None:
            result['adbpg_instance_cold_data_gb'] = self.adbpg_instance_cold_data_gb.to_map()

        if self.adbpg_instance_hot_data_gb is not None:
            result['adbpg_instance_hot_data_gb'] = self.adbpg_instance_hot_data_gb.to_map()

        if self.adbpg_instance_total_data_gb is not None:
            result['adbpg_instance_total_data_gb'] = self.adbpg_instance_total_data_gb.to_map()

        if self.adbpg_master_disk_usage_percent_max is not None:
            result['adbpg_master_disk_usage_percent_max'] = self.adbpg_master_disk_usage_percent_max.to_map()

        if self.adbpg_master_status is not None:
            result['adbpg_master_status'] = self.adbpg_master_status.to_map()

        if self.adbpg_segment_status is not None:
            result['adbpg_segment_status'] = self.adbpg_segment_status.to_map()

        if self.adbpg_status is not None:
            result['adbpg_status'] = self.adbpg_status.to_map()

        if self.node_master_connection_status is not None:
            result['node_master_connection_status'] = self.node_master_connection_status.to_map()

        if self.node_master_status is not None:
            result['node_master_status'] = self.node_master_status.to_map()

        if self.node_segment_connection_status is not None:
            result['node_segment_connection_status'] = self.node_segment_connection_status.to_map()

        if self.node_segment_disk_status is not None:
            result['node_segment_disk_status'] = self.node_segment_disk_status.to_map()

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('adbgp_segment_disk_usage_percent_max') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbgpSegmentDiskUsagePercentMax()
            self.adbgp_segment_disk_usage_percent_max = temp_model.from_map(m.get('adbgp_segment_disk_usage_percent_max'))

        if m.get('adbpg_connection_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgConnectionStatus()
            self.adbpg_connection_status = temp_model.from_map(m.get('adbpg_connection_status'))

        if m.get('adbpg_disk_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgDiskStatus()
            self.adbpg_disk_status = temp_model.from_map(m.get('adbpg_disk_status'))

        if m.get('adbpg_disk_usage_percent') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgDiskUsagePercent()
            self.adbpg_disk_usage_percent = temp_model.from_map(m.get('adbpg_disk_usage_percent'))

        if m.get('adbpg_instance_cold_data_gb') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgInstanceColdDataGb()
            self.adbpg_instance_cold_data_gb = temp_model.from_map(m.get('adbpg_instance_cold_data_gb'))

        if m.get('adbpg_instance_hot_data_gb') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgInstanceHotDataGb()
            self.adbpg_instance_hot_data_gb = temp_model.from_map(m.get('adbpg_instance_hot_data_gb'))

        if m.get('adbpg_instance_total_data_gb') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgInstanceTotalDataGb()
            self.adbpg_instance_total_data_gb = temp_model.from_map(m.get('adbpg_instance_total_data_gb'))

        if m.get('adbpg_master_disk_usage_percent_max') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgMasterDiskUsagePercentMax()
            self.adbpg_master_disk_usage_percent_max = temp_model.from_map(m.get('adbpg_master_disk_usage_percent_max'))

        if m.get('adbpg_master_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgMasterStatus()
            self.adbpg_master_status = temp_model.from_map(m.get('adbpg_master_status'))

        if m.get('adbpg_segment_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgSegmentStatus()
            self.adbpg_segment_status = temp_model.from_map(m.get('adbpg_segment_status'))

        if m.get('adbpg_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusAdbpgStatus()
            self.adbpg_status = temp_model.from_map(m.get('adbpg_status'))

        if m.get('node_master_connection_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusNodeMasterConnectionStatus()
            self.node_master_connection_status = temp_model.from_map(m.get('node_master_connection_status'))

        if m.get('node_master_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusNodeMasterStatus()
            self.node_master_status = temp_model.from_map(m.get('node_master_status'))

        if m.get('node_segment_connection_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusNodeSegmentConnectionStatus()
            self.node_segment_connection_status = temp_model.from_map(m.get('node_segment_connection_status'))

        if m.get('node_segment_disk_status') is not None:
            temp_model = main_models.DescribeHealthStatusResponseBodyStatusNodeSegmentDiskStatus()
            self.node_segment_disk_status = temp_model.from_map(m.get('node_segment_disk_status'))

        return self

class DescribeHealthStatusResponseBodyStatusNodeSegmentDiskStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # Instance storage status of segment nodes. Valid values:
        # 
        # - **critical**: Instance storage usage of segment nodes is greater than or equal to 90%. The status is displayed in red in the console, and the instance will be locked.
        # - **warning**: Instance storage usage of segment nodes is greater than or equal to 80% and less than 90%. The status is displayed in yellow in the console.
        # - **healthy**: Instance storage usage of segment nodes is less than 80%. The status is displayed in green in the console, indicating a healthy storage status.
        # 
        # > Instance storage usage of segment nodes is the maximum storage usage among all segment nodes.
        self.status = status
        # The metric value of the maximum storage usage of segment nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusNodeSegmentConnectionStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The connection health status of segment nodes. Valid values:
        # 
        # - **critical**: The connection usage of segment nodes is greater than or equal to 95%. The status is displayed in red in the console.
        # - **warning**: The connection usage of segment nodes is greater than or equal to 90% and less than 95%. The status is displayed in yellow in the console.
        # - **healthy**: The connection usage of segment nodes is less than 90%. The status is displayed in green in the console.
        # 
        # > The connection usage of segment nodes is the maximum connection usage among all segment nodes.
        self.status = status
        # The metric value of the connection usage of segment nodes, which is the maximum connection usage among all segment nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusNodeMasterStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The health status of master nodes. Valid values:
        # 
        # - **critical**: At least one primary or secondary master node is unavailable. The status is displayed in red in the console.
        # - **healthy**: All master nodes are available. The status is displayed in green in the console.
        self.status = status
        # The metric value of the master node health status. Valid values:
        # 
        # - **1**: healthy.
        # - **0**: critical.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusNodeMasterConnectionStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The connection health status of master nodes. Valid values:
        # 
        # - **critical**: The connection usage of master nodes is greater than or equal to 95%. The status is displayed in red in the console.
        # - **warning**: The connection usage of master nodes is greater than or equal to 90% and less than 95%. The status is displayed in yellow in the console.
        # - **healthy**: The connection usage of master nodes is less than 90%. The status is displayed in green in the console.
        # 
        # > The connection usage of master nodes is the maximum connection usage among all master nodes.
        self.status = status
        # The metric value of the connection usage of master nodes, which is the maximum connection usage among all master nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The health status of the instance. Valid values:
        # 
        # - **critical**: At least one master node or segment node is unavailable. The status is displayed in red in the console.
        # - **healthy**: All nodes are available. The status is displayed in green in the console.
        self.status = status
        # The metric value of the instance health status. Valid values:
        # 
        # - **1**: healthy.
        # - **0**: critical.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgSegmentStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The availability status of segment nodes. Valid values:
        # 
        # - **critical**: Both the primary and secondary nodes are unavailable. The status is displayed in red in the console.
        # - **warning**: 50% or more of the nodes are unavailable. The status is displayed in yellow in the console.
        # - **healthy**: All nodes are available. The status is displayed in green in the console.
        self.status = status
        # The metric value of the availability status of segment nodes.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgMasterStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The availability status of master nodes. Valid values:
        # 
        # - **critical**: Both the primary and secondary nodes are unavailable. The status is displayed in red in the console.
        # - **warning**: The primary or secondary node is unavailable. The status is displayed in yellow in the console.
        # - **healthy**: All nodes are available. The status is displayed in green in the console.
        self.status = status
        # The metric value of the availability status of master nodes. Valid values:
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgMasterDiskUsagePercentMax(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The maximum storage usage status of master nodes. Valid values:
        # 
        # - **critical**: Instance storage usage is greater than or equal to 90%, and the instance will be locked.
        # - **warning**: Instance storage usage is greater than or equal to 70% and less than 90%.
        # - **healthy**: Instance storage usage is less than 70%, indicating a healthy storage status.
        self.status = status
        # The metric value of the maximum storage usage of master nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgInstanceTotalDataGb(DaraModel):
    def __init__(
        self,
        value: float = None,
    ):
        # The total amount of instance storage data. Unit: GB.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgInstanceHotDataGb(DaraModel):
    def __init__(
        self,
        value: float = None,
    ):
        # The total amount of hot data stored. Unit: GB.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgInstanceColdDataGb(DaraModel):
    def __init__(
        self,
        value: float = None,
    ):
        # The total amount of cold data stored. Unit: GB.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgDiskUsagePercent(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # Instance storage usage status of the instance. Valid values:
        # 
        # - **critical**: Instance storage usage of the instance is greater than or equal to 90%, and the instance will be locked.
        # - **warning**: Instance storage usage of the instance is greater than or equal to 70% and less than 90%.
        # - **healthy**: Instance storage usage of the instance is less than 70%, indicating a healthy storage status.
        # 
        # > Instance storage usage of the instance is the average storage usage of all segment nodes.
        self.status = status
        # The metric value of the instance storage usage, which is the average storage usage of all segment nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgDiskStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # Instance storage status of the instance. Valid values:
        # 
        # - **critical**: Instance storage usage of the instance is greater than or equal to 90%. The status is displayed in red in the console, and the instance will be locked.
        # - **warning**: Instance storage usage of the instance is greater than or equal to 70% and less than 90%. The status is displayed in yellow in the console.
        # - **healthy**: Instance storage usage of the instance is less than 70%. The status is displayed in green in the console, indicating a healthy storage status.
        # 
        # > Instance storage usage of the instance is the average storage usage of all segment nodes.
        self.status = status
        # The metric value of the instance storage usage, which is the average storage usage of all segment nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbpgConnectionStatus(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The connection status of the instance. Valid values:
        # 
        # - **critical**: The connection usage of the instance is greater than 95%. The status is displayed in red in the console.
        # - **warning**: The connection usage of the instance is greater than 90% and less than or equal to 95%. The status is displayed in yellow in the console.
        # - **healthy**: The connection usage of the instance is less than or equal to 90%. The status is displayed in green in the console.
        # 
        # > The connection usage of the instance is the maximum connection usage among all master nodes and segment nodes.
        self.status = status
        # The metric value of the instance connection usage, which is the maximum connection usage among all master nodes and segment nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

class DescribeHealthStatusResponseBodyStatusAdbgpSegmentDiskUsagePercentMax(DaraModel):
    def __init__(
        self,
        status: str = None,
        value: float = None,
    ):
        # The maximum storage usage status of segment nodes. Valid values:
        # 
        # - **critical**: Instance storage usage is greater than or equal to 90%, and the instance will be locked.
        # - **warning**: Instance storage usage is greater than or equal to 80% and less than 90%.
        # - **healthy**: Instance storage usage is less than 80%, indicating a healthy storage status.
        self.status = status
        # The metric value of the maximum storage usage of segment nodes.
        # 
        # Unit: %.
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.status is not None:
            result['Status'] = self.status

        if self.value is not None:
            result['Value'] = self.value

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Status') is not None:
            self.status = m.get('Status')

        if m.get('Value') is not None:
            self.value = m.get('Value')

        return self

