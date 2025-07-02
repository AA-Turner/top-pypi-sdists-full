r'''
# `azurerm_hdinsight_spark_cluster`

Refer to the Terraform Registry for docs: [`azurerm_hdinsight_spark_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster).
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


class HdinsightSparkCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster azurerm_hdinsight_spark_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_version: builtins.str,
        component_version: typing.Union["HdinsightSparkClusterComponentVersion", typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightSparkClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightSparkClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union["HdinsightSparkClusterComputeIsolation", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extension: typing.Optional[typing.Union["HdinsightSparkClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightSparkClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightSparkClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightSparkClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightSparkClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightSparkClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightSparkClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightSparkClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster azurerm_hdinsight_spark_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#cluster_version HdinsightSparkCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#component_version HdinsightSparkCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#gateway HdinsightSparkCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#location HdinsightSparkCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#resource_group_name HdinsightSparkCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#roles HdinsightSparkCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tier HdinsightSparkCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#compute_isolation HdinsightSparkCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#disk_encryption HdinsightSparkCluster#disk_encryption}
        :param encryption_in_transit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_in_transit_enabled HdinsightSparkCluster#encryption_in_transit_enabled}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#extension HdinsightSparkCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#id HdinsightSparkCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#metastores HdinsightSparkCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#monitor HdinsightSparkCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#network HdinsightSparkCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_link_configuration HdinsightSparkCluster#private_link_configuration}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#security_profile HdinsightSparkCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account HdinsightSparkCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account_gen2 HdinsightSparkCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tags HdinsightSparkCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#timeouts HdinsightSparkCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tls_min_version HdinsightSparkCluster#tls_min_version}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#zones HdinsightSparkCluster#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995f259ea200d232f4557f6b215ac3c5f25da7074bcaa56fd899fc533117efb8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HdinsightSparkClusterConfig(
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
            security_profile=security_profile,
            storage_account=storage_account,
            storage_account_gen2=storage_account_gen2,
            tags=tags,
            timeouts=timeouts,
            tls_min_version=tls_min_version,
            zones=zones,
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
        '''Generates CDKTF code for importing a HdinsightSparkCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HdinsightSparkCluster to import.
        :param import_from_id: The id of the existing HdinsightSparkCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HdinsightSparkCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dc1cd572fbc00654bfa101e34aa9ada88f023b63367a0b2fa0fb1dedaa7790)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComponentVersion")
    def put_component_version(self, *, spark: builtins.str) -> None:
        '''
        :param spark: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#spark HdinsightSparkCluster#spark}.
        '''
        value = HdinsightSparkClusterComponentVersion(spark=spark)

        return typing.cast(None, jsii.invoke(self, "putComponentVersion", [value]))

    @jsii.member(jsii_name="putComputeIsolation")
    def put_compute_isolation(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#compute_isolation_enabled HdinsightSparkCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#host_sku HdinsightSparkCluster#host_sku}.
        '''
        value = HdinsightSparkClusterComputeIsolation(
            compute_isolation_enabled=compute_isolation_enabled, host_sku=host_sku
        )

        return typing.cast(None, jsii.invoke(self, "putComputeIsolation", [value]))

    @jsii.member(jsii_name="putDiskEncryption")
    def put_disk_encryption(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7daab7a626f420715c5ddbfbfb0eb26cca91e1b028b8b0fc22880202daf09b79)
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
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#log_analytics_workspace_id HdinsightSparkCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary_key HdinsightSparkCluster#primary_key}.
        '''
        value = HdinsightSparkClusterExtension(
            log_analytics_workspace_id=log_analytics_workspace_id,
            primary_key=primary_key,
        )

        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putGateway")
    def put_gateway(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        value = HdinsightSparkClusterGateway(password=password, username=username)

        return typing.cast(None, jsii.invoke(self, "putGateway", [value]))

    @jsii.member(jsii_name="putMetastores")
    def put_metastores(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightSparkClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightSparkClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightSparkClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ambari HdinsightSparkCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#hive HdinsightSparkCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#oozie HdinsightSparkCluster#oozie}
        '''
        value = HdinsightSparkClusterMetastores(ambari=ambari, hive=hive, oozie=oozie)

        return typing.cast(None, jsii.invoke(self, "putMetastores", [value]))

    @jsii.member(jsii_name="putMonitor")
    def put_monitor(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#log_analytics_workspace_id HdinsightSparkCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary_key HdinsightSparkCluster#primary_key}.
        '''
        value = HdinsightSparkClusterMonitor(
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
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#connection_direction HdinsightSparkCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_link_enabled HdinsightSparkCluster#private_link_enabled}.
        '''
        value = HdinsightSparkClusterNetwork(
            connection_direction=connection_direction,
            private_link_enabled=private_link_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putPrivateLinkConfiguration")
    def put_private_link_configuration(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#group_id HdinsightSparkCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ip_configuration HdinsightSparkCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        '''
        value = HdinsightSparkClusterPrivateLinkConfiguration(
            group_id=group_id, ip_configuration=ip_configuration, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateLinkConfiguration", [value]))

    @jsii.member(jsii_name="putRoles")
    def put_roles(
        self,
        *,
        head_node: typing.Union["HdinsightSparkClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightSparkClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightSparkClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#head_node HdinsightSparkCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#worker_node HdinsightSparkCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#zookeeper_node HdinsightSparkCluster#zookeeper_node}
        '''
        value = HdinsightSparkClusterRoles(
            head_node=head_node, worker_node=worker_node, zookeeper_node=zookeeper_node
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
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#aadds_resource_id HdinsightSparkCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_name HdinsightSparkCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_username HdinsightSparkCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_user_password HdinsightSparkCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ldaps_urls HdinsightSparkCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#msi_resource_id HdinsightSparkCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#cluster_users_group_dns HdinsightSparkCluster#cluster_users_group_dns}.
        '''
        value = HdinsightSparkClusterSecurityProfile(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5e700cc53a6954fa449350626d33a5fe10b7059f818d3713646ee76c9d62e5)
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
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#filesystem_id HdinsightSparkCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#is_default HdinsightSparkCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#managed_identity_resource_id HdinsightSparkCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_resource_id HdinsightSparkCluster#storage_resource_id}.
        '''
        value = HdinsightSparkClusterStorageAccountGen2(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#create HdinsightSparkCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#delete HdinsightSparkCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#read HdinsightSparkCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#update HdinsightSparkCluster#update}.
        '''
        value = HdinsightSparkClusterTimeouts(
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

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

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
    ) -> "HdinsightSparkClusterComponentVersionOutputReference":
        return typing.cast("HdinsightSparkClusterComponentVersionOutputReference", jsii.get(self, "componentVersion"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolation")
    def compute_isolation(
        self,
    ) -> "HdinsightSparkClusterComputeIsolationOutputReference":
        return typing.cast("HdinsightSparkClusterComputeIsolationOutputReference", jsii.get(self, "computeIsolation"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> "HdinsightSparkClusterDiskEncryptionList":
        return typing.cast("HdinsightSparkClusterDiskEncryptionList", jsii.get(self, "diskEncryption"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> "HdinsightSparkClusterExtensionOutputReference":
        return typing.cast("HdinsightSparkClusterExtensionOutputReference", jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> "HdinsightSparkClusterGatewayOutputReference":
        return typing.cast("HdinsightSparkClusterGatewayOutputReference", jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="httpsEndpoint")
    def https_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="metastores")
    def metastores(self) -> "HdinsightSparkClusterMetastoresOutputReference":
        return typing.cast("HdinsightSparkClusterMetastoresOutputReference", jsii.get(self, "metastores"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> "HdinsightSparkClusterMonitorOutputReference":
        return typing.cast("HdinsightSparkClusterMonitorOutputReference", jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "HdinsightSparkClusterNetworkOutputReference":
        return typing.cast("HdinsightSparkClusterNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> "HdinsightSparkClusterPrivateLinkConfigurationOutputReference":
        return typing.cast("HdinsightSparkClusterPrivateLinkConfigurationOutputReference", jsii.get(self, "privateLinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> "HdinsightSparkClusterRolesOutputReference":
        return typing.cast("HdinsightSparkClusterRolesOutputReference", jsii.get(self, "roles"))

    @builtins.property
    @jsii.member(jsii_name="securityProfile")
    def security_profile(self) -> "HdinsightSparkClusterSecurityProfileOutputReference":
        return typing.cast("HdinsightSparkClusterSecurityProfileOutputReference", jsii.get(self, "securityProfile"))

    @builtins.property
    @jsii.member(jsii_name="sshEndpoint")
    def ssh_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "HdinsightSparkClusterStorageAccountList":
        return typing.cast("HdinsightSparkClusterStorageAccountList", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2")
    def storage_account_gen2(
        self,
    ) -> "HdinsightSparkClusterStorageAccountGen2OutputReference":
        return typing.cast("HdinsightSparkClusterStorageAccountGen2OutputReference", jsii.get(self, "storageAccountGen2"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HdinsightSparkClusterTimeoutsOutputReference":
        return typing.cast("HdinsightSparkClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="componentVersionInput")
    def component_version_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterComponentVersion"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterComponentVersion"], jsii.get(self, "componentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationInput")
    def compute_isolation_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterComputeIsolation"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterComputeIsolation"], jsii.get(self, "computeIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterDiskEncryption"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterDiskEncryption"]]], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInTransitEnabledInput")
    def encryption_in_transit_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionInTransitEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(self) -> typing.Optional["HdinsightSparkClusterExtension"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterExtension"], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional["HdinsightSparkClusterGateway"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterGateway"], jsii.get(self, "gatewayInput"))

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
    def metastores_input(self) -> typing.Optional["HdinsightSparkClusterMetastores"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterMetastores"], jsii.get(self, "metastoresInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional["HdinsightSparkClusterMonitor"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterMonitor"], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["HdinsightSparkClusterNetwork"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationInput")
    def private_link_configuration_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterPrivateLinkConfiguration"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterPrivateLinkConfiguration"], jsii.get(self, "privateLinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional["HdinsightSparkClusterRoles"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterRoles"], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileInput")
    def security_profile_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterSecurityProfile"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterSecurityProfile"], jsii.get(self, "securityProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2Input")
    def storage_account_gen2_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterStorageAccountGen2"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterStorageAccountGen2"], jsii.get(self, "storageAccountGen2Input"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterStorageAccount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterStorageAccount"]]], jsii.get(self, "storageAccountInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightSparkClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightSparkClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersionInput")
    def tls_min_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsMinVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersion"))

    @cluster_version.setter
    def cluster_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52d8f99cda72c5fcda1d1dc84513cd5a13ded9feacf25285667465f8dd70e63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43a86dd6558478dc631f32f466009a4bacd5a027d5b7642424859d68dcc6575c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionInTransitEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8851155b0d56ab5b6271e05403693f0c2baae9995b038a212f4b9b8261c6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5baea4619994aac2227fd5b4511ea9e10e0dacd80b49e1c2579af0e0b55d49c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7148630001d2cf5f29c28402752d56e3f74671d35c058553a85dd006e7e6ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf270dabd5e16601892a5406b96329c0f4a0997e7aa09ce8be64136df179c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff68a5dfe2fe24dbdc2e31f4e594e635daf74539fa07103477f39fc9db9c8b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b0d251a964145789dc66fca9148d4301e0e589294b4299f6eb04421952ee31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersion")
    def tls_min_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsMinVersion"))

    @tls_min_version.setter
    def tls_min_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e244e0ad88630c1ec59dcd59508c65f889619458aa2c9cf98e66dd3b7dc82061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsMinVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f279692b4a939566598af8006ff5b85331c5add41b7dd3b97e73817c1b9fa83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterComponentVersion",
    jsii_struct_bases=[],
    name_mapping={"spark": "spark"},
)
class HdinsightSparkClusterComponentVersion:
    def __init__(self, *, spark: builtins.str) -> None:
        '''
        :param spark: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#spark HdinsightSparkCluster#spark}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32190a4889d359476e3d71c992d7e4e7b993da9fc4b027d5283fb5c05fa8066a)
            check_type(argname="argument spark", value=spark, expected_type=type_hints["spark"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "spark": spark,
        }

    @builtins.property
    def spark(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#spark HdinsightSparkCluster#spark}.'''
        result = self._values.get("spark")
        assert result is not None, "Required property 'spark' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterComponentVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterComponentVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterComponentVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43c63b91eafab8b925c6a8beb165b930ba8b79ca33f3e8ff7e125eebeaeeafb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sparkInput")
    def spark_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkInput"))

    @builtins.property
    @jsii.member(jsii_name="spark")
    def spark(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spark"))

    @spark.setter
    def spark(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2064cda0aae78d0286b932f5e71d83e4bb4a0edb04cb4a4deef5f6f8156ba344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spark", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterComponentVersion]:
        return typing.cast(typing.Optional[HdinsightSparkClusterComponentVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterComponentVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613d4435cf76a538d74e34b3d1614253e41f759d89eb76a8a5ba3be782f611c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterComputeIsolation",
    jsii_struct_bases=[],
    name_mapping={
        "compute_isolation_enabled": "computeIsolationEnabled",
        "host_sku": "hostSku",
    },
)
class HdinsightSparkClusterComputeIsolation:
    def __init__(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#compute_isolation_enabled HdinsightSparkCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#host_sku HdinsightSparkCluster#host_sku}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9668665878413f05693d55c6b64808797404f014c12f09dff89623522943e6cb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#compute_isolation_enabled HdinsightSparkCluster#compute_isolation_enabled}.'''
        result = self._values.get("compute_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#host_sku HdinsightSparkCluster#host_sku}.'''
        result = self._values.get("host_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterComputeIsolation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterComputeIsolationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterComputeIsolationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f8003315c053b165712af807aa0716aa14d2c71cf33643858f5c40c79d0bc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8342590ffaf3f5af00fbec7a1731e442c019c809b024f10565fb567a5142149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostSku")
    def host_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostSku"))

    @host_sku.setter
    def host_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034e7b2a5cd815f801a12c480a8830e5f344f245d4dfa6b32e94a7274aac3715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterComputeIsolation]:
        return typing.cast(typing.Optional[HdinsightSparkClusterComputeIsolation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterComputeIsolation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63150a1d26d3f6d98830af18e0f5f521b06df89e4d5a91088b327299b1085461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterConfig",
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
        "security_profile": "securityProfile",
        "storage_account": "storageAccount",
        "storage_account_gen2": "storageAccountGen2",
        "tags": "tags",
        "timeouts": "timeouts",
        "tls_min_version": "tlsMinVersion",
        "zones": "zones",
    },
)
class HdinsightSparkClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        component_version: typing.Union[HdinsightSparkClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightSparkClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightSparkClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union[HdinsightSparkClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extension: typing.Optional[typing.Union["HdinsightSparkClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightSparkClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightSparkClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightSparkClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightSparkClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightSparkClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightSparkClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightSparkClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#cluster_version HdinsightSparkCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#component_version HdinsightSparkCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#gateway HdinsightSparkCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#location HdinsightSparkCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#resource_group_name HdinsightSparkCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#roles HdinsightSparkCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tier HdinsightSparkCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#compute_isolation HdinsightSparkCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#disk_encryption HdinsightSparkCluster#disk_encryption}
        :param encryption_in_transit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_in_transit_enabled HdinsightSparkCluster#encryption_in_transit_enabled}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#extension HdinsightSparkCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#id HdinsightSparkCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#metastores HdinsightSparkCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#monitor HdinsightSparkCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#network HdinsightSparkCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_link_configuration HdinsightSparkCluster#private_link_configuration}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#security_profile HdinsightSparkCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account HdinsightSparkCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account_gen2 HdinsightSparkCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tags HdinsightSparkCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#timeouts HdinsightSparkCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tls_min_version HdinsightSparkCluster#tls_min_version}.
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#zones HdinsightSparkCluster#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(component_version, dict):
            component_version = HdinsightSparkClusterComponentVersion(**component_version)
        if isinstance(gateway, dict):
            gateway = HdinsightSparkClusterGateway(**gateway)
        if isinstance(roles, dict):
            roles = HdinsightSparkClusterRoles(**roles)
        if isinstance(compute_isolation, dict):
            compute_isolation = HdinsightSparkClusterComputeIsolation(**compute_isolation)
        if isinstance(extension, dict):
            extension = HdinsightSparkClusterExtension(**extension)
        if isinstance(metastores, dict):
            metastores = HdinsightSparkClusterMetastores(**metastores)
        if isinstance(monitor, dict):
            monitor = HdinsightSparkClusterMonitor(**monitor)
        if isinstance(network, dict):
            network = HdinsightSparkClusterNetwork(**network)
        if isinstance(private_link_configuration, dict):
            private_link_configuration = HdinsightSparkClusterPrivateLinkConfiguration(**private_link_configuration)
        if isinstance(security_profile, dict):
            security_profile = HdinsightSparkClusterSecurityProfile(**security_profile)
        if isinstance(storage_account_gen2, dict):
            storage_account_gen2 = HdinsightSparkClusterStorageAccountGen2(**storage_account_gen2)
        if isinstance(timeouts, dict):
            timeouts = HdinsightSparkClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f123d84241e9f1bb751f00ba2192d10dc189f74cf6e0cd4999223c443a99ba5f)
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
            check_type(argname="argument security_profile", value=security_profile, expected_type=type_hints["security_profile"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_account_gen2", value=storage_account_gen2, expected_type=type_hints["storage_account_gen2"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_min_version", value=tls_min_version, expected_type=type_hints["tls_min_version"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
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
        if zones is not None:
            self._values["zones"] = zones

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#cluster_version HdinsightSparkCluster#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def component_version(self) -> HdinsightSparkClusterComponentVersion:
        '''component_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#component_version HdinsightSparkCluster#component_version}
        '''
        result = self._values.get("component_version")
        assert result is not None, "Required property 'component_version' is missing"
        return typing.cast(HdinsightSparkClusterComponentVersion, result)

    @builtins.property
    def gateway(self) -> "HdinsightSparkClusterGateway":
        '''gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#gateway HdinsightSparkCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast("HdinsightSparkClusterGateway", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#location HdinsightSparkCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#resource_group_name HdinsightSparkCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> "HdinsightSparkClusterRoles":
        '''roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#roles HdinsightSparkCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast("HdinsightSparkClusterRoles", result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tier HdinsightSparkCluster#tier}.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_isolation(
        self,
    ) -> typing.Optional[HdinsightSparkClusterComputeIsolation]:
        '''compute_isolation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#compute_isolation HdinsightSparkCluster#compute_isolation}
        '''
        result = self._values.get("compute_isolation")
        return typing.cast(typing.Optional[HdinsightSparkClusterComputeIsolation], result)

    @builtins.property
    def disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterDiskEncryption"]]]:
        '''disk_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#disk_encryption HdinsightSparkCluster#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterDiskEncryption"]]], result)

    @builtins.property
    def encryption_in_transit_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_in_transit_enabled HdinsightSparkCluster#encryption_in_transit_enabled}.'''
        result = self._values.get("encryption_in_transit_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extension(self) -> typing.Optional["HdinsightSparkClusterExtension"]:
        '''extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#extension HdinsightSparkCluster#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional["HdinsightSparkClusterExtension"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#id HdinsightSparkCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastores(self) -> typing.Optional["HdinsightSparkClusterMetastores"]:
        '''metastores block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#metastores HdinsightSparkCluster#metastores}
        '''
        result = self._values.get("metastores")
        return typing.cast(typing.Optional["HdinsightSparkClusterMetastores"], result)

    @builtins.property
    def monitor(self) -> typing.Optional["HdinsightSparkClusterMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#monitor HdinsightSparkCluster#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["HdinsightSparkClusterMonitor"], result)

    @builtins.property
    def network(self) -> typing.Optional["HdinsightSparkClusterNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#network HdinsightSparkCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["HdinsightSparkClusterNetwork"], result)

    @builtins.property
    def private_link_configuration(
        self,
    ) -> typing.Optional["HdinsightSparkClusterPrivateLinkConfiguration"]:
        '''private_link_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_link_configuration HdinsightSparkCluster#private_link_configuration}
        '''
        result = self._values.get("private_link_configuration")
        return typing.cast(typing.Optional["HdinsightSparkClusterPrivateLinkConfiguration"], result)

    @builtins.property
    def security_profile(
        self,
    ) -> typing.Optional["HdinsightSparkClusterSecurityProfile"]:
        '''security_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#security_profile HdinsightSparkCluster#security_profile}
        '''
        result = self._values.get("security_profile")
        return typing.cast(typing.Optional["HdinsightSparkClusterSecurityProfile"], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterStorageAccount"]]]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account HdinsightSparkCluster#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterStorageAccount"]]], result)

    @builtins.property
    def storage_account_gen2(
        self,
    ) -> typing.Optional["HdinsightSparkClusterStorageAccountGen2"]:
        '''storage_account_gen2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account_gen2 HdinsightSparkCluster#storage_account_gen2}
        '''
        result = self._values.get("storage_account_gen2")
        return typing.cast(typing.Optional["HdinsightSparkClusterStorageAccountGen2"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tags HdinsightSparkCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HdinsightSparkClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#timeouts HdinsightSparkCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HdinsightSparkClusterTimeouts"], result)

    @builtins.property
    def tls_min_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#tls_min_version HdinsightSparkCluster#tls_min_version}.'''
        result = self._values.get("tls_min_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#zones HdinsightSparkCluster#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterDiskEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_algorithm": "encryptionAlgorithm",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
        "key_vault_key_id": "keyVaultKeyId",
        "key_vault_managed_identity_id": "keyVaultManagedIdentityId",
    },
)
class HdinsightSparkClusterDiskEncryption:
    def __init__(
        self,
        *,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_algorithm HdinsightSparkCluster#encryption_algorithm}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_at_host_enabled HdinsightSparkCluster#encryption_at_host_enabled}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#key_vault_key_id HdinsightSparkCluster#key_vault_key_id}.
        :param key_vault_managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#key_vault_managed_identity_id HdinsightSparkCluster#key_vault_managed_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c3b86864816b667e72c720c067e31fa98e5b9f9fdfdce7576c073c3b95466d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_algorithm HdinsightSparkCluster#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#encryption_at_host_enabled HdinsightSparkCluster#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#key_vault_key_id HdinsightSparkCluster#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_managed_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#key_vault_managed_identity_id HdinsightSparkCluster#key_vault_managed_identity_id}.'''
        result = self._values.get("key_vault_managed_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterDiskEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterDiskEncryptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterDiskEncryptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b3733bdc41b00d60022a7747c14ed9c1f0ee241d2909e7e3787f1b7ce6fc1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightSparkClusterDiskEncryptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8a241d237e142ca4c05d51e957a7fdda0f0c1d84d923bce1743e0ef896b5d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightSparkClusterDiskEncryptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e93154143e40dd2db5e5781606e03b4011cc016393df3d99de1a4bac782b30e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cfcc008c300e6c88d8c9f8d0fca6aa34a98f91551b87398da929e63711fe59b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5fd4d0d4387a25fc255b687a116fb87121c28df9d7b25bf41a81ac645cad579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterDiskEncryption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterDiskEncryption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterDiskEncryption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2050a3ac358b7878004ccc0b74331c9e293bf15450ca6e8f49ddcb86c5b8df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterDiskEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterDiskEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87ec87cab2e7a589e4678bc44d47a4e327fd7c17cb2952a284cdff3729f958ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e41eec6e94521b72d20c002174144e23d71f2361dd65d61029f96c1f38a698d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b57292bb18175dbe1657a79126188bb60f9312cfe100d27d515f0f5d0f3add5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f99628d246ce5e3981e61832a53c55449ae49b78f81994a593f0600e63377e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultManagedIdentityId")
    def key_vault_managed_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultManagedIdentityId"))

    @key_vault_managed_identity_id.setter
    def key_vault_managed_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60647a91b1c2681b077c505a9955b02ed035ab4518a26fbf38cb6909bfdfaa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultManagedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterDiskEncryption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterDiskEncryption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterDiskEncryption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea47e00aab2970b949617bd504e5e89bbecf4ff1d43e7435e1a0a260675363aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterExtension",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightSparkClusterExtension:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#log_analytics_workspace_id HdinsightSparkCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary_key HdinsightSparkCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7979c2cfb97bb4c32f89e5c7be629107fb4154c82a98a66d47e20e86851b696d)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#log_analytics_workspace_id HdinsightSparkCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary_key HdinsightSparkCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4883352dd54df1ca7837090c4bc901382c81e25f7ccc514f5f27ecededec8e3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e60ffb246594e08db8c37ced1b28c3e76c9e8184a86ccbdfc253e3ebec99e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221d2a1dd50be4f1d31ed7b4f5494d77dc7f6821c0f73f4091a3ed80097f23f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterExtension]:
        return typing.cast(typing.Optional[HdinsightSparkClusterExtension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterExtension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079e26f81c815b46bcd3290f8d56f7fcc37b3ff1fb3e629eabf7673afacfa749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterGateway",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class HdinsightSparkClusterGateway:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8204cf48c145cc53d724664b8545a44f723b4eb43decc28f58ea6cdf75c327fe)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb7324c6885279fa3186e6f7406b0d3c56f847be4ba984c6ed76432696c38e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fac5cd32052b460135396c23c8a8be1cbf6098fdfbee11e42348345dc6b8fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00475daeed03286e2dfc6c9f9b39af0528fcafb44740850b2879ad9733f6c65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterGateway]:
        return typing.cast(typing.Optional[HdinsightSparkClusterGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b4ba16aa80e2aa1ea81d359b6182e1919cc9249b2c8e6335dde19292bb184c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastores",
    jsii_struct_bases=[],
    name_mapping={"ambari": "ambari", "hive": "hive", "oozie": "oozie"},
)
class HdinsightSparkClusterMetastores:
    def __init__(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightSparkClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightSparkClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightSparkClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ambari HdinsightSparkCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#hive HdinsightSparkCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#oozie HdinsightSparkCluster#oozie}
        '''
        if isinstance(ambari, dict):
            ambari = HdinsightSparkClusterMetastoresAmbari(**ambari)
        if isinstance(hive, dict):
            hive = HdinsightSparkClusterMetastoresHive(**hive)
        if isinstance(oozie, dict):
            oozie = HdinsightSparkClusterMetastoresOozie(**oozie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e0db86c5982089ffbc3396b766329110d638cb4c979c9e8ccd0696787ad930)
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
    def ambari(self) -> typing.Optional["HdinsightSparkClusterMetastoresAmbari"]:
        '''ambari block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ambari HdinsightSparkCluster#ambari}
        '''
        result = self._values.get("ambari")
        return typing.cast(typing.Optional["HdinsightSparkClusterMetastoresAmbari"], result)

    @builtins.property
    def hive(self) -> typing.Optional["HdinsightSparkClusterMetastoresHive"]:
        '''hive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#hive HdinsightSparkCluster#hive}
        '''
        result = self._values.get("hive")
        return typing.cast(typing.Optional["HdinsightSparkClusterMetastoresHive"], result)

    @builtins.property
    def oozie(self) -> typing.Optional["HdinsightSparkClusterMetastoresOozie"]:
        '''oozie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#oozie HdinsightSparkCluster#oozie}
        '''
        result = self._values.get("oozie")
        return typing.cast(typing.Optional["HdinsightSparkClusterMetastoresOozie"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterMetastores(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresAmbari",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightSparkClusterMetastoresAmbari:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e17fa330e23190b8392f9fd2338fb73b2b80693117ababdec3432de53220426)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterMetastoresAmbari(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterMetastoresAmbariOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresAmbariOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bf00a8bab955354a45aa6c12bdc95c4bb376948d2f2396db10e3d8a738f7a63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__641d95e84e72e185c1112b9a8448f2527fa97a74630b7d8f0b1de33d1da01376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b29197a8081d834634d469b1505154b26fc3975d5324dc94352ba7eaedf4e08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca305b04399eb56bf5a82b0de7d9081b876ca355fd5c2c5389e94cca0344fc0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5b757cc0473101b14b3ddf197cc7cdc47373c50218c94cf1da6fb72971ee58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastoresAmbari], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterMetastoresAmbari],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f033cc61c9d68868873ae75bf4619efd00e7c213d679fe3b1250a677d4abbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresHive",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightSparkClusterMetastoresHive:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e742f97e3bf65b79ff25bd37bf466bc1ab7c0b77e7b0f78e635b45ed397fa6d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterMetastoresHive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterMetastoresHiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresHiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20854634e98fb9db6ac2353f2a5e288fbaeb22d5fdd20f97c077c09c26865711)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c3debf2cea5411dfe1179ecb81fd9116f8407b9ed3a3791211a087c858f3270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b9485fac72ef8f6cb9858cc6f10565cad2e7d764ea2e818b67d3f3d086c9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7847960a1a1072c02f4450e2407c3aeb71546c3480db547a2b0d2b4a9cc5332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f97e115ce99aab686025dbb1365b0547648aa6277976bb106f2703e1b4da90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastoresHive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterMetastoresHive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e783df98d63f127fbc00cfc01b127ae5fd2c68e410fb5d678c7cb5c944b0747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresOozie",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightSparkClusterMetastoresOozie:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c678a68163884ffc648cad514c11f1ce416e41e05560cdf7e505c680c43f09)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterMetastoresOozie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterMetastoresOozieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresOozieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8db300ce1385711eb20c08d24357bc14249954778401183409fba4fe78c63a39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f1226c611284790989e543bab700d695bba989b81593f341c9f47c2afa11865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6eb925b518f32cb6b023c7fe457fa35e1e12e052cc669749a411c2bf869f975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1b91b3242d543707d968f8ad9b3e89284b9bb44a9ff54ae777147c80047305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4488bad1a16e157be57f3faaa7c0c118836448dcdcdf6c838bac2338a4b405a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastoresOozie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterMetastoresOozie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ce2d7fd4dfadd51f0144d1e645863a327eb5ec21685ca2b23e2d36170f722a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterMetastoresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMetastoresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce28275904c64b50bade9baea9bf07e070562ca0e75b8db520586cc6f178dfa1)
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        value = HdinsightSparkClusterMetastoresAmbari(
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        value = HdinsightSparkClusterMetastoresHive(
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#database_name HdinsightSparkCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#server HdinsightSparkCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        '''
        value = HdinsightSparkClusterMetastoresOozie(
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
    def ambari(self) -> HdinsightSparkClusterMetastoresAmbariOutputReference:
        return typing.cast(HdinsightSparkClusterMetastoresAmbariOutputReference, jsii.get(self, "ambari"))

    @builtins.property
    @jsii.member(jsii_name="hive")
    def hive(self) -> HdinsightSparkClusterMetastoresHiveOutputReference:
        return typing.cast(HdinsightSparkClusterMetastoresHiveOutputReference, jsii.get(self, "hive"))

    @builtins.property
    @jsii.member(jsii_name="oozie")
    def oozie(self) -> HdinsightSparkClusterMetastoresOozieOutputReference:
        return typing.cast(HdinsightSparkClusterMetastoresOozieOutputReference, jsii.get(self, "oozie"))

    @builtins.property
    @jsii.member(jsii_name="ambariInput")
    def ambari_input(self) -> typing.Optional[HdinsightSparkClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastoresAmbari], jsii.get(self, "ambariInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveInput")
    def hive_input(self) -> typing.Optional[HdinsightSparkClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastoresHive], jsii.get(self, "hiveInput"))

    @builtins.property
    @jsii.member(jsii_name="oozieInput")
    def oozie_input(self) -> typing.Optional[HdinsightSparkClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastoresOozie], jsii.get(self, "oozieInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterMetastores]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMetastores], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterMetastores],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc90a057a0cff90e31d539a1e525b89718974450c1b891bf2a8e9746214015b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMonitor",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightSparkClusterMonitor:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#log_analytics_workspace_id HdinsightSparkCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary_key HdinsightSparkCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb76a84bfb31f1c12e9c345eb474259786163e26f9353a69dc86e3247aef6a05)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#log_analytics_workspace_id HdinsightSparkCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary_key HdinsightSparkCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterMonitorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15140c34b1633d346967d03b914ccabb1592dcc27ce92869db86b7bbeaedbf20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa990cbb1bb328415c701cebb2473b8ba1344ebca6fe46709fce8d1d04c4c0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38ec02c24703add136aee5811aaf16089dc2dd578780b236909523aec555bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterMonitor]:
        return typing.cast(typing.Optional[HdinsightSparkClusterMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5a49aedd68ab765116a089e84d1c3a87f92d0e0cdc5d67bb8c3a8ff90d1b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "connection_direction": "connectionDirection",
        "private_link_enabled": "privateLinkEnabled",
    },
)
class HdinsightSparkClusterNetwork:
    def __init__(
        self,
        *,
        connection_direction: typing.Optional[builtins.str] = None,
        private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#connection_direction HdinsightSparkCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_link_enabled HdinsightSparkCluster#private_link_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6249019c92d85f0777891527fa257f5876bd3ad08b359057fd8c0487a532f24)
            check_type(argname="argument connection_direction", value=connection_direction, expected_type=type_hints["connection_direction"])
            check_type(argname="argument private_link_enabled", value=private_link_enabled, expected_type=type_hints["private_link_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_direction is not None:
            self._values["connection_direction"] = connection_direction
        if private_link_enabled is not None:
            self._values["private_link_enabled"] = private_link_enabled

    @builtins.property
    def connection_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#connection_direction HdinsightSparkCluster#connection_direction}.'''
        result = self._values.get("connection_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_link_enabled HdinsightSparkCluster#private_link_enabled}.'''
        result = self._values.get("private_link_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c23cea514f137e79186ed3a87abbbe3e35be7d73bf9f08453315f7dd8f10be0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91834bf464f0079957ddf85b3324f32896a0e992fa4116f512eac0d554c4bda1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a1170356abf14cb9dd962e46404e7c4b87fbb29b411bc03d53a5757d9d8e4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterNetwork]:
        return typing.cast(typing.Optional[HdinsightSparkClusterNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2f5934327142e377632efbb4222787e0cedb144b9b893f0dfc0757e16098eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterPrivateLinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "ip_configuration": "ipConfiguration",
        "name": "name",
    },
)
class HdinsightSparkClusterPrivateLinkConfiguration:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#group_id HdinsightSparkCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ip_configuration HdinsightSparkCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        '''
        if isinstance(ip_configuration, dict):
            ip_configuration = HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration(**ip_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d928695501758f9ec61c00819c715dccd6d398020e04b7d355b895a2eb25b0ae)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#group_id HdinsightSparkCluster#group_id}.'''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_configuration(
        self,
    ) -> "HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration":
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ip_configuration HdinsightSparkCluster#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast("HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterPrivateLinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "primary": "primary",
        "private_ip_address": "privateIpAddress",
        "private_ip_allocation_method": "privateIpAllocationMethod",
        "subnet_id": "subnetId",
    },
)
class HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration:
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary HdinsightSparkCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_ip_address HdinsightSparkCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_ip_allocation_method HdinsightSparkCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdaba558323f4ee724560e5101af9e6ed52abeacf73cc1f7eb4fd31846120025)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary HdinsightSparkCluster#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_ip_address HdinsightSparkCluster#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_allocation_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_ip_allocation_method HdinsightSparkCluster#private_ip_allocation_method}.'''
        result = self._values.get("private_ip_allocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterPrivateLinkConfigurationIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterPrivateLinkConfigurationIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e1b714ced5e515992a1e1de19fc03ccf22990d6085d6016b0bbe612789e7038)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edc6d812f1ce6abe9703bd973f5f7c73dfca50fb4c443cbddc9d02ab166314c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c1aecb4118d98bb6264c7e2ac26a240d80b00c746b61bb863c27aeab862f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d49f4421958fe935773d40fb531f6a7438fa8624d8c96898e3d6568ee9b9324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAllocationMethod")
    def private_ip_allocation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAllocationMethod"))

    @private_ip_allocation_method.setter
    def private_ip_allocation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569254d03082c4266a4df7e650d94fd5657e3182ec527d4a4f014bd99c5f1f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAllocationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9c3622d2ec7d65a278da00c3ecbc304bd424ba0c485594b9b2d62e0d086c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9482d93eeff479e622336e2f83af73a1eae79c1d726c75c5540047098b7d6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterPrivateLinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterPrivateLinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5869fb10f530bf80aa48c3f673ab21c067c3ba769ba3c9dddc31435cf78aff3e)
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#primary HdinsightSparkCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_ip_address HdinsightSparkCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#private_ip_allocation_method HdinsightSparkCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        '''
        value = HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration(
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
    ) -> HdinsightSparkClusterPrivateLinkConfigurationIpConfigurationOutputReference:
        return typing.cast(HdinsightSparkClusterPrivateLinkConfigurationIpConfigurationOutputReference, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "ipConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__afb9baefd2df782a564dd6941ccf1b6832bad48066ba630ab58eb40dfd7f6c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cf7c5805638b3f1f227044cfff8025caa13f36d2ddf6142e97d4e2c953ffa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterPrivateLinkConfiguration]:
        return typing.cast(typing.Optional[HdinsightSparkClusterPrivateLinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterPrivateLinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a746c02c65708f2ac305730dd9c6e3f59cb15b4a0e4c115f706ed8f358d2f8a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRoles",
    jsii_struct_bases=[],
    name_mapping={
        "head_node": "headNode",
        "worker_node": "workerNode",
        "zookeeper_node": "zookeeperNode",
    },
)
class HdinsightSparkClusterRoles:
    def __init__(
        self,
        *,
        head_node: typing.Union["HdinsightSparkClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightSparkClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightSparkClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#head_node HdinsightSparkCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#worker_node HdinsightSparkCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#zookeeper_node HdinsightSparkCluster#zookeeper_node}
        '''
        if isinstance(head_node, dict):
            head_node = HdinsightSparkClusterRolesHeadNode(**head_node)
        if isinstance(worker_node, dict):
            worker_node = HdinsightSparkClusterRolesWorkerNode(**worker_node)
        if isinstance(zookeeper_node, dict):
            zookeeper_node = HdinsightSparkClusterRolesZookeeperNode(**zookeeper_node)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d4125f78550d5acfae28a6ced1bf7f9746b10376fc375146f5577cd27a9f20)
            check_type(argname="argument head_node", value=head_node, expected_type=type_hints["head_node"])
            check_type(argname="argument worker_node", value=worker_node, expected_type=type_hints["worker_node"])
            check_type(argname="argument zookeeper_node", value=zookeeper_node, expected_type=type_hints["zookeeper_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "head_node": head_node,
            "worker_node": worker_node,
            "zookeeper_node": zookeeper_node,
        }

    @builtins.property
    def head_node(self) -> "HdinsightSparkClusterRolesHeadNode":
        '''head_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#head_node HdinsightSparkCluster#head_node}
        '''
        result = self._values.get("head_node")
        assert result is not None, "Required property 'head_node' is missing"
        return typing.cast("HdinsightSparkClusterRolesHeadNode", result)

    @builtins.property
    def worker_node(self) -> "HdinsightSparkClusterRolesWorkerNode":
        '''worker_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#worker_node HdinsightSparkCluster#worker_node}
        '''
        result = self._values.get("worker_node")
        assert result is not None, "Required property 'worker_node' is missing"
        return typing.cast("HdinsightSparkClusterRolesWorkerNode", result)

    @builtins.property
    def zookeeper_node(self) -> "HdinsightSparkClusterRolesZookeeperNode":
        '''zookeeper_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#zookeeper_node HdinsightSparkCluster#zookeeper_node}
        '''
        result = self._values.get("zookeeper_node")
        assert result is not None, "Required property 'zookeeper_node' is missing"
        return typing.cast("HdinsightSparkClusterRolesZookeeperNode", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesHeadNode",
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
class HdinsightSparkClusterRolesHeadNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4636795db2e4b4c723b5badfa32bc9d10f058b47fae6caf963a28a8fddccd0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesHeadNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesHeadNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesHeadNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesHeadNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesHeadNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ce7e236632304b8b158dca78370bceda1667689a0949e43d15d748565bfb2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8692f2787f567570fa92c70b602f314a61d764add0dd3a3579c5108acec5335e)
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
    def script_actions(self) -> "HdinsightSparkClusterRolesHeadNodeScriptActionsList":
        return typing.cast("HdinsightSparkClusterRolesHeadNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesHeadNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesHeadNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__85388ed076140e418417fddca0b9c92b242cdcfe5eacf2141a2b8659bd3c3583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1737ce3181108c9687968208f741c168bab3d37d56206bf1c6ec7ca44984b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6ebaf36d4a387f819ea1b8aa3cbcb315e835eb820cf66065b4d611ca1497ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbea4a42d5cfd57a63b2c42fd2c80e6f86ab28a5220fd95deaba2439703cc33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e617943bcc290e76b6742b6ac197cb1cdc94a354c4bf3c6fc01eb9eaaf0d301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0f08f17dd22e19d3337f41b3b2c7324d4499d2934064605e08331bad11b9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesHeadNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRolesHeadNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cf7ea715ba366d99919d77a12bcc74a16ceabe7ccb0b944f6b2a12d421768e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesHeadNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightSparkClusterRolesHeadNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#uri HdinsightSparkCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#parameters HdinsightSparkCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d597def1051e9f1db4fd2c08e9dbf4863579e1042094b0a516342e282cc7f2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#uri HdinsightSparkCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#parameters HdinsightSparkCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesHeadNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesHeadNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesHeadNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__346147891184fae2a06e31f5cfc46e5c76cd09e73c7ca9b2f15b3ae7e115cdfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightSparkClusterRolesHeadNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52011945f255684c983980c95bdf82c6a1802d1b72e69b64d05e240c9c5c8dd2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightSparkClusterRolesHeadNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795d0628836b54bc2c87c2b204d6a45099624958b6d378ca703a1e8188718f24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ebb751acafd4210091f7a607ac3b964cbd3f1d4c4ed2f65e369e4b7ecc97a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__810fbffe449bad3bb6ebfe7d5ed92ca889fa84ad1abbe065603d13c70bfa133f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesHeadNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesHeadNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesHeadNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe8dce7f8ea11247f2711525bb9ec141d30fb1f2eda205d3fe554866b81e655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesHeadNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesHeadNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8227c80470d40bdb58d3c6c7de37083b5edfebc2bcf10b5571f6fdeb1a65a747)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3fc803cf61d8554a7140d9078a4084068635557c7b1b959e9b524d2b1974a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac3577ecf89d26564835a743df0b7d3e2531fa4301524644ea69916422106f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999c3e719a6c6e7f917795843275bb9a70baca7b5cc8ddb54fd95b6fedf3c6c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesHeadNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesHeadNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesHeadNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60ab86b915f1b1b755b00c2492bccae289fd0420309d02854f109ed925b533f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b1c877acf2a7be53efac673029cff86aeec15e3500772b16541be9d094b6b23)
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
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.
        '''
        value = HdinsightSparkClusterRolesHeadNode(
            username=username,
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putHeadNode", [value]))

    @jsii.member(jsii_name="putWorkerNode")
    def put_worker_node(
        self,
        *,
        target_instance_count: jsii.Number,
        username: builtins.str,
        vm_size: builtins.str,
        autoscale: typing.Optional[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#target_instance_count HdinsightSparkCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#autoscale HdinsightSparkCluster#autoscale}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.
        '''
        value = HdinsightSparkClusterRolesWorkerNode(
            target_instance_count=target_instance_count,
            username=username,
            vm_size=vm_size,
            autoscale=autoscale,
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
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.
        '''
        value = HdinsightSparkClusterRolesZookeeperNode(
            username=username,
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putZookeeperNode", [value]))

    @builtins.property
    @jsii.member(jsii_name="headNode")
    def head_node(self) -> HdinsightSparkClusterRolesHeadNodeOutputReference:
        return typing.cast(HdinsightSparkClusterRolesHeadNodeOutputReference, jsii.get(self, "headNode"))

    @builtins.property
    @jsii.member(jsii_name="workerNode")
    def worker_node(self) -> "HdinsightSparkClusterRolesWorkerNodeOutputReference":
        return typing.cast("HdinsightSparkClusterRolesWorkerNodeOutputReference", jsii.get(self, "workerNode"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNode")
    def zookeeper_node(
        self,
    ) -> "HdinsightSparkClusterRolesZookeeperNodeOutputReference":
        return typing.cast("HdinsightSparkClusterRolesZookeeperNodeOutputReference", jsii.get(self, "zookeeperNode"))

    @builtins.property
    @jsii.member(jsii_name="headNodeInput")
    def head_node_input(self) -> typing.Optional[HdinsightSparkClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesHeadNode], jsii.get(self, "headNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="workerNodeInput")
    def worker_node_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterRolesWorkerNode"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterRolesWorkerNode"], jsii.get(self, "workerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNodeInput")
    def zookeeper_node_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterRolesZookeeperNode"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterRolesZookeeperNode"], jsii.get(self, "zookeeperNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterRoles]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e95200902c008f09af945d6f77552a0a1a19831abf4ada01163cebc663526b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNode",
    jsii_struct_bases=[],
    name_mapping={
        "target_instance_count": "targetInstanceCount",
        "username": "username",
        "vm_size": "vmSize",
        "autoscale": "autoscale",
        "password": "password",
        "script_actions": "scriptActions",
        "ssh_keys": "sshKeys",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
    },
)
class HdinsightSparkClusterRolesWorkerNode:
    def __init__(
        self,
        *,
        target_instance_count: jsii.Number,
        username: builtins.str,
        vm_size: builtins.str,
        autoscale: typing.Optional[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#target_instance_count HdinsightSparkCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#autoscale HdinsightSparkCluster#autoscale}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.
        '''
        if isinstance(autoscale, dict):
            autoscale = HdinsightSparkClusterRolesWorkerNodeAutoscale(**autoscale)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1002f0cd0ffe8395a4fe9d52450d084db146ebeaa2b3e69ff675a570a5ed7f)
            check_type(argname="argument target_instance_count", value=target_instance_count, expected_type=type_hints["target_instance_count"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument autoscale", value=autoscale, expected_type=type_hints["autoscale"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument script_actions", value=script_actions, expected_type=type_hints["script_actions"])
            check_type(argname="argument ssh_keys", value=ssh_keys, expected_type=type_hints["ssh_keys"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_instance_count": target_instance_count,
            "username": username,
            "vm_size": vm_size,
        }
        if autoscale is not None:
            self._values["autoscale"] = autoscale
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
    def target_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#target_instance_count HdinsightSparkCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscale(
        self,
    ) -> typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscale"]:
        '''autoscale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#autoscale HdinsightSparkCluster#autoscale}
        '''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscale"], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesWorkerNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscale",
    jsii_struct_bases=[],
    name_mapping={"capacity": "capacity", "recurrence": "recurrence"},
)
class HdinsightSparkClusterRolesWorkerNodeAutoscale:
    def __init__(
        self,
        *,
        capacity: typing.Optional[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        recurrence: typing.Optional[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#capacity HdinsightSparkCluster#capacity}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#recurrence HdinsightSparkCluster#recurrence}
        '''
        if isinstance(capacity, dict):
            capacity = HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity(**capacity)
        if isinstance(recurrence, dict):
            recurrence = HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211cec0b4ae101c35c6c713534bc9d97920241235632af920b0b5d88042332de)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if recurrence is not None:
            self._values["recurrence"] = recurrence

    @builtins.property
    def capacity(
        self,
    ) -> typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity"]:
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#capacity HdinsightSparkCluster#capacity}
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity"], result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#recurrence HdinsightSparkCluster#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesWorkerNodeAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
    },
)
class HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity:
    def __init__(
        self,
        *,
        max_instance_count: jsii.Number,
        min_instance_count: jsii.Number,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#max_instance_count HdinsightSparkCluster#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#min_instance_count HdinsightSparkCluster#min_instance_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd93db12b83ac6a5f672abe3c5357f865a69b0fa908a04c47f17c3d146ab3ac5)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_instance_count": max_instance_count,
            "min_instance_count": min_instance_count,
        }

    @builtins.property
    def max_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#max_instance_count HdinsightSparkCluster#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        assert result is not None, "Required property 'max_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#min_instance_count HdinsightSparkCluster#min_instance_count}.'''
        result = self._values.get("min_instance_count")
        assert result is not None, "Required property 'min_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a43ca81a7ffb08e41a87dbc97e3ce29d5aff2226706120077bfea2fa2f567100)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aef4ab0a7c2a6a27de4fe9d2960530ce7231092dda3d5ff07ada223ca94dff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd80db45738d631b0baf118cef1fefff52197bbf729601dff49697eecb718ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3344c506da8e661741f9098f038fc7b17606f173e21b6f956eec44defbc86311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesWorkerNodeAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b10be7f59e29b1d89b10c07a9da85efb93e48beb72f419379f90700b48949109)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCapacity")
    def put_capacity(
        self,
        *,
        max_instance_count: jsii.Number,
        min_instance_count: jsii.Number,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#max_instance_count HdinsightSparkCluster#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#min_instance_count HdinsightSparkCluster#min_instance_count}.
        '''
        value = HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
        timezone: builtins.str,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#schedule HdinsightSparkCluster#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#timezone HdinsightSparkCluster#timezone}.
        '''
        value = HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence(
            schedule=schedule, timezone=timezone
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(
        self,
    ) -> HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacityOutputReference:
        return typing.cast(HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacityOutputReference, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference":
        return typing.cast("HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(
        self,
    ) -> typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence"]:
        return typing.cast(typing.Optional["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscale]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0722c8fd2a4870fa902aa57af0379359346622c56450173efb1b630481c3d22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule", "timezone": "timezone"},
)
class HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence:
    def __init__(
        self,
        *,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
        timezone: builtins.str,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#schedule HdinsightSparkCluster#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#timezone HdinsightSparkCluster#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541d6e892eb50f8923c966047eae2a078585a8b121574b57f81537be85ad86d5)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
            "timezone": timezone,
        }

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#schedule HdinsightSparkCluster#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]], result)

    @builtins.property
    def timezone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#timezone HdinsightSparkCluster#timezone}.'''
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7910b47bf9817a724aa84ddcad042130df8baaa9f9377f61ddc4ecc3bd670d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ecfc10ed9167c7f5f01c2eacdfbb7ac5480f23a796d52abe3d07102ccb02e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList":
        return typing.cast("HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d5191186428b1cf707b71894f33ca39ccdd032dad8e292310bcbdca974021d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce462ee5948a12aec74664e2df86ee69bae781a2d6a672287addb276258165ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "days": "days",
        "target_instance_count": "targetInstanceCount",
        "time": "time",
    },
)
class HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule:
    def __init__(
        self,
        *,
        days: typing.Sequence[builtins.str],
        target_instance_count: jsii.Number,
        time: builtins.str,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#days HdinsightSparkCluster#days}.
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#target_instance_count HdinsightSparkCluster#target_instance_count}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#time HdinsightSparkCluster#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d7379da924b57b51445663efb0599f06bc48d9da9dbed435bd17ca699ee489)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument target_instance_count", value=target_instance_count, expected_type=type_hints["target_instance_count"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
            "target_instance_count": target_instance_count,
            "time": time,
        }

    @builtins.property
    def days(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#days HdinsightSparkCluster#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#target_instance_count HdinsightSparkCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#time HdinsightSparkCluster#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b21d026b30bc61925b6c1cb9400a6ae96d4883e3ae2f0724496f76da70bd95d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca246b5da168c75c05b9ea2f42b6bb34536f825414a12b490333a68fc6b4e14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ae7a26f29581678e8f28a55d8f41e094afc7955eaa3ba5385c2f6b4588b43b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a74141d7959cdb635ea8fa074cb107bad5a0605706926d13443537b5855452)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df3fbb9a8a7d9e4515cac0df55c7f747f80d5d4184ae23b15a2808114cb44613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a4f02d775d694522e7a93b0d52e0baf8c5a1d8399c68218ae3536c849ffbd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc61ed538f0bdd23f8b05e497cb2a5b129513cbc57192b8d18cd651828f732cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCountInput")
    def target_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "days"))

    @days.setter
    def days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8754fc3abf4f99383bceeb38325ea301d274e10f888c39de263098efd5408c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e16e19209c957ab51582d6074a5406fded18aa74551edbb105d2f6858ce14c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b477a3111d32f61947271d3408a791604a86d67112bfed7e93d7b94cac9a88ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89a62730e805ffd3f2ad96a6f45be7202cb304306d88ec589f9a81208c0a2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesWorkerNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f359616f9c9f395c33c065b93243f8a6d44bca99f28459424f5d2c23960abfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(
        self,
        *,
        capacity: typing.Optional[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
        recurrence: typing.Optional[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#capacity HdinsightSparkCluster#capacity}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#recurrence HdinsightSparkCluster#recurrence}
        '''
        value = HdinsightSparkClusterRolesWorkerNodeAutoscale(
            capacity=capacity, recurrence=recurrence
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32e71ef2b4973fcd466a9e0e9c366fefbf53c67c5443c61222cb55cd0059de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScriptActions", [value]))

    @jsii.member(jsii_name="resetAutoscale")
    def reset_autoscale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscale", []))

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
    @jsii.member(jsii_name="autoscale")
    def autoscale(self) -> HdinsightSparkClusterRolesWorkerNodeAutoscaleOutputReference:
        return typing.cast(HdinsightSparkClusterRolesWorkerNodeAutoscaleOutputReference, jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(self) -> "HdinsightSparkClusterRolesWorkerNodeScriptActionsList":
        return typing.cast("HdinsightSparkClusterRolesWorkerNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(
        self,
    ) -> typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscale]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscale], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesWorkerNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f0f2286dadb41e93101bbdf03e51a534d63564e5405b08efcc97e9da1ab863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5577f43df7d620da9a6d375a9d23c9da9943dee4b05816ce2a1c3d9cf1771ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6a9c0ca795642816a67ac104fb6502aafce0eb88bf9709b33ae966c4451c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d704741377e63d4d00041eca9e58f79d2822e532957f2a6ecfd22c6dd408c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba86575ae36e3ba0ece1c1edad6a1b701c574b376479da7aca05d4e09a7e743e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea574ea7f897560adde91d622126eafbc31716458c4ae0f2f1d91cd35bbb1002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f270077edf6a83912ba7872d403fa97b284fec40c620fc6f9d4c55abd0f654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterRolesWorkerNode]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesWorkerNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRolesWorkerNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7f88d855b8d36b528d76367e2927859e36010d93bc2dfbc8189cab7822df5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightSparkClusterRolesWorkerNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#uri HdinsightSparkCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#parameters HdinsightSparkCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3a862e64cc17cb9cf6dc17a2b116c88511e90bb85546c258421f7378227faf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#uri HdinsightSparkCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#parameters HdinsightSparkCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesWorkerNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesWorkerNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c0ed0fbb28cc67cb6b145a11f7d01c390bc48c93ef486efbf3f497df300064)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightSparkClusterRolesWorkerNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64727c584148db595295c8a070ad5a43a78d01402e0de2280bc500c396bd556b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightSparkClusterRolesWorkerNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a0f5ab2c4b0d851f0994ee1559051a1cb58aa0809a9acc45f5074aa1e2cb2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9dc7c079f62e1447cc273a92250bfb35af5b1798ea7c74de63da02d2c793bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73a1cf893798e25c32f44d5467f89105753e69c4c7274190d5e79e07b33f3a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbbcb361194fb845af7f20694a7f20a9c702d9f33bb72e4c24be602fac6dc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesWorkerNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesWorkerNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf306ed280e1aafde8b5322271910a7b48d315ac46beeb9c7db0c5ace2ec8fa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8676d9649786b9523c393274fd67789866419b595f5c81bb697dfe2aa54f81f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50e6e444ce5cea7fa3caa1fb9f38158b449276f74a923c52c835145d8f67e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded643be996686cbf4a31f78dcb0d5f77b0887ae51b7f0c8cc75c94b367fca39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2497264fbb705aca75238264bb6fff46d36f92054c4a640947f7a677672ba8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesZookeeperNode",
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
class HdinsightSparkClusterRolesZookeeperNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cce9f771b8e7d84ba2dbea4e5ff8821c8771b132d303996bf0191cdae29d6a0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#username HdinsightSparkCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#vm_size HdinsightSparkCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#password HdinsightSparkCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesZookeeperNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#script_actions HdinsightSparkCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesZookeeperNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ssh_keys HdinsightSparkCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#subnet_id HdinsightSparkCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#virtual_network_id HdinsightSparkCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesZookeeperNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesZookeeperNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesZookeeperNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__802059c7ee9460443c67753912bff94d628c9df3886cd374e1be0c055f263786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightSparkClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7026f39df94d757d9e54d90ff33607536242ab0b125f9fc5264a4617cfdb9171)
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
    ) -> "HdinsightSparkClusterRolesZookeeperNodeScriptActionsList":
        return typing.cast("HdinsightSparkClusterRolesZookeeperNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesZookeeperNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightSparkClusterRolesZookeeperNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2dd8fdfc98033c3711083ed6d92311802e0f3c1f289a59f684e72e7bd6e8307f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2135c7037204a7a416e0684cd17df71957b4453202262b2bc3dcb262f5d08cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153dd47331bcb2cc67c4dc160d0b9f8dd6eef8d77f19a038054dc62b20290599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5781221fcab1e9b36d59e1bd55dc94529b411170a3dfdb7407bf7284f72a60a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9522aeee80a9cb5d6601527e0f0b15b3120cb92944e862a185628663f63ad450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4547467f0781930f630581b05e1ccaa26798701ea8ebad5c86dd5c8d852f6ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterRolesZookeeperNode]:
        return typing.cast(typing.Optional[HdinsightSparkClusterRolesZookeeperNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterRolesZookeeperNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285334e1768f188025252f57cc3666265525aa98e1bbd2f6f66c98e8e9ef7093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesZookeeperNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightSparkClusterRolesZookeeperNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#uri HdinsightSparkCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#parameters HdinsightSparkCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0515963d19164e1437511f03e712f416740b6df30c5bc854e10450239f82d82)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#name HdinsightSparkCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#uri HdinsightSparkCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#parameters HdinsightSparkCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterRolesZookeeperNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterRolesZookeeperNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesZookeeperNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c01a1039dbe43716a1406d4d65ccbdbb41ebab9f622ce5b4484d83ed7ffcc903)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightSparkClusterRolesZookeeperNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc64991110fcedc30bce41b5e8f460424704f29505aaf7f93227e1d81ff2e73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightSparkClusterRolesZookeeperNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f948a96a761125bc9007a30c1216b5818a0a1853a352aa36ba12079183991138)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c60d40cf90f6b01d797ce12040758d468f3e2f5d35785579c79d7521891e6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__028139975f46d4af9e792cc72586dd3e9ee5cb8e74f2fba6cc710edbba3481de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesZookeeperNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesZookeeperNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesZookeeperNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fa497b06dea3d864743ca6ea24b801703b64b16de860e7ecd75a93d0055c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterRolesZookeeperNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterRolesZookeeperNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63850690280aee6a84c7f35bfddf40c21a037879202e017c35a3d95db1d79349)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70cf56631754fded0b5abcbf96851af4dcc25c9b3a2f09e3f283190de73a9aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ec8cddf76a54a72359fadc1ffef529bc279ba4c36f3d6ee7c060f2e7d9d181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f94bed446b74fd3894158293cf8d7ca40f77181e3b243881e2208335268dfa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesZookeeperNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesZookeeperNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesZookeeperNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5048d622a4e7b7b242f22b0709a305123baff8a9f10e02cc5f809d1a493bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterSecurityProfile",
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
class HdinsightSparkClusterSecurityProfile:
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
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#aadds_resource_id HdinsightSparkCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_name HdinsightSparkCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_username HdinsightSparkCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_user_password HdinsightSparkCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ldaps_urls HdinsightSparkCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#msi_resource_id HdinsightSparkCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#cluster_users_group_dns HdinsightSparkCluster#cluster_users_group_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdb57d348d56c2bf3679c2cef3a3208fd3d0cde37701e61aa5f9e6ba428904d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#aadds_resource_id HdinsightSparkCluster#aadds_resource_id}.'''
        result = self._values.get("aadds_resource_id")
        assert result is not None, "Required property 'aadds_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_name HdinsightSparkCluster#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_username HdinsightSparkCluster#domain_username}.'''
        result = self._values.get("domain_username")
        assert result is not None, "Required property 'domain_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_user_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#domain_user_password HdinsightSparkCluster#domain_user_password}.'''
        result = self._values.get("domain_user_password")
        assert result is not None, "Required property 'domain_user_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ldaps_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#ldaps_urls HdinsightSparkCluster#ldaps_urls}.'''
        result = self._values.get("ldaps_urls")
        assert result is not None, "Required property 'ldaps_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def msi_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#msi_resource_id HdinsightSparkCluster#msi_resource_id}.'''
        result = self._values.get("msi_resource_id")
        assert result is not None, "Required property 'msi_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_users_group_dns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#cluster_users_group_dns HdinsightSparkCluster#cluster_users_group_dns}.'''
        result = self._values.get("cluster_users_group_dns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterSecurityProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterSecurityProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterSecurityProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a90fbb9e22425f93cc14899184e7ec79cf7d0b8a48ebf279741fb3821877703)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2182f8fbaf2e8ed6674b1ab2d1a38830d6fa18a26aefe965051aa7c608d63111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aaddsResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterUsersGroupDns")
    def cluster_users_group_dns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterUsersGroupDns"))

    @cluster_users_group_dns.setter
    def cluster_users_group_dns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a00a9c6d3eed1d836af08173e6c8e124cdc676a28ec3bc8550a290dd64be8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterUsersGroupDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42acb8d1afb13e6e22313b5ea3a63e80d7b2f2ba68c6b325d7132656ab18ac87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUsername")
    def domain_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUsername"))

    @domain_username.setter
    def domain_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60db4b4f4ed0d38fda45370ad31114f79f78bbf341a0dbe819771d8223d6305a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUserPassword")
    def domain_user_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUserPassword"))

    @domain_user_password.setter
    def domain_user_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a50aead3262010ebdb8de3ecd0288090b3aedabba84d3c12da58dff23a07aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUserPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapsUrls")
    def ldaps_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ldapsUrls"))

    @ldaps_urls.setter
    def ldaps_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83291ab9a9e6925b26ea0c78a985268e360ae6d4f9a2003b6ef4af67be210f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapsUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiResourceId")
    def msi_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "msiResourceId"))

    @msi_resource_id.setter
    def msi_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f50d5f5ef9d166a6ddcbd36182f96fe46f2c91769b58ac926a4c3a7a3530968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightSparkClusterSecurityProfile]:
        return typing.cast(typing.Optional[HdinsightSparkClusterSecurityProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterSecurityProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc865d624e145f128347c62826c053f86c834fe73915742674a8e9fb9ee42630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterStorageAccount",
    jsii_struct_bases=[],
    name_mapping={
        "is_default": "isDefault",
        "storage_account_key": "storageAccountKey",
        "storage_container_id": "storageContainerId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightSparkClusterStorageAccount:
    def __init__(
        self,
        *,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_account_key: builtins.str,
        storage_container_id: builtins.str,
        storage_resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#is_default HdinsightSparkCluster#is_default}.
        :param storage_account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account_key HdinsightSparkCluster#storage_account_key}.
        :param storage_container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_container_id HdinsightSparkCluster#storage_container_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_resource_id HdinsightSparkCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93b8c760dbbb2771655551f17259c38d2fe841443e503b4637dac5296539f86)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#is_default HdinsightSparkCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_account_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_account_key HdinsightSparkCluster#storage_account_key}.'''
        result = self._values.get("storage_account_key")
        assert result is not None, "Required property 'storage_account_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_container_id HdinsightSparkCluster#storage_container_id}.'''
        result = self._values.get("storage_container_id")
        assert result is not None, "Required property 'storage_container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_resource_id HdinsightSparkCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterStorageAccountGen2",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem_id": "filesystemId",
        "is_default": "isDefault",
        "managed_identity_resource_id": "managedIdentityResourceId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightSparkClusterStorageAccountGen2:
    def __init__(
        self,
        *,
        filesystem_id: builtins.str,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        managed_identity_resource_id: builtins.str,
        storage_resource_id: builtins.str,
    ) -> None:
        '''
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#filesystem_id HdinsightSparkCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#is_default HdinsightSparkCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#managed_identity_resource_id HdinsightSparkCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_resource_id HdinsightSparkCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e50a2bcba0a64891043df9d2255e1a2cd0d7c349b3e8d04acb540af913b851)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#filesystem_id HdinsightSparkCluster#filesystem_id}.'''
        result = self._values.get("filesystem_id")
        assert result is not None, "Required property 'filesystem_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#is_default HdinsightSparkCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def managed_identity_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#managed_identity_resource_id HdinsightSparkCluster#managed_identity_resource_id}.'''
        result = self._values.get("managed_identity_resource_id")
        assert result is not None, "Required property 'managed_identity_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#storage_resource_id HdinsightSparkCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        assert result is not None, "Required property 'storage_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterStorageAccountGen2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterStorageAccountGen2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterStorageAccountGen2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__205e83d64500fd1cb6fff0e180d8a8a94dc0eb608ddeaa4f0fa9d0553b5cde17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f4900bc22a74ac8eed54568301ec3bdef22ac9ed21271a2dcf2d837a47b8063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5ac66da5b1461f6457267c51c482f94a06f96195af7e7a546665e431d19799c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceId")
    def managed_identity_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityResourceId"))

    @managed_identity_resource_id.setter
    def managed_identity_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1c8d809204c0f814c73223bf8abfd7e28827da77c5b573b88f23676bd34dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c30ba819d5ac3b993fd181b3de3061bfa7da04ab427974b4b5454bb4199c96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightSparkClusterStorageAccountGen2]:
        return typing.cast(typing.Optional[HdinsightSparkClusterStorageAccountGen2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightSparkClusterStorageAccountGen2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c206f3bc0a573cc2e747c0367fb24671b171eba2aaae1253f3f0f59a77b36cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterStorageAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterStorageAccountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__126a51990e131f85b66285c1ea8f1db3d4901fa290cb58091e61bb46a9a434dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightSparkClusterStorageAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600e90f3d0710e38576c72fc2458b47020de4582c859d211fdc9471a74b8875c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightSparkClusterStorageAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6676817636512bc25eea46a23cc38fcaf999f8bf58d9338a37ba74da325c5a7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01aacf8e2f9ce6f245c761389ae7dd79da3388ba797b3ede90925fb6a7d1493)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9196f1b599d692dfcd42c070bf40a3499ae2d15975d3079d2addef291d304460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterStorageAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterStorageAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterStorageAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ed654d18abaa0e3d4f28b21a42720be9554e3bb22300e077b23085001da31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightSparkClusterStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8163b6b9fe6aa350cc7c11814d43e80d8fee132778e49376c82ebb4b319ba1cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb436bd59e6661d3787241c04c6b76616fc156ec54ece4e8a47b37326d52de49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountKey")
    def storage_account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountKey"))

    @storage_account_key.setter
    def storage_account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3fe80f3e5b2f160bcabd7ccd3ef14a616f84e4f6d5d4640f4bce9a70c798e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerId")
    def storage_container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerId"))

    @storage_container_id.setter
    def storage_container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c11e944cdd788816331c0f2b0a058e98d6d2cf407644d47911bf2a317ab6b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f277bd5da5aa1b9f23ce9b28eee035cf2cf3ef2e07a7b29a502f4e737c9ad69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterStorageAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterStorageAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterStorageAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff2c0d4af7acde929b8d1ff998697dcf71dded5e200463382cc0340a555b96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class HdinsightSparkClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#create HdinsightSparkCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#delete HdinsightSparkCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#read HdinsightSparkCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#update HdinsightSparkCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febee11f2e133667373da475e079c648db64be88d65d0ecca9c8bf644ee6d965)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#create HdinsightSparkCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#delete HdinsightSparkCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#read HdinsightSparkCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_spark_cluster#update HdinsightSparkCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightSparkClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightSparkClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightSparkCluster.HdinsightSparkClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b73c4bfd6191e16bea5558c23a12995f9caca8d59f395240357e8dcff76418)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c976ec2ab04ba89b82c2f63cf915a7e5f15e6538efddf93a67a85cc9ea2af2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9090e82713a00af0bcd3f80d6bdbf5fd24e519c33a0fe345d611a75db31d9d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e18466223417cc85c095f6fea6e620559b359afb5fe40cfeeae44617e06abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88fd8c10958a91bd68e0cb59addf74ff6b6f3a95c320ef649792ea974255fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd3e83960c68803f1a171cd1dafc642e3ef050001b6fdca023d1ce03ce7e20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HdinsightSparkCluster",
    "HdinsightSparkClusterComponentVersion",
    "HdinsightSparkClusterComponentVersionOutputReference",
    "HdinsightSparkClusterComputeIsolation",
    "HdinsightSparkClusterComputeIsolationOutputReference",
    "HdinsightSparkClusterConfig",
    "HdinsightSparkClusterDiskEncryption",
    "HdinsightSparkClusterDiskEncryptionList",
    "HdinsightSparkClusterDiskEncryptionOutputReference",
    "HdinsightSparkClusterExtension",
    "HdinsightSparkClusterExtensionOutputReference",
    "HdinsightSparkClusterGateway",
    "HdinsightSparkClusterGatewayOutputReference",
    "HdinsightSparkClusterMetastores",
    "HdinsightSparkClusterMetastoresAmbari",
    "HdinsightSparkClusterMetastoresAmbariOutputReference",
    "HdinsightSparkClusterMetastoresHive",
    "HdinsightSparkClusterMetastoresHiveOutputReference",
    "HdinsightSparkClusterMetastoresOozie",
    "HdinsightSparkClusterMetastoresOozieOutputReference",
    "HdinsightSparkClusterMetastoresOutputReference",
    "HdinsightSparkClusterMonitor",
    "HdinsightSparkClusterMonitorOutputReference",
    "HdinsightSparkClusterNetwork",
    "HdinsightSparkClusterNetworkOutputReference",
    "HdinsightSparkClusterPrivateLinkConfiguration",
    "HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration",
    "HdinsightSparkClusterPrivateLinkConfigurationIpConfigurationOutputReference",
    "HdinsightSparkClusterPrivateLinkConfigurationOutputReference",
    "HdinsightSparkClusterRoles",
    "HdinsightSparkClusterRolesHeadNode",
    "HdinsightSparkClusterRolesHeadNodeOutputReference",
    "HdinsightSparkClusterRolesHeadNodeScriptActions",
    "HdinsightSparkClusterRolesHeadNodeScriptActionsList",
    "HdinsightSparkClusterRolesHeadNodeScriptActionsOutputReference",
    "HdinsightSparkClusterRolesOutputReference",
    "HdinsightSparkClusterRolesWorkerNode",
    "HdinsightSparkClusterRolesWorkerNodeAutoscale",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacityOutputReference",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleOutputReference",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList",
    "HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference",
    "HdinsightSparkClusterRolesWorkerNodeOutputReference",
    "HdinsightSparkClusterRolesWorkerNodeScriptActions",
    "HdinsightSparkClusterRolesWorkerNodeScriptActionsList",
    "HdinsightSparkClusterRolesWorkerNodeScriptActionsOutputReference",
    "HdinsightSparkClusterRolesZookeeperNode",
    "HdinsightSparkClusterRolesZookeeperNodeOutputReference",
    "HdinsightSparkClusterRolesZookeeperNodeScriptActions",
    "HdinsightSparkClusterRolesZookeeperNodeScriptActionsList",
    "HdinsightSparkClusterRolesZookeeperNodeScriptActionsOutputReference",
    "HdinsightSparkClusterSecurityProfile",
    "HdinsightSparkClusterSecurityProfileOutputReference",
    "HdinsightSparkClusterStorageAccount",
    "HdinsightSparkClusterStorageAccountGen2",
    "HdinsightSparkClusterStorageAccountGen2OutputReference",
    "HdinsightSparkClusterStorageAccountList",
    "HdinsightSparkClusterStorageAccountOutputReference",
    "HdinsightSparkClusterTimeouts",
    "HdinsightSparkClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__995f259ea200d232f4557f6b215ac3c5f25da7074bcaa56fd899fc533117efb8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightSparkClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightSparkClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightSparkClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightSparkClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extension: typing.Optional[typing.Union[HdinsightSparkClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightSparkClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightSparkClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightSparkClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightSparkClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightSparkClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightSparkClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightSparkClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__53dc1cd572fbc00654bfa101e34aa9ada88f023b63367a0b2fa0fb1dedaa7790(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7daab7a626f420715c5ddbfbfb0eb26cca91e1b028b8b0fc22880202daf09b79(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5e700cc53a6954fa449350626d33a5fe10b7059f818d3713646ee76c9d62e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52d8f99cda72c5fcda1d1dc84513cd5a13ded9feacf25285667465f8dd70e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a86dd6558478dc631f32f466009a4bacd5a027d5b7642424859d68dcc6575c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8851155b0d56ab5b6271e05403693f0c2baae9995b038a212f4b9b8261c6c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5baea4619994aac2227fd5b4511ea9e10e0dacd80b49e1c2579af0e0b55d49c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7148630001d2cf5f29c28402752d56e3f74671d35c058553a85dd006e7e6ac1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf270dabd5e16601892a5406b96329c0f4a0997e7aa09ce8be64136df179c33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff68a5dfe2fe24dbdc2e31f4e594e635daf74539fa07103477f39fc9db9c8b6d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b0d251a964145789dc66fca9148d4301e0e589294b4299f6eb04421952ee31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e244e0ad88630c1ec59dcd59508c65f889619458aa2c9cf98e66dd3b7dc82061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f279692b4a939566598af8006ff5b85331c5add41b7dd3b97e73817c1b9fa83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32190a4889d359476e3d71c992d7e4e7b993da9fc4b027d5283fb5c05fa8066a(
    *,
    spark: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c63b91eafab8b925c6a8beb165b930ba8b79ca33f3e8ff7e125eebeaeeafb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2064cda0aae78d0286b932f5e71d83e4bb4a0edb04cb4a4deef5f6f8156ba344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613d4435cf76a538d74e34b3d1614253e41f759d89eb76a8a5ba3be782f611c7(
    value: typing.Optional[HdinsightSparkClusterComponentVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9668665878413f05693d55c6b64808797404f014c12f09dff89623522943e6cb(
    *,
    compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_sku: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f8003315c053b165712af807aa0716aa14d2c71cf33643858f5c40c79d0bc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8342590ffaf3f5af00fbec7a1731e442c019c809b024f10565fb567a5142149(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034e7b2a5cd815f801a12c480a8830e5f344f245d4dfa6b32e94a7274aac3715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63150a1d26d3f6d98830af18e0f5f521b06df89e4d5a91088b327299b1085461(
    value: typing.Optional[HdinsightSparkClusterComputeIsolation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f123d84241e9f1bb751f00ba2192d10dc189f74cf6e0cd4999223c443a99ba5f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightSparkClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightSparkClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightSparkClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightSparkClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extension: typing.Optional[typing.Union[HdinsightSparkClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightSparkClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightSparkClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightSparkClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightSparkClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightSparkClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightSparkClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightSparkClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c3b86864816b667e72c720c067e31fa98e5b9f9fdfdce7576c073c3b95466d(
    *,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b3733bdc41b00d60022a7747c14ed9c1f0ee241d2909e7e3787f1b7ce6fc1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8a241d237e142ca4c05d51e957a7fdda0f0c1d84d923bce1743e0ef896b5d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e93154143e40dd2db5e5781606e03b4011cc016393df3d99de1a4bac782b30e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfcc008c300e6c88d8c9f8d0fca6aa34a98f91551b87398da929e63711fe59b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fd4d0d4387a25fc255b687a116fb87121c28df9d7b25bf41a81ac645cad579(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2050a3ac358b7878004ccc0b74331c9e293bf15450ca6e8f49ddcb86c5b8df8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterDiskEncryption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ec87cab2e7a589e4678bc44d47a4e327fd7c17cb2952a284cdff3729f958ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41eec6e94521b72d20c002174144e23d71f2361dd65d61029f96c1f38a698d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57292bb18175dbe1657a79126188bb60f9312cfe100d27d515f0f5d0f3add5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f99628d246ce5e3981e61832a53c55449ae49b78f81994a593f0600e63377e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60647a91b1c2681b077c505a9955b02ed035ab4518a26fbf38cb6909bfdfaa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea47e00aab2970b949617bd504e5e89bbecf4ff1d43e7435e1a0a260675363aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterDiskEncryption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7979c2cfb97bb4c32f89e5c7be629107fb4154c82a98a66d47e20e86851b696d(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4883352dd54df1ca7837090c4bc901382c81e25f7ccc514f5f27ecededec8e3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e60ffb246594e08db8c37ced1b28c3e76c9e8184a86ccbdfc253e3ebec99e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221d2a1dd50be4f1d31ed7b4f5494d77dc7f6821c0f73f4091a3ed80097f23f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079e26f81c815b46bcd3290f8d56f7fcc37b3ff1fb3e629eabf7673afacfa749(
    value: typing.Optional[HdinsightSparkClusterExtension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8204cf48c145cc53d724664b8545a44f723b4eb43decc28f58ea6cdf75c327fe(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb7324c6885279fa3186e6f7406b0d3c56f847be4ba984c6ed76432696c38e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fac5cd32052b460135396c23c8a8be1cbf6098fdfbee11e42348345dc6b8fc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00475daeed03286e2dfc6c9f9b39af0528fcafb44740850b2879ad9733f6c65f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b4ba16aa80e2aa1ea81d359b6182e1919cc9249b2c8e6335dde19292bb184c(
    value: typing.Optional[HdinsightSparkClusterGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e0db86c5982089ffbc3396b766329110d638cb4c979c9e8ccd0696787ad930(
    *,
    ambari: typing.Optional[typing.Union[HdinsightSparkClusterMetastoresAmbari, typing.Dict[builtins.str, typing.Any]]] = None,
    hive: typing.Optional[typing.Union[HdinsightSparkClusterMetastoresHive, typing.Dict[builtins.str, typing.Any]]] = None,
    oozie: typing.Optional[typing.Union[HdinsightSparkClusterMetastoresOozie, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e17fa330e23190b8392f9fd2338fb73b2b80693117ababdec3432de53220426(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf00a8bab955354a45aa6c12bdc95c4bb376948d2f2396db10e3d8a738f7a63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641d95e84e72e185c1112b9a8448f2527fa97a74630b7d8f0b1de33d1da01376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b29197a8081d834634d469b1505154b26fc3975d5324dc94352ba7eaedf4e08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca305b04399eb56bf5a82b0de7d9081b876ca355fd5c2c5389e94cca0344fc0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5b757cc0473101b14b3ddf197cc7cdc47373c50218c94cf1da6fb72971ee58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f033cc61c9d68868873ae75bf4619efd00e7c213d679fe3b1250a677d4abbd(
    value: typing.Optional[HdinsightSparkClusterMetastoresAmbari],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e742f97e3bf65b79ff25bd37bf466bc1ab7c0b77e7b0f78e635b45ed397fa6d(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20854634e98fb9db6ac2353f2a5e288fbaeb22d5fdd20f97c077c09c26865711(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3debf2cea5411dfe1179ecb81fd9116f8407b9ed3a3791211a087c858f3270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b9485fac72ef8f6cb9858cc6f10565cad2e7d764ea2e818b67d3f3d086c9a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7847960a1a1072c02f4450e2407c3aeb71546c3480db547a2b0d2b4a9cc5332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f97e115ce99aab686025dbb1365b0547648aa6277976bb106f2703e1b4da90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e783df98d63f127fbc00cfc01b127ae5fd2c68e410fb5d678c7cb5c944b0747(
    value: typing.Optional[HdinsightSparkClusterMetastoresHive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c678a68163884ffc648cad514c11f1ce416e41e05560cdf7e505c680c43f09(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db300ce1385711eb20c08d24357bc14249954778401183409fba4fe78c63a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1226c611284790989e543bab700d695bba989b81593f341c9f47c2afa11865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6eb925b518f32cb6b023c7fe457fa35e1e12e052cc669749a411c2bf869f975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1b91b3242d543707d968f8ad9b3e89284b9bb44a9ff54ae777147c80047305(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4488bad1a16e157be57f3faaa7c0c118836448dcdcdf6c838bac2338a4b405a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ce2d7fd4dfadd51f0144d1e645863a327eb5ec21685ca2b23e2d36170f722a(
    value: typing.Optional[HdinsightSparkClusterMetastoresOozie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce28275904c64b50bade9baea9bf07e070562ca0e75b8db520586cc6f178dfa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc90a057a0cff90e31d539a1e525b89718974450c1b891bf2a8e9746214015b(
    value: typing.Optional[HdinsightSparkClusterMetastores],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb76a84bfb31f1c12e9c345eb474259786163e26f9353a69dc86e3247aef6a05(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15140c34b1633d346967d03b914ccabb1592dcc27ce92869db86b7bbeaedbf20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa990cbb1bb328415c701cebb2473b8ba1344ebca6fe46709fce8d1d04c4c0c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38ec02c24703add136aee5811aaf16089dc2dd578780b236909523aec555bf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5a49aedd68ab765116a089e84d1c3a87f92d0e0cdc5d67bb8c3a8ff90d1b72(
    value: typing.Optional[HdinsightSparkClusterMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6249019c92d85f0777891527fa257f5876bd3ad08b359057fd8c0487a532f24(
    *,
    connection_direction: typing.Optional[builtins.str] = None,
    private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c23cea514f137e79186ed3a87abbbe3e35be7d73bf9f08453315f7dd8f10be0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91834bf464f0079957ddf85b3324f32896a0e992fa4116f512eac0d554c4bda1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1170356abf14cb9dd962e46404e7c4b87fbb29b411bc03d53a5757d9d8e4ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2f5934327142e377632efbb4222787e0cedb144b9b893f0dfc0757e16098eb(
    value: typing.Optional[HdinsightSparkClusterNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d928695501758f9ec61c00819c715dccd6d398020e04b7d355b895a2eb25b0ae(
    *,
    group_id: builtins.str,
    ip_configuration: typing.Union[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaba558323f4ee724560e5101af9e6ed52abeacf73cc1f7eb4fd31846120025(
    *,
    name: builtins.str,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    private_ip_allocation_method: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1b714ced5e515992a1e1de19fc03ccf22990d6085d6016b0bbe612789e7038(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc6d812f1ce6abe9703bd973f5f7c73dfca50fb4c443cbddc9d02ab166314c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c1aecb4118d98bb6264c7e2ac26a240d80b00c746b61bb863c27aeab862f48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d49f4421958fe935773d40fb531f6a7438fa8624d8c96898e3d6568ee9b9324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569254d03082c4266a4df7e650d94fd5657e3182ec527d4a4f014bd99c5f1f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9c3622d2ec7d65a278da00c3ecbc304bd424ba0c485594b9b2d62e0d086c80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9482d93eeff479e622336e2f83af73a1eae79c1d726c75c5540047098b7d6f0(
    value: typing.Optional[HdinsightSparkClusterPrivateLinkConfigurationIpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5869fb10f530bf80aa48c3f673ab21c067c3ba769ba3c9dddc31435cf78aff3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb9baefd2df782a564dd6941ccf1b6832bad48066ba630ab58eb40dfd7f6c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cf7c5805638b3f1f227044cfff8025caa13f36d2ddf6142e97d4e2c953ffa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a746c02c65708f2ac305730dd9c6e3f59cb15b4a0e4c115f706ed8f358d2f8a2(
    value: typing.Optional[HdinsightSparkClusterPrivateLinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d4125f78550d5acfae28a6ced1bf7f9746b10376fc375146f5577cd27a9f20(
    *,
    head_node: typing.Union[HdinsightSparkClusterRolesHeadNode, typing.Dict[builtins.str, typing.Any]],
    worker_node: typing.Union[HdinsightSparkClusterRolesWorkerNode, typing.Dict[builtins.str, typing.Any]],
    zookeeper_node: typing.Union[HdinsightSparkClusterRolesZookeeperNode, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4636795db2e4b4c723b5badfa32bc9d10f058b47fae6caf963a28a8fddccd0(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ce7e236632304b8b158dca78370bceda1667689a0949e43d15d748565bfb2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8692f2787f567570fa92c70b602f314a61d764add0dd3a3579c5108acec5335e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85388ed076140e418417fddca0b9c92b242cdcfe5eacf2141a2b8659bd3c3583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1737ce3181108c9687968208f741c168bab3d37d56206bf1c6ec7ca44984b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6ebaf36d4a387f819ea1b8aa3cbcb315e835eb820cf66065b4d611ca1497ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbea4a42d5cfd57a63b2c42fd2c80e6f86ab28a5220fd95deaba2439703cc33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e617943bcc290e76b6742b6ac197cb1cdc94a354c4bf3c6fc01eb9eaaf0d301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0f08f17dd22e19d3337f41b3b2c7324d4499d2934064605e08331bad11b9b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cf7ea715ba366d99919d77a12bcc74a16ceabe7ccb0b944f6b2a12d421768e(
    value: typing.Optional[HdinsightSparkClusterRolesHeadNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d597def1051e9f1db4fd2c08e9dbf4863579e1042094b0a516342e282cc7f2(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346147891184fae2a06e31f5cfc46e5c76cd09e73c7ca9b2f15b3ae7e115cdfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52011945f255684c983980c95bdf82c6a1802d1b72e69b64d05e240c9c5c8dd2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795d0628836b54bc2c87c2b204d6a45099624958b6d378ca703a1e8188718f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ebb751acafd4210091f7a607ac3b964cbd3f1d4c4ed2f65e369e4b7ecc97a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810fbffe449bad3bb6ebfe7d5ed92ca889fa84ad1abbe065603d13c70bfa133f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe8dce7f8ea11247f2711525bb9ec141d30fb1f2eda205d3fe554866b81e655(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesHeadNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8227c80470d40bdb58d3c6c7de37083b5edfebc2bcf10b5571f6fdeb1a65a747(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fc803cf61d8554a7140d9078a4084068635557c7b1b959e9b524d2b1974a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac3577ecf89d26564835a743df0b7d3e2531fa4301524644ea69916422106f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999c3e719a6c6e7f917795843275bb9a70baca7b5cc8ddb54fd95b6fedf3c6c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60ab86b915f1b1b755b00c2492bccae289fd0420309d02854f109ed925b533f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesHeadNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1c877acf2a7be53efac673029cff86aeec15e3500772b16541be9d094b6b23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e95200902c008f09af945d6f77552a0a1a19831abf4ada01163cebc663526b(
    value: typing.Optional[HdinsightSparkClusterRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1002f0cd0ffe8395a4fe9d52450d084db146ebeaa2b3e69ff675a570a5ed7f(
    *,
    target_instance_count: jsii.Number,
    username: builtins.str,
    vm_size: builtins.str,
    autoscale: typing.Optional[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211cec0b4ae101c35c6c713534bc9d97920241235632af920b0b5d88042332de(
    *,
    capacity: typing.Optional[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    recurrence: typing.Optional[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd93db12b83ac6a5f672abe3c5357f865a69b0fa908a04c47f17c3d146ab3ac5(
    *,
    max_instance_count: jsii.Number,
    min_instance_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43ca81a7ffb08e41a87dbc97e3ce29d5aff2226706120077bfea2fa2f567100(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aef4ab0a7c2a6a27de4fe9d2960530ce7231092dda3d5ff07ada223ca94dff3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd80db45738d631b0baf118cef1fefff52197bbf729601dff49697eecb718ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3344c506da8e661741f9098f038fc7b17606f173e21b6f956eec44defbc86311(
    value: typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10be7f59e29b1d89b10c07a9da85efb93e48beb72f419379f90700b48949109(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0722c8fd2a4870fa902aa57af0379359346622c56450173efb1b630481c3d22b(
    value: typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541d6e892eb50f8923c966047eae2a078585a8b121574b57f81537be85ad86d5(
    *,
    schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]]],
    timezone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7910b47bf9817a724aa84ddcad042130df8baaa9f9377f61ddc4ecc3bd670d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ecfc10ed9167c7f5f01c2eacdfbb7ac5480f23a796d52abe3d07102ccb02e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d5191186428b1cf707b71894f33ca39ccdd032dad8e292310bcbdca974021d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce462ee5948a12aec74664e2df86ee69bae781a2d6a672287addb276258165ae(
    value: typing.Optional[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d7379da924b57b51445663efb0599f06bc48d9da9dbed435bd17ca699ee489(
    *,
    days: typing.Sequence[builtins.str],
    target_instance_count: jsii.Number,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21d026b30bc61925b6c1cb9400a6ae96d4883e3ae2f0724496f76da70bd95d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca246b5da168c75c05b9ea2f42b6bb34536f825414a12b490333a68fc6b4e14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ae7a26f29581678e8f28a55d8f41e094afc7955eaa3ba5385c2f6b4588b43b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a74141d7959cdb635ea8fa074cb107bad5a0605706926d13443537b5855452(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3fbb9a8a7d9e4515cac0df55c7f747f80d5d4184ae23b15a2808114cb44613(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a4f02d775d694522e7a93b0d52e0baf8c5a1d8399c68218ae3536c849ffbd0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc61ed538f0bdd23f8b05e497cb2a5b129513cbc57192b8d18cd651828f732cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8754fc3abf4f99383bceeb38325ea301d274e10f888c39de263098efd5408c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e16e19209c957ab51582d6074a5406fded18aa74551edbb105d2f6858ce14c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b477a3111d32f61947271d3408a791604a86d67112bfed7e93d7b94cac9a88ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89a62730e805ffd3f2ad96a6f45be7202cb304306d88ec589f9a81208c0a2b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f359616f9c9f395c33c065b93243f8a6d44bca99f28459424f5d2c23960abfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32e71ef2b4973fcd466a9e0e9c366fefbf53c67c5443c61222cb55cd0059de5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f0f2286dadb41e93101bbdf03e51a534d63564e5405b08efcc97e9da1ab863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5577f43df7d620da9a6d375a9d23c9da9943dee4b05816ce2a1c3d9cf1771ed8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6a9c0ca795642816a67ac104fb6502aafce0eb88bf9709b33ae966c4451c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d704741377e63d4d00041eca9e58f79d2822e532957f2a6ecfd22c6dd408c0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba86575ae36e3ba0ece1c1edad6a1b701c574b376479da7aca05d4e09a7e743e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea574ea7f897560adde91d622126eafbc31716458c4ae0f2f1d91cd35bbb1002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f270077edf6a83912ba7872d403fa97b284fec40c620fc6f9d4c55abd0f654(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7f88d855b8d36b528d76367e2927859e36010d93bc2dfbc8189cab7822df5c(
    value: typing.Optional[HdinsightSparkClusterRolesWorkerNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3a862e64cc17cb9cf6dc17a2b116c88511e90bb85546c258421f7378227faf(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c0ed0fbb28cc67cb6b145a11f7d01c390bc48c93ef486efbf3f497df300064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64727c584148db595295c8a070ad5a43a78d01402e0de2280bc500c396bd556b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a0f5ab2c4b0d851f0994ee1559051a1cb58aa0809a9acc45f5074aa1e2cb2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9dc7c079f62e1447cc273a92250bfb35af5b1798ea7c74de63da02d2c793bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a1cf893798e25c32f44d5467f89105753e69c4c7274190d5e79e07b33f3a5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbbcb361194fb845af7f20694a7f20a9c702d9f33bb72e4c24be602fac6dc3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesWorkerNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf306ed280e1aafde8b5322271910a7b48d315ac46beeb9c7db0c5ace2ec8fa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8676d9649786b9523c393274fd67789866419b595f5c81bb697dfe2aa54f81f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50e6e444ce5cea7fa3caa1fb9f38158b449276f74a923c52c835145d8f67e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded643be996686cbf4a31f78dcb0d5f77b0887ae51b7f0c8cc75c94b367fca39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2497264fbb705aca75238264bb6fff46d36f92054c4a640947f7a677672ba8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesWorkerNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cce9f771b8e7d84ba2dbea4e5ff8821c8771b132d303996bf0191cdae29d6a0(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802059c7ee9460443c67753912bff94d628c9df3886cd374e1be0c055f263786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7026f39df94d757d9e54d90ff33607536242ab0b125f9fc5264a4617cfdb9171(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightSparkClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd8fdfc98033c3711083ed6d92311802e0f3c1f289a59f684e72e7bd6e8307f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2135c7037204a7a416e0684cd17df71957b4453202262b2bc3dcb262f5d08cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153dd47331bcb2cc67c4dc160d0b9f8dd6eef8d77f19a038054dc62b20290599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5781221fcab1e9b36d59e1bd55dc94529b411170a3dfdb7407bf7284f72a60a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9522aeee80a9cb5d6601527e0f0b15b3120cb92944e862a185628663f63ad450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4547467f0781930f630581b05e1ccaa26798701ea8ebad5c86dd5c8d852f6ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285334e1768f188025252f57cc3666265525aa98e1bbd2f6f66c98e8e9ef7093(
    value: typing.Optional[HdinsightSparkClusterRolesZookeeperNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0515963d19164e1437511f03e712f416740b6df30c5bc854e10450239f82d82(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01a1039dbe43716a1406d4d65ccbdbb41ebab9f622ce5b4484d83ed7ffcc903(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc64991110fcedc30bce41b5e8f460424704f29505aaf7f93227e1d81ff2e73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f948a96a761125bc9007a30c1216b5818a0a1853a352aa36ba12079183991138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c60d40cf90f6b01d797ce12040758d468f3e2f5d35785579c79d7521891e6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028139975f46d4af9e792cc72586dd3e9ee5cb8e74f2fba6cc710edbba3481de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fa497b06dea3d864743ca6ea24b801703b64b16de860e7ecd75a93d0055c1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterRolesZookeeperNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63850690280aee6a84c7f35bfddf40c21a037879202e017c35a3d95db1d79349(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70cf56631754fded0b5abcbf96851af4dcc25c9b3a2f09e3f283190de73a9aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ec8cddf76a54a72359fadc1ffef529bc279ba4c36f3d6ee7c060f2e7d9d181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f94bed446b74fd3894158293cf8d7ca40f77181e3b243881e2208335268dfa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5048d622a4e7b7b242f22b0709a305123baff8a9f10e02cc5f809d1a493bb0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterRolesZookeeperNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdb57d348d56c2bf3679c2cef3a3208fd3d0cde37701e61aa5f9e6ba428904d(
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

def _typecheckingstub__6a90fbb9e22425f93cc14899184e7ec79cf7d0b8a48ebf279741fb3821877703(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2182f8fbaf2e8ed6674b1ab2d1a38830d6fa18a26aefe965051aa7c608d63111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a00a9c6d3eed1d836af08173e6c8e124cdc676a28ec3bc8550a290dd64be8a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42acb8d1afb13e6e22313b5ea3a63e80d7b2f2ba68c6b325d7132656ab18ac87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60db4b4f4ed0d38fda45370ad31114f79f78bbf341a0dbe819771d8223d6305a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a50aead3262010ebdb8de3ecd0288090b3aedabba84d3c12da58dff23a07aae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83291ab9a9e6925b26ea0c78a985268e360ae6d4f9a2003b6ef4af67be210f62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f50d5f5ef9d166a6ddcbd36182f96fe46f2c91769b58ac926a4c3a7a3530968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc865d624e145f128347c62826c053f86c834fe73915742674a8e9fb9ee42630(
    value: typing.Optional[HdinsightSparkClusterSecurityProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93b8c760dbbb2771655551f17259c38d2fe841443e503b4637dac5296539f86(
    *,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_account_key: builtins.str,
    storage_container_id: builtins.str,
    storage_resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e50a2bcba0a64891043df9d2255e1a2cd0d7c349b3e8d04acb540af913b851(
    *,
    filesystem_id: builtins.str,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    managed_identity_resource_id: builtins.str,
    storage_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205e83d64500fd1cb6fff0e180d8a8a94dc0eb608ddeaa4f0fa9d0553b5cde17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4900bc22a74ac8eed54568301ec3bdef22ac9ed21271a2dcf2d837a47b8063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ac66da5b1461f6457267c51c482f94a06f96195af7e7a546665e431d19799c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1c8d809204c0f814c73223bf8abfd7e28827da77c5b573b88f23676bd34dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c30ba819d5ac3b993fd181b3de3061bfa7da04ab427974b4b5454bb4199c96b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c206f3bc0a573cc2e747c0367fb24671b171eba2aaae1253f3f0f59a77b36cc1(
    value: typing.Optional[HdinsightSparkClusterStorageAccountGen2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126a51990e131f85b66285c1ea8f1db3d4901fa290cb58091e61bb46a9a434dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600e90f3d0710e38576c72fc2458b47020de4582c859d211fdc9471a74b8875c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6676817636512bc25eea46a23cc38fcaf999f8bf58d9338a37ba74da325c5a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01aacf8e2f9ce6f245c761389ae7dd79da3388ba797b3ede90925fb6a7d1493(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9196f1b599d692dfcd42c070bf40a3499ae2d15975d3079d2addef291d304460(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ed654d18abaa0e3d4f28b21a42720be9554e3bb22300e077b23085001da31a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightSparkClusterStorageAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8163b6b9fe6aa350cc7c11814d43e80d8fee132778e49376c82ebb4b319ba1cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb436bd59e6661d3787241c04c6b76616fc156ec54ece4e8a47b37326d52de49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3fe80f3e5b2f160bcabd7ccd3ef14a616f84e4f6d5d4640f4bce9a70c798e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c11e944cdd788816331c0f2b0a058e98d6d2cf407644d47911bf2a317ab6b32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f277bd5da5aa1b9f23ce9b28eee035cf2cf3ef2e07a7b29a502f4e737c9ad69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff2c0d4af7acde929b8d1ff998697dcf71dded5e200463382cc0340a555b96b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterStorageAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febee11f2e133667373da475e079c648db64be88d65d0ecca9c8bf644ee6d965(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b73c4bfd6191e16bea5558c23a12995f9caca8d59f395240357e8dcff76418(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c976ec2ab04ba89b82c2f63cf915a7e5f15e6538efddf93a67a85cc9ea2af2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9090e82713a00af0bcd3f80d6bdbf5fd24e519c33a0fe345d611a75db31d9d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e18466223417cc85c095f6fea6e620559b359afb5fe40cfeeae44617e06abc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88fd8c10958a91bd68e0cb59addf74ff6b6f3a95c320ef649792ea974255fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd3e83960c68803f1a171cd1dafc642e3ef050001b6fdca023d1ce03ce7e20d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightSparkClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
