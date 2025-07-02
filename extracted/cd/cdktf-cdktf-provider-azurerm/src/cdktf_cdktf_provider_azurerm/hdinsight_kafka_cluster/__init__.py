r'''
# `azurerm_hdinsight_kafka_cluster`

Refer to the Terraform Registry for docs: [`azurerm_hdinsight_kafka_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class HdinsightKafkaCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster azurerm_hdinsight_kafka_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_version: builtins.str,
        component_version: typing.Union["HdinsightKafkaClusterComponentVersion", typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightKafkaClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightKafkaClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union["HdinsightKafkaClusterComputeIsolation", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extension: typing.Optional[typing.Union["HdinsightKafkaClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightKafkaClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightKafkaClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightKafkaClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightKafkaClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        rest_proxy: typing.Optional[typing.Union["HdinsightKafkaClusterRestProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightKafkaClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightKafkaClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightKafkaClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster azurerm_hdinsight_kafka_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#cluster_version HdinsightKafkaCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#component_version HdinsightKafkaCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#gateway HdinsightKafkaCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#location HdinsightKafkaCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#resource_group_name HdinsightKafkaCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#roles HdinsightKafkaCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tier HdinsightKafkaCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#compute_isolation HdinsightKafkaCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#disk_encryption HdinsightKafkaCluster#disk_encryption}
        :param encryption_in_transit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_in_transit_enabled HdinsightKafkaCluster#encryption_in_transit_enabled}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#extension HdinsightKafkaCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#id HdinsightKafkaCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#metastores HdinsightKafkaCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#monitor HdinsightKafkaCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#network HdinsightKafkaCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_link_configuration HdinsightKafkaCluster#private_link_configuration}
        :param rest_proxy: rest_proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#rest_proxy HdinsightKafkaCluster#rest_proxy}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_profile HdinsightKafkaCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account HdinsightKafkaCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account_gen2 HdinsightKafkaCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tags HdinsightKafkaCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#timeouts HdinsightKafkaCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tls_min_version HdinsightKafkaCluster#tls_min_version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dceb5eafc6afac764728d72b85a419aba510f31c3d20bedbbcd056fd803afc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HdinsightKafkaClusterConfig(
            cluster_version=cluster_version,
            component_version=component_version,
            gateway=gateway,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            roles=roles,
            tier=tier,
            compute_isolation=compute_isolation,
            disk_encryption=disk_encryption,
            encryption_in_transit_enabled=encryption_in_transit_enabled,
            extension=extension,
            id=id,
            metastores=metastores,
            monitor=monitor,
            network=network,
            private_link_configuration=private_link_configuration,
            rest_proxy=rest_proxy,
            security_profile=security_profile,
            storage_account=storage_account,
            storage_account_gen2=storage_account_gen2,
            tags=tags,
            timeouts=timeouts,
            tls_min_version=tls_min_version,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a HdinsightKafkaCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HdinsightKafkaCluster to import.
        :param import_from_id: The id of the existing HdinsightKafkaCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HdinsightKafkaCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc2e17bfc35db06db4eb5ec2334494480ccb54540419477d4fb4e295ae5f948)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComponentVersion")
    def put_component_version(self, *, kafka: builtins.str) -> None:
        '''
        :param kafka: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#kafka HdinsightKafkaCluster#kafka}.
        '''
        value = HdinsightKafkaClusterComponentVersion(kafka=kafka)

        return typing.cast(None, jsii.invoke(self, "putComponentVersion", [value]))

    @jsii.member(jsii_name="putComputeIsolation")
    def put_compute_isolation(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#compute_isolation_enabled HdinsightKafkaCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#host_sku HdinsightKafkaCluster#host_sku}.
        '''
        value = HdinsightKafkaClusterComputeIsolation(
            compute_isolation_enabled=compute_isolation_enabled, host_sku=host_sku
        )

        return typing.cast(None, jsii.invoke(self, "putComputeIsolation", [value]))

    @jsii.member(jsii_name="putDiskEncryption")
    def put_disk_encryption(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50838bcf1fde785599873183b27b3f432aaf2690cdca6ec44805ca72827c3a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDiskEncryption", [value]))

    @jsii.member(jsii_name="putExtension")
    def put_extension(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#log_analytics_workspace_id HdinsightKafkaCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary_key HdinsightKafkaCluster#primary_key}.
        '''
        value = HdinsightKafkaClusterExtension(
            log_analytics_workspace_id=log_analytics_workspace_id,
            primary_key=primary_key,
        )

        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putGateway")
    def put_gateway(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        value = HdinsightKafkaClusterGateway(password=password, username=username)

        return typing.cast(None, jsii.invoke(self, "putGateway", [value]))

    @jsii.member(jsii_name="putMetastores")
    def put_metastores(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightKafkaClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightKafkaClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightKafkaClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ambari HdinsightKafkaCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#hive HdinsightKafkaCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#oozie HdinsightKafkaCluster#oozie}
        '''
        value = HdinsightKafkaClusterMetastores(ambari=ambari, hive=hive, oozie=oozie)

        return typing.cast(None, jsii.invoke(self, "putMetastores", [value]))

    @jsii.member(jsii_name="putMonitor")
    def put_monitor(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#log_analytics_workspace_id HdinsightKafkaCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary_key HdinsightKafkaCluster#primary_key}.
        '''
        value = HdinsightKafkaClusterMonitor(
            log_analytics_workspace_id=log_analytics_workspace_id,
            primary_key=primary_key,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitor", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        *,
        connection_direction: typing.Optional[builtins.str] = None,
        private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#connection_direction HdinsightKafkaCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_link_enabled HdinsightKafkaCluster#private_link_enabled}.
        '''
        value = HdinsightKafkaClusterNetwork(
            connection_direction=connection_direction,
            private_link_enabled=private_link_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putPrivateLinkConfiguration")
    def put_private_link_configuration(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#group_id HdinsightKafkaCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ip_configuration HdinsightKafkaCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        '''
        value = HdinsightKafkaClusterPrivateLinkConfiguration(
            group_id=group_id, ip_configuration=ip_configuration, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateLinkConfiguration", [value]))

    @jsii.member(jsii_name="putRestProxy")
    def put_rest_proxy(
        self,
        *,
        security_group_id: builtins.str,
        security_group_name: builtins.str,
    ) -> None:
        '''
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_group_id HdinsightKafkaCluster#security_group_id}.
        :param security_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_group_name HdinsightKafkaCluster#security_group_name}.
        '''
        value = HdinsightKafkaClusterRestProxy(
            security_group_id=security_group_id,
            security_group_name=security_group_name,
        )

        return typing.cast(None, jsii.invoke(self, "putRestProxy", [value]))

    @jsii.member(jsii_name="putRoles")
    def put_roles(
        self,
        *,
        head_node: typing.Union["HdinsightKafkaClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightKafkaClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightKafkaClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
        kafka_management_node: typing.Optional[typing.Union["HdinsightKafkaClusterRolesKafkaManagementNode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#head_node HdinsightKafkaCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#worker_node HdinsightKafkaCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#zookeeper_node HdinsightKafkaCluster#zookeeper_node}
        :param kafka_management_node: kafka_management_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#kafka_management_node HdinsightKafkaCluster#kafka_management_node}
        '''
        value = HdinsightKafkaClusterRoles(
            head_node=head_node,
            worker_node=worker_node,
            zookeeper_node=zookeeper_node,
            kafka_management_node=kafka_management_node,
        )

        return typing.cast(None, jsii.invoke(self, "putRoles", [value]))

    @jsii.member(jsii_name="putSecurityProfile")
    def put_security_profile(
        self,
        *,
        aadds_resource_id: builtins.str,
        domain_name: builtins.str,
        domain_username: builtins.str,
        domain_user_password: builtins.str,
        ldaps_urls: typing.Sequence[builtins.str],
        msi_resource_id: builtins.str,
        cluster_users_group_dns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#aadds_resource_id HdinsightKafkaCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_name HdinsightKafkaCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_username HdinsightKafkaCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_user_password HdinsightKafkaCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ldaps_urls HdinsightKafkaCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#msi_resource_id HdinsightKafkaCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#cluster_users_group_dns HdinsightKafkaCluster#cluster_users_group_dns}.
        '''
        value = HdinsightKafkaClusterSecurityProfile(
            aadds_resource_id=aadds_resource_id,
            domain_name=domain_name,
            domain_username=domain_username,
            domain_user_password=domain_user_password,
            ldaps_urls=ldaps_urls,
            msi_resource_id=msi_resource_id,
            cluster_users_group_dns=cluster_users_group_dns,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityProfile", [value]))

    @jsii.member(jsii_name="putStorageAccount")
    def put_storage_account(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87eb90661b796d317a6f95ef7808ebc5cb2b2fe2f0cb4c6b48a0940846659cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageAccount", [value]))

    @jsii.member(jsii_name="putStorageAccountGen2")
    def put_storage_account_gen2(
        self,
        *,
        filesystem_id: builtins.str,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        managed_identity_resource_id: builtins.str,
        storage_resource_id: builtins.str,
    ) -> None:
        '''
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#filesystem_id HdinsightKafkaCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#is_default HdinsightKafkaCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#managed_identity_resource_id HdinsightKafkaCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_resource_id HdinsightKafkaCluster#storage_resource_id}.
        '''
        value = HdinsightKafkaClusterStorageAccountGen2(
            filesystem_id=filesystem_id,
            is_default=is_default,
            managed_identity_resource_id=managed_identity_resource_id,
            storage_resource_id=storage_resource_id,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageAccountGen2", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#create HdinsightKafkaCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#delete HdinsightKafkaCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#read HdinsightKafkaCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#update HdinsightKafkaCluster#update}.
        '''
        value = HdinsightKafkaClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetComputeIsolation")
    def reset_compute_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeIsolation", []))

    @jsii.member(jsii_name="resetDiskEncryption")
    def reset_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryption", []))

    @jsii.member(jsii_name="resetEncryptionInTransitEnabled")
    def reset_encryption_in_transit_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionInTransitEnabled", []))

    @jsii.member(jsii_name="resetExtension")
    def reset_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtension", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetastores")
    def reset_metastores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastores", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPrivateLinkConfiguration")
    def reset_private_link_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkConfiguration", []))

    @jsii.member(jsii_name="resetRestProxy")
    def reset_rest_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestProxy", []))

    @jsii.member(jsii_name="resetSecurityProfile")
    def reset_security_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProfile", []))

    @jsii.member(jsii_name="resetStorageAccount")
    def reset_storage_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccount", []))

    @jsii.member(jsii_name="resetStorageAccountGen2")
    def reset_storage_account_gen2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountGen2", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTlsMinVersion")
    def reset_tls_min_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsMinVersion", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(
        self,
    ) -> "HdinsightKafkaClusterComponentVersionOutputReference":
        return typing.cast("HdinsightKafkaClusterComponentVersionOutputReference", jsii.get(self, "componentVersion"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolation")
    def compute_isolation(
        self,
    ) -> "HdinsightKafkaClusterComputeIsolationOutputReference":
        return typing.cast("HdinsightKafkaClusterComputeIsolationOutputReference", jsii.get(self, "computeIsolation"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> "HdinsightKafkaClusterDiskEncryptionList":
        return typing.cast("HdinsightKafkaClusterDiskEncryptionList", jsii.get(self, "diskEncryption"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> "HdinsightKafkaClusterExtensionOutputReference":
        return typing.cast("HdinsightKafkaClusterExtensionOutputReference", jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> "HdinsightKafkaClusterGatewayOutputReference":
        return typing.cast("HdinsightKafkaClusterGatewayOutputReference", jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="httpsEndpoint")
    def https_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="kafkaRestProxyEndpoint")
    def kafka_rest_proxy_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kafkaRestProxyEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="metastores")
    def metastores(self) -> "HdinsightKafkaClusterMetastoresOutputReference":
        return typing.cast("HdinsightKafkaClusterMetastoresOutputReference", jsii.get(self, "metastores"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> "HdinsightKafkaClusterMonitorOutputReference":
        return typing.cast("HdinsightKafkaClusterMonitorOutputReference", jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "HdinsightKafkaClusterNetworkOutputReference":
        return typing.cast("HdinsightKafkaClusterNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> "HdinsightKafkaClusterPrivateLinkConfigurationOutputReference":
        return typing.cast("HdinsightKafkaClusterPrivateLinkConfigurationOutputReference", jsii.get(self, "privateLinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="restProxy")
    def rest_proxy(self) -> "HdinsightKafkaClusterRestProxyOutputReference":
        return typing.cast("HdinsightKafkaClusterRestProxyOutputReference", jsii.get(self, "restProxy"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> "HdinsightKafkaClusterRolesOutputReference":
        return typing.cast("HdinsightKafkaClusterRolesOutputReference", jsii.get(self, "roles"))

    @builtins.property
    @jsii.member(jsii_name="securityProfile")
    def security_profile(self) -> "HdinsightKafkaClusterSecurityProfileOutputReference":
        return typing.cast("HdinsightKafkaClusterSecurityProfileOutputReference", jsii.get(self, "securityProfile"))

    @builtins.property
    @jsii.member(jsii_name="sshEndpoint")
    def ssh_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "HdinsightKafkaClusterStorageAccountList":
        return typing.cast("HdinsightKafkaClusterStorageAccountList", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2")
    def storage_account_gen2(
        self,
    ) -> "HdinsightKafkaClusterStorageAccountGen2OutputReference":
        return typing.cast("HdinsightKafkaClusterStorageAccountGen2OutputReference", jsii.get(self, "storageAccountGen2"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HdinsightKafkaClusterTimeoutsOutputReference":
        return typing.cast("HdinsightKafkaClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="componentVersionInput")
    def component_version_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterComponentVersion"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterComponentVersion"], jsii.get(self, "componentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationInput")
    def compute_isolation_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterComputeIsolation"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterComputeIsolation"], jsii.get(self, "computeIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterDiskEncryption"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterDiskEncryption"]]], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInTransitEnabledInput")
    def encryption_in_transit_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionInTransitEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(self) -> typing.Optional["HdinsightKafkaClusterExtension"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterExtension"], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional["HdinsightKafkaClusterGateway"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterGateway"], jsii.get(self, "gatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoresInput")
    def metastores_input(self) -> typing.Optional["HdinsightKafkaClusterMetastores"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterMetastores"], jsii.get(self, "metastoresInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional["HdinsightKafkaClusterMonitor"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterMonitor"], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["HdinsightKafkaClusterNetwork"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationInput")
    def private_link_configuration_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterPrivateLinkConfiguration"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterPrivateLinkConfiguration"], jsii.get(self, "privateLinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="restProxyInput")
    def rest_proxy_input(self) -> typing.Optional["HdinsightKafkaClusterRestProxy"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterRestProxy"], jsii.get(self, "restProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional["HdinsightKafkaClusterRoles"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterRoles"], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileInput")
    def security_profile_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterSecurityProfile"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterSecurityProfile"], jsii.get(self, "securityProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2Input")
    def storage_account_gen2_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterStorageAccountGen2"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterStorageAccountGen2"], jsii.get(self, "storageAccountGen2Input"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterStorageAccount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterStorageAccount"]]], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightKafkaClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightKafkaClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersionInput")
    def tls_min_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsMinVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersion"))

    @cluster_version.setter
    def cluster_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450be19f17a827308824953af7a3afdc26560e8f78f4e5e4103a428dc36de991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionInTransitEnabled")
    def encryption_in_transit_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionInTransitEnabled"))

    @encryption_in_transit_enabled.setter
    def encryption_in_transit_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f222b1ad24efc804e2fe4fbd0d7f02c72f71c18bec81bbac52d56607cec24bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionInTransitEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbefcd59e95117a96cd6e648c539737949ed1aeeeb4a5cedfd5f2435a9ae90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a28088e25680451bf1579ffd3e9ee4cebc09585d564a5d4e48948067608292b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725b7a97f09ebfca30b41f89db2325ddfccf7899a5f952a664a3a89787bf90f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b20d0c099aa29349aa0825bdef6b12a07d9b56d8cd4fa55568bb107c2234d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a620cf4d435d1d306d1f4a0e7bcc0937e9170375091499189c25e9a4de8d8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3963e98d9408cdf38d569c2d59456908c331fb6c190ee31f3d4fc60215397651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersion")
    def tls_min_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsMinVersion"))

    @tls_min_version.setter
    def tls_min_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99255e20cbe66bdc78b650912059350746cc2b689f41a4818ca7a9dcaa1b8f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsMinVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterComponentVersion",
    jsii_struct_bases=[],
    name_mapping={"kafka": "kafka"},
)
class HdinsightKafkaClusterComponentVersion:
    def __init__(self, *, kafka: builtins.str) -> None:
        '''
        :param kafka: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#kafka HdinsightKafkaCluster#kafka}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432f6d8d871a46bc905e89b9f40eef17a5b519a0d1a685585e662d35de375303)
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kafka": kafka,
        }

    @builtins.property
    def kafka(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#kafka HdinsightKafkaCluster#kafka}.'''
        result = self._values.get("kafka")
        assert result is not None, "Required property 'kafka' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterComponentVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterComponentVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterComponentVersionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e64d3d6412bf630ba0b7f33c549b4b5860dff6640b04924cd40fca0d497f5dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kafkaInput")
    def kafka_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kafkaInput"))

    @builtins.property
    @jsii.member(jsii_name="kafka")
    def kafka(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kafka"))

    @kafka.setter
    def kafka(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1113548660d39d5dd8e100d75a256970d48f942b830f7e11ebb14ca1169351e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kafka", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterComponentVersion]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterComponentVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterComponentVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd35d5b1aadb509ae5994ea03d5439281299caf51a979af2caea788b2234537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterComputeIsolation",
    jsii_struct_bases=[],
    name_mapping={
        "compute_isolation_enabled": "computeIsolationEnabled",
        "host_sku": "hostSku",
    },
)
class HdinsightKafkaClusterComputeIsolation:
    def __init__(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#compute_isolation_enabled HdinsightKafkaCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#host_sku HdinsightKafkaCluster#host_sku}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f45694aa0c27f5c9e0022bc16ed373a0f8065b9c446122e2faf735f65ced215)
            check_type(argname="argument compute_isolation_enabled", value=compute_isolation_enabled, expected_type=type_hints["compute_isolation_enabled"])
            check_type(argname="argument host_sku", value=host_sku, expected_type=type_hints["host_sku"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_isolation_enabled is not None:
            self._values["compute_isolation_enabled"] = compute_isolation_enabled
        if host_sku is not None:
            self._values["host_sku"] = host_sku

    @builtins.property
    def compute_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#compute_isolation_enabled HdinsightKafkaCluster#compute_isolation_enabled}.'''
        result = self._values.get("compute_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#host_sku HdinsightKafkaCluster#host_sku}.'''
        result = self._values.get("host_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterComputeIsolation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterComputeIsolationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterComputeIsolationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534675524c3dd9789f79d08981ea12040ed61c87c1551eda1c922d7b83c70476)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComputeIsolationEnabled")
    def reset_compute_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeIsolationEnabled", []))

    @jsii.member(jsii_name="resetHostSku")
    def reset_host_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostSku", []))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationEnabledInput")
    def compute_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "computeIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostSkuInput")
    def host_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationEnabled")
    def compute_isolation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "computeIsolationEnabled"))

    @compute_isolation_enabled.setter
    def compute_isolation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d411c9f3aed01ab04ee5a22f5931d5202b57a413f3ace74a9bf272e8e4d2857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostSku")
    def host_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostSku"))

    @host_sku.setter
    def host_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7efe717f265c207f749f587170e873a10aef14f909192176f51471e1c5755ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterComputeIsolation]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterComputeIsolation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterComputeIsolation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389353f0e8e7dc766ba3468fd66e66b5302647fe7104a7030d3428b2100a0882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_version": "clusterVersion",
        "component_version": "componentVersion",
        "gateway": "gateway",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "roles": "roles",
        "tier": "tier",
        "compute_isolation": "computeIsolation",
        "disk_encryption": "diskEncryption",
        "encryption_in_transit_enabled": "encryptionInTransitEnabled",
        "extension": "extension",
        "id": "id",
        "metastores": "metastores",
        "monitor": "monitor",
        "network": "network",
        "private_link_configuration": "privateLinkConfiguration",
        "rest_proxy": "restProxy",
        "security_profile": "securityProfile",
        "storage_account": "storageAccount",
        "storage_account_gen2": "storageAccountGen2",
        "tags": "tags",
        "timeouts": "timeouts",
        "tls_min_version": "tlsMinVersion",
    },
)
class HdinsightKafkaClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_version: builtins.str,
        component_version: typing.Union[HdinsightKafkaClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightKafkaClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightKafkaClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union[HdinsightKafkaClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extension: typing.Optional[typing.Union["HdinsightKafkaClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightKafkaClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightKafkaClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightKafkaClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightKafkaClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        rest_proxy: typing.Optional[typing.Union["HdinsightKafkaClusterRestProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightKafkaClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightKafkaClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightKafkaClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#cluster_version HdinsightKafkaCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#component_version HdinsightKafkaCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#gateway HdinsightKafkaCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#location HdinsightKafkaCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#resource_group_name HdinsightKafkaCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#roles HdinsightKafkaCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tier HdinsightKafkaCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#compute_isolation HdinsightKafkaCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#disk_encryption HdinsightKafkaCluster#disk_encryption}
        :param encryption_in_transit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_in_transit_enabled HdinsightKafkaCluster#encryption_in_transit_enabled}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#extension HdinsightKafkaCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#id HdinsightKafkaCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#metastores HdinsightKafkaCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#monitor HdinsightKafkaCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#network HdinsightKafkaCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_link_configuration HdinsightKafkaCluster#private_link_configuration}
        :param rest_proxy: rest_proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#rest_proxy HdinsightKafkaCluster#rest_proxy}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_profile HdinsightKafkaCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account HdinsightKafkaCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account_gen2 HdinsightKafkaCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tags HdinsightKafkaCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#timeouts HdinsightKafkaCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tls_min_version HdinsightKafkaCluster#tls_min_version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(component_version, dict):
            component_version = HdinsightKafkaClusterComponentVersion(**component_version)
        if isinstance(gateway, dict):
            gateway = HdinsightKafkaClusterGateway(**gateway)
        if isinstance(roles, dict):
            roles = HdinsightKafkaClusterRoles(**roles)
        if isinstance(compute_isolation, dict):
            compute_isolation = HdinsightKafkaClusterComputeIsolation(**compute_isolation)
        if isinstance(extension, dict):
            extension = HdinsightKafkaClusterExtension(**extension)
        if isinstance(metastores, dict):
            metastores = HdinsightKafkaClusterMetastores(**metastores)
        if isinstance(monitor, dict):
            monitor = HdinsightKafkaClusterMonitor(**monitor)
        if isinstance(network, dict):
            network = HdinsightKafkaClusterNetwork(**network)
        if isinstance(private_link_configuration, dict):
            private_link_configuration = HdinsightKafkaClusterPrivateLinkConfiguration(**private_link_configuration)
        if isinstance(rest_proxy, dict):
            rest_proxy = HdinsightKafkaClusterRestProxy(**rest_proxy)
        if isinstance(security_profile, dict):
            security_profile = HdinsightKafkaClusterSecurityProfile(**security_profile)
        if isinstance(storage_account_gen2, dict):
            storage_account_gen2 = HdinsightKafkaClusterStorageAccountGen2(**storage_account_gen2)
        if isinstance(timeouts, dict):
            timeouts = HdinsightKafkaClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba34d8314e766ae96172d67c8afd70a3c83b4d85b0eb992e302cfc6ab50bb2a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument compute_isolation", value=compute_isolation, expected_type=type_hints["compute_isolation"])
            check_type(argname="argument disk_encryption", value=disk_encryption, expected_type=type_hints["disk_encryption"])
            check_type(argname="argument encryption_in_transit_enabled", value=encryption_in_transit_enabled, expected_type=type_hints["encryption_in_transit_enabled"])
            check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metastores", value=metastores, expected_type=type_hints["metastores"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument private_link_configuration", value=private_link_configuration, expected_type=type_hints["private_link_configuration"])
            check_type(argname="argument rest_proxy", value=rest_proxy, expected_type=type_hints["rest_proxy"])
            check_type(argname="argument security_profile", value=security_profile, expected_type=type_hints["security_profile"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_account_gen2", value=storage_account_gen2, expected_type=type_hints["storage_account_gen2"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_min_version", value=tls_min_version, expected_type=type_hints["tls_min_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_version": cluster_version,
            "component_version": component_version,
            "gateway": gateway,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "roles": roles,
            "tier": tier,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if compute_isolation is not None:
            self._values["compute_isolation"] = compute_isolation
        if disk_encryption is not None:
            self._values["disk_encryption"] = disk_encryption
        if encryption_in_transit_enabled is not None:
            self._values["encryption_in_transit_enabled"] = encryption_in_transit_enabled
        if extension is not None:
            self._values["extension"] = extension
        if id is not None:
            self._values["id"] = id
        if metastores is not None:
            self._values["metastores"] = metastores
        if monitor is not None:
            self._values["monitor"] = monitor
        if network is not None:
            self._values["network"] = network
        if private_link_configuration is not None:
            self._values["private_link_configuration"] = private_link_configuration
        if rest_proxy is not None:
            self._values["rest_proxy"] = rest_proxy
        if security_profile is not None:
            self._values["security_profile"] = security_profile
        if storage_account is not None:
            self._values["storage_account"] = storage_account
        if storage_account_gen2 is not None:
            self._values["storage_account_gen2"] = storage_account_gen2
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls_min_version is not None:
            self._values["tls_min_version"] = tls_min_version

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def cluster_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#cluster_version HdinsightKafkaCluster#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def component_version(self) -> HdinsightKafkaClusterComponentVersion:
        '''component_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#component_version HdinsightKafkaCluster#component_version}
        '''
        result = self._values.get("component_version")
        assert result is not None, "Required property 'component_version' is missing"
        return typing.cast(HdinsightKafkaClusterComponentVersion, result)

    @builtins.property
    def gateway(self) -> "HdinsightKafkaClusterGateway":
        '''gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#gateway HdinsightKafkaCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast("HdinsightKafkaClusterGateway", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#location HdinsightKafkaCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#resource_group_name HdinsightKafkaCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> "HdinsightKafkaClusterRoles":
        '''roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#roles HdinsightKafkaCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast("HdinsightKafkaClusterRoles", result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tier HdinsightKafkaCluster#tier}.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_isolation(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterComputeIsolation]:
        '''compute_isolation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#compute_isolation HdinsightKafkaCluster#compute_isolation}
        '''
        result = self._values.get("compute_isolation")
        return typing.cast(typing.Optional[HdinsightKafkaClusterComputeIsolation], result)

    @builtins.property
    def disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterDiskEncryption"]]]:
        '''disk_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#disk_encryption HdinsightKafkaCluster#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterDiskEncryption"]]], result)

    @builtins.property
    def encryption_in_transit_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_in_transit_enabled HdinsightKafkaCluster#encryption_in_transit_enabled}.'''
        result = self._values.get("encryption_in_transit_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extension(self) -> typing.Optional["HdinsightKafkaClusterExtension"]:
        '''extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#extension HdinsightKafkaCluster#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional["HdinsightKafkaClusterExtension"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#id HdinsightKafkaCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastores(self) -> typing.Optional["HdinsightKafkaClusterMetastores"]:
        '''metastores block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#metastores HdinsightKafkaCluster#metastores}
        '''
        result = self._values.get("metastores")
        return typing.cast(typing.Optional["HdinsightKafkaClusterMetastores"], result)

    @builtins.property
    def monitor(self) -> typing.Optional["HdinsightKafkaClusterMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#monitor HdinsightKafkaCluster#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["HdinsightKafkaClusterMonitor"], result)

    @builtins.property
    def network(self) -> typing.Optional["HdinsightKafkaClusterNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#network HdinsightKafkaCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["HdinsightKafkaClusterNetwork"], result)

    @builtins.property
    def private_link_configuration(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterPrivateLinkConfiguration"]:
        '''private_link_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_link_configuration HdinsightKafkaCluster#private_link_configuration}
        '''
        result = self._values.get("private_link_configuration")
        return typing.cast(typing.Optional["HdinsightKafkaClusterPrivateLinkConfiguration"], result)

    @builtins.property
    def rest_proxy(self) -> typing.Optional["HdinsightKafkaClusterRestProxy"]:
        '''rest_proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#rest_proxy HdinsightKafkaCluster#rest_proxy}
        '''
        result = self._values.get("rest_proxy")
        return typing.cast(typing.Optional["HdinsightKafkaClusterRestProxy"], result)

    @builtins.property
    def security_profile(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterSecurityProfile"]:
        '''security_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_profile HdinsightKafkaCluster#security_profile}
        '''
        result = self._values.get("security_profile")
        return typing.cast(typing.Optional["HdinsightKafkaClusterSecurityProfile"], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterStorageAccount"]]]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account HdinsightKafkaCluster#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterStorageAccount"]]], result)

    @builtins.property
    def storage_account_gen2(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterStorageAccountGen2"]:
        '''storage_account_gen2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account_gen2 HdinsightKafkaCluster#storage_account_gen2}
        '''
        result = self._values.get("storage_account_gen2")
        return typing.cast(typing.Optional["HdinsightKafkaClusterStorageAccountGen2"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tags HdinsightKafkaCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HdinsightKafkaClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#timeouts HdinsightKafkaCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HdinsightKafkaClusterTimeouts"], result)

    @builtins.property
    def tls_min_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#tls_min_version HdinsightKafkaCluster#tls_min_version}.'''
        result = self._values.get("tls_min_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterDiskEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_algorithm": "encryptionAlgorithm",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
        "key_vault_key_id": "keyVaultKeyId",
        "key_vault_managed_identity_id": "keyVaultManagedIdentityId",
    },
)
class HdinsightKafkaClusterDiskEncryption:
    def __init__(
        self,
        *,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_algorithm HdinsightKafkaCluster#encryption_algorithm}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_at_host_enabled HdinsightKafkaCluster#encryption_at_host_enabled}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#key_vault_key_id HdinsightKafkaCluster#key_vault_key_id}.
        :param key_vault_managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#key_vault_managed_identity_id HdinsightKafkaCluster#key_vault_managed_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7484980f5667c25596b855a0ad7b263a4b92e6a0262605d6b18387ec50833e6d)
            check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
            check_type(argname="argument encryption_at_host_enabled", value=encryption_at_host_enabled, expected_type=type_hints["encryption_at_host_enabled"])
            check_type(argname="argument key_vault_key_id", value=key_vault_key_id, expected_type=type_hints["key_vault_key_id"])
            check_type(argname="argument key_vault_managed_identity_id", value=key_vault_managed_identity_id, expected_type=type_hints["key_vault_managed_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_algorithm is not None:
            self._values["encryption_algorithm"] = encryption_algorithm
        if encryption_at_host_enabled is not None:
            self._values["encryption_at_host_enabled"] = encryption_at_host_enabled
        if key_vault_key_id is not None:
            self._values["key_vault_key_id"] = key_vault_key_id
        if key_vault_managed_identity_id is not None:
            self._values["key_vault_managed_identity_id"] = key_vault_managed_identity_id

    @builtins.property
    def encryption_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_algorithm HdinsightKafkaCluster#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#encryption_at_host_enabled HdinsightKafkaCluster#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#key_vault_key_id HdinsightKafkaCluster#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_managed_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#key_vault_managed_identity_id HdinsightKafkaCluster#key_vault_managed_identity_id}.'''
        result = self._values.get("key_vault_managed_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterDiskEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterDiskEncryptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterDiskEncryptionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a379d3bb69774d71044579f4e625449b5e024a170a742185365c7c416e52311)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightKafkaClusterDiskEncryptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc00c90b0869a4670e1f309f9d3474b08cc82606a2ee938a06297689ad25baf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightKafkaClusterDiskEncryptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d562b3d7bcfc60cc8f36d40f47211a25d227550d87e0cdb6906c063565cb68ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f67a0dc094f47fa29c68f9c1fe49c61e20486b131f2daed8d373f250942dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d7bb3d02a4c7eb182d25b69cf12653959d1bbe6e377fe01cd533df3da5d946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterDiskEncryption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterDiskEncryption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterDiskEncryption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a8da519e7d4297a0bc54ffd9ff7f6c013084aa09ae16798b5ee01e07f373f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterDiskEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterDiskEncryptionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d374e29d760fa107af3cce787f96338bb7091a1c30668838f36331559f3f462e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEncryptionAlgorithm")
    def reset_encryption_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAlgorithm", []))

    @jsii.member(jsii_name="resetEncryptionAtHostEnabled")
    def reset_encryption_at_host_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAtHostEnabled", []))

    @jsii.member(jsii_name="resetKeyVaultKeyId")
    def reset_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetKeyVaultManagedIdentityId")
    def reset_key_vault_managed_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultManagedIdentityId", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithmInput")
    def encryption_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAtHostEnabledInput")
    def encryption_at_host_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionAtHostEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyIdInput")
    def key_vault_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultManagedIdentityIdInput")
    def key_vault_managed_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultManagedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAlgorithm")
    def encryption_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAlgorithm"))

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cccd99f5ffc2015acfbf43a90ddad7489bb595903ea1ca06a8e346b364da6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionAtHostEnabled")
    def encryption_at_host_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionAtHostEnabled"))

    @encryption_at_host_enabled.setter
    def encryption_at_host_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e3af73872044131bbde404e5c16dc8d0687a2f111e23e5610355bc81412d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675eaacfcbbf280201dddd57cc46d504dfb6dfc8802be35cb068b47f67efc585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultManagedIdentityId")
    def key_vault_managed_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultManagedIdentityId"))

    @key_vault_managed_identity_id.setter
    def key_vault_managed_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6bc055afdeaa6a64169004ec6a9afe87917ce740fd05d0f4a8c3b5a853bfb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultManagedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterDiskEncryption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterDiskEncryption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterDiskEncryption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2918d61e9b16f9bbde08b6f3e208beccda7869e81ba11b822ab5a21a46eaefcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterExtension",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightKafkaClusterExtension:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#log_analytics_workspace_id HdinsightKafkaCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary_key HdinsightKafkaCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccd4b39ef5be73173eccb805abefdd4b3da4e1ee0a3a77fe94e0f1e93f714c4)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#log_analytics_workspace_id HdinsightKafkaCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary_key HdinsightKafkaCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterExtensionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c815c358f28ed6c61aeb76686b69d8bab6ef00373944b369b09586a0ab626edc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f4ba4a81484f579ac3e442f853531d1232ef92d82da51fee2e5c9455e57a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2081cc8b09c666bb6298b348cb478d10a4d6691b248b31d34552f9c5f6a7041a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterExtension]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterExtension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterExtension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579a6196bb029a554baebc5438c23d723b4336520e75d814559b6a33cd3dff77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterGateway",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class HdinsightKafkaClusterGateway:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861b002857caa548b12f22efd20f592eefbbf5439de17e6e07d68bef8e1e81ab)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterGatewayOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85b73ba8432e9221078b8f85dc73665287d63951119143476aae5b049639b65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87256c3277e9f84cb5d85f016908f6c7f6848dde4f3fc407396ec5c72c25c3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9170927cc559bdf76cd8fadba30ddab0b5f2f31ba6ee3a6769084bb4b99ca21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterGateway]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fa58d462e9f9a1064834d8a156fca09b284784c20173a8156b7668bb03e921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastores",
    jsii_struct_bases=[],
    name_mapping={"ambari": "ambari", "hive": "hive", "oozie": "oozie"},
)
class HdinsightKafkaClusterMetastores:
    def __init__(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightKafkaClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightKafkaClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightKafkaClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ambari HdinsightKafkaCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#hive HdinsightKafkaCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#oozie HdinsightKafkaCluster#oozie}
        '''
        if isinstance(ambari, dict):
            ambari = HdinsightKafkaClusterMetastoresAmbari(**ambari)
        if isinstance(hive, dict):
            hive = HdinsightKafkaClusterMetastoresHive(**hive)
        if isinstance(oozie, dict):
            oozie = HdinsightKafkaClusterMetastoresOozie(**oozie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3714b7aaa672f6af1d80f295a87d7bbbf0022e5f5a4a4db1a93cb196f6a07d)
            check_type(argname="argument ambari", value=ambari, expected_type=type_hints["ambari"])
            check_type(argname="argument hive", value=hive, expected_type=type_hints["hive"])
            check_type(argname="argument oozie", value=oozie, expected_type=type_hints["oozie"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ambari is not None:
            self._values["ambari"] = ambari
        if hive is not None:
            self._values["hive"] = hive
        if oozie is not None:
            self._values["oozie"] = oozie

    @builtins.property
    def ambari(self) -> typing.Optional["HdinsightKafkaClusterMetastoresAmbari"]:
        '''ambari block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ambari HdinsightKafkaCluster#ambari}
        '''
        result = self._values.get("ambari")
        return typing.cast(typing.Optional["HdinsightKafkaClusterMetastoresAmbari"], result)

    @builtins.property
    def hive(self) -> typing.Optional["HdinsightKafkaClusterMetastoresHive"]:
        '''hive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#hive HdinsightKafkaCluster#hive}
        '''
        result = self._values.get("hive")
        return typing.cast(typing.Optional["HdinsightKafkaClusterMetastoresHive"], result)

    @builtins.property
    def oozie(self) -> typing.Optional["HdinsightKafkaClusterMetastoresOozie"]:
        '''oozie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#oozie HdinsightKafkaCluster#oozie}
        '''
        result = self._values.get("oozie")
        return typing.cast(typing.Optional["HdinsightKafkaClusterMetastoresOozie"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterMetastores(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresAmbari",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightKafkaClusterMetastoresAmbari:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61a8707f3634ab451e68ce4eb0e8e85321bc9eb7e901b0aaccb2611b4f3a6a3)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "password": password,
            "server": server,
            "username": username,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterMetastoresAmbari(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterMetastoresAmbariOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresAmbariOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e6c866bd90d02ea041c1b9f90ea857addce7177671b17bd1e88da949edc170)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1296c1bbb12933b9f2f4332e9c1fd05a05a9fc76aca9a60eed759a30d6676fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3e9fcd33d193a9529080e2e4246c2bc47c8485ff3a63c156c2de8f58609c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc7ad00950836fa53bcd4e4d6dcda72b71c7d282f76d36eeaf05ac94da0fc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9200b9b840faae37e18879991aa6e20d226ea37d1b709a6a5740971d7c66082d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastoresAmbari], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterMetastoresAmbari],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3ab4dd9c630b532218916f0f63790912e4a306cdba551c73d56c6f3db1d51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresHive",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightKafkaClusterMetastoresHive:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42837f8a4648b141fdffb9f511a84473deb5fb9447d371a1d9b809ae2e42a92e)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "password": password,
            "server": server,
            "username": username,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterMetastoresHive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterMetastoresHiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresHiveOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4d67c72e771de505275d0c91a1942c01d1599b93d201e70bfe235eae42f885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b872feae300b5e6f4bdd0c5753f0a017a9e7725ae4724b08fd523805d1b565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f38743d77a43153464e2782f4fe5ef0b307bf37d02ddd6689ff69b499597a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4e35cbbba50f753df1733d5551d6deb3e9cdc5f607995cac57a46fbafaa662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22268b165e7a61b25c64fecef2e9df3ef92b3ac6835b3d4b56da631c96da9b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastoresHive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterMetastoresHive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40b8738e50c0ab9fd60e8ccae692f83369edd8fb15c496439adaf16d0c4f142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresOozie",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightKafkaClusterMetastoresOozie:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fd082f932622173bb3796357174abef36336f2324db309425b27fc30f0ff58)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "password": password,
            "server": server,
            "username": username,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterMetastoresOozie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterMetastoresOozieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresOozieOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e4240709b88afb185d1a1ccbeff8400c1b3528eff4e11cc89332798370ebce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468a9cf70b7cb6b8e92f845e71796bf4c53789fdfe32a84f6a1e290d6eeaa54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7bc25ae3de5510d4004bd578d6922c8e2bac1a12d7ee043c51cf84cde51943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1c1d5c059c96ea768355234962c74cdf3a67c55004f30f88d66d650014a13f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5fd2b3a2bd34e90114987c3bfa15f648564d64ea6092cd0070b7050be0312e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastoresOozie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterMetastoresOozie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b14f22d9b80353a579f7719708dc86da74abdc2648db96bb7f75281011ccbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterMetastoresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMetastoresOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba45535eb3ddb4732d93a09d424ddb5d044f0884bd7559b451985cd2523fe48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmbari")
    def put_ambari(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        value = HdinsightKafkaClusterMetastoresAmbari(
            database_name=database_name,
            password=password,
            server=server,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putAmbari", [value]))

    @jsii.member(jsii_name="putHive")
    def put_hive(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        value = HdinsightKafkaClusterMetastoresHive(
            database_name=database_name,
            password=password,
            server=server,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putHive", [value]))

    @jsii.member(jsii_name="putOozie")
    def put_oozie(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#database_name HdinsightKafkaCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#server HdinsightKafkaCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        '''
        value = HdinsightKafkaClusterMetastoresOozie(
            database_name=database_name,
            password=password,
            server=server,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putOozie", [value]))

    @jsii.member(jsii_name="resetAmbari")
    def reset_ambari(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmbari", []))

    @jsii.member(jsii_name="resetHive")
    def reset_hive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHive", []))

    @jsii.member(jsii_name="resetOozie")
    def reset_oozie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOozie", []))

    @builtins.property
    @jsii.member(jsii_name="ambari")
    def ambari(self) -> HdinsightKafkaClusterMetastoresAmbariOutputReference:
        return typing.cast(HdinsightKafkaClusterMetastoresAmbariOutputReference, jsii.get(self, "ambari"))

    @builtins.property
    @jsii.member(jsii_name="hive")
    def hive(self) -> HdinsightKafkaClusterMetastoresHiveOutputReference:
        return typing.cast(HdinsightKafkaClusterMetastoresHiveOutputReference, jsii.get(self, "hive"))

    @builtins.property
    @jsii.member(jsii_name="oozie")
    def oozie(self) -> HdinsightKafkaClusterMetastoresOozieOutputReference:
        return typing.cast(HdinsightKafkaClusterMetastoresOozieOutputReference, jsii.get(self, "oozie"))

    @builtins.property
    @jsii.member(jsii_name="ambariInput")
    def ambari_input(self) -> typing.Optional[HdinsightKafkaClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastoresAmbari], jsii.get(self, "ambariInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveInput")
    def hive_input(self) -> typing.Optional[HdinsightKafkaClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastoresHive], jsii.get(self, "hiveInput"))

    @builtins.property
    @jsii.member(jsii_name="oozieInput")
    def oozie_input(self) -> typing.Optional[HdinsightKafkaClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastoresOozie], jsii.get(self, "oozieInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterMetastores]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMetastores], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterMetastores],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073a85beac394476322b084c41171f4b92c88135b20fb8e066c274b3d2a6c706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMonitor",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightKafkaClusterMonitor:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#log_analytics_workspace_id HdinsightKafkaCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary_key HdinsightKafkaCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a22d522b0a82617083e5011378615ef7ae4b7c224993b3ca1b5c45d9452244e)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#log_analytics_workspace_id HdinsightKafkaCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary_key HdinsightKafkaCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterMonitorOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7d4fdff73d5ff606b5ca6ea40bd3d5273afd9e6bdeb69e5fc122839985cf13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18f64c5b9ab93034ce29940ff49f92940dae5be5a986b04b4ba1a8678e9cbf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28e62af195ab8a8ec143ad792943ba73f11426512b754a8f8c6bf55fef0b78be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterMonitor]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67e1d6202cba3f4df037a640c354eba459225110f7f64a7e5aafee83d757e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "connection_direction": "connectionDirection",
        "private_link_enabled": "privateLinkEnabled",
    },
)
class HdinsightKafkaClusterNetwork:
    def __init__(
        self,
        *,
        connection_direction: typing.Optional[builtins.str] = None,
        private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#connection_direction HdinsightKafkaCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_link_enabled HdinsightKafkaCluster#private_link_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4131c116c4c546c2d5f672c844b6079cda13d5e12ab8f961a779a885e55cc3f8)
            check_type(argname="argument connection_direction", value=connection_direction, expected_type=type_hints["connection_direction"])
            check_type(argname="argument private_link_enabled", value=private_link_enabled, expected_type=type_hints["private_link_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_direction is not None:
            self._values["connection_direction"] = connection_direction
        if private_link_enabled is not None:
            self._values["private_link_enabled"] = private_link_enabled

    @builtins.property
    def connection_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#connection_direction HdinsightKafkaCluster#connection_direction}.'''
        result = self._values.get("connection_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_link_enabled HdinsightKafkaCluster#private_link_enabled}.'''
        result = self._values.get("private_link_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterNetworkOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ec3a827a37c399626aa2b07141a2b8e8425f96a88f8c02344681106f9cd094)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnectionDirection")
    def reset_connection_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionDirection", []))

    @jsii.member(jsii_name="resetPrivateLinkEnabled")
    def reset_private_link_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="connectionDirectionInput")
    def connection_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkEnabledInput")
    def private_link_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateLinkEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionDirection")
    def connection_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionDirection"))

    @connection_direction.setter
    def connection_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1321c33eeaad4cc6cafa686afca619a7f83b51ef7c0599b19d234a17a719b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateLinkEnabled")
    def private_link_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateLinkEnabled"))

    @private_link_enabled.setter
    def private_link_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c4224497308e4df831ceac573dc71b5d900bb8d88adb60da4584030bbcb031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterNetwork]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976301df75ecd9338408584b5eacc0a8f023291039c4b0250b174b9408ca976b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterPrivateLinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "ip_configuration": "ipConfiguration",
        "name": "name",
    },
)
class HdinsightKafkaClusterPrivateLinkConfiguration:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#group_id HdinsightKafkaCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ip_configuration HdinsightKafkaCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        '''
        if isinstance(ip_configuration, dict):
            ip_configuration = HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration(**ip_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ea5868bb7f0d7910244d3f9ac66eb752e57dc1136c7fcddca7d7b24a622970)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
            "ip_configuration": ip_configuration,
            "name": name,
        }

    @builtins.property
    def group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#group_id HdinsightKafkaCluster#group_id}.'''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_configuration(
        self,
    ) -> "HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration":
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ip_configuration HdinsightKafkaCluster#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast("HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterPrivateLinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "primary": "primary",
        "private_ip_address": "privateIpAddress",
        "private_ip_allocation_method": "privateIpAllocationMethod",
        "subnet_id": "subnetId",
    },
)
class HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        private_ip_allocation_method: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary HdinsightKafkaCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_ip_address HdinsightKafkaCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_ip_allocation_method HdinsightKafkaCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b898724f473cb07f9caca46b0b0b9c05a419d5c49f34c5c06e30bb8abdfa2c9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument private_ip_allocation_method", value=private_ip_allocation_method, expected_type=type_hints["private_ip_allocation_method"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if primary is not None:
            self._values["primary"] = primary
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if private_ip_allocation_method is not None:
            self._values["private_ip_allocation_method"] = private_ip_allocation_method
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary HdinsightKafkaCluster#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_ip_address HdinsightKafkaCluster#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_allocation_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_ip_allocation_method HdinsightKafkaCluster#private_ip_allocation_method}.'''
        result = self._values.get("private_ip_allocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterPrivateLinkConfigurationIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterPrivateLinkConfigurationIpConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b933fe43c034148b35a4026ac83ea9c85305e6214b03ce41db319f041c71224e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrimary")
    def reset_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimary", []))

    @jsii.member(jsii_name="resetPrivateIpAddress")
    def reset_private_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddress", []))

    @jsii.member(jsii_name="resetPrivateIpAllocationMethod")
    def reset_private_ip_allocation_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAllocationMethod", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressInput")
    def private_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAllocationMethodInput")
    def private_ip_allocation_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAllocationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a425f38371ae52fb8c841bf5255f4769dc8148a5b2cff322e4558cfb3f82aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primary"))

    @primary.setter
    def primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7422dd0dd6ea1535e054d19485bb093bdac50cb418973a4fd341f3169632381f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2a261e6a44c14f4d4365c58a45e3d551b0ea061b8d324b9e75964a97832bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAllocationMethod")
    def private_ip_allocation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAllocationMethod"))

    @private_ip_allocation_method.setter
    def private_ip_allocation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cbbe84c208b08d2d30d594057099a3353e328ee44459fafc40645f94676e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAllocationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b08434b7af747dc83ca24fb4c8d12a39f228b03ea1203799efdca49c76ef8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62c501e4f536316f9d90cb130601dcceb1dd88d493cb33225604a439df73f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterPrivateLinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterPrivateLinkConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b823bbbbcebada0c5d190f0a5d6922d7ba104b23232fec513e51147707f7b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpConfiguration")
    def put_ip_configuration(
        self,
        *,
        name: builtins.str,
        primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        private_ip_allocation_method: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#primary HdinsightKafkaCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_ip_address HdinsightKafkaCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#private_ip_allocation_method HdinsightKafkaCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        '''
        value = HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration(
            name=name,
            primary=primary,
            private_ip_address=private_ip_address,
            private_ip_allocation_method=private_ip_allocation_method,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putIpConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(
        self,
    ) -> HdinsightKafkaClusterPrivateLinkConfigurationIpConfigurationOutputReference:
        return typing.cast(HdinsightKafkaClusterPrivateLinkConfigurationIpConfigurationOutputReference, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e794ed306e6f92c88dec124940b87a663d700704cc44747d97748c920396d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8082fcf8cb96dd57fba1a005dc400fd1c3bb13b9cf21831481e8f16e276f8ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterPrivateLinkConfiguration]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterPrivateLinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterPrivateLinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cf7377aa52bde3c4f41d17985d902dd881fc3325138ef76e1b0812a9c0cfd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRestProxy",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_id": "securityGroupId",
        "security_group_name": "securityGroupName",
    },
)
class HdinsightKafkaClusterRestProxy:
    def __init__(
        self,
        *,
        security_group_id: builtins.str,
        security_group_name: builtins.str,
    ) -> None:
        '''
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_group_id HdinsightKafkaCluster#security_group_id}.
        :param security_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_group_name HdinsightKafkaCluster#security_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cab362482b4825d975e99c181fdfb0ce5e30c11c232f2d5d8d905d19948c45)
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument security_group_name", value=security_group_name, expected_type=type_hints["security_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_id": security_group_id,
            "security_group_name": security_group_name,
        }

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_group_id HdinsightKafkaCluster#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#security_group_name HdinsightKafkaCluster#security_group_name}.'''
        result = self._values.get("security_group_name")
        assert result is not None, "Required property 'security_group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRestProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRestProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRestProxyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e41e02c53c9fa744cd563b97d9e2acdab3a959e16e29d4638052e821f78cb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupNameInput")
    def security_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc6d907231c27b32aea10dbab13b78dfd798fd26519c3ddd1edd3d69296e2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupName"))

    @security_group_name.setter
    def security_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c1c6ac78ebabc1e9c9434c28fe065b8ee73823396c2e09eda0265ce93cdc18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterRestProxy]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRestProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterRestProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf02267b5757185286e0ddfd0b89fa1ec271f50b3343c7f91368c31fde0fac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRoles",
    jsii_struct_bases=[],
    name_mapping={
        "head_node": "headNode",
        "worker_node": "workerNode",
        "zookeeper_node": "zookeeperNode",
        "kafka_management_node": "kafkaManagementNode",
    },
)
class HdinsightKafkaClusterRoles:
    def __init__(
        self,
        *,
        head_node: typing.Union["HdinsightKafkaClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightKafkaClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightKafkaClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
        kafka_management_node: typing.Optional[typing.Union["HdinsightKafkaClusterRolesKafkaManagementNode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#head_node HdinsightKafkaCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#worker_node HdinsightKafkaCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#zookeeper_node HdinsightKafkaCluster#zookeeper_node}
        :param kafka_management_node: kafka_management_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#kafka_management_node HdinsightKafkaCluster#kafka_management_node}
        '''
        if isinstance(head_node, dict):
            head_node = HdinsightKafkaClusterRolesHeadNode(**head_node)
        if isinstance(worker_node, dict):
            worker_node = HdinsightKafkaClusterRolesWorkerNode(**worker_node)
        if isinstance(zookeeper_node, dict):
            zookeeper_node = HdinsightKafkaClusterRolesZookeeperNode(**zookeeper_node)
        if isinstance(kafka_management_node, dict):
            kafka_management_node = HdinsightKafkaClusterRolesKafkaManagementNode(**kafka_management_node)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d6f348f26be35d76737112d1a7abbb9f337de1afbe01dd7ba12abd0cd5732a)
            check_type(argname="argument head_node", value=head_node, expected_type=type_hints["head_node"])
            check_type(argname="argument worker_node", value=worker_node, expected_type=type_hints["worker_node"])
            check_type(argname="argument zookeeper_node", value=zookeeper_node, expected_type=type_hints["zookeeper_node"])
            check_type(argname="argument kafka_management_node", value=kafka_management_node, expected_type=type_hints["kafka_management_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "head_node": head_node,
            "worker_node": worker_node,
            "zookeeper_node": zookeeper_node,
        }
        if kafka_management_node is not None:
            self._values["kafka_management_node"] = kafka_management_node

    @builtins.property
    def head_node(self) -> "HdinsightKafkaClusterRolesHeadNode":
        '''head_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#head_node HdinsightKafkaCluster#head_node}
        '''
        result = self._values.get("head_node")
        assert result is not None, "Required property 'head_node' is missing"
        return typing.cast("HdinsightKafkaClusterRolesHeadNode", result)

    @builtins.property
    def worker_node(self) -> "HdinsightKafkaClusterRolesWorkerNode":
        '''worker_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#worker_node HdinsightKafkaCluster#worker_node}
        '''
        result = self._values.get("worker_node")
        assert result is not None, "Required property 'worker_node' is missing"
        return typing.cast("HdinsightKafkaClusterRolesWorkerNode", result)

    @builtins.property
    def zookeeper_node(self) -> "HdinsightKafkaClusterRolesZookeeperNode":
        '''zookeeper_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#zookeeper_node HdinsightKafkaCluster#zookeeper_node}
        '''
        result = self._values.get("zookeeper_node")
        assert result is not None, "Required property 'zookeeper_node' is missing"
        return typing.cast("HdinsightKafkaClusterRolesZookeeperNode", result)

    @builtins.property
    def kafka_management_node(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterRolesKafkaManagementNode"]:
        '''kafka_management_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#kafka_management_node HdinsightKafkaCluster#kafka_management_node}
        '''
        result = self._values.get("kafka_management_node")
        return typing.cast(typing.Optional["HdinsightKafkaClusterRolesKafkaManagementNode"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesHeadNode",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "vm_size": "vmSize",
        "password": "password",
        "script_actions": "scriptActions",
        "ssh_keys": "sshKeys",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
    },
)
class HdinsightKafkaClusterRolesHeadNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ec644fc2ea13378ebfbc5322ec4f06167b11a8b3c28462185040a7b0e28ff9)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument script_actions", value=script_actions, expected_type=type_hints["script_actions"])
            check_type(argname="argument ssh_keys", value=ssh_keys, expected_type=type_hints["ssh_keys"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
            "vm_size": vm_size,
        }
        if password is not None:
            self._values["password"] = password
        if script_actions is not None:
            self._values["script_actions"] = script_actions
        if ssh_keys is not None:
            self._values["ssh_keys"] = ssh_keys
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesHeadNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesHeadNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesHeadNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesHeadNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesHeadNodeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f04d149b884285865e5321372da1438428d05689d626ba115f8f55964cc2665)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f348422add18a4a92a8128fc0617410159e5f92e24c5fe581fd2b1e540f1d5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScriptActions", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetScriptActions")
    def reset_script_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptActions", []))

    @jsii.member(jsii_name="resetSshKeys")
    def reset_ssh_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeys", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(self) -> "HdinsightKafkaClusterRolesHeadNodeScriptActionsList":
        return typing.cast("HdinsightKafkaClusterRolesHeadNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesHeadNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesHeadNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeysInput")
    def ssh_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98290c5848417dea2b0810d23b1db501751960a5d89f0e6cc1d2150aec5d395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b785f3752ed166b275d9d0574c59a4a9f50c645a518515df7a56a16935822b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5232f1aa80b8a3872054777828d52243f322492c9f5c569f12579a956d654fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79dbfa4da50fbb14b0d6543853dc5e35253d54e14bb92710a2c8d287899703ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7630d8b0cd8fb657e3c6b2aa40b92856399c94dbe27afd41fce6d6f089b08cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20d91453e96725d30b4347337333e7ce02e100188c6eca8bef8a93b407618a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRolesHeadNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterRolesHeadNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde1bb347602956c020787783b685b1146b7d42b22839cd9379b3b1b81ea6bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesHeadNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightKafkaClusterRolesHeadNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19f1bd02bb258d268c020fc4f98c2fa67aa4212c1820580e56f0bcd9f2c180e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "uri": uri,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesHeadNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesHeadNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesHeadNodeScriptActionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fc24cf30c57a7163370146dd9a8f567953f1a4a802368385b6b9a0c754453d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightKafkaClusterRolesHeadNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843621273886e918c853b41569e5b74c7e0978e095f27f5b24fe13f4433926b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightKafkaClusterRolesHeadNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88ed4635d7f3f5d8721e84f69a376dd146d73f0500410f913be8fe3e7d94337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af23b634229d2058ae5cf3a2ad7b829b0ba81a4498e7daae89fc758e43dfed7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f53c74f908eb463f5b1b602be2bec1ab54f2fb6a7f1f76413ba73dcd09f78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesHeadNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesHeadNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesHeadNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc4fe54b18df25afc64457ab7ca6d64d80aa9e31474ae7714716cf98d9b13f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterRolesHeadNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesHeadNodeScriptActionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0623f316504a3ea15ab19c73bf18f7bdc944e1e9391d2f28bf264b3f238725b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ace0d85167d8da2a9adfa52cbc631adbfd3410628cdccce6cf6284eaf3da0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c209b08cfdfa5296135aacd5eb60b4b03e79213e4d3b3e3d5ac241363cf72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc867a110fc7db9b178075f6920f21c00207125cec731765b6cb04a4adc73f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesHeadNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesHeadNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesHeadNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a691438cca4311411686f5c441a4182324a2bf453c9ede1d12b11a90861b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesKafkaManagementNode",
    jsii_struct_bases=[],
    name_mapping={
        "vm_size": "vmSize",
        "password": "password",
        "script_actions": "scriptActions",
        "ssh_keys": "sshKeys",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
    },
)
class HdinsightKafkaClusterRolesKafkaManagementNode:
    def __init__(
        self,
        *,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6a39da11579e30ddf4d394d3aa9c3003ec87002dc09ff6b405eec276162f39)
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument script_actions", value=script_actions, expected_type=type_hints["script_actions"])
            check_type(argname="argument ssh_keys", value=ssh_keys, expected_type=type_hints["ssh_keys"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vm_size": vm_size,
        }
        if password is not None:
            self._values["password"] = password
        if script_actions is not None:
            self._values["script_actions"] = script_actions
        if ssh_keys is not None:
            self._values["ssh_keys"] = ssh_keys
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesKafkaManagementNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesKafkaManagementNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesKafkaManagementNodeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8359b976cf0b2269e06ed6ce4bdb301b6386ad2adf33c6888c941efcb4a489)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbf4ce063f738d4a459d352f56c68aa553a6761ceaa38855dcce31dd6959740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScriptActions", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetScriptActions")
    def reset_script_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptActions", []))

    @jsii.member(jsii_name="resetSshKeys")
    def reset_ssh_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeys", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(
        self,
    ) -> "HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsList":
        return typing.cast("HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeysInput")
    def ssh_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb5fdaa7c71e7612831bf5b6dba248859bd6523e41837db6c379fd22aea9fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8b22139d547e738f03581b99ee087ec28b1783b0d375429bf7b81f1a591241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e70a864ea378ce137e36ad16698c0fb03171e33b598bf00356fbbb6160118b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2668ee62b72e57902b00675e2ab25e952fee3189c117969028806456cdc89fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a2420c3daca57c8783cd8d73ed49ceb8dd1c93af9f9708e31b67b99ed28b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterRolesKafkaManagementNode]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRolesKafkaManagementNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterRolesKafkaManagementNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f80902fad2dc9e4d1dd828d1b8616e1cade30d1dbbaf1c457d781b68005cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba68dde5c5ea1d569880a706a5cf43bdf06ea8c1d235f338eb8132012208fc21)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "uri": uri,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec382746fb9afd67ecbe7c30280232d36faf8d79c9d791f61c84f30ea642fa26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8753663368cee90f631a7b02c8625bf09e09951bece7dcedf554413722863bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32c92d33a9022ffd5f78490a057b02d03451eddbfa16eb8314fe259d7e31625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb80dfc3b57cd7acec861323d8e1309793d78f593047e34c952f17118a8e634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493738671ce775c42c972d5de204a5899325391f08978a01b13ad3edaeb69779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acfc65526d888925ae648e2bfea7ec8197e5fb0dffbead3813522cfa3b180ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878625d1d4a56bb65cbc4b382105d486e6f868a7279ace47041adf26d79e8049)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e203fe8372d6406e586ca9565b7521c2d8d49554e03ce6f6d5eec7570131c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1054d038e647669263f4d6c731a8c3063ba30750baea0545c0f9ccf9c29ae3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca3388521b033e9e45faea5914a1342ec782b284e473447f004e2a5eaff9b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3782012019d14866e78875b4063c99ed26d895b30c587484d5844cfaf9a049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce288a5c990a83cf1bcccd03a6ceb01e01b8ecad4f9ade723408db8205d885f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeadNode")
    def put_head_node(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        value = HdinsightKafkaClusterRolesHeadNode(
            username=username,
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putHeadNode", [value]))

    @jsii.member(jsii_name="putKafkaManagementNode")
    def put_kafka_management_node(
        self,
        *,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        value = HdinsightKafkaClusterRolesKafkaManagementNode(
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putKafkaManagementNode", [value]))

    @jsii.member(jsii_name="putWorkerNode")
    def put_worker_node(
        self,
        *,
        number_of_disks_per_node: jsii.Number,
        target_instance_count: jsii.Number,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param number_of_disks_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#number_of_disks_per_node HdinsightKafkaCluster#number_of_disks_per_node}.
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#target_instance_count HdinsightKafkaCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        value = HdinsightKafkaClusterRolesWorkerNode(
            number_of_disks_per_node=number_of_disks_per_node,
            target_instance_count=target_instance_count,
            username=username,
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerNode", [value]))

    @jsii.member(jsii_name="putZookeeperNode")
    def put_zookeeper_node(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        value = HdinsightKafkaClusterRolesZookeeperNode(
            username=username,
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putZookeeperNode", [value]))

    @jsii.member(jsii_name="resetKafkaManagementNode")
    def reset_kafka_management_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafkaManagementNode", []))

    @builtins.property
    @jsii.member(jsii_name="headNode")
    def head_node(self) -> HdinsightKafkaClusterRolesHeadNodeOutputReference:
        return typing.cast(HdinsightKafkaClusterRolesHeadNodeOutputReference, jsii.get(self, "headNode"))

    @builtins.property
    @jsii.member(jsii_name="kafkaManagementNode")
    def kafka_management_node(
        self,
    ) -> HdinsightKafkaClusterRolesKafkaManagementNodeOutputReference:
        return typing.cast(HdinsightKafkaClusterRolesKafkaManagementNodeOutputReference, jsii.get(self, "kafkaManagementNode"))

    @builtins.property
    @jsii.member(jsii_name="workerNode")
    def worker_node(self) -> "HdinsightKafkaClusterRolesWorkerNodeOutputReference":
        return typing.cast("HdinsightKafkaClusterRolesWorkerNodeOutputReference", jsii.get(self, "workerNode"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNode")
    def zookeeper_node(
        self,
    ) -> "HdinsightKafkaClusterRolesZookeeperNodeOutputReference":
        return typing.cast("HdinsightKafkaClusterRolesZookeeperNodeOutputReference", jsii.get(self, "zookeeperNode"))

    @builtins.property
    @jsii.member(jsii_name="headNodeInput")
    def head_node_input(self) -> typing.Optional[HdinsightKafkaClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRolesHeadNode], jsii.get(self, "headNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaManagementNodeInput")
    def kafka_management_node_input(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterRolesKafkaManagementNode]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRolesKafkaManagementNode], jsii.get(self, "kafkaManagementNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="workerNodeInput")
    def worker_node_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterRolesWorkerNode"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterRolesWorkerNode"], jsii.get(self, "workerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNodeInput")
    def zookeeper_node_input(
        self,
    ) -> typing.Optional["HdinsightKafkaClusterRolesZookeeperNode"]:
        return typing.cast(typing.Optional["HdinsightKafkaClusterRolesZookeeperNode"], jsii.get(self, "zookeeperNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterRoles]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d4cbf39b7b410d0e34fb0c5d832473279bf5d44e261c2087305de7a00bc6a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesWorkerNode",
    jsii_struct_bases=[],
    name_mapping={
        "number_of_disks_per_node": "numberOfDisksPerNode",
        "target_instance_count": "targetInstanceCount",
        "username": "username",
        "vm_size": "vmSize",
        "password": "password",
        "script_actions": "scriptActions",
        "ssh_keys": "sshKeys",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
    },
)
class HdinsightKafkaClusterRolesWorkerNode:
    def __init__(
        self,
        *,
        number_of_disks_per_node: jsii.Number,
        target_instance_count: jsii.Number,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param number_of_disks_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#number_of_disks_per_node HdinsightKafkaCluster#number_of_disks_per_node}.
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#target_instance_count HdinsightKafkaCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6b0f757c9a6fc48d040bc32ab9bdda3bc32e34c2d4493534853de1412d3e76)
            check_type(argname="argument number_of_disks_per_node", value=number_of_disks_per_node, expected_type=type_hints["number_of_disks_per_node"])
            check_type(argname="argument target_instance_count", value=target_instance_count, expected_type=type_hints["target_instance_count"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument script_actions", value=script_actions, expected_type=type_hints["script_actions"])
            check_type(argname="argument ssh_keys", value=ssh_keys, expected_type=type_hints["ssh_keys"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "number_of_disks_per_node": number_of_disks_per_node,
            "target_instance_count": target_instance_count,
            "username": username,
            "vm_size": vm_size,
        }
        if password is not None:
            self._values["password"] = password
        if script_actions is not None:
            self._values["script_actions"] = script_actions
        if ssh_keys is not None:
            self._values["ssh_keys"] = ssh_keys
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id

    @builtins.property
    def number_of_disks_per_node(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#number_of_disks_per_node HdinsightKafkaCluster#number_of_disks_per_node}.'''
        result = self._values.get("number_of_disks_per_node")
        assert result is not None, "Required property 'number_of_disks_per_node' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def target_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#target_instance_count HdinsightKafkaCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesWorkerNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesWorkerNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesWorkerNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesWorkerNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesWorkerNodeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a78e58531d5c63a80493a6e4049c569dd0f4e74ae131c3db4f60437354b21c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f3e3c1ba02dace3bfbf71413667fee072c64e0b0c36ed5286b84d3265bf857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScriptActions", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetScriptActions")
    def reset_script_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptActions", []))

    @jsii.member(jsii_name="resetSshKeys")
    def reset_ssh_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeys", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(self) -> "HdinsightKafkaClusterRolesWorkerNodeScriptActionsList":
        return typing.cast("HdinsightKafkaClusterRolesWorkerNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="numberOfDisksPerNodeInput")
    def number_of_disks_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfDisksPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesWorkerNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesWorkerNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeysInput")
    def ssh_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCountInput")
    def target_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfDisksPerNode")
    def number_of_disks_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfDisksPerNode"))

    @number_of_disks_per_node.setter
    def number_of_disks_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4726c55d2b6d296be463996d265cb4dab0916b7b12b84deb61c6f83d0e35ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfDisksPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dac03eca80112ab79ee7b1e477138af41b4589192cb4c2c68e712770b6c7f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d63005984577a403c96e0b2700905871d179b94b852fa8c0af615cf63a640ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdcb63c5208f889a12b86d91283b7faeed47ad766bae3c4d781add00ad095f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68096796ba4b45fc055609ebcfece4692ccd60d699ad8453ade7bb562e842ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f19b34032754d4af596383ebcd6c4218296c2ddee9a2231badb08ec147007a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db4a009ad05dee02ed6b00e85ef48456939d7e2a82ee3bb1d68bcfc3b9f8023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3288f7ee2c1be4b59927ba402cc8c3e79cf0d7e46960c76a8face83f0401a10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterRolesWorkerNode]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRolesWorkerNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterRolesWorkerNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97946d6b69e8adf6e01e9fcd1c101265cc96971fa3ffe78de963d7623b589994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesWorkerNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightKafkaClusterRolesWorkerNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c720676d183f0fb0550ab96974f04a0fe1cc092363bc3c9c4b2fdb55eded898d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "uri": uri,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesWorkerNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesWorkerNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesWorkerNodeScriptActionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b845f7225d0d2f98da97ec994de69fa9035a55fa85d1d2e93c9b6104e52f96e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightKafkaClusterRolesWorkerNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edd1bfe07474567e61b8be0e0227e849c3d488052110da887375b9144bb6666)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightKafkaClusterRolesWorkerNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809fbc96682e11c15a96276757bdc3303ac72485b99d0b58ae90805f72b80923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64a823d9eaa9ef7de4732adb66b05acef63980eba4e0197d08caab26861d29f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311b69ded078fd7962a8a648f3f1faeb1d25b0a5f9f67e29893dd26ad774329b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesWorkerNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesWorkerNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesWorkerNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b423115a22c99a4a13fef74a9cb6b885eb4c17b9c7e504481a745aedea6430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterRolesWorkerNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesWorkerNodeScriptActionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2d73fae72f64a8e201b86f320421bd088d846377f6869e8f09a3ddc631738d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b698c713df97b45955b2f932dad933084324eba7f67e0ecc962bc1bfa75a294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef0917a4357afbc8fde77db81ebae35392491a84ba0685b8d3349f4f5b7bbd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7303c1c392d9aeadd4048347d4de23b29be903e3195d79f8b9f35275c313378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesWorkerNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesWorkerNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesWorkerNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353ec9ca73de3cc9ad1097aab068b04632a7c59bb2a56b848e508b4fddc87b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesZookeeperNode",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "vm_size": "vmSize",
        "password": "password",
        "script_actions": "scriptActions",
        "ssh_keys": "sshKeys",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
    },
)
class HdinsightKafkaClusterRolesZookeeperNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb51fd30bae887dff4c96b924201c914007ce6e39f5dc57ef3b7112b7bc8c073)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument script_actions", value=script_actions, expected_type=type_hints["script_actions"])
            check_type(argname="argument ssh_keys", value=ssh_keys, expected_type=type_hints["ssh_keys"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
            "vm_size": vm_size,
        }
        if password is not None:
            self._values["password"] = password
        if script_actions is not None:
            self._values["script_actions"] = script_actions
        if ssh_keys is not None:
            self._values["ssh_keys"] = ssh_keys
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#username HdinsightKafkaCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#vm_size HdinsightKafkaCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#password HdinsightKafkaCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesZookeeperNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#script_actions HdinsightKafkaCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesZookeeperNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ssh_keys HdinsightKafkaCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#subnet_id HdinsightKafkaCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#virtual_network_id HdinsightKafkaCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesZookeeperNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesZookeeperNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesZookeeperNodeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b95878d18d4d2d189995af1ab96101ed8dd419dcf405d397bb6c273d525682)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightKafkaClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1bc5051d257431d23e7de1071592b14bad3dbf98a5c2641f35a8f6ee18a572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScriptActions", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetScriptActions")
    def reset_script_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptActions", []))

    @jsii.member(jsii_name="resetSshKeys")
    def reset_ssh_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeys", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(
        self,
    ) -> "HdinsightKafkaClusterRolesZookeeperNodeScriptActionsList":
        return typing.cast("HdinsightKafkaClusterRolesZookeeperNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesZookeeperNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightKafkaClusterRolesZookeeperNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeysInput")
    def ssh_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7522914ec53b8e6562260b50c0e5d7d8455ad29e4d505f1dab72dd1cb4ff8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e441d3f1f2940b8c1eddb13facc179635e97013d154fcab0fbd16482fd7a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b9eea956ddb033bdeca99341b5fe8592c62497d4599ef05686545d644df1d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7f1220e063778a4b1dc59f2ee2fcb8f0c7444836fecb62faac4d6ea4653cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e72a0cbc267da4b122555f590fcd93261af2f7c12e53ca03ee51e1b318a0373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579e97b67f60b18bd3f2743b942072ec76babdd35f6103d4bd5c0f90835fab1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterRolesZookeeperNode]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterRolesZookeeperNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterRolesZookeeperNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7987d6ab34aac6a928ce55d7358a6a11625a2d648a1a16442311665dca2a9d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesZookeeperNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightKafkaClusterRolesZookeeperNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8a9af643b0be3ac1b7a5b7fd1a58b7a5f6875e015a710d69fd55d29936ac6f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "uri": uri,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#name HdinsightKafkaCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#uri HdinsightKafkaCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#parameters HdinsightKafkaCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterRolesZookeeperNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterRolesZookeeperNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesZookeeperNodeScriptActionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c406548c2fc8b4a0bbf2a9dd1faf0ecf915335251f966982c0040293bc6447)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightKafkaClusterRolesZookeeperNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8b7528cf1122cac4355cb348e3840b849da18a32d2c0ea297a17dcea52c9b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightKafkaClusterRolesZookeeperNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bbde734a45a8f0174f3c446ee09c264cb7cf5b8430853d555ebe1a1f4bfbea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c383693ddb9db63f0673f7012d00491a88880453c72d53d813e12a7de1a160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f1a8fbcb877c5b45bbb680cab35689468aefe2f6f68237e33b577e436b3a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesZookeeperNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesZookeeperNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesZookeeperNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5db31a36f76a8e42e223c5ac2d2c3766fa68ccb1b82b161cd71b029252a6161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterRolesZookeeperNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterRolesZookeeperNodeScriptActionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b151a0749cf025b5de5497e7d247d89bbed32a7a3e8fd3e3c574bba35c294e7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dda7425d3d5b636f9d654144b5b0c0855ce719341eb474ddb642fdbb74e967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6cdbf413759549613caa644e2a0473a7f2c44663e0d54c58fd31aaedb988839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71deb0878620b901b8fc9c208cc67df71a1aa8173812169a4ecbf780a0b0d53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesZookeeperNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesZookeeperNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesZookeeperNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d0b9653b94a88ef67b025ac8514c4e981ee999e44b0f71177b853956cef4c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterSecurityProfile",
    jsii_struct_bases=[],
    name_mapping={
        "aadds_resource_id": "aaddsResourceId",
        "domain_name": "domainName",
        "domain_username": "domainUsername",
        "domain_user_password": "domainUserPassword",
        "ldaps_urls": "ldapsUrls",
        "msi_resource_id": "msiResourceId",
        "cluster_users_group_dns": "clusterUsersGroupDns",
    },
)
class HdinsightKafkaClusterSecurityProfile:
    def __init__(
        self,
        *,
        aadds_resource_id: builtins.str,
        domain_name: builtins.str,
        domain_username: builtins.str,
        domain_user_password: builtins.str,
        ldaps_urls: typing.Sequence[builtins.str],
        msi_resource_id: builtins.str,
        cluster_users_group_dns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#aadds_resource_id HdinsightKafkaCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_name HdinsightKafkaCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_username HdinsightKafkaCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_user_password HdinsightKafkaCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ldaps_urls HdinsightKafkaCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#msi_resource_id HdinsightKafkaCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#cluster_users_group_dns HdinsightKafkaCluster#cluster_users_group_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f534577332faccd3f0df5b45279f5a3473e641e9b09409a3dcb4a93e1e171ed6)
            check_type(argname="argument aadds_resource_id", value=aadds_resource_id, expected_type=type_hints["aadds_resource_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_username", value=domain_username, expected_type=type_hints["domain_username"])
            check_type(argname="argument domain_user_password", value=domain_user_password, expected_type=type_hints["domain_user_password"])
            check_type(argname="argument ldaps_urls", value=ldaps_urls, expected_type=type_hints["ldaps_urls"])
            check_type(argname="argument msi_resource_id", value=msi_resource_id, expected_type=type_hints["msi_resource_id"])
            check_type(argname="argument cluster_users_group_dns", value=cluster_users_group_dns, expected_type=type_hints["cluster_users_group_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aadds_resource_id": aadds_resource_id,
            "domain_name": domain_name,
            "domain_username": domain_username,
            "domain_user_password": domain_user_password,
            "ldaps_urls": ldaps_urls,
            "msi_resource_id": msi_resource_id,
        }
        if cluster_users_group_dns is not None:
            self._values["cluster_users_group_dns"] = cluster_users_group_dns

    @builtins.property
    def aadds_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#aadds_resource_id HdinsightKafkaCluster#aadds_resource_id}.'''
        result = self._values.get("aadds_resource_id")
        assert result is not None, "Required property 'aadds_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_name HdinsightKafkaCluster#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_username HdinsightKafkaCluster#domain_username}.'''
        result = self._values.get("domain_username")
        assert result is not None, "Required property 'domain_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_user_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#domain_user_password HdinsightKafkaCluster#domain_user_password}.'''
        result = self._values.get("domain_user_password")
        assert result is not None, "Required property 'domain_user_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ldaps_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#ldaps_urls HdinsightKafkaCluster#ldaps_urls}.'''
        result = self._values.get("ldaps_urls")
        assert result is not None, "Required property 'ldaps_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def msi_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#msi_resource_id HdinsightKafkaCluster#msi_resource_id}.'''
        result = self._values.get("msi_resource_id")
        assert result is not None, "Required property 'msi_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_users_group_dns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#cluster_users_group_dns HdinsightKafkaCluster#cluster_users_group_dns}.'''
        result = self._values.get("cluster_users_group_dns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterSecurityProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterSecurityProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterSecurityProfileOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216f28baf593affcc1a35d9de2e1019b5a93cd2bd085e375a6650bd43512fd22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterUsersGroupDns")
    def reset_cluster_users_group_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterUsersGroupDns", []))

    @builtins.property
    @jsii.member(jsii_name="aaddsResourceIdInput")
    def aadds_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aaddsResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterUsersGroupDnsInput")
    def cluster_users_group_dns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusterUsersGroupDnsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainUsernameInput")
    def domain_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainUserPasswordInput")
    def domain_user_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainUserPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="ldapsUrlsInput")
    def ldaps_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ldapsUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="msiResourceIdInput")
    def msi_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="aaddsResourceId")
    def aadds_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aaddsResourceId"))

    @aadds_resource_id.setter
    def aadds_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f9cd8b9c6b4683a3963a1dbc05fc600c62e0a2a48c1303e65b809f79418d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aaddsResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterUsersGroupDns")
    def cluster_users_group_dns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterUsersGroupDns"))

    @cluster_users_group_dns.setter
    def cluster_users_group_dns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db8c22fc0079009066c697032ca411cc60bae5cc4d4a430c1040a7e3ba32806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterUsersGroupDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02200eba68eef973038aadbd4a9ccea7a891cfa9c4cd68501908df43162da767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUsername")
    def domain_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUsername"))

    @domain_username.setter
    def domain_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ee2240e77c5791aad3eefc7eb79793199514c2ad3e61a4ea526f1ad713b289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUserPassword")
    def domain_user_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUserPassword"))

    @domain_user_password.setter
    def domain_user_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e40e9b4dd13169d8944efdd0bb9a485ad2607db58c460f5f0b1320bbd60c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUserPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapsUrls")
    def ldaps_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ldapsUrls"))

    @ldaps_urls.setter
    def ldaps_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0441e2551547109d05060cc4dbe961345566d23ff2a8466c2942ab15892370b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapsUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiResourceId")
    def msi_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "msiResourceId"))

    @msi_resource_id.setter
    def msi_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830d41e4c81ca36a64de71ee96a553d0b34c044285c29509f10796143e50ae6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightKafkaClusterSecurityProfile]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterSecurityProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterSecurityProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2892aa79d35702361f6d300adcf6a835f10189533c539f4734710a1e5c6f45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterStorageAccount",
    jsii_struct_bases=[],
    name_mapping={
        "is_default": "isDefault",
        "storage_account_key": "storageAccountKey",
        "storage_container_id": "storageContainerId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightKafkaClusterStorageAccount:
    def __init__(
        self,
        *,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_account_key: builtins.str,
        storage_container_id: builtins.str,
        storage_resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#is_default HdinsightKafkaCluster#is_default}.
        :param storage_account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account_key HdinsightKafkaCluster#storage_account_key}.
        :param storage_container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_container_id HdinsightKafkaCluster#storage_container_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_resource_id HdinsightKafkaCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a61eea5c11a54c48ed9becfaa28c5cc2bae2bf464833e7bd7202c74dde52f4)
            check_type(argname="argument is_default", value=is_default, expected_type=type_hints["is_default"])
            check_type(argname="argument storage_account_key", value=storage_account_key, expected_type=type_hints["storage_account_key"])
            check_type(argname="argument storage_container_id", value=storage_container_id, expected_type=type_hints["storage_container_id"])
            check_type(argname="argument storage_resource_id", value=storage_resource_id, expected_type=type_hints["storage_resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_default": is_default,
            "storage_account_key": storage_account_key,
            "storage_container_id": storage_container_id,
        }
        if storage_resource_id is not None:
            self._values["storage_resource_id"] = storage_resource_id

    @builtins.property
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#is_default HdinsightKafkaCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_account_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_account_key HdinsightKafkaCluster#storage_account_key}.'''
        result = self._values.get("storage_account_key")
        assert result is not None, "Required property 'storage_account_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_container_id HdinsightKafkaCluster#storage_container_id}.'''
        result = self._values.get("storage_container_id")
        assert result is not None, "Required property 'storage_container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_resource_id HdinsightKafkaCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterStorageAccountGen2",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem_id": "filesystemId",
        "is_default": "isDefault",
        "managed_identity_resource_id": "managedIdentityResourceId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightKafkaClusterStorageAccountGen2:
    def __init__(
        self,
        *,
        filesystem_id: builtins.str,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        managed_identity_resource_id: builtins.str,
        storage_resource_id: builtins.str,
    ) -> None:
        '''
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#filesystem_id HdinsightKafkaCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#is_default HdinsightKafkaCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#managed_identity_resource_id HdinsightKafkaCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_resource_id HdinsightKafkaCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bc1faf6d03b751358719ebf600deb97a35fbba031710f4fb356868124cabc9)
            check_type(argname="argument filesystem_id", value=filesystem_id, expected_type=type_hints["filesystem_id"])
            check_type(argname="argument is_default", value=is_default, expected_type=type_hints["is_default"])
            check_type(argname="argument managed_identity_resource_id", value=managed_identity_resource_id, expected_type=type_hints["managed_identity_resource_id"])
            check_type(argname="argument storage_resource_id", value=storage_resource_id, expected_type=type_hints["storage_resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filesystem_id": filesystem_id,
            "is_default": is_default,
            "managed_identity_resource_id": managed_identity_resource_id,
            "storage_resource_id": storage_resource_id,
        }

    @builtins.property
    def filesystem_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#filesystem_id HdinsightKafkaCluster#filesystem_id}.'''
        result = self._values.get("filesystem_id")
        assert result is not None, "Required property 'filesystem_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#is_default HdinsightKafkaCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def managed_identity_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#managed_identity_resource_id HdinsightKafkaCluster#managed_identity_resource_id}.'''
        result = self._values.get("managed_identity_resource_id")
        assert result is not None, "Required property 'managed_identity_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#storage_resource_id HdinsightKafkaCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        assert result is not None, "Required property 'storage_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterStorageAccountGen2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterStorageAccountGen2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterStorageAccountGen2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431203b7bbb1e402d99ae1992a594ed8f35fd17522d935e892f6284aa17a1901)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="filesystemIdInput")
    def filesystem_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filesystemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isDefaultInput")
    def is_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceIdInput")
    def managed_identity_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedIdentityResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageResourceIdInput")
    def storage_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="filesystemId")
    def filesystem_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filesystemId"))

    @filesystem_id.setter
    def filesystem_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659f2161ef465fb77574a08d93fc1d2d730918898a16867b45011610e1cd662c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesystemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDefault"))

    @is_default.setter
    def is_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba60ecde06c13341c1129309152bd358fd8575224dabfad5778dfc00fb55a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceId")
    def managed_identity_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityResourceId"))

    @managed_identity_resource_id.setter
    def managed_identity_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653e0ba8f6a7a53d6da1268e2588c8abc146288a9185a8b0c129872d85271293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280ee767d8935f1f5e67c75e22a974416fe44287e783df39db9ad3877d8b0431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightKafkaClusterStorageAccountGen2]:
        return typing.cast(typing.Optional[HdinsightKafkaClusterStorageAccountGen2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightKafkaClusterStorageAccountGen2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66e119d5eb1c0cb4b17dbebf3517b08359cab44c4c26cdbc645a18f4cc223ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterStorageAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterStorageAccountList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381f7d11f67e51676eb062fded61b9afdee22f4c160e487fce0c7ff43a0b8080)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightKafkaClusterStorageAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1d3905e67ad53faab6b3f7aff535f8dd61a9a281ebf7b38017499b137b8a15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightKafkaClusterStorageAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c919da55573fdf359a774c555f2bb7b8aed762a60ce3680d8b7b0529dc24948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18d767d43e0aacef061b2d81c3f5b2395569967bdefae0d08c0fcdc6fde4804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5414fb3b377d8da971e232de1d4b351210a76874a1797773a7a8b9ac068c6a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterStorageAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterStorageAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterStorageAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2180ce90ef170ebf4bce599d9d0cf0f66d69f269081de8b75a47817588ecdb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightKafkaClusterStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterStorageAccountOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64edaa3e0537299c99b8828420d492f4733fe05bb0d01fceba2bac26839bd919)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStorageResourceId")
    def reset_storage_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageResourceId", []))

    @builtins.property
    @jsii.member(jsii_name="isDefaultInput")
    def is_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountKeyInput")
    def storage_account_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerIdInput")
    def storage_container_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageResourceIdInput")
    def storage_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDefault"))

    @is_default.setter
    def is_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e8b4e9672c92c242da36e52431f0d543b66c28f88c25fb40c5038d27f4553f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountKey")
    def storage_account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountKey"))

    @storage_account_key.setter
    def storage_account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606bdfe69bb67a70a955444defdbdbfe464afa63b2bbcea8689a9fb479eed839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerId")
    def storage_container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerId"))

    @storage_container_id.setter
    def storage_container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cebe9d1d71f382c743e40006a2f89ebbeb409c989680c86f8160dc729af664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e410b636006bd2974c485e5f4061ecb6eb11f4043e7cf2fe17d90a901a7c31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterStorageAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterStorageAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterStorageAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66eeb19975ae0ccb664d7444b91ccb22312106f02369d15e7d5202945325e3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class HdinsightKafkaClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#create HdinsightKafkaCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#delete HdinsightKafkaCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#read HdinsightKafkaCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#update HdinsightKafkaCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e288b0c53651e26dd7bca9735826536fb83b9fe174e22dd1e4bdfc1a7b077e)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#create HdinsightKafkaCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#delete HdinsightKafkaCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#read HdinsightKafkaCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_kafka_cluster#update HdinsightKafkaCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightKafkaClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightKafkaClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightKafkaCluster.HdinsightKafkaClusterTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6ed6e70355f2a5fe405ee66495b34cea105ae14caf857a6702f695c85c2a58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46131ae2dfa20600c088ee62aad26249f11b825ec3aa92ea08346b2246613321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cedd72f1dc728ba627a16ff63c7e9d1fc2b0f6715a9b265e7483271d9a29379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aecde954360576c59e7c6e4d4da9ed6213a048f8a2c4ed6a6f7c6e80425f429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bdbd676ce008d1195ab2d1fd8c5a64cc18615395f99c8fec40755141a74968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1db55b21e4f108e4857ade28407637ea35cffa8732fd24017eecfbc35e4b13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HdinsightKafkaCluster",
    "HdinsightKafkaClusterComponentVersion",
    "HdinsightKafkaClusterComponentVersionOutputReference",
    "HdinsightKafkaClusterComputeIsolation",
    "HdinsightKafkaClusterComputeIsolationOutputReference",
    "HdinsightKafkaClusterConfig",
    "HdinsightKafkaClusterDiskEncryption",
    "HdinsightKafkaClusterDiskEncryptionList",
    "HdinsightKafkaClusterDiskEncryptionOutputReference",
    "HdinsightKafkaClusterExtension",
    "HdinsightKafkaClusterExtensionOutputReference",
    "HdinsightKafkaClusterGateway",
    "HdinsightKafkaClusterGatewayOutputReference",
    "HdinsightKafkaClusterMetastores",
    "HdinsightKafkaClusterMetastoresAmbari",
    "HdinsightKafkaClusterMetastoresAmbariOutputReference",
    "HdinsightKafkaClusterMetastoresHive",
    "HdinsightKafkaClusterMetastoresHiveOutputReference",
    "HdinsightKafkaClusterMetastoresOozie",
    "HdinsightKafkaClusterMetastoresOozieOutputReference",
    "HdinsightKafkaClusterMetastoresOutputReference",
    "HdinsightKafkaClusterMonitor",
    "HdinsightKafkaClusterMonitorOutputReference",
    "HdinsightKafkaClusterNetwork",
    "HdinsightKafkaClusterNetworkOutputReference",
    "HdinsightKafkaClusterPrivateLinkConfiguration",
    "HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration",
    "HdinsightKafkaClusterPrivateLinkConfigurationIpConfigurationOutputReference",
    "HdinsightKafkaClusterPrivateLinkConfigurationOutputReference",
    "HdinsightKafkaClusterRestProxy",
    "HdinsightKafkaClusterRestProxyOutputReference",
    "HdinsightKafkaClusterRoles",
    "HdinsightKafkaClusterRolesHeadNode",
    "HdinsightKafkaClusterRolesHeadNodeOutputReference",
    "HdinsightKafkaClusterRolesHeadNodeScriptActions",
    "HdinsightKafkaClusterRolesHeadNodeScriptActionsList",
    "HdinsightKafkaClusterRolesHeadNodeScriptActionsOutputReference",
    "HdinsightKafkaClusterRolesKafkaManagementNode",
    "HdinsightKafkaClusterRolesKafkaManagementNodeOutputReference",
    "HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions",
    "HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsList",
    "HdinsightKafkaClusterRolesKafkaManagementNodeScriptActionsOutputReference",
    "HdinsightKafkaClusterRolesOutputReference",
    "HdinsightKafkaClusterRolesWorkerNode",
    "HdinsightKafkaClusterRolesWorkerNodeOutputReference",
    "HdinsightKafkaClusterRolesWorkerNodeScriptActions",
    "HdinsightKafkaClusterRolesWorkerNodeScriptActionsList",
    "HdinsightKafkaClusterRolesWorkerNodeScriptActionsOutputReference",
    "HdinsightKafkaClusterRolesZookeeperNode",
    "HdinsightKafkaClusterRolesZookeeperNodeOutputReference",
    "HdinsightKafkaClusterRolesZookeeperNodeScriptActions",
    "HdinsightKafkaClusterRolesZookeeperNodeScriptActionsList",
    "HdinsightKafkaClusterRolesZookeeperNodeScriptActionsOutputReference",
    "HdinsightKafkaClusterSecurityProfile",
    "HdinsightKafkaClusterSecurityProfileOutputReference",
    "HdinsightKafkaClusterStorageAccount",
    "HdinsightKafkaClusterStorageAccountGen2",
    "HdinsightKafkaClusterStorageAccountGen2OutputReference",
    "HdinsightKafkaClusterStorageAccountList",
    "HdinsightKafkaClusterStorageAccountOutputReference",
    "HdinsightKafkaClusterTimeouts",
    "HdinsightKafkaClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1dceb5eafc6afac764728d72b85a419aba510f31c3d20bedbbcd056fd803afc1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightKafkaClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightKafkaClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightKafkaClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightKafkaClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extension: typing.Optional[typing.Union[HdinsightKafkaClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightKafkaClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightKafkaClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightKafkaClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightKafkaClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    rest_proxy: typing.Optional[typing.Union[HdinsightKafkaClusterRestProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightKafkaClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightKafkaClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightKafkaClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc2e17bfc35db06db4eb5ec2334494480ccb54540419477d4fb4e295ae5f948(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50838bcf1fde785599873183b27b3f432aaf2690cdca6ec44805ca72827c3a26(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87eb90661b796d317a6f95ef7808ebc5cb2b2fe2f0cb4c6b48a0940846659cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450be19f17a827308824953af7a3afdc26560e8f78f4e5e4103a428dc36de991(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f222b1ad24efc804e2fe4fbd0d7f02c72f71c18bec81bbac52d56607cec24bca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbefcd59e95117a96cd6e648c539737949ed1aeeeb4a5cedfd5f2435a9ae90a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a28088e25680451bf1579ffd3e9ee4cebc09585d564a5d4e48948067608292b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725b7a97f09ebfca30b41f89db2325ddfccf7899a5f952a664a3a89787bf90f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b20d0c099aa29349aa0825bdef6b12a07d9b56d8cd4fa55568bb107c2234d37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a620cf4d435d1d306d1f4a0e7bcc0937e9170375091499189c25e9a4de8d8c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3963e98d9408cdf38d569c2d59456908c331fb6c190ee31f3d4fc60215397651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99255e20cbe66bdc78b650912059350746cc2b689f41a4818ca7a9dcaa1b8f3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432f6d8d871a46bc905e89b9f40eef17a5b519a0d1a685585e662d35de375303(
    *,
    kafka: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e64d3d6412bf630ba0b7f33c549b4b5860dff6640b04924cd40fca0d497f5dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1113548660d39d5dd8e100d75a256970d48f942b830f7e11ebb14ca1169351e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd35d5b1aadb509ae5994ea03d5439281299caf51a979af2caea788b2234537(
    value: typing.Optional[HdinsightKafkaClusterComponentVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f45694aa0c27f5c9e0022bc16ed373a0f8065b9c446122e2faf735f65ced215(
    *,
    compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_sku: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534675524c3dd9789f79d08981ea12040ed61c87c1551eda1c922d7b83c70476(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d411c9f3aed01ab04ee5a22f5931d5202b57a413f3ace74a9bf272e8e4d2857(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efe717f265c207f749f587170e873a10aef14f909192176f51471e1c5755ea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389353f0e8e7dc766ba3468fd66e66b5302647fe7104a7030d3428b2100a0882(
    value: typing.Optional[HdinsightKafkaClusterComputeIsolation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba34d8314e766ae96172d67c8afd70a3c83b4d85b0eb992e302cfc6ab50bb2a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightKafkaClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightKafkaClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightKafkaClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightKafkaClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extension: typing.Optional[typing.Union[HdinsightKafkaClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightKafkaClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightKafkaClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightKafkaClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightKafkaClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    rest_proxy: typing.Optional[typing.Union[HdinsightKafkaClusterRestProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightKafkaClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightKafkaClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightKafkaClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7484980f5667c25596b855a0ad7b263a4b92e6a0262605d6b18387ec50833e6d(
    *,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a379d3bb69774d71044579f4e625449b5e024a170a742185365c7c416e52311(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc00c90b0869a4670e1f309f9d3474b08cc82606a2ee938a06297689ad25baf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d562b3d7bcfc60cc8f36d40f47211a25d227550d87e0cdb6906c063565cb68ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f67a0dc094f47fa29c68f9c1fe49c61e20486b131f2daed8d373f250942dc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d7bb3d02a4c7eb182d25b69cf12653959d1bbe6e377fe01cd533df3da5d946(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a8da519e7d4297a0bc54ffd9ff7f6c013084aa09ae16798b5ee01e07f373f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterDiskEncryption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d374e29d760fa107af3cce787f96338bb7091a1c30668838f36331559f3f462e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cccd99f5ffc2015acfbf43a90ddad7489bb595903ea1ca06a8e346b364da6df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e3af73872044131bbde404e5c16dc8d0687a2f111e23e5610355bc81412d42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675eaacfcbbf280201dddd57cc46d504dfb6dfc8802be35cb068b47f67efc585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6bc055afdeaa6a64169004ec6a9afe87917ce740fd05d0f4a8c3b5a853bfb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2918d61e9b16f9bbde08b6f3e208beccda7869e81ba11b822ab5a21a46eaefcb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterDiskEncryption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccd4b39ef5be73173eccb805abefdd4b3da4e1ee0a3a77fe94e0f1e93f714c4(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c815c358f28ed6c61aeb76686b69d8bab6ef00373944b369b09586a0ab626edc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f4ba4a81484f579ac3e442f853531d1232ef92d82da51fee2e5c9455e57a2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2081cc8b09c666bb6298b348cb478d10a4d6691b248b31d34552f9c5f6a7041a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579a6196bb029a554baebc5438c23d723b4336520e75d814559b6a33cd3dff77(
    value: typing.Optional[HdinsightKafkaClusterExtension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861b002857caa548b12f22efd20f592eefbbf5439de17e6e07d68bef8e1e81ab(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85b73ba8432e9221078b8f85dc73665287d63951119143476aae5b049639b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87256c3277e9f84cb5d85f016908f6c7f6848dde4f3fc407396ec5c72c25c3e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9170927cc559bdf76cd8fadba30ddab0b5f2f31ba6ee3a6769084bb4b99ca21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fa58d462e9f9a1064834d8a156fca09b284784c20173a8156b7668bb03e921(
    value: typing.Optional[HdinsightKafkaClusterGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3714b7aaa672f6af1d80f295a87d7bbbf0022e5f5a4a4db1a93cb196f6a07d(
    *,
    ambari: typing.Optional[typing.Union[HdinsightKafkaClusterMetastoresAmbari, typing.Dict[builtins.str, typing.Any]]] = None,
    hive: typing.Optional[typing.Union[HdinsightKafkaClusterMetastoresHive, typing.Dict[builtins.str, typing.Any]]] = None,
    oozie: typing.Optional[typing.Union[HdinsightKafkaClusterMetastoresOozie, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61a8707f3634ab451e68ce4eb0e8e85321bc9eb7e901b0aaccb2611b4f3a6a3(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e6c866bd90d02ea041c1b9f90ea857addce7177671b17bd1e88da949edc170(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1296c1bbb12933b9f2f4332e9c1fd05a05a9fc76aca9a60eed759a30d6676fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3e9fcd33d193a9529080e2e4246c2bc47c8485ff3a63c156c2de8f58609c29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc7ad00950836fa53bcd4e4d6dcda72b71c7d282f76d36eeaf05ac94da0fc10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9200b9b840faae37e18879991aa6e20d226ea37d1b709a6a5740971d7c66082d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3ab4dd9c630b532218916f0f63790912e4a306cdba551c73d56c6f3db1d51c(
    value: typing.Optional[HdinsightKafkaClusterMetastoresAmbari],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42837f8a4648b141fdffb9f511a84473deb5fb9447d371a1d9b809ae2e42a92e(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4d67c72e771de505275d0c91a1942c01d1599b93d201e70bfe235eae42f885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b872feae300b5e6f4bdd0c5753f0a017a9e7725ae4724b08fd523805d1b565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f38743d77a43153464e2782f4fe5ef0b307bf37d02ddd6689ff69b499597a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4e35cbbba50f753df1733d5551d6deb3e9cdc5f607995cac57a46fbafaa662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22268b165e7a61b25c64fecef2e9df3ef92b3ac6835b3d4b56da631c96da9b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40b8738e50c0ab9fd60e8ccae692f83369edd8fb15c496439adaf16d0c4f142(
    value: typing.Optional[HdinsightKafkaClusterMetastoresHive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fd082f932622173bb3796357174abef36336f2324db309425b27fc30f0ff58(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e4240709b88afb185d1a1ccbeff8400c1b3528eff4e11cc89332798370ebce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468a9cf70b7cb6b8e92f845e71796bf4c53789fdfe32a84f6a1e290d6eeaa54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7bc25ae3de5510d4004bd578d6922c8e2bac1a12d7ee043c51cf84cde51943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1c1d5c059c96ea768355234962c74cdf3a67c55004f30f88d66d650014a13f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5fd2b3a2bd34e90114987c3bfa15f648564d64ea6092cd0070b7050be0312e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b14f22d9b80353a579f7719708dc86da74abdc2648db96bb7f75281011ccbc(
    value: typing.Optional[HdinsightKafkaClusterMetastoresOozie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba45535eb3ddb4732d93a09d424ddb5d044f0884bd7559b451985cd2523fe48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073a85beac394476322b084c41171f4b92c88135b20fb8e066c274b3d2a6c706(
    value: typing.Optional[HdinsightKafkaClusterMetastores],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a22d522b0a82617083e5011378615ef7ae4b7c224993b3ca1b5c45d9452244e(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7d4fdff73d5ff606b5ca6ea40bd3d5273afd9e6bdeb69e5fc122839985cf13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18f64c5b9ab93034ce29940ff49f92940dae5be5a986b04b4ba1a8678e9cbf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e62af195ab8a8ec143ad792943ba73f11426512b754a8f8c6bf55fef0b78be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67e1d6202cba3f4df037a640c354eba459225110f7f64a7e5aafee83d757e17(
    value: typing.Optional[HdinsightKafkaClusterMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4131c116c4c546c2d5f672c844b6079cda13d5e12ab8f961a779a885e55cc3f8(
    *,
    connection_direction: typing.Optional[builtins.str] = None,
    private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ec3a827a37c399626aa2b07141a2b8e8425f96a88f8c02344681106f9cd094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1321c33eeaad4cc6cafa686afca619a7f83b51ef7c0599b19d234a17a719b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c4224497308e4df831ceac573dc71b5d900bb8d88adb60da4584030bbcb031(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976301df75ecd9338408584b5eacc0a8f023291039c4b0250b174b9408ca976b(
    value: typing.Optional[HdinsightKafkaClusterNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ea5868bb7f0d7910244d3f9ac66eb752e57dc1136c7fcddca7d7b24a622970(
    *,
    group_id: builtins.str,
    ip_configuration: typing.Union[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b898724f473cb07f9caca46b0b0b9c05a419d5c49f34c5c06e30bb8abdfa2c9(
    *,
    name: builtins.str,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    private_ip_allocation_method: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b933fe43c034148b35a4026ac83ea9c85305e6214b03ce41db319f041c71224e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a425f38371ae52fb8c841bf5255f4769dc8148a5b2cff322e4558cfb3f82aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7422dd0dd6ea1535e054d19485bb093bdac50cb418973a4fd341f3169632381f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2a261e6a44c14f4d4365c58a45e3d551b0ea061b8d324b9e75964a97832bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cbbe84c208b08d2d30d594057099a3353e328ee44459fafc40645f94676e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b08434b7af747dc83ca24fb4c8d12a39f228b03ea1203799efdca49c76ef8b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62c501e4f536316f9d90cb130601dcceb1dd88d493cb33225604a439df73f87(
    value: typing.Optional[HdinsightKafkaClusterPrivateLinkConfigurationIpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b823bbbbcebada0c5d190f0a5d6922d7ba104b23232fec513e51147707f7b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e794ed306e6f92c88dec124940b87a663d700704cc44747d97748c920396d40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8082fcf8cb96dd57fba1a005dc400fd1c3bb13b9cf21831481e8f16e276f8ee1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cf7377aa52bde3c4f41d17985d902dd881fc3325138ef76e1b0812a9c0cfd4(
    value: typing.Optional[HdinsightKafkaClusterPrivateLinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cab362482b4825d975e99c181fdfb0ce5e30c11c232f2d5d8d905d19948c45(
    *,
    security_group_id: builtins.str,
    security_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e41e02c53c9fa744cd563b97d9e2acdab3a959e16e29d4638052e821f78cb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc6d907231c27b32aea10dbab13b78dfd798fd26519c3ddd1edd3d69296e2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c1c6ac78ebabc1e9c9434c28fe065b8ee73823396c2e09eda0265ce93cdc18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf02267b5757185286e0ddfd0b89fa1ec271f50b3343c7f91368c31fde0fac6(
    value: typing.Optional[HdinsightKafkaClusterRestProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d6f348f26be35d76737112d1a7abbb9f337de1afbe01dd7ba12abd0cd5732a(
    *,
    head_node: typing.Union[HdinsightKafkaClusterRolesHeadNode, typing.Dict[builtins.str, typing.Any]],
    worker_node: typing.Union[HdinsightKafkaClusterRolesWorkerNode, typing.Dict[builtins.str, typing.Any]],
    zookeeper_node: typing.Union[HdinsightKafkaClusterRolesZookeeperNode, typing.Dict[builtins.str, typing.Any]],
    kafka_management_node: typing.Optional[typing.Union[HdinsightKafkaClusterRolesKafkaManagementNode, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ec644fc2ea13378ebfbc5322ec4f06167b11a8b3c28462185040a7b0e28ff9(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f04d149b884285865e5321372da1438428d05689d626ba115f8f55964cc2665(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f348422add18a4a92a8128fc0617410159e5f92e24c5fe581fd2b1e540f1d5a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98290c5848417dea2b0810d23b1db501751960a5d89f0e6cc1d2150aec5d395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b785f3752ed166b275d9d0574c59a4a9f50c645a518515df7a56a16935822b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5232f1aa80b8a3872054777828d52243f322492c9f5c569f12579a956d654fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79dbfa4da50fbb14b0d6543853dc5e35253d54e14bb92710a2c8d287899703ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7630d8b0cd8fb657e3c6b2aa40b92856399c94dbe27afd41fce6d6f089b08cf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20d91453e96725d30b4347337333e7ce02e100188c6eca8bef8a93b407618a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde1bb347602956c020787783b685b1146b7d42b22839cd9379b3b1b81ea6bc1(
    value: typing.Optional[HdinsightKafkaClusterRolesHeadNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19f1bd02bb258d268c020fc4f98c2fa67aa4212c1820580e56f0bcd9f2c180e(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fc24cf30c57a7163370146dd9a8f567953f1a4a802368385b6b9a0c754453d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843621273886e918c853b41569e5b74c7e0978e095f27f5b24fe13f4433926b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88ed4635d7f3f5d8721e84f69a376dd146d73f0500410f913be8fe3e7d94337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af23b634229d2058ae5cf3a2ad7b829b0ba81a4498e7daae89fc758e43dfed7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f53c74f908eb463f5b1b602be2bec1ab54f2fb6a7f1f76413ba73dcd09f78e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc4fe54b18df25afc64457ab7ca6d64d80aa9e31474ae7714716cf98d9b13f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesHeadNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0623f316504a3ea15ab19c73bf18f7bdc944e1e9391d2f28bf264b3f238725b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ace0d85167d8da2a9adfa52cbc631adbfd3410628cdccce6cf6284eaf3da0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c209b08cfdfa5296135aacd5eb60b4b03e79213e4d3b3e3d5ac241363cf72d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc867a110fc7db9b178075f6920f21c00207125cec731765b6cb04a4adc73f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a691438cca4311411686f5c441a4182324a2bf453c9ede1d12b11a90861b01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesHeadNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6a39da11579e30ddf4d394d3aa9c3003ec87002dc09ff6b405eec276162f39(
    *,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8359b976cf0b2269e06ed6ce4bdb301b6386ad2adf33c6888c941efcb4a489(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbf4ce063f738d4a459d352f56c68aa553a6761ceaa38855dcce31dd6959740(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb5fdaa7c71e7612831bf5b6dba248859bd6523e41837db6c379fd22aea9fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8b22139d547e738f03581b99ee087ec28b1783b0d375429bf7b81f1a591241(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e70a864ea378ce137e36ad16698c0fb03171e33b598bf00356fbbb6160118b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2668ee62b72e57902b00675e2ab25e952fee3189c117969028806456cdc89fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a2420c3daca57c8783cd8d73ed49ceb8dd1c93af9f9708e31b67b99ed28b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f80902fad2dc9e4d1dd828d1b8616e1cade30d1dbbaf1c457d781b68005cf0(
    value: typing.Optional[HdinsightKafkaClusterRolesKafkaManagementNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba68dde5c5ea1d569880a706a5cf43bdf06ea8c1d235f338eb8132012208fc21(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec382746fb9afd67ecbe7c30280232d36faf8d79c9d791f61c84f30ea642fa26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8753663368cee90f631a7b02c8625bf09e09951bece7dcedf554413722863bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32c92d33a9022ffd5f78490a057b02d03451eddbfa16eb8314fe259d7e31625(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb80dfc3b57cd7acec861323d8e1309793d78f593047e34c952f17118a8e634(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493738671ce775c42c972d5de204a5899325391f08978a01b13ad3edaeb69779(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acfc65526d888925ae648e2bfea7ec8197e5fb0dffbead3813522cfa3b180ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878625d1d4a56bb65cbc4b382105d486e6f868a7279ace47041adf26d79e8049(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e203fe8372d6406e586ca9565b7521c2d8d49554e03ce6f6d5eec7570131c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1054d038e647669263f4d6c731a8c3063ba30750baea0545c0f9ccf9c29ae3de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca3388521b033e9e45faea5914a1342ec782b284e473447f004e2a5eaff9b53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3782012019d14866e78875b4063c99ed26d895b30c587484d5844cfaf9a049(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesKafkaManagementNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce288a5c990a83cf1bcccd03a6ceb01e01b8ecad4f9ade723408db8205d885f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d4cbf39b7b410d0e34fb0c5d832473279bf5d44e261c2087305de7a00bc6a2(
    value: typing.Optional[HdinsightKafkaClusterRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6b0f757c9a6fc48d040bc32ab9bdda3bc32e34c2d4493534853de1412d3e76(
    *,
    number_of_disks_per_node: jsii.Number,
    target_instance_count: jsii.Number,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a78e58531d5c63a80493a6e4049c569dd0f4e74ae131c3db4f60437354b21c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f3e3c1ba02dace3bfbf71413667fee072c64e0b0c36ed5286b84d3265bf857(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4726c55d2b6d296be463996d265cb4dab0916b7b12b84deb61c6f83d0e35ced(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dac03eca80112ab79ee7b1e477138af41b4589192cb4c2c68e712770b6c7f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d63005984577a403c96e0b2700905871d179b94b852fa8c0af615cf63a640ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcb63c5208f889a12b86d91283b7faeed47ad766bae3c4d781add00ad095f2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68096796ba4b45fc055609ebcfece4692ccd60d699ad8453ade7bb562e842ae2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f19b34032754d4af596383ebcd6c4218296c2ddee9a2231badb08ec147007a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db4a009ad05dee02ed6b00e85ef48456939d7e2a82ee3bb1d68bcfc3b9f8023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3288f7ee2c1be4b59927ba402cc8c3e79cf0d7e46960c76a8face83f0401a10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97946d6b69e8adf6e01e9fcd1c101265cc96971fa3ffe78de963d7623b589994(
    value: typing.Optional[HdinsightKafkaClusterRolesWorkerNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c720676d183f0fb0550ab96974f04a0fe1cc092363bc3c9c4b2fdb55eded898d(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b845f7225d0d2f98da97ec994de69fa9035a55fa85d1d2e93c9b6104e52f96e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edd1bfe07474567e61b8be0e0227e849c3d488052110da887375b9144bb6666(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809fbc96682e11c15a96276757bdc3303ac72485b99d0b58ae90805f72b80923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64a823d9eaa9ef7de4732adb66b05acef63980eba4e0197d08caab26861d29f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311b69ded078fd7962a8a648f3f1faeb1d25b0a5f9f67e29893dd26ad774329b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b423115a22c99a4a13fef74a9cb6b885eb4c17b9c7e504481a745aedea6430(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesWorkerNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2d73fae72f64a8e201b86f320421bd088d846377f6869e8f09a3ddc631738d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b698c713df97b45955b2f932dad933084324eba7f67e0ecc962bc1bfa75a294(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef0917a4357afbc8fde77db81ebae35392491a84ba0685b8d3349f4f5b7bbd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7303c1c392d9aeadd4048347d4de23b29be903e3195d79f8b9f35275c313378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353ec9ca73de3cc9ad1097aab068b04632a7c59bb2a56b848e508b4fddc87b6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesWorkerNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb51fd30bae887dff4c96b924201c914007ce6e39f5dc57ef3b7112b7bc8c073(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b95878d18d4d2d189995af1ab96101ed8dd419dcf405d397bb6c273d525682(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1bc5051d257431d23e7de1071592b14bad3dbf98a5c2641f35a8f6ee18a572(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightKafkaClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7522914ec53b8e6562260b50c0e5d7d8455ad29e4d505f1dab72dd1cb4ff8ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e441d3f1f2940b8c1eddb13facc179635e97013d154fcab0fbd16482fd7a63(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b9eea956ddb033bdeca99341b5fe8592c62497d4599ef05686545d644df1d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7f1220e063778a4b1dc59f2ee2fcb8f0c7444836fecb62faac4d6ea4653cae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e72a0cbc267da4b122555f590fcd93261af2f7c12e53ca03ee51e1b318a0373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579e97b67f60b18bd3f2743b942072ec76babdd35f6103d4bd5c0f90835fab1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7987d6ab34aac6a928ce55d7358a6a11625a2d648a1a16442311665dca2a9d82(
    value: typing.Optional[HdinsightKafkaClusterRolesZookeeperNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8a9af643b0be3ac1b7a5b7fd1a58b7a5f6875e015a710d69fd55d29936ac6f(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c406548c2fc8b4a0bbf2a9dd1faf0ecf915335251f966982c0040293bc6447(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8b7528cf1122cac4355cb348e3840b849da18a32d2c0ea297a17dcea52c9b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bbde734a45a8f0174f3c446ee09c264cb7cf5b8430853d555ebe1a1f4bfbea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c383693ddb9db63f0673f7012d00491a88880453c72d53d813e12a7de1a160(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f1a8fbcb877c5b45bbb680cab35689468aefe2f6f68237e33b577e436b3a11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5db31a36f76a8e42e223c5ac2d2c3766fa68ccb1b82b161cd71b029252a6161(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterRolesZookeeperNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b151a0749cf025b5de5497e7d247d89bbed32a7a3e8fd3e3c574bba35c294e7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dda7425d3d5b636f9d654144b5b0c0855ce719341eb474ddb642fdbb74e967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cdbf413759549613caa644e2a0473a7f2c44663e0d54c58fd31aaedb988839(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71deb0878620b901b8fc9c208cc67df71a1aa8173812169a4ecbf780a0b0d53c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d0b9653b94a88ef67b025ac8514c4e981ee999e44b0f71177b853956cef4c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterRolesZookeeperNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f534577332faccd3f0df5b45279f5a3473e641e9b09409a3dcb4a93e1e171ed6(
    *,
    aadds_resource_id: builtins.str,
    domain_name: builtins.str,
    domain_username: builtins.str,
    domain_user_password: builtins.str,
    ldaps_urls: typing.Sequence[builtins.str],
    msi_resource_id: builtins.str,
    cluster_users_group_dns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216f28baf593affcc1a35d9de2e1019b5a93cd2bd085e375a6650bd43512fd22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f9cd8b9c6b4683a3963a1dbc05fc600c62e0a2a48c1303e65b809f79418d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db8c22fc0079009066c697032ca411cc60bae5cc4d4a430c1040a7e3ba32806(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02200eba68eef973038aadbd4a9ccea7a891cfa9c4cd68501908df43162da767(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ee2240e77c5791aad3eefc7eb79793199514c2ad3e61a4ea526f1ad713b289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e40e9b4dd13169d8944efdd0bb9a485ad2607db58c460f5f0b1320bbd60c63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0441e2551547109d05060cc4dbe961345566d23ff2a8466c2942ab15892370b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830d41e4c81ca36a64de71ee96a553d0b34c044285c29509f10796143e50ae6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2892aa79d35702361f6d300adcf6a835f10189533c539f4734710a1e5c6f45a(
    value: typing.Optional[HdinsightKafkaClusterSecurityProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a61eea5c11a54c48ed9becfaa28c5cc2bae2bf464833e7bd7202c74dde52f4(
    *,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_account_key: builtins.str,
    storage_container_id: builtins.str,
    storage_resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bc1faf6d03b751358719ebf600deb97a35fbba031710f4fb356868124cabc9(
    *,
    filesystem_id: builtins.str,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    managed_identity_resource_id: builtins.str,
    storage_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431203b7bbb1e402d99ae1992a594ed8f35fd17522d935e892f6284aa17a1901(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659f2161ef465fb77574a08d93fc1d2d730918898a16867b45011610e1cd662c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba60ecde06c13341c1129309152bd358fd8575224dabfad5778dfc00fb55a2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653e0ba8f6a7a53d6da1268e2588c8abc146288a9185a8b0c129872d85271293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280ee767d8935f1f5e67c75e22a974416fe44287e783df39db9ad3877d8b0431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66e119d5eb1c0cb4b17dbebf3517b08359cab44c4c26cdbc645a18f4cc223ae(
    value: typing.Optional[HdinsightKafkaClusterStorageAccountGen2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381f7d11f67e51676eb062fded61b9afdee22f4c160e487fce0c7ff43a0b8080(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1d3905e67ad53faab6b3f7aff535f8dd61a9a281ebf7b38017499b137b8a15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c919da55573fdf359a774c555f2bb7b8aed762a60ce3680d8b7b0529dc24948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18d767d43e0aacef061b2d81c3f5b2395569967bdefae0d08c0fcdc6fde4804(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5414fb3b377d8da971e232de1d4b351210a76874a1797773a7a8b9ac068c6a06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2180ce90ef170ebf4bce599d9d0cf0f66d69f269081de8b75a47817588ecdb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightKafkaClusterStorageAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64edaa3e0537299c99b8828420d492f4733fe05bb0d01fceba2bac26839bd919(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e8b4e9672c92c242da36e52431f0d543b66c28f88c25fb40c5038d27f4553f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606bdfe69bb67a70a955444defdbdbfe464afa63b2bbcea8689a9fb479eed839(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cebe9d1d71f382c743e40006a2f89ebbeb409c989680c86f8160dc729af664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e410b636006bd2974c485e5f4061ecb6eb11f4043e7cf2fe17d90a901a7c31b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66eeb19975ae0ccb664d7444b91ccb22312106f02369d15e7d5202945325e3ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterStorageAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e288b0c53651e26dd7bca9735826536fb83b9fe174e22dd1e4bdfc1a7b077e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6ed6e70355f2a5fe405ee66495b34cea105ae14caf857a6702f695c85c2a58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46131ae2dfa20600c088ee62aad26249f11b825ec3aa92ea08346b2246613321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cedd72f1dc728ba627a16ff63c7e9d1fc2b0f6715a9b265e7483271d9a29379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aecde954360576c59e7c6e4d4da9ed6213a048f8a2c4ed6a6f7c6e80425f429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bdbd676ce008d1195ab2d1fd8c5a64cc18615395f99c8fec40755141a74968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1db55b21e4f108e4857ade28407637ea35cffa8732fd24017eecfbc35e4b13a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightKafkaClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
