r'''
# `azurerm_hdinsight_hadoop_cluster`

Refer to the Terraform Registry for docs: [`azurerm_hdinsight_hadoop_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster).
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


class HdinsightHadoopCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster azurerm_hdinsight_hadoop_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_version: builtins.str,
        component_version: typing.Union["HdinsightHadoopClusterComponentVersion", typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightHadoopClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightHadoopClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union["HdinsightHadoopClusterComputeIsolation", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extension: typing.Optional[typing.Union["HdinsightHadoopClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightHadoopClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightHadoopClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightHadoopClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightHadoopClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightHadoopClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightHadoopClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightHadoopClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster azurerm_hdinsight_hadoop_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#cluster_version HdinsightHadoopCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#component_version HdinsightHadoopCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#gateway HdinsightHadoopCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#location HdinsightHadoopCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#resource_group_name HdinsightHadoopCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#roles HdinsightHadoopCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tier HdinsightHadoopCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#compute_isolation HdinsightHadoopCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#disk_encryption HdinsightHadoopCluster#disk_encryption}
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#extension HdinsightHadoopCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#id HdinsightHadoopCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#metastores HdinsightHadoopCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#monitor HdinsightHadoopCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#network HdinsightHadoopCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_link_configuration HdinsightHadoopCluster#private_link_configuration}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#security_profile HdinsightHadoopCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account HdinsightHadoopCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account_gen2 HdinsightHadoopCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tags HdinsightHadoopCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#timeouts HdinsightHadoopCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tls_min_version HdinsightHadoopCluster#tls_min_version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af73de75d9e157dc9d82edd3cf90367b49505d1d734e5161c03e7f19a0fc5813)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HdinsightHadoopClusterConfig(
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
        '''Generates CDKTF code for importing a HdinsightHadoopCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HdinsightHadoopCluster to import.
        :param import_from_id: The id of the existing HdinsightHadoopCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HdinsightHadoopCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4780b6ebf9fbfff27e6785ce270080b6dc7a6a5649b746c6cfc0aca6aa9acd4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComponentVersion")
    def put_component_version(self, *, hadoop: builtins.str) -> None:
        '''
        :param hadoop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#hadoop HdinsightHadoopCluster#hadoop}.
        '''
        value = HdinsightHadoopClusterComponentVersion(hadoop=hadoop)

        return typing.cast(None, jsii.invoke(self, "putComponentVersion", [value]))

    @jsii.member(jsii_name="putComputeIsolation")
    def put_compute_isolation(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#compute_isolation_enabled HdinsightHadoopCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#host_sku HdinsightHadoopCluster#host_sku}.
        '''
        value = HdinsightHadoopClusterComputeIsolation(
            compute_isolation_enabled=compute_isolation_enabled, host_sku=host_sku
        )

        return typing.cast(None, jsii.invoke(self, "putComputeIsolation", [value]))

    @jsii.member(jsii_name="putDiskEncryption")
    def put_disk_encryption(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96dc21decc9fb62a14070b4faccb54724cc4347cd31516fb7caad2edf95a3c6)
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
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#log_analytics_workspace_id HdinsightHadoopCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary_key HdinsightHadoopCluster#primary_key}.
        '''
        value = HdinsightHadoopClusterExtension(
            log_analytics_workspace_id=log_analytics_workspace_id,
            primary_key=primary_key,
        )

        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putGateway")
    def put_gateway(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        value = HdinsightHadoopClusterGateway(password=password, username=username)

        return typing.cast(None, jsii.invoke(self, "putGateway", [value]))

    @jsii.member(jsii_name="putMetastores")
    def put_metastores(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightHadoopClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightHadoopClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightHadoopClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ambari HdinsightHadoopCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#hive HdinsightHadoopCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#oozie HdinsightHadoopCluster#oozie}
        '''
        value = HdinsightHadoopClusterMetastores(ambari=ambari, hive=hive, oozie=oozie)

        return typing.cast(None, jsii.invoke(self, "putMetastores", [value]))

    @jsii.member(jsii_name="putMonitor")
    def put_monitor(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#log_analytics_workspace_id HdinsightHadoopCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary_key HdinsightHadoopCluster#primary_key}.
        '''
        value = HdinsightHadoopClusterMonitor(
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
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#connection_direction HdinsightHadoopCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_link_enabled HdinsightHadoopCluster#private_link_enabled}.
        '''
        value = HdinsightHadoopClusterNetwork(
            connection_direction=connection_direction,
            private_link_enabled=private_link_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putPrivateLinkConfiguration")
    def put_private_link_configuration(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#group_id HdinsightHadoopCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ip_configuration HdinsightHadoopCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        '''
        value = HdinsightHadoopClusterPrivateLinkConfiguration(
            group_id=group_id, ip_configuration=ip_configuration, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateLinkConfiguration", [value]))

    @jsii.member(jsii_name="putRoles")
    def put_roles(
        self,
        *,
        head_node: typing.Union["HdinsightHadoopClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightHadoopClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightHadoopClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
        edge_node: typing.Optional[typing.Union["HdinsightHadoopClusterRolesEdgeNode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#head_node HdinsightHadoopCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#worker_node HdinsightHadoopCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#zookeeper_node HdinsightHadoopCluster#zookeeper_node}
        :param edge_node: edge_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#edge_node HdinsightHadoopCluster#edge_node}
        '''
        value = HdinsightHadoopClusterRoles(
            head_node=head_node,
            worker_node=worker_node,
            zookeeper_node=zookeeper_node,
            edge_node=edge_node,
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
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#aadds_resource_id HdinsightHadoopCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_name HdinsightHadoopCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_username HdinsightHadoopCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_user_password HdinsightHadoopCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ldaps_urls HdinsightHadoopCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#msi_resource_id HdinsightHadoopCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#cluster_users_group_dns HdinsightHadoopCluster#cluster_users_group_dns}.
        '''
        value = HdinsightHadoopClusterSecurityProfile(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4be0273e7910f76068225953bf85c99415cb8a359da54bc3bff64026fa8da48)
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
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#filesystem_id HdinsightHadoopCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#is_default HdinsightHadoopCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#managed_identity_resource_id HdinsightHadoopCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_resource_id HdinsightHadoopCluster#storage_resource_id}.
        '''
        value = HdinsightHadoopClusterStorageAccountGen2(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#create HdinsightHadoopCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#delete HdinsightHadoopCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#read HdinsightHadoopCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#update HdinsightHadoopCluster#update}.
        '''
        value = HdinsightHadoopClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetComputeIsolation")
    def reset_compute_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeIsolation", []))

    @jsii.member(jsii_name="resetDiskEncryption")
    def reset_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryption", []))

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
    ) -> "HdinsightHadoopClusterComponentVersionOutputReference":
        return typing.cast("HdinsightHadoopClusterComponentVersionOutputReference", jsii.get(self, "componentVersion"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolation")
    def compute_isolation(
        self,
    ) -> "HdinsightHadoopClusterComputeIsolationOutputReference":
        return typing.cast("HdinsightHadoopClusterComputeIsolationOutputReference", jsii.get(self, "computeIsolation"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> "HdinsightHadoopClusterDiskEncryptionList":
        return typing.cast("HdinsightHadoopClusterDiskEncryptionList", jsii.get(self, "diskEncryption"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> "HdinsightHadoopClusterExtensionOutputReference":
        return typing.cast("HdinsightHadoopClusterExtensionOutputReference", jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> "HdinsightHadoopClusterGatewayOutputReference":
        return typing.cast("HdinsightHadoopClusterGatewayOutputReference", jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="httpsEndpoint")
    def https_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="metastores")
    def metastores(self) -> "HdinsightHadoopClusterMetastoresOutputReference":
        return typing.cast("HdinsightHadoopClusterMetastoresOutputReference", jsii.get(self, "metastores"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> "HdinsightHadoopClusterMonitorOutputReference":
        return typing.cast("HdinsightHadoopClusterMonitorOutputReference", jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "HdinsightHadoopClusterNetworkOutputReference":
        return typing.cast("HdinsightHadoopClusterNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> "HdinsightHadoopClusterPrivateLinkConfigurationOutputReference":
        return typing.cast("HdinsightHadoopClusterPrivateLinkConfigurationOutputReference", jsii.get(self, "privateLinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> "HdinsightHadoopClusterRolesOutputReference":
        return typing.cast("HdinsightHadoopClusterRolesOutputReference", jsii.get(self, "roles"))

    @builtins.property
    @jsii.member(jsii_name="securityProfile")
    def security_profile(
        self,
    ) -> "HdinsightHadoopClusterSecurityProfileOutputReference":
        return typing.cast("HdinsightHadoopClusterSecurityProfileOutputReference", jsii.get(self, "securityProfile"))

    @builtins.property
    @jsii.member(jsii_name="sshEndpoint")
    def ssh_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "HdinsightHadoopClusterStorageAccountList":
        return typing.cast("HdinsightHadoopClusterStorageAccountList", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2")
    def storage_account_gen2(
        self,
    ) -> "HdinsightHadoopClusterStorageAccountGen2OutputReference":
        return typing.cast("HdinsightHadoopClusterStorageAccountGen2OutputReference", jsii.get(self, "storageAccountGen2"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HdinsightHadoopClusterTimeoutsOutputReference":
        return typing.cast("HdinsightHadoopClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="componentVersionInput")
    def component_version_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterComponentVersion"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterComponentVersion"], jsii.get(self, "componentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationInput")
    def compute_isolation_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterComputeIsolation"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterComputeIsolation"], jsii.get(self, "computeIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterDiskEncryption"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterDiskEncryption"]]], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(self) -> typing.Optional["HdinsightHadoopClusterExtension"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterExtension"], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional["HdinsightHadoopClusterGateway"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterGateway"], jsii.get(self, "gatewayInput"))

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
    def metastores_input(self) -> typing.Optional["HdinsightHadoopClusterMetastores"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterMetastores"], jsii.get(self, "metastoresInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional["HdinsightHadoopClusterMonitor"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterMonitor"], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["HdinsightHadoopClusterNetwork"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationInput")
    def private_link_configuration_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterPrivateLinkConfiguration"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterPrivateLinkConfiguration"], jsii.get(self, "privateLinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional["HdinsightHadoopClusterRoles"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterRoles"], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileInput")
    def security_profile_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterSecurityProfile"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterSecurityProfile"], jsii.get(self, "securityProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2Input")
    def storage_account_gen2_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterStorageAccountGen2"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterStorageAccountGen2"], jsii.get(self, "storageAccountGen2Input"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterStorageAccount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterStorageAccount"]]], jsii.get(self, "storageAccountInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightHadoopClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightHadoopClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__172431f7b8ab7458408fb44f28501d3498e8fbac22b33d406bd517cccd1db878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de3b8c30ef3acc708a16afdddb7bc53c294a1037adf8024f0b0e2f779ca0ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0b7d0f26386d8fd785b88d58c195c05c0ff58c906b24580c0649d7db378558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9da8615f773f22f9e6fca9eec7f40975b2b664c50e58645f6dcfadb9425e28c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cb11070a80e8c9438d7ef12f4771de10d0ecc34be03382d6a2ebd591e611db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7101267a85b098b3b7def3ed50544fa36015796bdfa46913a2deacc266698f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8005f408efdec4bcf791f6d1af4ee8b098cf47a2566123b7e7a8519ebace5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersion")
    def tls_min_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsMinVersion"))

    @tls_min_version.setter
    def tls_min_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916e513a06590c189febc79cdce98a1df4493d7ae93e478714d8664c0acbbbd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsMinVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterComponentVersion",
    jsii_struct_bases=[],
    name_mapping={"hadoop": "hadoop"},
)
class HdinsightHadoopClusterComponentVersion:
    def __init__(self, *, hadoop: builtins.str) -> None:
        '''
        :param hadoop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#hadoop HdinsightHadoopCluster#hadoop}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc54a2289e0960a12742150636b237646a074587ee41686ab0222a7bb92c791)
            check_type(argname="argument hadoop", value=hadoop, expected_type=type_hints["hadoop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hadoop": hadoop,
        }

    @builtins.property
    def hadoop(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#hadoop HdinsightHadoopCluster#hadoop}.'''
        result = self._values.get("hadoop")
        assert result is not None, "Required property 'hadoop' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterComponentVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterComponentVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterComponentVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e212ed90191ce745bad5d4dc4585def78e9689858340a06898c68e0b7f21d05f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hadoopInput")
    def hadoop_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hadoopInput"))

    @builtins.property
    @jsii.member(jsii_name="hadoop")
    def hadoop(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hadoop"))

    @hadoop.setter
    def hadoop(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc6b8732046da4bbc32f5f0c6a96ea4eb3c9a75766256ae39f140a7c2c6f0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hadoop", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterComponentVersion]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterComponentVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterComponentVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810ac478df1633006c7960411b40efde929a80494d5a67a6e7ec9f0064dd3bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterComputeIsolation",
    jsii_struct_bases=[],
    name_mapping={
        "compute_isolation_enabled": "computeIsolationEnabled",
        "host_sku": "hostSku",
    },
)
class HdinsightHadoopClusterComputeIsolation:
    def __init__(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#compute_isolation_enabled HdinsightHadoopCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#host_sku HdinsightHadoopCluster#host_sku}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7933e6ce26b38f456f562ba7ff4805c81fb658adf8ca5d0113b9cf55e703e4f1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#compute_isolation_enabled HdinsightHadoopCluster#compute_isolation_enabled}.'''
        result = self._values.get("compute_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#host_sku HdinsightHadoopCluster#host_sku}.'''
        result = self._values.get("host_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterComputeIsolation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterComputeIsolationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterComputeIsolationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d749f0f4d8886b007a05b26e93ce29a5786e69d2fc420cd2d5948ba40a59ba5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a30a0d47bf29909e0a2ced157ce46527319fafec185d7c138b8aa6584f00a268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostSku")
    def host_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostSku"))

    @host_sku.setter
    def host_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363488e63faea548859101a1b67f150046acc671245d45135d37d048402dbcd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterComputeIsolation]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterComputeIsolation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterComputeIsolation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52ddbda38a48c0df754e0ba062cf6bd38621a4d76ed57c0db4f6e26204fab6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterConfig",
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
    },
)
class HdinsightHadoopClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        component_version: typing.Union[HdinsightHadoopClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightHadoopClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightHadoopClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union[HdinsightHadoopClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extension: typing.Optional[typing.Union["HdinsightHadoopClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightHadoopClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightHadoopClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightHadoopClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightHadoopClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightHadoopClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightHadoopClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightHadoopClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#cluster_version HdinsightHadoopCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#component_version HdinsightHadoopCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#gateway HdinsightHadoopCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#location HdinsightHadoopCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#resource_group_name HdinsightHadoopCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#roles HdinsightHadoopCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tier HdinsightHadoopCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#compute_isolation HdinsightHadoopCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#disk_encryption HdinsightHadoopCluster#disk_encryption}
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#extension HdinsightHadoopCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#id HdinsightHadoopCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#metastores HdinsightHadoopCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#monitor HdinsightHadoopCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#network HdinsightHadoopCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_link_configuration HdinsightHadoopCluster#private_link_configuration}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#security_profile HdinsightHadoopCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account HdinsightHadoopCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account_gen2 HdinsightHadoopCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tags HdinsightHadoopCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#timeouts HdinsightHadoopCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tls_min_version HdinsightHadoopCluster#tls_min_version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(component_version, dict):
            component_version = HdinsightHadoopClusterComponentVersion(**component_version)
        if isinstance(gateway, dict):
            gateway = HdinsightHadoopClusterGateway(**gateway)
        if isinstance(roles, dict):
            roles = HdinsightHadoopClusterRoles(**roles)
        if isinstance(compute_isolation, dict):
            compute_isolation = HdinsightHadoopClusterComputeIsolation(**compute_isolation)
        if isinstance(extension, dict):
            extension = HdinsightHadoopClusterExtension(**extension)
        if isinstance(metastores, dict):
            metastores = HdinsightHadoopClusterMetastores(**metastores)
        if isinstance(monitor, dict):
            monitor = HdinsightHadoopClusterMonitor(**monitor)
        if isinstance(network, dict):
            network = HdinsightHadoopClusterNetwork(**network)
        if isinstance(private_link_configuration, dict):
            private_link_configuration = HdinsightHadoopClusterPrivateLinkConfiguration(**private_link_configuration)
        if isinstance(security_profile, dict):
            security_profile = HdinsightHadoopClusterSecurityProfile(**security_profile)
        if isinstance(storage_account_gen2, dict):
            storage_account_gen2 = HdinsightHadoopClusterStorageAccountGen2(**storage_account_gen2)
        if isinstance(timeouts, dict):
            timeouts = HdinsightHadoopClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ab2667c5d2d43baf1bb127e48d1c4dd98546e20c05c8d90d7f0f790c505f36)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#cluster_version HdinsightHadoopCluster#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def component_version(self) -> HdinsightHadoopClusterComponentVersion:
        '''component_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#component_version HdinsightHadoopCluster#component_version}
        '''
        result = self._values.get("component_version")
        assert result is not None, "Required property 'component_version' is missing"
        return typing.cast(HdinsightHadoopClusterComponentVersion, result)

    @builtins.property
    def gateway(self) -> "HdinsightHadoopClusterGateway":
        '''gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#gateway HdinsightHadoopCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast("HdinsightHadoopClusterGateway", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#location HdinsightHadoopCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#resource_group_name HdinsightHadoopCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> "HdinsightHadoopClusterRoles":
        '''roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#roles HdinsightHadoopCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast("HdinsightHadoopClusterRoles", result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tier HdinsightHadoopCluster#tier}.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_isolation(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterComputeIsolation]:
        '''compute_isolation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#compute_isolation HdinsightHadoopCluster#compute_isolation}
        '''
        result = self._values.get("compute_isolation")
        return typing.cast(typing.Optional[HdinsightHadoopClusterComputeIsolation], result)

    @builtins.property
    def disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterDiskEncryption"]]]:
        '''disk_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#disk_encryption HdinsightHadoopCluster#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterDiskEncryption"]]], result)

    @builtins.property
    def extension(self) -> typing.Optional["HdinsightHadoopClusterExtension"]:
        '''extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#extension HdinsightHadoopCluster#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional["HdinsightHadoopClusterExtension"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#id HdinsightHadoopCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastores(self) -> typing.Optional["HdinsightHadoopClusterMetastores"]:
        '''metastores block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#metastores HdinsightHadoopCluster#metastores}
        '''
        result = self._values.get("metastores")
        return typing.cast(typing.Optional["HdinsightHadoopClusterMetastores"], result)

    @builtins.property
    def monitor(self) -> typing.Optional["HdinsightHadoopClusterMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#monitor HdinsightHadoopCluster#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["HdinsightHadoopClusterMonitor"], result)

    @builtins.property
    def network(self) -> typing.Optional["HdinsightHadoopClusterNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#network HdinsightHadoopCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["HdinsightHadoopClusterNetwork"], result)

    @builtins.property
    def private_link_configuration(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterPrivateLinkConfiguration"]:
        '''private_link_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_link_configuration HdinsightHadoopCluster#private_link_configuration}
        '''
        result = self._values.get("private_link_configuration")
        return typing.cast(typing.Optional["HdinsightHadoopClusterPrivateLinkConfiguration"], result)

    @builtins.property
    def security_profile(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterSecurityProfile"]:
        '''security_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#security_profile HdinsightHadoopCluster#security_profile}
        '''
        result = self._values.get("security_profile")
        return typing.cast(typing.Optional["HdinsightHadoopClusterSecurityProfile"], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterStorageAccount"]]]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account HdinsightHadoopCluster#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterStorageAccount"]]], result)

    @builtins.property
    def storage_account_gen2(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterStorageAccountGen2"]:
        '''storage_account_gen2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account_gen2 HdinsightHadoopCluster#storage_account_gen2}
        '''
        result = self._values.get("storage_account_gen2")
        return typing.cast(typing.Optional["HdinsightHadoopClusterStorageAccountGen2"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tags HdinsightHadoopCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HdinsightHadoopClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#timeouts HdinsightHadoopCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HdinsightHadoopClusterTimeouts"], result)

    @builtins.property
    def tls_min_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#tls_min_version HdinsightHadoopCluster#tls_min_version}.'''
        result = self._values.get("tls_min_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterDiskEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_algorithm": "encryptionAlgorithm",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
        "key_vault_key_id": "keyVaultKeyId",
        "key_vault_managed_identity_id": "keyVaultManagedIdentityId",
    },
)
class HdinsightHadoopClusterDiskEncryption:
    def __init__(
        self,
        *,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#encryption_algorithm HdinsightHadoopCluster#encryption_algorithm}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#encryption_at_host_enabled HdinsightHadoopCluster#encryption_at_host_enabled}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#key_vault_key_id HdinsightHadoopCluster#key_vault_key_id}.
        :param key_vault_managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#key_vault_managed_identity_id HdinsightHadoopCluster#key_vault_managed_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23cdaf2dae896a2e4c2a885ea70bf79a2bb4f64ec3742fff8fe2374f1a8ebe85)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#encryption_algorithm HdinsightHadoopCluster#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#encryption_at_host_enabled HdinsightHadoopCluster#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#key_vault_key_id HdinsightHadoopCluster#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_managed_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#key_vault_managed_identity_id HdinsightHadoopCluster#key_vault_managed_identity_id}.'''
        result = self._values.get("key_vault_managed_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterDiskEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterDiskEncryptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterDiskEncryptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b281654fa274f994c939dc3077966f56534db001bdd88a29ee6917de7e4ec92e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterDiskEncryptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc1b386a5ac5394b5004a5189fea90e273f1e6af0f91a7a85e29bc4a1149bd3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterDiskEncryptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bc6bfad6f537c7cdc045775b07127ceb24ea48aa44d2298089788fc9f72f52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e78a25cf9952acc39cf22555abbeab5b81fc3646e5e6b49b12dd2c2bb103bff6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62436e63e753ac9af76b7e147d32ebd0147bf32d7c699370ed7896fe3300e6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterDiskEncryption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterDiskEncryption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterDiskEncryption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8fd663fdeae7d61616d1532f5f123283a584f18350890033e3b271b09de2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterDiskEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterDiskEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88e432f84cf9cb567008b28d0158cce7c9a36adf83374aaf5a5b8a1053e60f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7bb65e02fa0eaa844a2c66d73e58cefa42ea65778ba0cfd968c250ffffd8198)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d21578786800fd87684b87fc85dabbe32f9a8d06cd7b50d6daccf31d4cfcda1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cbdf405c976ece92657afc2b7e46f0f2ce036881f592a698c00acc1fef1ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultManagedIdentityId")
    def key_vault_managed_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultManagedIdentityId"))

    @key_vault_managed_identity_id.setter
    def key_vault_managed_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304314d5250ca1f20f93f5904e51f8fdc4bef470dcf60e86c5e47d7a1fa00e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultManagedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterDiskEncryption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterDiskEncryption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterDiskEncryption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635a399df202c48617fd601e6860dbd98e0c9a43d72d1f8835eded34245ff620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterExtension",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightHadoopClusterExtension:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#log_analytics_workspace_id HdinsightHadoopCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary_key HdinsightHadoopCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89589dfc7000198ee7b451d59742bdf742cb12cd2068c6d5ff76f5e72b7551ec)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#log_analytics_workspace_id HdinsightHadoopCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary_key HdinsightHadoopCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb1779ad90492b0ec45e3285277e47d404acf7678d17a19590fd1e4e1ce2096)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d193ea5415cd979356472d1bc7bc43bb4767ca5f373130ef7b8faeb7ed98b0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fa9a488fc31a4aa6b35110203aa15d4ea8af9d4c4027f74dac0de0d3fbc634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterExtension]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterExtension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterExtension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e08737eedc92aea9d953e6a5cce3ea46c3b125aa1fd0600e5d97d1fc5d47cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterGateway",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class HdinsightHadoopClusterGateway:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__890827897343e91f51ad69ed7f7e2b94610d8ea01d6923b4ab281abf206b74e7)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa668b1349c4ab500e428b8896dc0dd973bbd2a5f86e93bd45f14ca378e54893)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1869de0dc665919ad53f9b8e23c9943d9efc2c0e3c4a33028f74304c2be8b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a30137365c8977db4b580dbc7c62ec19de2558348dd0b2238069ad9710d18a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterGateway]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f7a16bd28bbf25c33b9b7c6947646cd94ad0e9d87e1285eaceb89abd89296a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastores",
    jsii_struct_bases=[],
    name_mapping={"ambari": "ambari", "hive": "hive", "oozie": "oozie"},
)
class HdinsightHadoopClusterMetastores:
    def __init__(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightHadoopClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightHadoopClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightHadoopClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ambari HdinsightHadoopCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#hive HdinsightHadoopCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#oozie HdinsightHadoopCluster#oozie}
        '''
        if isinstance(ambari, dict):
            ambari = HdinsightHadoopClusterMetastoresAmbari(**ambari)
        if isinstance(hive, dict):
            hive = HdinsightHadoopClusterMetastoresHive(**hive)
        if isinstance(oozie, dict):
            oozie = HdinsightHadoopClusterMetastoresOozie(**oozie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3bc923d1292cd4c8c31ee8dfe5f4a5261d92eba503d42a3c1d8f4b8e89ddca)
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
    def ambari(self) -> typing.Optional["HdinsightHadoopClusterMetastoresAmbari"]:
        '''ambari block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ambari HdinsightHadoopCluster#ambari}
        '''
        result = self._values.get("ambari")
        return typing.cast(typing.Optional["HdinsightHadoopClusterMetastoresAmbari"], result)

    @builtins.property
    def hive(self) -> typing.Optional["HdinsightHadoopClusterMetastoresHive"]:
        '''hive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#hive HdinsightHadoopCluster#hive}
        '''
        result = self._values.get("hive")
        return typing.cast(typing.Optional["HdinsightHadoopClusterMetastoresHive"], result)

    @builtins.property
    def oozie(self) -> typing.Optional["HdinsightHadoopClusterMetastoresOozie"]:
        '''oozie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#oozie HdinsightHadoopCluster#oozie}
        '''
        result = self._values.get("oozie")
        return typing.cast(typing.Optional["HdinsightHadoopClusterMetastoresOozie"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterMetastores(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresAmbari",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightHadoopClusterMetastoresAmbari:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1d4e1bee3d603d48cb9bca6482c2af43a1dcddad451a94759f2fa5d598ff98)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterMetastoresAmbari(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterMetastoresAmbariOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresAmbariOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b426c19918a4c57d2fd3553f0a4345ba89ad8af16f32afd8f595bf26cdecdc96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb31fb70f21babd85160eee03892a972cc48189c8483ae02ff5b83fe6b19860f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef7458d8153e5c888402c3b94064bce52e3d6d9a05c9f5bf0191da337b63d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df7cc18e866f50d9ee7d2dd05926f55f58d258dac8b6a9482fd87b94c3bfccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e8db0c42f8ac1bbb26b7116d01b77fdc27a02ee8b89316af81f4209980fe08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastoresAmbari], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterMetastoresAmbari],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645dee054de2dd244a6995846d38cb84ebe7f089611ee3f95ef2f5f54f800b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresHive",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightHadoopClusterMetastoresHive:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6761d88aad418b24f9405186dd1e6e79539ce0f66672de120672401bbaee75e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterMetastoresHive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterMetastoresHiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresHiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97b17c44b654925fe5034b3c10e75c388b434eafbb5783573c535479292a9df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49ea62d245809d5c122043b89f8a8ae3436bf8003aa9ee53f4f765896a88eb2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7668e7798648258c9e45dfd47c3b94c0709363b633790c0480f98c9c74009042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a545e9bb439a551e8110cf10af10bbb66cb75f3e77802093df4b779db3dc73d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28376e3467837a09f8ed747b729e5719b938972aea183556b39bbcc03110c393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastoresHive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterMetastoresHive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37844f12d27bc34c0f0f6c9dc963aa605166214628eb5ada2184ad6162e04dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresOozie",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightHadoopClusterMetastoresOozie:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dfab906fbe51c111dd105006bd8ebb8c49ae860c04141ee6955fc547f2bd53)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterMetastoresOozie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterMetastoresOozieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresOozieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fef26b4738a458cfbbcce8d55f574b78dda1972b5b2c8a820717f633565ff80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bfff9d1a9e629def132adfcc064d7762d2bfdc5ddecb3ca99561b91974c2a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e782273eec25d49b7cc5a529cb3840cb66d6bc70763b783875bcecd133080bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1c7ae98fc5ce6f745e2ff40b01ec97a203a1212ded3afe1063eeb9281159e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f12a8abce494747052677864f214bb38c476dd206086bc445aebf34ab9c347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastoresOozie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterMetastoresOozie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb61d9e6919c342cb37924ba102b599192c759252ca2e6f479eba731bbedcc4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterMetastoresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMetastoresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d7b5281bb9051eac7f99aa5d926ac568bdcb4c36abed0b3ef17e1f024957490)
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        value = HdinsightHadoopClusterMetastoresAmbari(
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        value = HdinsightHadoopClusterMetastoresHive(
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#database_name HdinsightHadoopCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#server HdinsightHadoopCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        '''
        value = HdinsightHadoopClusterMetastoresOozie(
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
    def ambari(self) -> HdinsightHadoopClusterMetastoresAmbariOutputReference:
        return typing.cast(HdinsightHadoopClusterMetastoresAmbariOutputReference, jsii.get(self, "ambari"))

    @builtins.property
    @jsii.member(jsii_name="hive")
    def hive(self) -> HdinsightHadoopClusterMetastoresHiveOutputReference:
        return typing.cast(HdinsightHadoopClusterMetastoresHiveOutputReference, jsii.get(self, "hive"))

    @builtins.property
    @jsii.member(jsii_name="oozie")
    def oozie(self) -> HdinsightHadoopClusterMetastoresOozieOutputReference:
        return typing.cast(HdinsightHadoopClusterMetastoresOozieOutputReference, jsii.get(self, "oozie"))

    @builtins.property
    @jsii.member(jsii_name="ambariInput")
    def ambari_input(self) -> typing.Optional[HdinsightHadoopClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastoresAmbari], jsii.get(self, "ambariInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveInput")
    def hive_input(self) -> typing.Optional[HdinsightHadoopClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastoresHive], jsii.get(self, "hiveInput"))

    @builtins.property
    @jsii.member(jsii_name="oozieInput")
    def oozie_input(self) -> typing.Optional[HdinsightHadoopClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastoresOozie], jsii.get(self, "oozieInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterMetastores]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMetastores], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterMetastores],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776308bc33a78a3e8d261b63475a9f783a641e84b71989b7c5f38977fd392184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMonitor",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightHadoopClusterMonitor:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#log_analytics_workspace_id HdinsightHadoopCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary_key HdinsightHadoopCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3492f49603b03f67d1abb903bc1af99c6f3fb9c3633f14ff21773d7c79966a)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#log_analytics_workspace_id HdinsightHadoopCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary_key HdinsightHadoopCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterMonitorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__151f58ef5e5ab9b34152ea6a77c67ad6901ddb3d4ab2f866f295a4246eb2edb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6819d02746074a668e0c734ee12f706727b618a76735faff35c44188d14192d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a457677a61d7cfb5b1b11e7cfbca8b2c734f53605354cfa377efdc1c09ed77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterMonitor]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4efe123fec31ee8226ccfa4823b36e20eb49e5c8a0af692fddefc02f3b0a6ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "connection_direction": "connectionDirection",
        "private_link_enabled": "privateLinkEnabled",
    },
)
class HdinsightHadoopClusterNetwork:
    def __init__(
        self,
        *,
        connection_direction: typing.Optional[builtins.str] = None,
        private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#connection_direction HdinsightHadoopCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_link_enabled HdinsightHadoopCluster#private_link_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d382e69eb7b78894a0e49bab650e4076facf12fe412a9e620f599251a5b500e6)
            check_type(argname="argument connection_direction", value=connection_direction, expected_type=type_hints["connection_direction"])
            check_type(argname="argument private_link_enabled", value=private_link_enabled, expected_type=type_hints["private_link_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_direction is not None:
            self._values["connection_direction"] = connection_direction
        if private_link_enabled is not None:
            self._values["private_link_enabled"] = private_link_enabled

    @builtins.property
    def connection_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#connection_direction HdinsightHadoopCluster#connection_direction}.'''
        result = self._values.get("connection_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_link_enabled HdinsightHadoopCluster#private_link_enabled}.'''
        result = self._values.get("private_link_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ede7f94252c2f930d7a1f29c45a866dd9028f6fe97b91c19d1ae515e4d0c2aad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d808d59bf2d3ff6c53bf2370e7a5498837f65c627d083e04a71fca56c16c3167)
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
            type_hints = typing.get_type_hints(_typecheckingstub__374ba9f3b62d49fd88bf018bc4b8b4e9be4e1f4bd13e334c4ee8933747fbfa79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterNetwork]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec5e7d41c8d0ee0a744b40bf8d208f8a3857532a24318e0110a9d13515492a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterPrivateLinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "ip_configuration": "ipConfiguration",
        "name": "name",
    },
)
class HdinsightHadoopClusterPrivateLinkConfiguration:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#group_id HdinsightHadoopCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ip_configuration HdinsightHadoopCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        '''
        if isinstance(ip_configuration, dict):
            ip_configuration = HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration(**ip_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ddda831f614a2158e4ff8d594049b0ff206276c4347666f6b4ece747f91071)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#group_id HdinsightHadoopCluster#group_id}.'''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_configuration(
        self,
    ) -> "HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration":
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ip_configuration HdinsightHadoopCluster#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast("HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterPrivateLinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "primary": "primary",
        "private_ip_address": "privateIpAddress",
        "private_ip_allocation_method": "privateIpAllocationMethod",
        "subnet_id": "subnetId",
    },
)
class HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration:
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary HdinsightHadoopCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_address HdinsightHadoopCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_allocation_method HdinsightHadoopCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fcb2dfeddf5f1ad33cce66073d33e454387e46f4f45ab54a7574a701c66071)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary HdinsightHadoopCluster#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_address HdinsightHadoopCluster#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_allocation_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_allocation_method HdinsightHadoopCluster#private_ip_allocation_method}.'''
        result = self._values.get("private_ip_allocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterPrivateLinkConfigurationIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterPrivateLinkConfigurationIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce73cdd589eec68bccebf855785c431fa502ef671a50743912e079a33d0bb62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c588c87e872688ae74a295a998ef893c40a071fa3584acb4c841345694745b09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__528cdfa1112a30d791af00a7efca030ea7c6a762720374b7aa175a0666fcc566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ed91f61a3f1e3d1064ce60d6a7200461ec9d53b0eaebc3be1587cdafa57389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAllocationMethod")
    def private_ip_allocation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAllocationMethod"))

    @private_ip_allocation_method.setter
    def private_ip_allocation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c886abe52dad15c01caeb044e74246996ecb443af21ffc43a3f6b91352e4747c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAllocationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2630a4281f15156110e59251ba553384727ca6fcd7c975939c843721e6075891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7757469f09f54963be51908e39d52cf5dfe1add35b6a4494db968a1d766226df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterPrivateLinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterPrivateLinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b51c5eb2b4039c1ef99175300f102a0bc616412c1e6488c4e99ac377dc36c71)
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#primary HdinsightHadoopCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_address HdinsightHadoopCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_allocation_method HdinsightHadoopCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        '''
        value = HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration(
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
    ) -> HdinsightHadoopClusterPrivateLinkConfigurationIpConfigurationOutputReference:
        return typing.cast(HdinsightHadoopClusterPrivateLinkConfigurationIpConfigurationOutputReference, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "ipConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6bed3a8d02a476730e3f381cb745df284e6b043ff3ef1f513363eae3d1066403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06175acc3d460180f532ccf139649596e0977c936517ebb13d5fc95062f6a6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterPrivateLinkConfiguration]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterPrivateLinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterPrivateLinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a36e2e434c6f61596d91d2b0ac5f5ddc233d53d36ba4d71fed086e3454b253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRoles",
    jsii_struct_bases=[],
    name_mapping={
        "head_node": "headNode",
        "worker_node": "workerNode",
        "zookeeper_node": "zookeeperNode",
        "edge_node": "edgeNode",
    },
)
class HdinsightHadoopClusterRoles:
    def __init__(
        self,
        *,
        head_node: typing.Union["HdinsightHadoopClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightHadoopClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightHadoopClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
        edge_node: typing.Optional[typing.Union["HdinsightHadoopClusterRolesEdgeNode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#head_node HdinsightHadoopCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#worker_node HdinsightHadoopCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#zookeeper_node HdinsightHadoopCluster#zookeeper_node}
        :param edge_node: edge_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#edge_node HdinsightHadoopCluster#edge_node}
        '''
        if isinstance(head_node, dict):
            head_node = HdinsightHadoopClusterRolesHeadNode(**head_node)
        if isinstance(worker_node, dict):
            worker_node = HdinsightHadoopClusterRolesWorkerNode(**worker_node)
        if isinstance(zookeeper_node, dict):
            zookeeper_node = HdinsightHadoopClusterRolesZookeeperNode(**zookeeper_node)
        if isinstance(edge_node, dict):
            edge_node = HdinsightHadoopClusterRolesEdgeNode(**edge_node)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368b064e01289a8e9de72e20f3226a1806dc81e5a67646cfe7822a6c5a94d8a3)
            check_type(argname="argument head_node", value=head_node, expected_type=type_hints["head_node"])
            check_type(argname="argument worker_node", value=worker_node, expected_type=type_hints["worker_node"])
            check_type(argname="argument zookeeper_node", value=zookeeper_node, expected_type=type_hints["zookeeper_node"])
            check_type(argname="argument edge_node", value=edge_node, expected_type=type_hints["edge_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "head_node": head_node,
            "worker_node": worker_node,
            "zookeeper_node": zookeeper_node,
        }
        if edge_node is not None:
            self._values["edge_node"] = edge_node

    @builtins.property
    def head_node(self) -> "HdinsightHadoopClusterRolesHeadNode":
        '''head_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#head_node HdinsightHadoopCluster#head_node}
        '''
        result = self._values.get("head_node")
        assert result is not None, "Required property 'head_node' is missing"
        return typing.cast("HdinsightHadoopClusterRolesHeadNode", result)

    @builtins.property
    def worker_node(self) -> "HdinsightHadoopClusterRolesWorkerNode":
        '''worker_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#worker_node HdinsightHadoopCluster#worker_node}
        '''
        result = self._values.get("worker_node")
        assert result is not None, "Required property 'worker_node' is missing"
        return typing.cast("HdinsightHadoopClusterRolesWorkerNode", result)

    @builtins.property
    def zookeeper_node(self) -> "HdinsightHadoopClusterRolesZookeeperNode":
        '''zookeeper_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#zookeeper_node HdinsightHadoopCluster#zookeeper_node}
        '''
        result = self._values.get("zookeeper_node")
        assert result is not None, "Required property 'zookeeper_node' is missing"
        return typing.cast("HdinsightHadoopClusterRolesZookeeperNode", result)

    @builtins.property
    def edge_node(self) -> typing.Optional["HdinsightHadoopClusterRolesEdgeNode"]:
        '''edge_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#edge_node HdinsightHadoopCluster#edge_node}
        '''
        result = self._values.get("edge_node")
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesEdgeNode"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNode",
    jsii_struct_bases=[],
    name_mapping={
        "install_script_action": "installScriptAction",
        "target_instance_count": "targetInstanceCount",
        "vm_size": "vmSize",
        "https_endpoints": "httpsEndpoints",
        "uninstall_script_actions": "uninstallScriptActions",
    },
)
class HdinsightHadoopClusterRolesEdgeNode:
    def __init__(
        self,
        *,
        install_script_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction", typing.Dict[builtins.str, typing.Any]]]],
        target_instance_count: jsii.Number,
        vm_size: builtins.str,
        https_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        uninstall_script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param install_script_action: install_script_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#install_script_action HdinsightHadoopCluster#install_script_action}
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param https_endpoints: https_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#https_endpoints HdinsightHadoopCluster#https_endpoints}
        :param uninstall_script_actions: uninstall_script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uninstall_script_actions HdinsightHadoopCluster#uninstall_script_actions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e86eb4755c33d7d76c268802d41faaa1596f8e4d5b9014e084b2d3ea13a7d2)
            check_type(argname="argument install_script_action", value=install_script_action, expected_type=type_hints["install_script_action"])
            check_type(argname="argument target_instance_count", value=target_instance_count, expected_type=type_hints["target_instance_count"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument https_endpoints", value=https_endpoints, expected_type=type_hints["https_endpoints"])
            check_type(argname="argument uninstall_script_actions", value=uninstall_script_actions, expected_type=type_hints["uninstall_script_actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "install_script_action": install_script_action,
            "target_instance_count": target_instance_count,
            "vm_size": vm_size,
        }
        if https_endpoints is not None:
            self._values["https_endpoints"] = https_endpoints
        if uninstall_script_actions is not None:
            self._values["uninstall_script_actions"] = uninstall_script_actions

    @builtins.property
    def install_script_action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction"]]:
        '''install_script_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#install_script_action HdinsightHadoopCluster#install_script_action}
        '''
        result = self._values.get("install_script_action")
        assert result is not None, "Required property 'install_script_action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction"]], result)

    @builtins.property
    def target_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def https_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints"]]]:
        '''https_endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#https_endpoints HdinsightHadoopCluster#https_endpoints}
        '''
        result = self._values.get("https_endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints"]]], result)

    @builtins.property
    def uninstall_script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions"]]]:
        '''uninstall_script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uninstall_script_actions HdinsightHadoopCluster#uninstall_script_actions}
        '''
        result = self._values.get("uninstall_script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesEdgeNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints",
    jsii_struct_bases=[],
    name_mapping={
        "access_modes": "accessModes",
        "destination_port": "destinationPort",
        "disable_gateway_auth": "disableGatewayAuth",
        "private_ip_address": "privateIpAddress",
        "sub_domain_suffix": "subDomainSuffix",
    },
)
class HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints:
    def __init__(
        self,
        *,
        access_modes: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination_port: typing.Optional[jsii.Number] = None,
        disable_gateway_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ip_address: typing.Optional[builtins.str] = None,
        sub_domain_suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_modes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#access_modes HdinsightHadoopCluster#access_modes}.
        :param destination_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#destination_port HdinsightHadoopCluster#destination_port}.
        :param disable_gateway_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#disable_gateway_auth HdinsightHadoopCluster#disable_gateway_auth}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_address HdinsightHadoopCluster#private_ip_address}.
        :param sub_domain_suffix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#sub_domain_suffix HdinsightHadoopCluster#sub_domain_suffix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a514458060c6751d45147c6131ed3fea471eb44e9d486efd7da3199df2d951)
            check_type(argname="argument access_modes", value=access_modes, expected_type=type_hints["access_modes"])
            check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
            check_type(argname="argument disable_gateway_auth", value=disable_gateway_auth, expected_type=type_hints["disable_gateway_auth"])
            check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
            check_type(argname="argument sub_domain_suffix", value=sub_domain_suffix, expected_type=type_hints["sub_domain_suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_modes is not None:
            self._values["access_modes"] = access_modes
        if destination_port is not None:
            self._values["destination_port"] = destination_port
        if disable_gateway_auth is not None:
            self._values["disable_gateway_auth"] = disable_gateway_auth
        if private_ip_address is not None:
            self._values["private_ip_address"] = private_ip_address
        if sub_domain_suffix is not None:
            self._values["sub_domain_suffix"] = sub_domain_suffix

    @builtins.property
    def access_modes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#access_modes HdinsightHadoopCluster#access_modes}.'''
        result = self._values.get("access_modes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destination_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#destination_port HdinsightHadoopCluster#destination_port}.'''
        result = self._values.get("destination_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disable_gateway_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#disable_gateway_auth HdinsightHadoopCluster#disable_gateway_auth}.'''
        result = self._values.get("disable_gateway_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#private_ip_address HdinsightHadoopCluster#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sub_domain_suffix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#sub_domain_suffix HdinsightHadoopCluster#sub_domain_suffix}.'''
        result = self._values.get("sub_domain_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a752e9dd304b7f6b10d668249f462cf78db1f506fa167c99356be9c9409af725)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a29b15e71856d8f29552e168cbadccd25923062c3439c6f16987704b70bdca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1da4aa7ab874190a79195b9e4c8340407fa441a7e761e734e31bec6667cb05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d78322162a963a7ab6932cdbfcf4136ed128867d18015d5ee6262c9cd95b73fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2777d365b0969c836a2bff5886448f963e0d9df4c0eae5f4706d3f634fe129f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8729fa16794d6e7269bcfff28e11d74963268cf88926800e11c817cd1e0e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__826242784e92c67ce5e4b9eda52fbef202bb21526dff12a58928039a9fa23e66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessModes")
    def reset_access_modes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessModes", []))

    @jsii.member(jsii_name="resetDestinationPort")
    def reset_destination_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPort", []))

    @jsii.member(jsii_name="resetDisableGatewayAuth")
    def reset_disable_gateway_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableGatewayAuth", []))

    @jsii.member(jsii_name="resetPrivateIpAddress")
    def reset_private_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpAddress", []))

    @jsii.member(jsii_name="resetSubDomainSuffix")
    def reset_sub_domain_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubDomainSuffix", []))

    @builtins.property
    @jsii.member(jsii_name="accessModesInput")
    def access_modes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessModesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPortInput")
    def destination_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "destinationPortInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGatewayAuthInput")
    def disable_gateway_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableGatewayAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddressInput")
    def private_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="subDomainSuffixInput")
    def sub_domain_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subDomainSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="accessModes")
    def access_modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessModes"))

    @access_modes.setter
    def access_modes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e344e11ddfe9a26d15b30e7f5b3d5af2036c534ee49f65cda15491bfd025418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessModes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationPort")
    def destination_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "destinationPort"))

    @destination_port.setter
    def destination_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74172018d090182c1abb922b000abe71846fd0ed65669d486ed567b36a4c8f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableGatewayAuth")
    def disable_gateway_auth(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableGatewayAuth"))

    @disable_gateway_auth.setter
    def disable_gateway_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647f9e1c48f0c00dbbe9e6fdbbc9373c2dd8f72b6c04dc6730f3c5b2bad87916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableGatewayAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a7a78aa647dfd613e526f4cfec0b25903b27555fcf17ca097c93fcc6b6c5d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subDomainSuffix")
    def sub_domain_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subDomainSuffix"))

    @sub_domain_suffix.setter
    def sub_domain_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f615aaafcf5fbe6dd718903654bc7ae8959ca826022571e7c61e38ab4e3b806a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subDomainSuffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24258c335b33b2b2b88a65992866c4a30bfe245337a4c8978215113bd4e729a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb0f7d7c872f96301d8afb946bce63477dd73daad81302ddfc95cb10e641ec2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dde04b90070fbeabf88b123ebdb403a0fc4224c6b1cefb2c48cc28640c707e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233e3a08824693287bad16ebb81603c9b369bc8853a10c41b366072189057135)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795145102bc27ef0a301bfc85ec21e73ed2147927aa364bed8b693c4ab153cc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95cf18b2248c67834c3c41dc4b0231c246c5d8e2c935b77c94f78db0757faf1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bfaf4a17df20b4081810034c87a594845c8500af7e2a5eef766bf12d0a55fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1094251178d25c0114e158470bb108a00feb229e221c018a3d39dc892dbae55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__143e338a60d487ba13c04af93dcb5b04e269a09392cdd8ba9b408760488de3c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fcfbd05d229c75103d3d7b22e6b5a17833837e4e72a8431d1b46a1882442291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a49edd3cdecab731d46b312e79b8497f74acf20e0519f8a4c11d606ce51d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ed6f444b6f583b0ab83c9168924d4240d31c9b91f10bb697660c344c43e1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d8bb3a7f598b4c69162af6c3070bc8cc3b792bfbf63516c3e1f4d86e15c69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesEdgeNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a6a9f6049121e0b244ee6b093c4302e9b23bde72592cf2e5e5568f6d3c60ac3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpsEndpoints")
    def put_https_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f247d81f0c80a75e7527d2e5441f8a1f1ae7fa9d494992ce7bdfb23c6dd4af14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpsEndpoints", [value]))

    @jsii.member(jsii_name="putInstallScriptAction")
    def put_install_script_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222563f8f735dfae2b79909aa0f60bcb5086a14cdccca568d2238ee3e2bca234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstallScriptAction", [value]))

    @jsii.member(jsii_name="putUninstallScriptActions")
    def put_uninstall_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9895a282e1d90138c5da8ab0e053d1adf4d0c01929f7e66a92c6e7a45106e02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUninstallScriptActions", [value]))

    @jsii.member(jsii_name="resetHttpsEndpoints")
    def reset_https_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsEndpoints", []))

    @jsii.member(jsii_name="resetUninstallScriptActions")
    def reset_uninstall_script_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUninstallScriptActions", []))

    @builtins.property
    @jsii.member(jsii_name="httpsEndpoints")
    def https_endpoints(self) -> HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsList:
        return typing.cast(HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsList, jsii.get(self, "httpsEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="installScriptAction")
    def install_script_action(
        self,
    ) -> HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionList:
        return typing.cast(HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionList, jsii.get(self, "installScriptAction"))

    @builtins.property
    @jsii.member(jsii_name="uninstallScriptActions")
    def uninstall_script_actions(
        self,
    ) -> "HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsList":
        return typing.cast("HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsList", jsii.get(self, "uninstallScriptActions"))

    @builtins.property
    @jsii.member(jsii_name="httpsEndpointsInput")
    def https_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]], jsii.get(self, "httpsEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="installScriptActionInput")
    def install_script_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]], jsii.get(self, "installScriptActionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCountInput")
    def target_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="uninstallScriptActionsInput")
    def uninstall_script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions"]]], jsii.get(self, "uninstallScriptActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8dced5d564deeeefddec17eabc68802b02376e9d83c27cb8e25e671c1593805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930588d21737651ad4ffc6b974fb419baa8c40feb5527d59418fa9b70ec0e21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterRolesEdgeNode]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesEdgeNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesEdgeNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f45478e5fe7e0d56d93d6dee69e606dce308bc15cda4f7cf109420a1e510476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0684d5777e249120595888e23e47c143640794a29b66dfb466c086c38c76ed)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3822a7ceffcd5f2634cb0a8280eb474ec382bbed6109873c01296df0cf90a2ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d651ea3569011bfcdc04d8d5894e1fb9f553c80fae48d5d18d0ef40204e1d9a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8bba4310cc169a0a662ae3561c98eaca522efb5c814f47a1fa4e442d8edd1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd22f09801f04b44bf2586650086714cdf04603b91c56151c6afac1a9f49a041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54cbf0fa52ca35f8b9e562e362e8457cbc244f6765c1ac723ae56b6b0fdef1ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db67910275f46c908a0990b1ff00055e8b16773f2084cedab9326cadeafe0562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6237cda6d2f55895a9e07efec6b83aa74ed14ea640954f9bf5362df692afc08b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cabb5b6daacdbacbbe1fec889cc8e9447c5d9ec61af668e6ad31ff819b89baad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73052a67fd1709494c18c585ee97fa13bf419eff71c447b2780475e7743ddda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cc1bdfea8d82acb6eecabab4684d205f2873553868a9a1c9083957acdfac6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09f1f1d5a5e3c27711c6d66615e7f3b1089cedb0fa148ccb3ac577258a01f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesHeadNode",
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
class HdinsightHadoopClusterRolesHeadNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ae3fa923a08ef876574b9d1d48289e0234089d0a206a59ce4417dea42bc564)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesHeadNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesHeadNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesHeadNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesHeadNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesHeadNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ec03d45eaf7795bc2d7ca13ddbadc8a90e5a014386e2f1313f49a37528dd1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a0eac67273bb7faf446b2f798f889e535f3b81e196409af35616d55074af1b)
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
    def script_actions(self) -> "HdinsightHadoopClusterRolesHeadNodeScriptActionsList":
        return typing.cast("HdinsightHadoopClusterRolesHeadNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesHeadNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesHeadNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__90a53b241a94dac5d180218666fa1e0c81f9ef515e7e91e90d600070719fd00d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27e4f0a0828cb7089d2450a65dadd80246d44e63ce59e5bdc6b30259b7d4598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a5cd3b352fa06b19abeacb947b895f5d8905bf3497216ddca2c9e2492cbc85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814f17231ac080acde94a454e6cb9a5c6731351b1fbaba03fc50e6f97ca32853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b7f15d0fb9f44ae5dc0e366d51686d4086d1810e9fa977c270e7fe962d5ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d767022f035673931463b7396267149d7b771cfac9125292f2e179cc01e79b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesHeadNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesHeadNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4468023862029e997e666be4c744589ca1fcd12e94abddc7b157346d06090423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesHeadNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightHadoopClusterRolesHeadNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab69c0f9ba970477fd4c2e17dfec635f56e601fec14ad575901f3372d381a41)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesHeadNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesHeadNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesHeadNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d56b33f6b5c2a6ebd9a5f4a2ecce11c5842ba64230ef704cc4d24d30410cdd42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesHeadNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a4887e9ebbf3a717a2a9dfd8cf0f6e12b88f395c7e705f75623b165db2483d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesHeadNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c43d9b5aafb2cf992e2ec76b409a4db4ab9797f270b9cc93156fd625a7a29b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57da1c7286040fcbe6248b9b7165c09bfc5b05bab23077bd7d458359c38b7184)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ac94941b0810c6d2a0697474a3da79712269006e1218e98d2f381605e91489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesHeadNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesHeadNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesHeadNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98722a74abed427e69e47444e2fa31d397bbf16821798a6f6d7a6f92403e8ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesHeadNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesHeadNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d4f2c7895cdbb8bf73e5e8afc9d0b88689ab590dd8ee671777aee4e58f9018)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b89789da7144c11d94086f5d79e6effb0535b2a452156ea65009da7727dce87a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ac74618074e15101cd8504eb63962e99b91b27d12dde95a8226f1a3655fe8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80df5a5bc2e8a4f8ff8d42abb01b5b6e5fc90e1072228f61c7e5043f56b5a578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesHeadNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesHeadNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesHeadNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f4f00227c50cf087d24263ba99e94996b2080b546b581e6a79c80e31c36d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__286da027e20bf8f8cd83eb194e08b8b8ea9efa9c7e02803802404f49caec3e7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEdgeNode")
    def put_edge_node(
        self,
        *,
        install_script_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction, typing.Dict[builtins.str, typing.Any]]]],
        target_instance_count: jsii.Number,
        vm_size: builtins.str,
        https_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
        uninstall_script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param install_script_action: install_script_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#install_script_action HdinsightHadoopCluster#install_script_action}
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param https_endpoints: https_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#https_endpoints HdinsightHadoopCluster#https_endpoints}
        :param uninstall_script_actions: uninstall_script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uninstall_script_actions HdinsightHadoopCluster#uninstall_script_actions}
        '''
        value = HdinsightHadoopClusterRolesEdgeNode(
            install_script_action=install_script_action,
            target_instance_count=target_instance_count,
            vm_size=vm_size,
            https_endpoints=https_endpoints,
            uninstall_script_actions=uninstall_script_actions,
        )

        return typing.cast(None, jsii.invoke(self, "putEdgeNode", [value]))

    @jsii.member(jsii_name="putHeadNode")
    def put_head_node(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.
        '''
        value = HdinsightHadoopClusterRolesHeadNode(
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
        autoscale: typing.Optional[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#autoscale HdinsightHadoopCluster#autoscale}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.
        '''
        value = HdinsightHadoopClusterRolesWorkerNode(
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
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.
        '''
        value = HdinsightHadoopClusterRolesZookeeperNode(
            username=username,
            vm_size=vm_size,
            password=password,
            script_actions=script_actions,
            ssh_keys=ssh_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putZookeeperNode", [value]))

    @jsii.member(jsii_name="resetEdgeNode")
    def reset_edge_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeNode", []))

    @builtins.property
    @jsii.member(jsii_name="edgeNode")
    def edge_node(self) -> HdinsightHadoopClusterRolesEdgeNodeOutputReference:
        return typing.cast(HdinsightHadoopClusterRolesEdgeNodeOutputReference, jsii.get(self, "edgeNode"))

    @builtins.property
    @jsii.member(jsii_name="headNode")
    def head_node(self) -> HdinsightHadoopClusterRolesHeadNodeOutputReference:
        return typing.cast(HdinsightHadoopClusterRolesHeadNodeOutputReference, jsii.get(self, "headNode"))

    @builtins.property
    @jsii.member(jsii_name="workerNode")
    def worker_node(self) -> "HdinsightHadoopClusterRolesWorkerNodeOutputReference":
        return typing.cast("HdinsightHadoopClusterRolesWorkerNodeOutputReference", jsii.get(self, "workerNode"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNode")
    def zookeeper_node(
        self,
    ) -> "HdinsightHadoopClusterRolesZookeeperNodeOutputReference":
        return typing.cast("HdinsightHadoopClusterRolesZookeeperNodeOutputReference", jsii.get(self, "zookeeperNode"))

    @builtins.property
    @jsii.member(jsii_name="edgeNodeInput")
    def edge_node_input(self) -> typing.Optional[HdinsightHadoopClusterRolesEdgeNode]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesEdgeNode], jsii.get(self, "edgeNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="headNodeInput")
    def head_node_input(self) -> typing.Optional[HdinsightHadoopClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesHeadNode], jsii.get(self, "headNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="workerNodeInput")
    def worker_node_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterRolesWorkerNode"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesWorkerNode"], jsii.get(self, "workerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNodeInput")
    def zookeeper_node_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterRolesZookeeperNode"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesZookeeperNode"], jsii.get(self, "zookeeperNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterRoles]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7ef53b8c5974a0ebe4037c4cc7e0fe7206a80e68675379d55a3392c0e4c0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNode",
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
class HdinsightHadoopClusterRolesWorkerNode:
    def __init__(
        self,
        *,
        target_instance_count: jsii.Number,
        username: builtins.str,
        vm_size: builtins.str,
        autoscale: typing.Optional[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#autoscale HdinsightHadoopCluster#autoscale}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.
        '''
        if isinstance(autoscale, dict):
            autoscale = HdinsightHadoopClusterRolesWorkerNodeAutoscale(**autoscale)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264a35182c683e84db41dfbeb4304316b898ffa660f8d0904cb913a930dd9f82)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscale(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscale"]:
        '''autoscale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#autoscale HdinsightHadoopCluster#autoscale}
        '''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscale"], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesWorkerNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscale",
    jsii_struct_bases=[],
    name_mapping={"capacity": "capacity", "recurrence": "recurrence"},
)
class HdinsightHadoopClusterRolesWorkerNodeAutoscale:
    def __init__(
        self,
        *,
        capacity: typing.Optional[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        recurrence: typing.Optional[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#capacity HdinsightHadoopCluster#capacity}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#recurrence HdinsightHadoopCluster#recurrence}
        '''
        if isinstance(capacity, dict):
            capacity = HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity(**capacity)
        if isinstance(recurrence, dict):
            recurrence = HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a04357458df28b76a035d7b7794bcfda982ed6badc3248eecbb25cb930556a)
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
    ) -> typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity"]:
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#capacity HdinsightHadoopCluster#capacity}
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity"], result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#recurrence HdinsightHadoopCluster#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesWorkerNodeAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
    },
)
class HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity:
    def __init__(
        self,
        *,
        max_instance_count: jsii.Number,
        min_instance_count: jsii.Number,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#max_instance_count HdinsightHadoopCluster#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#min_instance_count HdinsightHadoopCluster#min_instance_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0507bd3b7316223b2be11556220deb9e4b94c21e9d077462ee3c71c710d807)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_instance_count": max_instance_count,
            "min_instance_count": min_instance_count,
        }

    @builtins.property
    def max_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#max_instance_count HdinsightHadoopCluster#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        assert result is not None, "Required property 'max_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#min_instance_count HdinsightHadoopCluster#min_instance_count}.'''
        result = self._values.get("min_instance_count")
        assert result is not None, "Required property 'min_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__228b5ac275b2f75456e104b47b0daed20d210f32bcc6e7ff079114bbab822e5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efc5ac23578a79cf036669bddd681fc4584d73a582332b449dc93bed22e1339d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9540c70cff0972e2e98c29ffb63a8c0bbb110ad8529ce1a611edecfff22daed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573d937204fc37dccb4777869af6482a653ad441c545a6c90b2068281eb3e27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesWorkerNodeAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06512d0e0074b01cf29de34d3f0f96cf37dfc7da0383dd874bb7e0ad913f19ee)
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
        :param max_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#max_instance_count HdinsightHadoopCluster#max_instance_count}.
        :param min_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#min_instance_count HdinsightHadoopCluster#min_instance_count}.
        '''
        value = HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
        )

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
        timezone: builtins.str,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#schedule HdinsightHadoopCluster#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#timezone HdinsightHadoopCluster#timezone}.
        '''
        value = HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence(
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
    ) -> HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacityOutputReference:
        return typing.cast(HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacityOutputReference, jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference":
        return typing.cast("HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence"]:
        return typing.cast(typing.Optional["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscale]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4050eacb6e86f19495d7856c667bf55c5e162e8cf46c189657e88c37bb8d8bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule", "timezone": "timezone"},
)
class HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence:
    def __init__(
        self,
        *,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
        timezone: builtins.str,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#schedule HdinsightHadoopCluster#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#timezone HdinsightHadoopCluster#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b41588b79c85d9e6d9ad3b2a4c7a762f5d57de9f3f5d44ae6fce4869b5e90f)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
            "timezone": timezone,
        }

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#schedule HdinsightHadoopCluster#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]], result)

    @builtins.property
    def timezone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#timezone HdinsightHadoopCluster#timezone}.'''
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b24037121377a6d43d743364fe44ac2651b199ef610a8ac8b2b0845eac415c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d1780e07ec8c5ac79fb09a3f4a5b1675b5e91054c0b56c3c4b1f27221ab1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList":
        return typing.cast("HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]], jsii.get(self, "scheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e07e24c99a4b28eadfc86d662d8446ed40ceef0d0aaf5b51fac12b45ecf02605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828e7d9f31aa3d4bc3747fa6c83a2d6fefb638925641b08e80aa5e716e4d38fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "days": "days",
        "target_instance_count": "targetInstanceCount",
        "time": "time",
    },
)
class HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule:
    def __init__(
        self,
        *,
        days: typing.Sequence[builtins.str],
        target_instance_count: jsii.Number,
        time: builtins.str,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#days HdinsightHadoopCluster#days}.
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#time HdinsightHadoopCluster#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329c445370d5ecf23dd9cfde78d23573707b8149ab6c300d44d1c56caf16e1a7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#days HdinsightHadoopCluster#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#target_instance_count HdinsightHadoopCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#time HdinsightHadoopCluster#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c247241a8e5acc00af8e77381c04f6300d93f0cb58d14feb49a5b47c078c7df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de34823358359ec3bc54b39e6bf3ffdeb524f55e0fe3f742e444798b59f02138)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b017907985046a10995dcc7df5570081e3497727ae373536c74ecc073ea824)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06c1b2cf5f669b3a97327e7f10aef8bfeffc0b6daa2af28119704c9bda06fff3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29137376122db41820d7f0bc75347032f643a5a07de38e13c100a13a4fab1f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6ee6afacaf4581e9b313a808d4a683b217313f2388f320901e33c7946544aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f7a9601689627e41772b9eb36c0361c7c98761ab9293c4f00d961ea278fd0a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb56768d014126b62eac68ffa4cce41b341af50c4d8b2d44781de2bb9279209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968d5d1dcf5981fdb8c617272d86cafef5dcc5ac98fda455910265c0b742fb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf4d49eb77d9991e5e86d45962637d80eab1f82f268dc49c9b779a4339269a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639d3852f54f0e9ee93d93d91f2a546a01c8422ec05fae44d67bfd58eb01b107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesWorkerNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c088d08a0ac43dbbdd13cc194c50b8cc29a6dda5d80a4e3483d74923619c7f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(
        self,
        *,
        capacity: typing.Optional[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
        recurrence: typing.Optional[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#capacity HdinsightHadoopCluster#capacity}
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#recurrence HdinsightHadoopCluster#recurrence}
        '''
        value = HdinsightHadoopClusterRolesWorkerNodeAutoscale(
            capacity=capacity, recurrence=recurrence
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82a3f36d2ef100ccad02a11b6e47ec3522efccd60cd9c8c0475bca49a625f92)
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
    def autoscale(
        self,
    ) -> HdinsightHadoopClusterRolesWorkerNodeAutoscaleOutputReference:
        return typing.cast(HdinsightHadoopClusterRolesWorkerNodeAutoscaleOutputReference, jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(
        self,
    ) -> "HdinsightHadoopClusterRolesWorkerNodeScriptActionsList":
        return typing.cast("HdinsightHadoopClusterRolesWorkerNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscale]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscale], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesWorkerNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__46f5ee33bd0976de6ed688a3548b950f12de48e952aaf48f0eb6d5e7cb21e42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ddf7ca5ae97d720865aa88ef52b32f90500041c4fc518bad6f66e8998d9316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25aaf98519581dffc454c2cee118bace3e77adbb4078fbe12bc51a8aeae9ce56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb9751052e48a85f9c15f9379509ed44871ff7b86b3837a21ce2dab805e87ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48001f8170bae91756a3020a9f31c43306a5cc0de58c105d91335cd91dc128d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a253f719509621b58f4550176c4b2899054f43c909d887573eba07761ba7cd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3bf4707423d64cb108e9c45158bf1f869c5ee528927ca279b87b8463ff8b1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterRolesWorkerNode]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesWorkerNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesWorkerNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6300813b20e1e7d942a914eccdb55dbade2fcf59c51e82f5e3e4fea1102db42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightHadoopClusterRolesWorkerNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3092f642f74354016e00042ca87a3d8ddad79828ba7432288cf8a5071f9c576)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesWorkerNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesWorkerNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a3c65c6200299b3af8dccd8bae13014fa33231fc498fedfbc3f5b5e340d3e08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesWorkerNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ce620d33fef753cbf9ac9048ef4300d7bac4c649d6755e5e83adda47ecd9b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesWorkerNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c936e268803e59766cc63773318bf26a3fef3cd75d77299e9fa395d15afdd2de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__690e7a577c3973f21d43544e89a3ce8ab9b05060a96d1e59a55531115ed2ea34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53a1bd7f51da22009249062812bd45aa6cca665cfb8c3555afd0c8299fde93fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e7ab61338a07ab450db2bc2aca19893c67ceacf0ce68aa62222a801da4b00a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesWorkerNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesWorkerNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acb71edb7707573bc157da1e6bcbbb1dd65dd7f8af63d5b41f94c2900e8a42f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e29ad951ca50bad57437372a445f3866763d3129c708426f0dc33c46756f3d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15237ad4f1aafbf3c9e252515370a155d426cc7d0296fa404ff23098c1c2a8c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5e00ef2203afb732c304c60f72cedc1569f71d8c8bede6f3ba886a6f8db0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02e90e8f61695222a5e2edbbbafe1c42ec5e10c744344601c7a12a03ad15ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesZookeeperNode",
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
class HdinsightHadoopClusterRolesZookeeperNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd674b09f4db79f50bdc207ecf41e1eda15e650a585994fe12a1c0d47f10e546)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#username HdinsightHadoopCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#vm_size HdinsightHadoopCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#password HdinsightHadoopCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesZookeeperNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#script_actions HdinsightHadoopCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesZookeeperNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ssh_keys HdinsightHadoopCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#subnet_id HdinsightHadoopCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#virtual_network_id HdinsightHadoopCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesZookeeperNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesZookeeperNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesZookeeperNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5132ad85ba2fecf0e41dd0f84df09d7914894cdda5db6ad833655ae2bfaf501d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightHadoopClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2f036ba8325dbe911f34248b300426ba230488d8dd80ae1fe5ac1baf07ceff)
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
    ) -> "HdinsightHadoopClusterRolesZookeeperNodeScriptActionsList":
        return typing.cast("HdinsightHadoopClusterRolesZookeeperNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesZookeeperNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightHadoopClusterRolesZookeeperNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5cdabd648eb92c23220c49b57e1f894d8fd2e025ebc770a501d721a3556ac912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dbe70e5410ce1841f2748fefc5cf1fb99fa1e274cdee126793b7faa74b1a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa32d4da059601691772b91095d306c7a712ebb54404c82bf105f343a38267f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec8da15bf2578f81adea5553689720009e2c5ebb57815e4095479b4ebed0b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40543156f722b97592e62ba6a27a8f62af98499fc8ca5fb0de6e03bccf5efe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4df56503a3cf8f4296249d86e437474daa92d5b61df386fd60f98de3d5273b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterRolesZookeeperNode]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterRolesZookeeperNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterRolesZookeeperNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf9f91c2324a0092a3aa5e7bf1200fe4867cf939f924a56d4c4811ea254ef52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesZookeeperNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightHadoopClusterRolesZookeeperNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28abcc43a66bc05995b2ee360e672338d0e87ae1e39a3a52892f3594cac50c7a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#name HdinsightHadoopCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#uri HdinsightHadoopCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#parameters HdinsightHadoopCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterRolesZookeeperNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterRolesZookeeperNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesZookeeperNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78ab594db2da68950d96882e5c67b7895d87f53275b5d9c5792a1fc4dd327464)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterRolesZookeeperNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb77aebd0534309dde76d317d7a7cc820607ad6dfc4d384c60013b301a06a628)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterRolesZookeeperNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153b2a72b6e8f23fca6cf82e4d43043185b4a936744901dab802777ad3e4e995)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b0ac02712e1c7f722eee23677051acf4df19c12353509625eff39fd8fb464e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd6d3f5624043bdb6c6c0c645ce190de4666a1a68267975dfa9415e8da1e51e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesZookeeperNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesZookeeperNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesZookeeperNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb0feb900599a74ecd858a347be8eaf11919b375aa12c8e756f2d6e6fec7b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterRolesZookeeperNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterRolesZookeeperNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d879e0dae3e5f8554ed0ddd90b081c79dbbd79483197e2815bbb566a8d4ae6e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ce3fa7ecf62b2f3b3fedd3333b59413f06d3cd69b225588f1bb9a8454d7ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2741a651251bd2fd8c41f4a2bbf7df6e568490f8117fce7ea9123721e18630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77fbf7e87d984d21c07bb0761b02f92730b643287e04516ad37a547d560739f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesZookeeperNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesZookeeperNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesZookeeperNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bfd74ce9966d0aed97e48b692fc33991fbcf0cb3efed78b92d84056c9ff82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterSecurityProfile",
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
class HdinsightHadoopClusterSecurityProfile:
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
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#aadds_resource_id HdinsightHadoopCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_name HdinsightHadoopCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_username HdinsightHadoopCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_user_password HdinsightHadoopCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ldaps_urls HdinsightHadoopCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#msi_resource_id HdinsightHadoopCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#cluster_users_group_dns HdinsightHadoopCluster#cluster_users_group_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d02a8a138d0b6264c772edf24939b1c6eeea6175199a92438abf229e393957)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#aadds_resource_id HdinsightHadoopCluster#aadds_resource_id}.'''
        result = self._values.get("aadds_resource_id")
        assert result is not None, "Required property 'aadds_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_name HdinsightHadoopCluster#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_username HdinsightHadoopCluster#domain_username}.'''
        result = self._values.get("domain_username")
        assert result is not None, "Required property 'domain_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_user_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#domain_user_password HdinsightHadoopCluster#domain_user_password}.'''
        result = self._values.get("domain_user_password")
        assert result is not None, "Required property 'domain_user_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ldaps_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#ldaps_urls HdinsightHadoopCluster#ldaps_urls}.'''
        result = self._values.get("ldaps_urls")
        assert result is not None, "Required property 'ldaps_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def msi_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#msi_resource_id HdinsightHadoopCluster#msi_resource_id}.'''
        result = self._values.get("msi_resource_id")
        assert result is not None, "Required property 'msi_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_users_group_dns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#cluster_users_group_dns HdinsightHadoopCluster#cluster_users_group_dns}.'''
        result = self._values.get("cluster_users_group_dns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterSecurityProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterSecurityProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterSecurityProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7184671479189a5fd70e91d97dbcc1395dfb6fc81130a8cbef7b2af91973c8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a9fe4cea799468657f1c58b43d52dcb977a426958c59e526d0da042c426109b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aaddsResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterUsersGroupDns")
    def cluster_users_group_dns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterUsersGroupDns"))

    @cluster_users_group_dns.setter
    def cluster_users_group_dns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dec0b0fb8a884d295117be01425ad41257eea53ac7b63c3e6669425b6d36faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterUsersGroupDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab46643c39ad12008abb86e5ca7d25e52f8e1a0126fa8802de450172e117be38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUsername")
    def domain_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUsername"))

    @domain_username.setter
    def domain_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76e86e56b75a82cbd6aeb0e9aecd4ed154d8d2fc6549bfad6c94da3eda77c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUserPassword")
    def domain_user_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUserPassword"))

    @domain_user_password.setter
    def domain_user_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b602454ebb78e32382ce833eddb78a7dc287cfb45c1a4d8800383f0cb48cf3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUserPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapsUrls")
    def ldaps_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ldapsUrls"))

    @ldaps_urls.setter
    def ldaps_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4da01a57322da3ecbb6b37ee1bb404fb423883e96a4a99e74d65a5e1c83633e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapsUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiResourceId")
    def msi_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "msiResourceId"))

    @msi_resource_id.setter
    def msi_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e264dc4d3140ed9abeca6d5e0cc54044b98c85ff2544dee00bb903a64a45def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightHadoopClusterSecurityProfile]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterSecurityProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterSecurityProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6df61929441e4221a787b444da727db788238c5eb59abdfe7d0e6ef5ef5fa04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterStorageAccount",
    jsii_struct_bases=[],
    name_mapping={
        "is_default": "isDefault",
        "storage_account_key": "storageAccountKey",
        "storage_container_id": "storageContainerId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightHadoopClusterStorageAccount:
    def __init__(
        self,
        *,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_account_key: builtins.str,
        storage_container_id: builtins.str,
        storage_resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#is_default HdinsightHadoopCluster#is_default}.
        :param storage_account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account_key HdinsightHadoopCluster#storage_account_key}.
        :param storage_container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_container_id HdinsightHadoopCluster#storage_container_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_resource_id HdinsightHadoopCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abbc4f835f95fbeceef93c8c958524cb24a8486507fa285ed1b59128f8c148f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#is_default HdinsightHadoopCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_account_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_account_key HdinsightHadoopCluster#storage_account_key}.'''
        result = self._values.get("storage_account_key")
        assert result is not None, "Required property 'storage_account_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_container_id HdinsightHadoopCluster#storage_container_id}.'''
        result = self._values.get("storage_container_id")
        assert result is not None, "Required property 'storage_container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_resource_id HdinsightHadoopCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterStorageAccountGen2",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem_id": "filesystemId",
        "is_default": "isDefault",
        "managed_identity_resource_id": "managedIdentityResourceId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightHadoopClusterStorageAccountGen2:
    def __init__(
        self,
        *,
        filesystem_id: builtins.str,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        managed_identity_resource_id: builtins.str,
        storage_resource_id: builtins.str,
    ) -> None:
        '''
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#filesystem_id HdinsightHadoopCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#is_default HdinsightHadoopCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#managed_identity_resource_id HdinsightHadoopCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_resource_id HdinsightHadoopCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af99690cb9a0a155fc5ab1efa3fc98772ef618540d5d65f4865f510e1010dfd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#filesystem_id HdinsightHadoopCluster#filesystem_id}.'''
        result = self._values.get("filesystem_id")
        assert result is not None, "Required property 'filesystem_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#is_default HdinsightHadoopCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def managed_identity_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#managed_identity_resource_id HdinsightHadoopCluster#managed_identity_resource_id}.'''
        result = self._values.get("managed_identity_resource_id")
        assert result is not None, "Required property 'managed_identity_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#storage_resource_id HdinsightHadoopCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        assert result is not None, "Required property 'storage_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterStorageAccountGen2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterStorageAccountGen2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterStorageAccountGen2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__117abbd9feaee2a9f868fc59eb803b4a0e93928d5d8b601849a90d5eb4017176)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eb11cb7f248564272c09afb61045ecbf269686f7c6a9b6d50bd515dc05559ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6bbfc29a7f9c493b55b300de28f611f860b0769ff08fa059cef91ad84be0e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceId")
    def managed_identity_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityResourceId"))

    @managed_identity_resource_id.setter
    def managed_identity_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6b67d28b230f70e45aabfa25e3310c51910548708db73fe0ec3c7a0c680eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c104d7bc13430f6cf00917a7fb6c0949f9ff6009ef6fff1e444861af3bb8a5b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightHadoopClusterStorageAccountGen2]:
        return typing.cast(typing.Optional[HdinsightHadoopClusterStorageAccountGen2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightHadoopClusterStorageAccountGen2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a1f3e2f42a06061f9563b84101e34316282747efe7d905fc3463940396a983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterStorageAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterStorageAccountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71672ae89d6b08e5357046f33f22048be3bcdf2cd011fc2186dedaddd4b22848)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightHadoopClusterStorageAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2dda737d39d123784dec070cd233b14bff79b59f22974f778e34c77275ea3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightHadoopClusterStorageAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8c4b70ffad9a58e06498e1ee024b32024013baae6a426eebc842c6fd585e86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d76acf03a286ab810d742ace3efc4431b4779a9211c7c4627605b42c9d8d30d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__904d18830fe15d89401eb5aca68762e1d2c790a80b7f07a59efcf0a3fc1d6d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterStorageAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterStorageAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterStorageAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf970d0b7665b8f6718e2292493b8ac314a1290ef2462a79972c1abe7fbfe74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightHadoopClusterStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ca5d1e4d0d24b6cc79dcd6611b46ef62cd23cda5015315388a349dd435190f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97d35949f4bb8f10bdec2de1f391234fbfc5e1d6e5e90383379ec81a41376625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountKey")
    def storage_account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountKey"))

    @storage_account_key.setter
    def storage_account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b17b7e4807ec7f929e478fd01283bf00c1fde8fcc5260b1201395f1c794281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerId")
    def storage_container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerId"))

    @storage_container_id.setter
    def storage_container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e583fe19bdaf3d8df14b057a952c6d3016d1efd0d7428c2e23c9a9286232df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086c5abcf2949d021e81a15d043aa463316baad1b884176fe673ec7f8a94b85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterStorageAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterStorageAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterStorageAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0775c76350f523ce65ed46fbac3199b6c90ec6e5789b43dd8c593122c7e0d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class HdinsightHadoopClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#create HdinsightHadoopCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#delete HdinsightHadoopCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#read HdinsightHadoopCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#update HdinsightHadoopCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57669a53667c01698e365fedf41921d843462c1bfe63853c9b3f11e40114a2b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#create HdinsightHadoopCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#delete HdinsightHadoopCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#read HdinsightHadoopCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_hadoop_cluster#update HdinsightHadoopCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightHadoopClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightHadoopClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightHadoopCluster.HdinsightHadoopClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac7b4fdfac739eae03254f94a6e3d0e31a1ee643833e3136f16c74d0a2a949f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d1dbf72545e07c9154126c446bcfc7d098595d7e63e668602e368c5f60cf545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a27bf2e827deff52ecb5e90073b1036c438c42c23cb3509cc34dd5f46b7912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c3d5eb56ea22f86708cd41e939c0869d00b716fd895d3aa0dd90f26243ac77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e2cb945124b6400e8651a0880c4e2999b256c36d41bd18305797f307ad6d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1dd8bbda04ec77dd2b3ad9cf237b7fe14d224efc992a40bc334d350ad7d6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HdinsightHadoopCluster",
    "HdinsightHadoopClusterComponentVersion",
    "HdinsightHadoopClusterComponentVersionOutputReference",
    "HdinsightHadoopClusterComputeIsolation",
    "HdinsightHadoopClusterComputeIsolationOutputReference",
    "HdinsightHadoopClusterConfig",
    "HdinsightHadoopClusterDiskEncryption",
    "HdinsightHadoopClusterDiskEncryptionList",
    "HdinsightHadoopClusterDiskEncryptionOutputReference",
    "HdinsightHadoopClusterExtension",
    "HdinsightHadoopClusterExtensionOutputReference",
    "HdinsightHadoopClusterGateway",
    "HdinsightHadoopClusterGatewayOutputReference",
    "HdinsightHadoopClusterMetastores",
    "HdinsightHadoopClusterMetastoresAmbari",
    "HdinsightHadoopClusterMetastoresAmbariOutputReference",
    "HdinsightHadoopClusterMetastoresHive",
    "HdinsightHadoopClusterMetastoresHiveOutputReference",
    "HdinsightHadoopClusterMetastoresOozie",
    "HdinsightHadoopClusterMetastoresOozieOutputReference",
    "HdinsightHadoopClusterMetastoresOutputReference",
    "HdinsightHadoopClusterMonitor",
    "HdinsightHadoopClusterMonitorOutputReference",
    "HdinsightHadoopClusterNetwork",
    "HdinsightHadoopClusterNetworkOutputReference",
    "HdinsightHadoopClusterPrivateLinkConfiguration",
    "HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration",
    "HdinsightHadoopClusterPrivateLinkConfigurationIpConfigurationOutputReference",
    "HdinsightHadoopClusterPrivateLinkConfigurationOutputReference",
    "HdinsightHadoopClusterRoles",
    "HdinsightHadoopClusterRolesEdgeNode",
    "HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints",
    "HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsList",
    "HdinsightHadoopClusterRolesEdgeNodeHttpsEndpointsOutputReference",
    "HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction",
    "HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionList",
    "HdinsightHadoopClusterRolesEdgeNodeInstallScriptActionOutputReference",
    "HdinsightHadoopClusterRolesEdgeNodeOutputReference",
    "HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions",
    "HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsList",
    "HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActionsOutputReference",
    "HdinsightHadoopClusterRolesHeadNode",
    "HdinsightHadoopClusterRolesHeadNodeOutputReference",
    "HdinsightHadoopClusterRolesHeadNodeScriptActions",
    "HdinsightHadoopClusterRolesHeadNodeScriptActionsList",
    "HdinsightHadoopClusterRolesHeadNodeScriptActionsOutputReference",
    "HdinsightHadoopClusterRolesOutputReference",
    "HdinsightHadoopClusterRolesWorkerNode",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscale",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacityOutputReference",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleOutputReference",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList",
    "HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference",
    "HdinsightHadoopClusterRolesWorkerNodeOutputReference",
    "HdinsightHadoopClusterRolesWorkerNodeScriptActions",
    "HdinsightHadoopClusterRolesWorkerNodeScriptActionsList",
    "HdinsightHadoopClusterRolesWorkerNodeScriptActionsOutputReference",
    "HdinsightHadoopClusterRolesZookeeperNode",
    "HdinsightHadoopClusterRolesZookeeperNodeOutputReference",
    "HdinsightHadoopClusterRolesZookeeperNodeScriptActions",
    "HdinsightHadoopClusterRolesZookeeperNodeScriptActionsList",
    "HdinsightHadoopClusterRolesZookeeperNodeScriptActionsOutputReference",
    "HdinsightHadoopClusterSecurityProfile",
    "HdinsightHadoopClusterSecurityProfileOutputReference",
    "HdinsightHadoopClusterStorageAccount",
    "HdinsightHadoopClusterStorageAccountGen2",
    "HdinsightHadoopClusterStorageAccountGen2OutputReference",
    "HdinsightHadoopClusterStorageAccountList",
    "HdinsightHadoopClusterStorageAccountOutputReference",
    "HdinsightHadoopClusterTimeouts",
    "HdinsightHadoopClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__af73de75d9e157dc9d82edd3cf90367b49505d1d734e5161c03e7f19a0fc5813(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightHadoopClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightHadoopClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightHadoopClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightHadoopClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension: typing.Optional[typing.Union[HdinsightHadoopClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightHadoopClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightHadoopClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightHadoopClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightHadoopClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightHadoopClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightHadoopClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightHadoopClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c4780b6ebf9fbfff27e6785ce270080b6dc7a6a5649b746c6cfc0aca6aa9acd4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96dc21decc9fb62a14070b4faccb54724cc4347cd31516fb7caad2edf95a3c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4be0273e7910f76068225953bf85c99415cb8a359da54bc3bff64026fa8da48(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172431f7b8ab7458408fb44f28501d3498e8fbac22b33d406bd517cccd1db878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de3b8c30ef3acc708a16afdddb7bc53c294a1037adf8024f0b0e2f779ca0ac5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0b7d0f26386d8fd785b88d58c195c05c0ff58c906b24580c0649d7db378558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9da8615f773f22f9e6fca9eec7f40975b2b664c50e58645f6dcfadb9425e28c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cb11070a80e8c9438d7ef12f4771de10d0ecc34be03382d6a2ebd591e611db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7101267a85b098b3b7def3ed50544fa36015796bdfa46913a2deacc266698f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8005f408efdec4bcf791f6d1af4ee8b098cf47a2566123b7e7a8519ebace5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916e513a06590c189febc79cdce98a1df4493d7ae93e478714d8664c0acbbbd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc54a2289e0960a12742150636b237646a074587ee41686ab0222a7bb92c791(
    *,
    hadoop: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e212ed90191ce745bad5d4dc4585def78e9689858340a06898c68e0b7f21d05f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc6b8732046da4bbc32f5f0c6a96ea4eb3c9a75766256ae39f140a7c2c6f0d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810ac478df1633006c7960411b40efde929a80494d5a67a6e7ec9f0064dd3bc6(
    value: typing.Optional[HdinsightHadoopClusterComponentVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7933e6ce26b38f456f562ba7ff4805c81fb658adf8ca5d0113b9cf55e703e4f1(
    *,
    compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_sku: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d749f0f4d8886b007a05b26e93ce29a5786e69d2fc420cd2d5948ba40a59ba5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30a0d47bf29909e0a2ced157ce46527319fafec185d7c138b8aa6584f00a268(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363488e63faea548859101a1b67f150046acc671245d45135d37d048402dbcd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52ddbda38a48c0df754e0ba062cf6bd38621a4d76ed57c0db4f6e26204fab6f(
    value: typing.Optional[HdinsightHadoopClusterComputeIsolation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ab2667c5d2d43baf1bb127e48d1c4dd98546e20c05c8d90d7f0f790c505f36(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightHadoopClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightHadoopClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightHadoopClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightHadoopClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extension: typing.Optional[typing.Union[HdinsightHadoopClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightHadoopClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightHadoopClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightHadoopClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightHadoopClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightHadoopClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightHadoopClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightHadoopClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cdaf2dae896a2e4c2a885ea70bf79a2bb4f64ec3742fff8fe2374f1a8ebe85(
    *,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b281654fa274f994c939dc3077966f56534db001bdd88a29ee6917de7e4ec92e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc1b386a5ac5394b5004a5189fea90e273f1e6af0f91a7a85e29bc4a1149bd3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bc6bfad6f537c7cdc045775b07127ceb24ea48aa44d2298089788fc9f72f52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78a25cf9952acc39cf22555abbeab5b81fc3646e5e6b49b12dd2c2bb103bff6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62436e63e753ac9af76b7e147d32ebd0147bf32d7c699370ed7896fe3300e6fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8fd663fdeae7d61616d1532f5f123283a584f18350890033e3b271b09de2e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterDiskEncryption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88e432f84cf9cb567008b28d0158cce7c9a36adf83374aaf5a5b8a1053e60f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bb65e02fa0eaa844a2c66d73e58cefa42ea65778ba0cfd968c250ffffd8198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d21578786800fd87684b87fc85dabbe32f9a8d06cd7b50d6daccf31d4cfcda1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cbdf405c976ece92657afc2b7e46f0f2ce036881f592a698c00acc1fef1ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304314d5250ca1f20f93f5904e51f8fdc4bef470dcf60e86c5e47d7a1fa00e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635a399df202c48617fd601e6860dbd98e0c9a43d72d1f8835eded34245ff620(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterDiskEncryption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89589dfc7000198ee7b451d59742bdf742cb12cd2068c6d5ff76f5e72b7551ec(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb1779ad90492b0ec45e3285277e47d404acf7678d17a19590fd1e4e1ce2096(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d193ea5415cd979356472d1bc7bc43bb4767ca5f373130ef7b8faeb7ed98b0b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fa9a488fc31a4aa6b35110203aa15d4ea8af9d4c4027f74dac0de0d3fbc634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e08737eedc92aea9d953e6a5cce3ea46c3b125aa1fd0600e5d97d1fc5d47cb6(
    value: typing.Optional[HdinsightHadoopClusterExtension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890827897343e91f51ad69ed7f7e2b94610d8ea01d6923b4ab281abf206b74e7(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa668b1349c4ab500e428b8896dc0dd973bbd2a5f86e93bd45f14ca378e54893(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1869de0dc665919ad53f9b8e23c9943d9efc2c0e3c4a33028f74304c2be8b8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a30137365c8977db4b580dbc7c62ec19de2558348dd0b2238069ad9710d18a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f7a16bd28bbf25c33b9b7c6947646cd94ad0e9d87e1285eaceb89abd89296a(
    value: typing.Optional[HdinsightHadoopClusterGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3bc923d1292cd4c8c31ee8dfe5f4a5261d92eba503d42a3c1d8f4b8e89ddca(
    *,
    ambari: typing.Optional[typing.Union[HdinsightHadoopClusterMetastoresAmbari, typing.Dict[builtins.str, typing.Any]]] = None,
    hive: typing.Optional[typing.Union[HdinsightHadoopClusterMetastoresHive, typing.Dict[builtins.str, typing.Any]]] = None,
    oozie: typing.Optional[typing.Union[HdinsightHadoopClusterMetastoresOozie, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1d4e1bee3d603d48cb9bca6482c2af43a1dcddad451a94759f2fa5d598ff98(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b426c19918a4c57d2fd3553f0a4345ba89ad8af16f32afd8f595bf26cdecdc96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb31fb70f21babd85160eee03892a972cc48189c8483ae02ff5b83fe6b19860f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef7458d8153e5c888402c3b94064bce52e3d6d9a05c9f5bf0191da337b63d1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df7cc18e866f50d9ee7d2dd05926f55f58d258dac8b6a9482fd87b94c3bfccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e8db0c42f8ac1bbb26b7116d01b77fdc27a02ee8b89316af81f4209980fe08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645dee054de2dd244a6995846d38cb84ebe7f089611ee3f95ef2f5f54f800b16(
    value: typing.Optional[HdinsightHadoopClusterMetastoresAmbari],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6761d88aad418b24f9405186dd1e6e79539ce0f66672de120672401bbaee75e(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97b17c44b654925fe5034b3c10e75c388b434eafbb5783573c535479292a9df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ea62d245809d5c122043b89f8a8ae3436bf8003aa9ee53f4f765896a88eb2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7668e7798648258c9e45dfd47c3b94c0709363b633790c0480f98c9c74009042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a545e9bb439a551e8110cf10af10bbb66cb75f3e77802093df4b779db3dc73d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28376e3467837a09f8ed747b729e5719b938972aea183556b39bbcc03110c393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37844f12d27bc34c0f0f6c9dc963aa605166214628eb5ada2184ad6162e04dcb(
    value: typing.Optional[HdinsightHadoopClusterMetastoresHive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dfab906fbe51c111dd105006bd8ebb8c49ae860c04141ee6955fc547f2bd53(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fef26b4738a458cfbbcce8d55f574b78dda1972b5b2c8a820717f633565ff80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfff9d1a9e629def132adfcc064d7762d2bfdc5ddecb3ca99561b91974c2a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e782273eec25d49b7cc5a529cb3840cb66d6bc70763b783875bcecd133080bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1c7ae98fc5ce6f745e2ff40b01ec97a203a1212ded3afe1063eeb9281159e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f12a8abce494747052677864f214bb38c476dd206086bc445aebf34ab9c347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb61d9e6919c342cb37924ba102b599192c759252ca2e6f479eba731bbedcc4a(
    value: typing.Optional[HdinsightHadoopClusterMetastoresOozie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7b5281bb9051eac7f99aa5d926ac568bdcb4c36abed0b3ef17e1f024957490(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776308bc33a78a3e8d261b63475a9f783a641e84b71989b7c5f38977fd392184(
    value: typing.Optional[HdinsightHadoopClusterMetastores],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3492f49603b03f67d1abb903bc1af99c6f3fb9c3633f14ff21773d7c79966a(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151f58ef5e5ab9b34152ea6a77c67ad6901ddb3d4ab2f866f295a4246eb2edb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6819d02746074a668e0c734ee12f706727b618a76735faff35c44188d14192d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a457677a61d7cfb5b1b11e7cfbca8b2c734f53605354cfa377efdc1c09ed77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4efe123fec31ee8226ccfa4823b36e20eb49e5c8a0af692fddefc02f3b0a6ca(
    value: typing.Optional[HdinsightHadoopClusterMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d382e69eb7b78894a0e49bab650e4076facf12fe412a9e620f599251a5b500e6(
    *,
    connection_direction: typing.Optional[builtins.str] = None,
    private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede7f94252c2f930d7a1f29c45a866dd9028f6fe97b91c19d1ae515e4d0c2aad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d808d59bf2d3ff6c53bf2370e7a5498837f65c627d083e04a71fca56c16c3167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374ba9f3b62d49fd88bf018bc4b8b4e9be4e1f4bd13e334c4ee8933747fbfa79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec5e7d41c8d0ee0a744b40bf8d208f8a3857532a24318e0110a9d13515492a2(
    value: typing.Optional[HdinsightHadoopClusterNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ddda831f614a2158e4ff8d594049b0ff206276c4347666f6b4ece747f91071(
    *,
    group_id: builtins.str,
    ip_configuration: typing.Union[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fcb2dfeddf5f1ad33cce66073d33e454387e46f4f45ab54a7574a701c66071(
    *,
    name: builtins.str,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    private_ip_allocation_method: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce73cdd589eec68bccebf855785c431fa502ef671a50743912e079a33d0bb62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c588c87e872688ae74a295a998ef893c40a071fa3584acb4c841345694745b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528cdfa1112a30d791af00a7efca030ea7c6a762720374b7aa175a0666fcc566(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ed91f61a3f1e3d1064ce60d6a7200461ec9d53b0eaebc3be1587cdafa57389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c886abe52dad15c01caeb044e74246996ecb443af21ffc43a3f6b91352e4747c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2630a4281f15156110e59251ba553384727ca6fcd7c975939c843721e6075891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7757469f09f54963be51908e39d52cf5dfe1add35b6a4494db968a1d766226df(
    value: typing.Optional[HdinsightHadoopClusterPrivateLinkConfigurationIpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b51c5eb2b4039c1ef99175300f102a0bc616412c1e6488c4e99ac377dc36c71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bed3a8d02a476730e3f381cb745df284e6b043ff3ef1f513363eae3d1066403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06175acc3d460180f532ccf139649596e0977c936517ebb13d5fc95062f6a6b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a36e2e434c6f61596d91d2b0ac5f5ddc233d53d36ba4d71fed086e3454b253(
    value: typing.Optional[HdinsightHadoopClusterPrivateLinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368b064e01289a8e9de72e20f3226a1806dc81e5a67646cfe7822a6c5a94d8a3(
    *,
    head_node: typing.Union[HdinsightHadoopClusterRolesHeadNode, typing.Dict[builtins.str, typing.Any]],
    worker_node: typing.Union[HdinsightHadoopClusterRolesWorkerNode, typing.Dict[builtins.str, typing.Any]],
    zookeeper_node: typing.Union[HdinsightHadoopClusterRolesZookeeperNode, typing.Dict[builtins.str, typing.Any]],
    edge_node: typing.Optional[typing.Union[HdinsightHadoopClusterRolesEdgeNode, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e86eb4755c33d7d76c268802d41faaa1596f8e4d5b9014e084b2d3ea13a7d2(
    *,
    install_script_action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction, typing.Dict[builtins.str, typing.Any]]]],
    target_instance_count: jsii.Number,
    vm_size: builtins.str,
    https_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    uninstall_script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a514458060c6751d45147c6131ed3fea471eb44e9d486efd7da3199df2d951(
    *,
    access_modes: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination_port: typing.Optional[jsii.Number] = None,
    disable_gateway_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    sub_domain_suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a752e9dd304b7f6b10d668249f462cf78db1f506fa167c99356be9c9409af725(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a29b15e71856d8f29552e168cbadccd25923062c3439c6f16987704b70bdca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1da4aa7ab874190a79195b9e4c8340407fa441a7e761e734e31bec6667cb05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78322162a963a7ab6932cdbfcf4136ed128867d18015d5ee6262c9cd95b73fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2777d365b0969c836a2bff5886448f963e0d9df4c0eae5f4706d3f634fe129f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8729fa16794d6e7269bcfff28e11d74963268cf88926800e11c817cd1e0e8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826242784e92c67ce5e4b9eda52fbef202bb21526dff12a58928039a9fa23e66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e344e11ddfe9a26d15b30e7f5b3d5af2036c534ee49f65cda15491bfd025418(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74172018d090182c1abb922b000abe71846fd0ed65669d486ed567b36a4c8f2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647f9e1c48f0c00dbbe9e6fdbbc9373c2dd8f72b6c04dc6730f3c5b2bad87916(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a7a78aa647dfd613e526f4cfec0b25903b27555fcf17ca097c93fcc6b6c5d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f615aaafcf5fbe6dd718903654bc7ae8959ca826022571e7c61e38ab4e3b806a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24258c335b33b2b2b88a65992866c4a30bfe245337a4c8978215113bd4e729a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb0f7d7c872f96301d8afb946bce63477dd73daad81302ddfc95cb10e641ec2(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dde04b90070fbeabf88b123ebdb403a0fc4224c6b1cefb2c48cc28640c707e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233e3a08824693287bad16ebb81603c9b369bc8853a10c41b366072189057135(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795145102bc27ef0a301bfc85ec21e73ed2147927aa364bed8b693c4ab153cc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cf18b2248c67834c3c41dc4b0231c246c5d8e2c935b77c94f78db0757faf1f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfaf4a17df20b4081810034c87a594845c8500af7e2a5eef766bf12d0a55fb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1094251178d25c0114e158470bb108a00feb229e221c018a3d39dc892dbae55e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143e338a60d487ba13c04af93dcb5b04e269a09392cdd8ba9b408760488de3c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcfbd05d229c75103d3d7b22e6b5a17833837e4e72a8431d1b46a1882442291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a49edd3cdecab731d46b312e79b8497f74acf20e0519f8a4c11d606ce51d57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ed6f444b6f583b0ab83c9168924d4240d31c9b91f10bb697660c344c43e1ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d8bb3a7f598b4c69162af6c3070bc8cc3b792bfbf63516c3e1f4d86e15c69f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6a9f6049121e0b244ee6b093c4302e9b23bde72592cf2e5e5568f6d3c60ac3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f247d81f0c80a75e7527d2e5441f8a1f1ae7fa9d494992ce7bdfb23c6dd4af14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeHttpsEndpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222563f8f735dfae2b79909aa0f60bcb5086a14cdccca568d2238ee3e2bca234(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeInstallScriptAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9895a282e1d90138c5da8ab0e053d1adf4d0c01929f7e66a92c6e7a45106e02b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dced5d564deeeefddec17eabc68802b02376e9d83c27cb8e25e671c1593805(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930588d21737651ad4ffc6b974fb419baa8c40feb5527d59418fa9b70ec0e21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f45478e5fe7e0d56d93d6dee69e606dce308bc15cda4f7cf109420a1e510476(
    value: typing.Optional[HdinsightHadoopClusterRolesEdgeNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0684d5777e249120595888e23e47c143640794a29b66dfb466c086c38c76ed(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3822a7ceffcd5f2634cb0a8280eb474ec382bbed6109873c01296df0cf90a2ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d651ea3569011bfcdc04d8d5894e1fb9f553c80fae48d5d18d0ef40204e1d9a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8bba4310cc169a0a662ae3561c98eaca522efb5c814f47a1fa4e442d8edd1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd22f09801f04b44bf2586650086714cdf04603b91c56151c6afac1a9f49a041(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cbf0fa52ca35f8b9e562e362e8457cbc244f6765c1ac723ae56b6b0fdef1ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db67910275f46c908a0990b1ff00055e8b16773f2084cedab9326cadeafe0562(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6237cda6d2f55895a9e07efec6b83aa74ed14ea640954f9bf5362df692afc08b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabb5b6daacdbacbbe1fec889cc8e9447c5d9ec61af668e6ad31ff819b89baad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73052a67fd1709494c18c585ee97fa13bf419eff71c447b2780475e7743ddda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cc1bdfea8d82acb6eecabab4684d205f2873553868a9a1c9083957acdfac6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09f1f1d5a5e3c27711c6d66615e7f3b1089cedb0fa148ccb3ac577258a01f50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesEdgeNodeUninstallScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ae3fa923a08ef876574b9d1d48289e0234089d0a206a59ce4417dea42bc564(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ec03d45eaf7795bc2d7ca13ddbadc8a90e5a014386e2f1313f49a37528dd1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a0eac67273bb7faf446b2f798f889e535f3b81e196409af35616d55074af1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a53b241a94dac5d180218666fa1e0c81f9ef515e7e91e90d600070719fd00d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27e4f0a0828cb7089d2450a65dadd80246d44e63ce59e5bdc6b30259b7d4598(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a5cd3b352fa06b19abeacb947b895f5d8905bf3497216ddca2c9e2492cbc85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814f17231ac080acde94a454e6cb9a5c6731351b1fbaba03fc50e6f97ca32853(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b7f15d0fb9f44ae5dc0e366d51686d4086d1810e9fa977c270e7fe962d5ec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d767022f035673931463b7396267149d7b771cfac9125292f2e179cc01e79b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4468023862029e997e666be4c744589ca1fcd12e94abddc7b157346d06090423(
    value: typing.Optional[HdinsightHadoopClusterRolesHeadNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab69c0f9ba970477fd4c2e17dfec635f56e601fec14ad575901f3372d381a41(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56b33f6b5c2a6ebd9a5f4a2ecce11c5842ba64230ef704cc4d24d30410cdd42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a4887e9ebbf3a717a2a9dfd8cf0f6e12b88f395c7e705f75623b165db2483d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c43d9b5aafb2cf992e2ec76b409a4db4ab9797f270b9cc93156fd625a7a29b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57da1c7286040fcbe6248b9b7165c09bfc5b05bab23077bd7d458359c38b7184(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ac94941b0810c6d2a0697474a3da79712269006e1218e98d2f381605e91489(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98722a74abed427e69e47444e2fa31d397bbf16821798a6f6d7a6f92403e8ed7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesHeadNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d4f2c7895cdbb8bf73e5e8afc9d0b88689ab590dd8ee671777aee4e58f9018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89789da7144c11d94086f5d79e6effb0535b2a452156ea65009da7727dce87a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ac74618074e15101cd8504eb63962e99b91b27d12dde95a8226f1a3655fe8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80df5a5bc2e8a4f8ff8d42abb01b5b6e5fc90e1072228f61c7e5043f56b5a578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f4f00227c50cf087d24263ba99e94996b2080b546b581e6a79c80e31c36d48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesHeadNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286da027e20bf8f8cd83eb194e08b8b8ea9efa9c7e02803802404f49caec3e7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7ef53b8c5974a0ebe4037c4cc7e0fe7206a80e68675379d55a3392c0e4c0e1(
    value: typing.Optional[HdinsightHadoopClusterRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264a35182c683e84db41dfbeb4304316b898ffa660f8d0904cb913a930dd9f82(
    *,
    target_instance_count: jsii.Number,
    username: builtins.str,
    vm_size: builtins.str,
    autoscale: typing.Optional[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a04357458df28b76a035d7b7794bcfda982ed6badc3248eecbb25cb930556a(
    *,
    capacity: typing.Optional[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    recurrence: typing.Optional[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0507bd3b7316223b2be11556220deb9e4b94c21e9d077462ee3c71c710d807(
    *,
    max_instance_count: jsii.Number,
    min_instance_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228b5ac275b2f75456e104b47b0daed20d210f32bcc6e7ff079114bbab822e5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc5ac23578a79cf036669bddd681fc4584d73a582332b449dc93bed22e1339d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9540c70cff0972e2e98c29ffb63a8c0bbb110ad8529ce1a611edecfff22daed3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573d937204fc37dccb4777869af6482a653ad441c545a6c90b2068281eb3e27a(
    value: typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06512d0e0074b01cf29de34d3f0f96cf37dfc7da0383dd874bb7e0ad913f19ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4050eacb6e86f19495d7856c667bf55c5e162e8cf46c189657e88c37bb8d8bff(
    value: typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b41588b79c85d9e6d9ad3b2a4c7a762f5d57de9f3f5d44ae6fce4869b5e90f(
    *,
    schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]]],
    timezone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b24037121377a6d43d743364fe44ac2651b199ef610a8ac8b2b0845eac415c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d1780e07ec8c5ac79fb09a3f4a5b1675b5e91054c0b56c3c4b1f27221ab1be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07e24c99a4b28eadfc86d662d8446ed40ceef0d0aaf5b51fac12b45ecf02605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828e7d9f31aa3d4bc3747fa6c83a2d6fefb638925641b08e80aa5e716e4d38fe(
    value: typing.Optional[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329c445370d5ecf23dd9cfde78d23573707b8149ab6c300d44d1c56caf16e1a7(
    *,
    days: typing.Sequence[builtins.str],
    target_instance_count: jsii.Number,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c247241a8e5acc00af8e77381c04f6300d93f0cb58d14feb49a5b47c078c7df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de34823358359ec3bc54b39e6bf3ffdeb524f55e0fe3f742e444798b59f02138(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b017907985046a10995dcc7df5570081e3497727ae373536c74ecc073ea824(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c1b2cf5f669b3a97327e7f10aef8bfeffc0b6daa2af28119704c9bda06fff3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29137376122db41820d7f0bc75347032f643a5a07de38e13c100a13a4fab1f6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6ee6afacaf4581e9b313a808d4a683b217313f2388f320901e33c7946544aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7a9601689627e41772b9eb36c0361c7c98761ab9293c4f00d961ea278fd0a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb56768d014126b62eac68ffa4cce41b341af50c4d8b2d44781de2bb9279209(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968d5d1dcf5981fdb8c617272d86cafef5dcc5ac98fda455910265c0b742fb31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf4d49eb77d9991e5e86d45962637d80eab1f82f268dc49c9b779a4339269a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639d3852f54f0e9ee93d93d91f2a546a01c8422ec05fae44d67bfd58eb01b107(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c088d08a0ac43dbbdd13cc194c50b8cc29a6dda5d80a4e3483d74923619c7f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82a3f36d2ef100ccad02a11b6e47ec3522efccd60cd9c8c0475bca49a625f92(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f5ee33bd0976de6ed688a3548b950f12de48e952aaf48f0eb6d5e7cb21e42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ddf7ca5ae97d720865aa88ef52b32f90500041c4fc518bad6f66e8998d9316(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25aaf98519581dffc454c2cee118bace3e77adbb4078fbe12bc51a8aeae9ce56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb9751052e48a85f9c15f9379509ed44871ff7b86b3837a21ce2dab805e87ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48001f8170bae91756a3020a9f31c43306a5cc0de58c105d91335cd91dc128d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a253f719509621b58f4550176c4b2899054f43c909d887573eba07761ba7cd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3bf4707423d64cb108e9c45158bf1f869c5ee528927ca279b87b8463ff8b1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6300813b20e1e7d942a914eccdb55dbade2fcf59c51e82f5e3e4fea1102db42(
    value: typing.Optional[HdinsightHadoopClusterRolesWorkerNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3092f642f74354016e00042ca87a3d8ddad79828ba7432288cf8a5071f9c576(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3c65c6200299b3af8dccd8bae13014fa33231fc498fedfbc3f5b5e340d3e08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ce620d33fef753cbf9ac9048ef4300d7bac4c649d6755e5e83adda47ecd9b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c936e268803e59766cc63773318bf26a3fef3cd75d77299e9fa395d15afdd2de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690e7a577c3973f21d43544e89a3ce8ab9b05060a96d1e59a55531115ed2ea34(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a1bd7f51da22009249062812bd45aa6cca665cfb8c3555afd0c8299fde93fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e7ab61338a07ab450db2bc2aca19893c67ceacf0ce68aa62222a801da4b00a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesWorkerNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb71edb7707573bc157da1e6bcbbb1dd65dd7f8af63d5b41f94c2900e8a42f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29ad951ca50bad57437372a445f3866763d3129c708426f0dc33c46756f3d4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15237ad4f1aafbf3c9e252515370a155d426cc7d0296fa404ff23098c1c2a8c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5e00ef2203afb732c304c60f72cedc1569f71d8c8bede6f3ba886a6f8db0cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02e90e8f61695222a5e2edbbbafe1c42ec5e10c744344601c7a12a03ad15ee7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesWorkerNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd674b09f4db79f50bdc207ecf41e1eda15e650a585994fe12a1c0d47f10e546(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5132ad85ba2fecf0e41dd0f84df09d7914894cdda5db6ad833655ae2bfaf501d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2f036ba8325dbe911f34248b300426ba230488d8dd80ae1fe5ac1baf07ceff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightHadoopClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdabd648eb92c23220c49b57e1f894d8fd2e025ebc770a501d721a3556ac912(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dbe70e5410ce1841f2748fefc5cf1fb99fa1e274cdee126793b7faa74b1a23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa32d4da059601691772b91095d306c7a712ebb54404c82bf105f343a38267f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec8da15bf2578f81adea5553689720009e2c5ebb57815e4095479b4ebed0b7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40543156f722b97592e62ba6a27a8f62af98499fc8ca5fb0de6e03bccf5efe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4df56503a3cf8f4296249d86e437474daa92d5b61df386fd60f98de3d5273b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf9f91c2324a0092a3aa5e7bf1200fe4867cf939f924a56d4c4811ea254ef52(
    value: typing.Optional[HdinsightHadoopClusterRolesZookeeperNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28abcc43a66bc05995b2ee360e672338d0e87ae1e39a3a52892f3594cac50c7a(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ab594db2da68950d96882e5c67b7895d87f53275b5d9c5792a1fc4dd327464(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb77aebd0534309dde76d317d7a7cc820607ad6dfc4d384c60013b301a06a628(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153b2a72b6e8f23fca6cf82e4d43043185b4a936744901dab802777ad3e4e995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0ac02712e1c7f722eee23677051acf4df19c12353509625eff39fd8fb464e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6d3f5624043bdb6c6c0c645ce190de4666a1a68267975dfa9415e8da1e51e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb0feb900599a74ecd858a347be8eaf11919b375aa12c8e756f2d6e6fec7b89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterRolesZookeeperNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d879e0dae3e5f8554ed0ddd90b081c79dbbd79483197e2815bbb566a8d4ae6e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ce3fa7ecf62b2f3b3fedd3333b59413f06d3cd69b225588f1bb9a8454d7ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2741a651251bd2fd8c41f4a2bbf7df6e568490f8117fce7ea9123721e18630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77fbf7e87d984d21c07bb0761b02f92730b643287e04516ad37a547d560739f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bfd74ce9966d0aed97e48b692fc33991fbcf0cb3efed78b92d84056c9ff82b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterRolesZookeeperNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d02a8a138d0b6264c772edf24939b1c6eeea6175199a92438abf229e393957(
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

def _typecheckingstub__a7184671479189a5fd70e91d97dbcc1395dfb6fc81130a8cbef7b2af91973c8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9fe4cea799468657f1c58b43d52dcb977a426958c59e526d0da042c426109b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dec0b0fb8a884d295117be01425ad41257eea53ac7b63c3e6669425b6d36faa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab46643c39ad12008abb86e5ca7d25e52f8e1a0126fa8802de450172e117be38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76e86e56b75a82cbd6aeb0e9aecd4ed154d8d2fc6549bfad6c94da3eda77c59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b602454ebb78e32382ce833eddb78a7dc287cfb45c1a4d8800383f0cb48cf3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4da01a57322da3ecbb6b37ee1bb404fb423883e96a4a99e74d65a5e1c83633e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e264dc4d3140ed9abeca6d5e0cc54044b98c85ff2544dee00bb903a64a45def(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6df61929441e4221a787b444da727db788238c5eb59abdfe7d0e6ef5ef5fa04(
    value: typing.Optional[HdinsightHadoopClusterSecurityProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abbc4f835f95fbeceef93c8c958524cb24a8486507fa285ed1b59128f8c148f(
    *,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_account_key: builtins.str,
    storage_container_id: builtins.str,
    storage_resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af99690cb9a0a155fc5ab1efa3fc98772ef618540d5d65f4865f510e1010dfd(
    *,
    filesystem_id: builtins.str,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    managed_identity_resource_id: builtins.str,
    storage_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117abbd9feaee2a9f868fc59eb803b4a0e93928d5d8b601849a90d5eb4017176(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb11cb7f248564272c09afb61045ecbf269686f7c6a9b6d50bd515dc05559ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bbfc29a7f9c493b55b300de28f611f860b0769ff08fa059cef91ad84be0e85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6b67d28b230f70e45aabfa25e3310c51910548708db73fe0ec3c7a0c680eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c104d7bc13430f6cf00917a7fb6c0949f9ff6009ef6fff1e444861af3bb8a5b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a1f3e2f42a06061f9563b84101e34316282747efe7d905fc3463940396a983(
    value: typing.Optional[HdinsightHadoopClusterStorageAccountGen2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71672ae89d6b08e5357046f33f22048be3bcdf2cd011fc2186dedaddd4b22848(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2dda737d39d123784dec070cd233b14bff79b59f22974f778e34c77275ea3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8c4b70ffad9a58e06498e1ee024b32024013baae6a426eebc842c6fd585e86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d76acf03a286ab810d742ace3efc4431b4779a9211c7c4627605b42c9d8d30d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904d18830fe15d89401eb5aca68762e1d2c790a80b7f07a59efcf0a3fc1d6d4a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf970d0b7665b8f6718e2292493b8ac314a1290ef2462a79972c1abe7fbfe74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightHadoopClusterStorageAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ca5d1e4d0d24b6cc79dcd6611b46ef62cd23cda5015315388a349dd435190f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d35949f4bb8f10bdec2de1f391234fbfc5e1d6e5e90383379ec81a41376625(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b17b7e4807ec7f929e478fd01283bf00c1fde8fcc5260b1201395f1c794281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e583fe19bdaf3d8df14b057a952c6d3016d1efd0d7428c2e23c9a9286232df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086c5abcf2949d021e81a15d043aa463316baad1b884176fe673ec7f8a94b85b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0775c76350f523ce65ed46fbac3199b6c90ec6e5789b43dd8c593122c7e0d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterStorageAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57669a53667c01698e365fedf41921d843462c1bfe63853c9b3f11e40114a2b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac7b4fdfac739eae03254f94a6e3d0e31a1ee643833e3136f16c74d0a2a949f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1dbf72545e07c9154126c446bcfc7d098595d7e63e668602e368c5f60cf545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a27bf2e827deff52ecb5e90073b1036c438c42c23cb3509cc34dd5f46b7912(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c3d5eb56ea22f86708cd41e939c0869d00b716fd895d3aa0dd90f26243ac77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e2cb945124b6400e8651a0880c4e2999b256c36d41bd18305797f307ad6d4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1dd8bbda04ec77dd2b3ad9cf237b7fe14d224efc992a40bc334d350ad7d6e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightHadoopClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
