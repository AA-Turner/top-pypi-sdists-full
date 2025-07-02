r'''
# `azurerm_hdinsight_interactive_query_cluster`

Refer to the Terraform Registry for docs: [`azurerm_hdinsight_interactive_query_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster).
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


class HdinsightInteractiveQueryCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster azurerm_hdinsight_interactive_query_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_version: builtins.str,
        component_version: typing.Union["HdinsightInteractiveQueryClusterComponentVersion", typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightInteractiveQueryClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightInteractiveQueryClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterComputeIsolation", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extension: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_min_version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster azurerm_hdinsight_interactive_query_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#cluster_version HdinsightInteractiveQueryCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#component_version HdinsightInteractiveQueryCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#gateway HdinsightInteractiveQueryCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#location HdinsightInteractiveQueryCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#resource_group_name HdinsightInteractiveQueryCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#roles HdinsightInteractiveQueryCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tier HdinsightInteractiveQueryCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#compute_isolation HdinsightInteractiveQueryCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#disk_encryption HdinsightInteractiveQueryCluster#disk_encryption}
        :param encryption_in_transit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_in_transit_enabled HdinsightInteractiveQueryCluster#encryption_in_transit_enabled}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#extension HdinsightInteractiveQueryCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#id HdinsightInteractiveQueryCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#metastores HdinsightInteractiveQueryCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#monitor HdinsightInteractiveQueryCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#network HdinsightInteractiveQueryCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_link_configuration HdinsightInteractiveQueryCluster#private_link_configuration}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#security_profile HdinsightInteractiveQueryCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account HdinsightInteractiveQueryCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account_gen2 HdinsightInteractiveQueryCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tags HdinsightInteractiveQueryCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#timeouts HdinsightInteractiveQueryCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tls_min_version HdinsightInteractiveQueryCluster#tls_min_version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89afd3d05fa80ad0488d2f49934ca37b6fb9756e840a8075c1c4c93e55f11c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HdinsightInteractiveQueryClusterConfig(
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
        '''Generates CDKTF code for importing a HdinsightInteractiveQueryCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HdinsightInteractiveQueryCluster to import.
        :param import_from_id: The id of the existing HdinsightInteractiveQueryCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HdinsightInteractiveQueryCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6bdcb6d9f62a728598ce2365399b143df90e6fc8dd0d346db15b7382eb596b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putComponentVersion")
    def put_component_version(self, *, interactive_hive: builtins.str) -> None:
        '''
        :param interactive_hive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#interactive_hive HdinsightInteractiveQueryCluster#interactive_hive}.
        '''
        value = HdinsightInteractiveQueryClusterComponentVersion(
            interactive_hive=interactive_hive
        )

        return typing.cast(None, jsii.invoke(self, "putComponentVersion", [value]))

    @jsii.member(jsii_name="putComputeIsolation")
    def put_compute_isolation(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#compute_isolation_enabled HdinsightInteractiveQueryCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#host_sku HdinsightInteractiveQueryCluster#host_sku}.
        '''
        value = HdinsightInteractiveQueryClusterComputeIsolation(
            compute_isolation_enabled=compute_isolation_enabled, host_sku=host_sku
        )

        return typing.cast(None, jsii.invoke(self, "putComputeIsolation", [value]))

    @jsii.member(jsii_name="putDiskEncryption")
    def put_disk_encryption(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5431b34c711f80d9cfb283ef736b7d4f1d02127acc91b8d883ba7995ae80c2a2)
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
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#log_analytics_workspace_id HdinsightInteractiveQueryCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary_key HdinsightInteractiveQueryCluster#primary_key}.
        '''
        value = HdinsightInteractiveQueryClusterExtension(
            log_analytics_workspace_id=log_analytics_workspace_id,
            primary_key=primary_key,
        )

        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putGateway")
    def put_gateway(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        value = HdinsightInteractiveQueryClusterGateway(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putGateway", [value]))

    @jsii.member(jsii_name="putMetastores")
    def put_metastores(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ambari HdinsightInteractiveQueryCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#hive HdinsightInteractiveQueryCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#oozie HdinsightInteractiveQueryCluster#oozie}
        '''
        value = HdinsightInteractiveQueryClusterMetastores(
            ambari=ambari, hive=hive, oozie=oozie
        )

        return typing.cast(None, jsii.invoke(self, "putMetastores", [value]))

    @jsii.member(jsii_name="putMonitor")
    def put_monitor(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#log_analytics_workspace_id HdinsightInteractiveQueryCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary_key HdinsightInteractiveQueryCluster#primary_key}.
        '''
        value = HdinsightInteractiveQueryClusterMonitor(
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
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#connection_direction HdinsightInteractiveQueryCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_link_enabled HdinsightInteractiveQueryCluster#private_link_enabled}.
        '''
        value = HdinsightInteractiveQueryClusterNetwork(
            connection_direction=connection_direction,
            private_link_enabled=private_link_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putPrivateLinkConfiguration")
    def put_private_link_configuration(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#group_id HdinsightInteractiveQueryCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ip_configuration HdinsightInteractiveQueryCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        '''
        value = HdinsightInteractiveQueryClusterPrivateLinkConfiguration(
            group_id=group_id, ip_configuration=ip_configuration, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateLinkConfiguration", [value]))

    @jsii.member(jsii_name="putRoles")
    def put_roles(
        self,
        *,
        head_node: typing.Union["HdinsightInteractiveQueryClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightInteractiveQueryClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#head_node HdinsightInteractiveQueryCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#worker_node HdinsightInteractiveQueryCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#zookeeper_node HdinsightInteractiveQueryCluster#zookeeper_node}
        '''
        value = HdinsightInteractiveQueryClusterRoles(
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
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#aadds_resource_id HdinsightInteractiveQueryCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_name HdinsightInteractiveQueryCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_username HdinsightInteractiveQueryCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_user_password HdinsightInteractiveQueryCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ldaps_urls HdinsightInteractiveQueryCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#msi_resource_id HdinsightInteractiveQueryCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#cluster_users_group_dns HdinsightInteractiveQueryCluster#cluster_users_group_dns}.
        '''
        value = HdinsightInteractiveQueryClusterSecurityProfile(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d7bf56e4cd0343c693f57c37a5b58e975583bff53b1a237c1ae3c9e5ddffa9)
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
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#filesystem_id HdinsightInteractiveQueryCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#is_default HdinsightInteractiveQueryCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#managed_identity_resource_id HdinsightInteractiveQueryCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_resource_id HdinsightInteractiveQueryCluster#storage_resource_id}.
        '''
        value = HdinsightInteractiveQueryClusterStorageAccountGen2(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#create HdinsightInteractiveQueryCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#delete HdinsightInteractiveQueryCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#read HdinsightInteractiveQueryCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#update HdinsightInteractiveQueryCluster#update}.
        '''
        value = HdinsightInteractiveQueryClusterTimeouts(
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
    ) -> "HdinsightInteractiveQueryClusterComponentVersionOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterComponentVersionOutputReference", jsii.get(self, "componentVersion"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolation")
    def compute_isolation(
        self,
    ) -> "HdinsightInteractiveQueryClusterComputeIsolationOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterComputeIsolationOutputReference", jsii.get(self, "computeIsolation"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> "HdinsightInteractiveQueryClusterDiskEncryptionList":
        return typing.cast("HdinsightInteractiveQueryClusterDiskEncryptionList", jsii.get(self, "diskEncryption"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> "HdinsightInteractiveQueryClusterExtensionOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterExtensionOutputReference", jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> "HdinsightInteractiveQueryClusterGatewayOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterGatewayOutputReference", jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="httpsEndpoint")
    def https_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="metastores")
    def metastores(self) -> "HdinsightInteractiveQueryClusterMetastoresOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterMetastoresOutputReference", jsii.get(self, "metastores"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> "HdinsightInteractiveQueryClusterMonitorOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterMonitorOutputReference", jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "HdinsightInteractiveQueryClusterNetworkOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfiguration")
    def private_link_configuration(
        self,
    ) -> "HdinsightInteractiveQueryClusterPrivateLinkConfigurationOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterPrivateLinkConfigurationOutputReference", jsii.get(self, "privateLinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> "HdinsightInteractiveQueryClusterRolesOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterRolesOutputReference", jsii.get(self, "roles"))

    @builtins.property
    @jsii.member(jsii_name="securityProfile")
    def security_profile(
        self,
    ) -> "HdinsightInteractiveQueryClusterSecurityProfileOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterSecurityProfileOutputReference", jsii.get(self, "securityProfile"))

    @builtins.property
    @jsii.member(jsii_name="sshEndpoint")
    def ssh_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "HdinsightInteractiveQueryClusterStorageAccountList":
        return typing.cast("HdinsightInteractiveQueryClusterStorageAccountList", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2")
    def storage_account_gen2(
        self,
    ) -> "HdinsightInteractiveQueryClusterStorageAccountGen2OutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterStorageAccountGen2OutputReference", jsii.get(self, "storageAccountGen2"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HdinsightInteractiveQueryClusterTimeoutsOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="componentVersionInput")
    def component_version_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterComponentVersion"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterComponentVersion"], jsii.get(self, "componentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="computeIsolationInput")
    def compute_isolation_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterComputeIsolation"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterComputeIsolation"], jsii.get(self, "computeIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterDiskEncryption"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterDiskEncryption"]]], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInTransitEnabledInput")
    def encryption_in_transit_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionInTransitEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterExtension"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterExtension"], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterGateway"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterGateway"], jsii.get(self, "gatewayInput"))

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
    def metastores_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterMetastores"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMetastores"], jsii.get(self, "metastoresInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterMonitor"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMonitor"], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterNetwork"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkConfigurationInput")
    def private_link_configuration_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterPrivateLinkConfiguration"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterPrivateLinkConfiguration"], jsii.get(self, "privateLinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional["HdinsightInteractiveQueryClusterRoles"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterRoles"], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileInput")
    def security_profile_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterSecurityProfile"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterSecurityProfile"], jsii.get(self, "securityProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountGen2Input")
    def storage_account_gen2_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterStorageAccountGen2"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterStorageAccountGen2"], jsii.get(self, "storageAccountGen2Input"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterStorageAccount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterStorageAccount"]]], jsii.get(self, "storageAccountInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightInteractiveQueryClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HdinsightInteractiveQueryClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__03b848c612d9404801ac762fa4c57977dbe701519d9fa239e1fa2a9496298428)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da165493bb58bdbb7058a062473e54f836b2a067351fecce2310e7cc52dd69ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionInTransitEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7314af08240a8c129919ac8efa1d967fa011242e7a0d746cdf4dcc42bf72013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e1404787899200be84354fce0eb99138e038b9218db7a1b3ab0cb8be5b22ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68270cecaa94ba25df66cdda92c4099edf5b19b70fd1c715696f0239ba483652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3cb58499c41d698f0f7d799730f5cd121ab30857543b2240b30b298a83761b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4278c78c0b2d4d0930bbcd647bcc5ff7d9ffd9fe5dfa44eb4034eed82c7c13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8427539cc51d23128e0e6907b8266b559c047e25d0f8ee35971557b1d877eb99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsMinVersion")
    def tls_min_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsMinVersion"))

    @tls_min_version.setter
    def tls_min_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f509b9a9aacec691d5f34878aed64c7426a04c80bb46c1f79c1c4b92bb24f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsMinVersion", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterComponentVersion",
    jsii_struct_bases=[],
    name_mapping={"interactive_hive": "interactiveHive"},
)
class HdinsightInteractiveQueryClusterComponentVersion:
    def __init__(self, *, interactive_hive: builtins.str) -> None:
        '''
        :param interactive_hive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#interactive_hive HdinsightInteractiveQueryCluster#interactive_hive}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bd4d80c070e8f344a1d0de1c27b5db8f1b813d0d681ff60b74f22b55faed56)
            check_type(argname="argument interactive_hive", value=interactive_hive, expected_type=type_hints["interactive_hive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interactive_hive": interactive_hive,
        }

    @builtins.property
    def interactive_hive(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#interactive_hive HdinsightInteractiveQueryCluster#interactive_hive}.'''
        result = self._values.get("interactive_hive")
        assert result is not None, "Required property 'interactive_hive' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterComponentVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterComponentVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterComponentVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac47157365a7a1edb8a62455b77daaea5c9a705eabc20276505a47fcaa99837)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="interactiveHiveInput")
    def interactive_hive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interactiveHiveInput"))

    @builtins.property
    @jsii.member(jsii_name="interactiveHive")
    def interactive_hive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interactiveHive"))

    @interactive_hive.setter
    def interactive_hive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1edad14b073a35a280925e71b0855ef6a6909a63776bbe373df276c440b1d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interactiveHive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterComponentVersion]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterComponentVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterComponentVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44739d2384a4fc2ad3e7ecf026c0b4ce5095b7d84124e312a0f5e1799bbe79e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterComputeIsolation",
    jsii_struct_bases=[],
    name_mapping={
        "compute_isolation_enabled": "computeIsolationEnabled",
        "host_sku": "hostSku",
    },
)
class HdinsightInteractiveQueryClusterComputeIsolation:
    def __init__(
        self,
        *,
        compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_sku: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compute_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#compute_isolation_enabled HdinsightInteractiveQueryCluster#compute_isolation_enabled}.
        :param host_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#host_sku HdinsightInteractiveQueryCluster#host_sku}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb02d02b6864a3dbe2a8906a28abd426ab9185b64e8b8fb3b39a16cb814a1ad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#compute_isolation_enabled HdinsightInteractiveQueryCluster#compute_isolation_enabled}.'''
        result = self._values.get("compute_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#host_sku HdinsightInteractiveQueryCluster#host_sku}.'''
        result = self._values.get("host_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterComputeIsolation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterComputeIsolationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterComputeIsolationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b904886d5595b4775876dec981cd94981872c5f752ba815eca27b69c774c9490)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3d66b16bf8be2e0564baeb464598a459892c25660407ab6832e3122a0b779ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostSku")
    def host_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostSku"))

    @host_sku.setter
    def host_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3821250fe0e4da016686130c8a2d06ca230ea83e41eb7e1d50b799850e6f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterComputeIsolation]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterComputeIsolation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterComputeIsolation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83af40f83bee08bbc1f4355568e283d511ba588ea06326f0523866cd519d41a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterConfig",
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
    },
)
class HdinsightInteractiveQueryClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        component_version: typing.Union[HdinsightInteractiveQueryClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
        gateway: typing.Union["HdinsightInteractiveQueryClusterGateway", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        roles: typing.Union["HdinsightInteractiveQueryClusterRoles", typing.Dict[builtins.str, typing.Any]],
        tier: builtins.str,
        compute_isolation: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
        disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterDiskEncryption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extension: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        metastores: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastores", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        private_link_configuration: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterPrivateLinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_profile: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterSecurityProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_gen2: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterStorageAccountGen2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#cluster_version HdinsightInteractiveQueryCluster#cluster_version}.
        :param component_version: component_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#component_version HdinsightInteractiveQueryCluster#component_version}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#gateway HdinsightInteractiveQueryCluster#gateway}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#location HdinsightInteractiveQueryCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#resource_group_name HdinsightInteractiveQueryCluster#resource_group_name}.
        :param roles: roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#roles HdinsightInteractiveQueryCluster#roles}
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tier HdinsightInteractiveQueryCluster#tier}.
        :param compute_isolation: compute_isolation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#compute_isolation HdinsightInteractiveQueryCluster#compute_isolation}
        :param disk_encryption: disk_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#disk_encryption HdinsightInteractiveQueryCluster#disk_encryption}
        :param encryption_in_transit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_in_transit_enabled HdinsightInteractiveQueryCluster#encryption_in_transit_enabled}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#extension HdinsightInteractiveQueryCluster#extension}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#id HdinsightInteractiveQueryCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metastores: metastores block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#metastores HdinsightInteractiveQueryCluster#metastores}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#monitor HdinsightInteractiveQueryCluster#monitor}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#network HdinsightInteractiveQueryCluster#network}
        :param private_link_configuration: private_link_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_link_configuration HdinsightInteractiveQueryCluster#private_link_configuration}
        :param security_profile: security_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#security_profile HdinsightInteractiveQueryCluster#security_profile}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account HdinsightInteractiveQueryCluster#storage_account}
        :param storage_account_gen2: storage_account_gen2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account_gen2 HdinsightInteractiveQueryCluster#storage_account_gen2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tags HdinsightInteractiveQueryCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#timeouts HdinsightInteractiveQueryCluster#timeouts}
        :param tls_min_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tls_min_version HdinsightInteractiveQueryCluster#tls_min_version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(component_version, dict):
            component_version = HdinsightInteractiveQueryClusterComponentVersion(**component_version)
        if isinstance(gateway, dict):
            gateway = HdinsightInteractiveQueryClusterGateway(**gateway)
        if isinstance(roles, dict):
            roles = HdinsightInteractiveQueryClusterRoles(**roles)
        if isinstance(compute_isolation, dict):
            compute_isolation = HdinsightInteractiveQueryClusterComputeIsolation(**compute_isolation)
        if isinstance(extension, dict):
            extension = HdinsightInteractiveQueryClusterExtension(**extension)
        if isinstance(metastores, dict):
            metastores = HdinsightInteractiveQueryClusterMetastores(**metastores)
        if isinstance(monitor, dict):
            monitor = HdinsightInteractiveQueryClusterMonitor(**monitor)
        if isinstance(network, dict):
            network = HdinsightInteractiveQueryClusterNetwork(**network)
        if isinstance(private_link_configuration, dict):
            private_link_configuration = HdinsightInteractiveQueryClusterPrivateLinkConfiguration(**private_link_configuration)
        if isinstance(security_profile, dict):
            security_profile = HdinsightInteractiveQueryClusterSecurityProfile(**security_profile)
        if isinstance(storage_account_gen2, dict):
            storage_account_gen2 = HdinsightInteractiveQueryClusterStorageAccountGen2(**storage_account_gen2)
        if isinstance(timeouts, dict):
            timeouts = HdinsightInteractiveQueryClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd71ac3660fba0bbf641a41e01a2f599fe3aaec8aa4bf998af77f11bea901329)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#cluster_version HdinsightInteractiveQueryCluster#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def component_version(self) -> HdinsightInteractiveQueryClusterComponentVersion:
        '''component_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#component_version HdinsightInteractiveQueryCluster#component_version}
        '''
        result = self._values.get("component_version")
        assert result is not None, "Required property 'component_version' is missing"
        return typing.cast(HdinsightInteractiveQueryClusterComponentVersion, result)

    @builtins.property
    def gateway(self) -> "HdinsightInteractiveQueryClusterGateway":
        '''gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#gateway HdinsightInteractiveQueryCluster#gateway}
        '''
        result = self._values.get("gateway")
        assert result is not None, "Required property 'gateway' is missing"
        return typing.cast("HdinsightInteractiveQueryClusterGateway", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#location HdinsightInteractiveQueryCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#resource_group_name HdinsightInteractiveQueryCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> "HdinsightInteractiveQueryClusterRoles":
        '''roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#roles HdinsightInteractiveQueryCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast("HdinsightInteractiveQueryClusterRoles", result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tier HdinsightInteractiveQueryCluster#tier}.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_isolation(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterComputeIsolation]:
        '''compute_isolation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#compute_isolation HdinsightInteractiveQueryCluster#compute_isolation}
        '''
        result = self._values.get("compute_isolation")
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterComputeIsolation], result)

    @builtins.property
    def disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterDiskEncryption"]]]:
        '''disk_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#disk_encryption HdinsightInteractiveQueryCluster#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterDiskEncryption"]]], result)

    @builtins.property
    def encryption_in_transit_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_in_transit_enabled HdinsightInteractiveQueryCluster#encryption_in_transit_enabled}.'''
        result = self._values.get("encryption_in_transit_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extension(self) -> typing.Optional["HdinsightInteractiveQueryClusterExtension"]:
        '''extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#extension HdinsightInteractiveQueryCluster#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterExtension"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#id HdinsightInteractiveQueryCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastores(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterMetastores"]:
        '''metastores block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#metastores HdinsightInteractiveQueryCluster#metastores}
        '''
        result = self._values.get("metastores")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMetastores"], result)

    @builtins.property
    def monitor(self) -> typing.Optional["HdinsightInteractiveQueryClusterMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#monitor HdinsightInteractiveQueryCluster#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMonitor"], result)

    @builtins.property
    def network(self) -> typing.Optional["HdinsightInteractiveQueryClusterNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#network HdinsightInteractiveQueryCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterNetwork"], result)

    @builtins.property
    def private_link_configuration(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterPrivateLinkConfiguration"]:
        '''private_link_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_link_configuration HdinsightInteractiveQueryCluster#private_link_configuration}
        '''
        result = self._values.get("private_link_configuration")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterPrivateLinkConfiguration"], result)

    @builtins.property
    def security_profile(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterSecurityProfile"]:
        '''security_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#security_profile HdinsightInteractiveQueryCluster#security_profile}
        '''
        result = self._values.get("security_profile")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterSecurityProfile"], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterStorageAccount"]]]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account HdinsightInteractiveQueryCluster#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterStorageAccount"]]], result)

    @builtins.property
    def storage_account_gen2(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterStorageAccountGen2"]:
        '''storage_account_gen2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account_gen2 HdinsightInteractiveQueryCluster#storage_account_gen2}
        '''
        result = self._values.get("storage_account_gen2")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterStorageAccountGen2"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tags HdinsightInteractiveQueryCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HdinsightInteractiveQueryClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#timeouts HdinsightInteractiveQueryCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterTimeouts"], result)

    @builtins.property
    def tls_min_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#tls_min_version HdinsightInteractiveQueryCluster#tls_min_version}.'''
        result = self._values.get("tls_min_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterDiskEncryption",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_algorithm": "encryptionAlgorithm",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
        "key_vault_key_id": "keyVaultKeyId",
        "key_vault_managed_identity_id": "keyVaultManagedIdentityId",
    },
)
class HdinsightInteractiveQueryClusterDiskEncryption:
    def __init__(
        self,
        *,
        encryption_algorithm: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_algorithm HdinsightInteractiveQueryCluster#encryption_algorithm}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_at_host_enabled HdinsightInteractiveQueryCluster#encryption_at_host_enabled}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#key_vault_key_id HdinsightInteractiveQueryCluster#key_vault_key_id}.
        :param key_vault_managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#key_vault_managed_identity_id HdinsightInteractiveQueryCluster#key_vault_managed_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dad84457ecbdbe016714c310680c7c6913aff92ed9e43002e4c9614b9930c4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_algorithm HdinsightInteractiveQueryCluster#encryption_algorithm}.'''
        result = self._values.get("encryption_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#encryption_at_host_enabled HdinsightInteractiveQueryCluster#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#key_vault_key_id HdinsightInteractiveQueryCluster#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_managed_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#key_vault_managed_identity_id HdinsightInteractiveQueryCluster#key_vault_managed_identity_id}.'''
        result = self._values.get("key_vault_managed_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterDiskEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterDiskEncryptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterDiskEncryptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90f8cee8f8495aae407cb12ced2b69a17fac4b02bcd151e62b16a065e35e461b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightInteractiveQueryClusterDiskEncryptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc4bedeae6f83caf1afdd9250cb224ddc67b1473ea17a09aa23f7c53ee0b8f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightInteractiveQueryClusterDiskEncryptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f360a316d1b7d30279d01a7206ccf65c2aaa626f3c984670e5e4a195a8bc41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa6103ab35e837406fbb5738b189b0217b21c7f5330ebe008a5bc912c320b0a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8ac05f4ddf835a364ecd050b2bfd2a5e2505436415f01affd56aba88648f0b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterDiskEncryption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterDiskEncryption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterDiskEncryption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ceb0b5d25a2ee4fa526573a9ae4c979cd20f3a989aad3891d409292c90fe1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterDiskEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterDiskEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5830dbd355763876a29ed4e8c65579b0ec421f49da57a6b095846ee9b82acab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec4a3aeff8a85c0d19f9ab739be7505814b6b317e487a3cfc716148d031b6e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f8294bc838d84fa21a14ad46e8a7a1029daf76338aca4d27296b031e83eff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56170ef994ee35e736401c9b2f1847f00573d9df806be5133586777f5bbceadd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultManagedIdentityId")
    def key_vault_managed_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultManagedIdentityId"))

    @key_vault_managed_identity_id.setter
    def key_vault_managed_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6d1481a84738a969efc1e0b6027409eec4f7985d6c883bf39660e0bbc5be6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultManagedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterDiskEncryption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterDiskEncryption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterDiskEncryption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60743d8d4792b1c01fbac8c6fdfb9d89238ef5c3f2176427b35042feecf02337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterExtension",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightInteractiveQueryClusterExtension:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#log_analytics_workspace_id HdinsightInteractiveQueryCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary_key HdinsightInteractiveQueryCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba3200f575fbbcf99c33f9bef0ab3fbdaf4ee627aa106b5b36089a1aa81af11)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#log_analytics_workspace_id HdinsightInteractiveQueryCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary_key HdinsightInteractiveQueryCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e4bac2ea6873e61cb69e184df48bbcf45b349195b171cff6878c39643364c9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c56df940b3324c5733d3914143eac566c4951306cb5a80da25b0678177effa62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68317d398896ed1e073f72beba8f659937751bd04d9eb619d1977ecc95e29f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterExtension]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterExtension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterExtension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1511353673fed4cc071e40fa7f8b1a176b8afbb3bb7d2005627f98780109beb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterGateway",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class HdinsightInteractiveQueryClusterGateway:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf713e76c9c48d3f8b07cb5df660fb6b50a35ba5772e16b68749626e18c3458)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7915f536e29caecdbdff220c9019609d690c1e012a48d6773952e7bade00fb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae3a1fcdc091fdf5afbf0eafddb0d19fcceb622b6a0cb18155bc8f51f89faed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e943446bc610a7a53ab1405ad880a8ea49a5e71c8ae70eee496bd9bcf3297215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterGateway]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e68a28d14b0620694efa89b20ead59bafa167ae0c63e1fa7361f45f059bdb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastores",
    jsii_struct_bases=[],
    name_mapping={"ambari": "ambari", "hive": "hive", "oozie": "oozie"},
)
class HdinsightInteractiveQueryClusterMetastores:
    def __init__(
        self,
        *,
        ambari: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastoresAmbari", typing.Dict[builtins.str, typing.Any]]] = None,
        hive: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastoresHive", typing.Dict[builtins.str, typing.Any]]] = None,
        oozie: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterMetastoresOozie", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ambari: ambari block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ambari HdinsightInteractiveQueryCluster#ambari}
        :param hive: hive block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#hive HdinsightInteractiveQueryCluster#hive}
        :param oozie: oozie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#oozie HdinsightInteractiveQueryCluster#oozie}
        '''
        if isinstance(ambari, dict):
            ambari = HdinsightInteractiveQueryClusterMetastoresAmbari(**ambari)
        if isinstance(hive, dict):
            hive = HdinsightInteractiveQueryClusterMetastoresHive(**hive)
        if isinstance(oozie, dict):
            oozie = HdinsightInteractiveQueryClusterMetastoresOozie(**oozie)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9a77fa4eb51d1634225c4ea30fb3aba9cd2bf23ec9c503b29d68e9275475c6)
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
    def ambari(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterMetastoresAmbari"]:
        '''ambari block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ambari HdinsightInteractiveQueryCluster#ambari}
        '''
        result = self._values.get("ambari")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMetastoresAmbari"], result)

    @builtins.property
    def hive(self) -> typing.Optional["HdinsightInteractiveQueryClusterMetastoresHive"]:
        '''hive block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#hive HdinsightInteractiveQueryCluster#hive}
        '''
        result = self._values.get("hive")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMetastoresHive"], result)

    @builtins.property
    def oozie(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterMetastoresOozie"]:
        '''oozie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#oozie HdinsightInteractiveQueryCluster#oozie}
        '''
        result = self._values.get("oozie")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterMetastoresOozie"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterMetastores(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresAmbari",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightInteractiveQueryClusterMetastoresAmbari:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88148511435c219d84a04e00ad574599606b51c0766973c2682c0fe114de4e88)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterMetastoresAmbari(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterMetastoresAmbariOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresAmbariOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4fc57ae55b2d8f2b079157415c075f91e908681ea6ae5aa273cb924984601e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a13b466a9b03669a73235d1e97b553c6a72a874d659f490c0cb6f99085eb0341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bf6ac2f845d7bf04b8fb19f9c4842aa6c2157b961d2561612339093a7721f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dba585c6937c27ea652e95676c42b41149c0468538c0c01bda6fd21c165f4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27885c63e018bd8149d7f4189cb5c43f1ad008bd888f7853de02c797f8f274c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastoresAmbari], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterMetastoresAmbari],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10f9cd535cd88c64ebff2385c5cab98f4333a837b00e8ece94790664b7ad438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresHive",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightInteractiveQueryClusterMetastoresHive:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6750748e378d40db8fb7fb77663612ee65c1089129d186e537661cba5ea008)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterMetastoresHive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterMetastoresHiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresHiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8bccbc975eae8dca20f8ca2f87dd61af13e60a505ba689e48ff2e95b8c47da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23e2ea80469b499abbf753131064ea300dbacd62e65bc5c40b6a8829a5b765c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a20d5bc1473d1fbb3714bcb6d1db75ef2395ffeed564cf79376fd95712b93bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b83d1d451227b81bdb799283ff44d08b807b26e692a7ad6915ede8009adbfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7611ca0fbda369ef78a8f694ff411463b493660abb0f126351030515a8a6461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastoresHive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterMetastoresHive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30012f67d63d9e579b3025676ade7e25535b9f39dce6f8110086f824ae2ab2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresOozie",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class HdinsightInteractiveQueryClusterMetastoresOozie:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b54f156ebe55ea22bcbabd58b6f733df70a810098d413535623449109f39c5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterMetastoresOozie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterMetastoresOozieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresOozieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5519398b9c784a2d36d90fd373c997981725268c846413810b1655f5f6d22e05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__622d7adf6ddcd5e3481beaa01d367807fade3202056cbc490ac336605f085900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e7f8b7674e68ccd0b8b73a8ec5b7faec6be2d02461a51d75fb4f75b62b5656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e608ed6a71b72e02c6c39142f04c5425fad54f0487bbbd65f13a0586b4900ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3677a740b9d39c951fad1d6ac94f028b067cb350eb04e45e43b1041fc3f6616c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastoresOozie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterMetastoresOozie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6bfba4e4d29f25391cbffa177dd478f114227f3a2131c664de9b48c56e2b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterMetastoresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMetastoresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89738712ce6d91ecda8186ec23f00be8d0f5a54e3d2d55776e194783f8fccdc5)
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        value = HdinsightInteractiveQueryClusterMetastoresAmbari(
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        value = HdinsightInteractiveQueryClusterMetastoresHive(
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
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#database_name HdinsightInteractiveQueryCluster#database_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#server HdinsightInteractiveQueryCluster#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        '''
        value = HdinsightInteractiveQueryClusterMetastoresOozie(
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
    def ambari(self) -> HdinsightInteractiveQueryClusterMetastoresAmbariOutputReference:
        return typing.cast(HdinsightInteractiveQueryClusterMetastoresAmbariOutputReference, jsii.get(self, "ambari"))

    @builtins.property
    @jsii.member(jsii_name="hive")
    def hive(self) -> HdinsightInteractiveQueryClusterMetastoresHiveOutputReference:
        return typing.cast(HdinsightInteractiveQueryClusterMetastoresHiveOutputReference, jsii.get(self, "hive"))

    @builtins.property
    @jsii.member(jsii_name="oozie")
    def oozie(self) -> HdinsightInteractiveQueryClusterMetastoresOozieOutputReference:
        return typing.cast(HdinsightInteractiveQueryClusterMetastoresOozieOutputReference, jsii.get(self, "oozie"))

    @builtins.property
    @jsii.member(jsii_name="ambariInput")
    def ambari_input(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastoresAmbari]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastoresAmbari], jsii.get(self, "ambariInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveInput")
    def hive_input(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastoresHive]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastoresHive], jsii.get(self, "hiveInput"))

    @builtins.property
    @jsii.member(jsii_name="oozieInput")
    def oozie_input(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastoresOozie]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastoresOozie], jsii.get(self, "oozieInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMetastores]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMetastores], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterMetastores],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1708bf398c8692a7c29e30d1606600f2409326c56a3f5e542a57a7734b3a4480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMonitor",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "primary_key": "primaryKey",
    },
)
class HdinsightInteractiveQueryClusterMonitor:
    def __init__(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
        primary_key: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#log_analytics_workspace_id HdinsightInteractiveQueryCluster#log_analytics_workspace_id}.
        :param primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary_key HdinsightInteractiveQueryCluster#primary_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79731f5ddf63245c8960f0fa3f3fda73f2065206136d006163b032bcd7a5460)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
            "primary_key": primary_key,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#log_analytics_workspace_id HdinsightInteractiveQueryCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary_key HdinsightInteractiveQueryCluster#primary_key}.'''
        result = self._values.get("primary_key")
        assert result is not None, "Required property 'primary_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterMonitorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fec1c32a68217efe29881bf88e11afab66778985272f725851aea7cb357915b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a701675e96d766d4e28a4e4f07fa875f7dc3c7e283b615fb8758cf6927f83d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6c47b8b3a3a64f588d057fd724d8042ac6a21b0d1d781f1ec1d698697e2305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterMonitor]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f2941d011917645bbd79cfdbd14a33f24156b0dc7d1a9e6c2ed70b3618d7fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "connection_direction": "connectionDirection",
        "private_link_enabled": "privateLinkEnabled",
    },
)
class HdinsightInteractiveQueryClusterNetwork:
    def __init__(
        self,
        *,
        connection_direction: typing.Optional[builtins.str] = None,
        private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#connection_direction HdinsightInteractiveQueryCluster#connection_direction}.
        :param private_link_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_link_enabled HdinsightInteractiveQueryCluster#private_link_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8430fd20d6b16385a54fbffce37a57dcd21b416c745cd2e98b2c5f6114e2b14b)
            check_type(argname="argument connection_direction", value=connection_direction, expected_type=type_hints["connection_direction"])
            check_type(argname="argument private_link_enabled", value=private_link_enabled, expected_type=type_hints["private_link_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_direction is not None:
            self._values["connection_direction"] = connection_direction
        if private_link_enabled is not None:
            self._values["private_link_enabled"] = private_link_enabled

    @builtins.property
    def connection_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#connection_direction HdinsightInteractiveQueryCluster#connection_direction}.'''
        result = self._values.get("connection_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_link_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_link_enabled HdinsightInteractiveQueryCluster#private_link_enabled}.'''
        result = self._values.get("private_link_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73b968bf23d077ddabc899c69d15764d3df635ea9e002eb02d124b1696a840c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__724ad5e1af999b4a3d0a40a8691ad880c4ac2d3b813a90dfddbe10642cec6cca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd17651ec02347d3dbf8551c2767ee05cfab33a946279bcb45bbfe33a692793a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateLinkEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterNetwork]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bd4d2d561335663ade601a544d405950e54325f0b9a01ed041b09f348803ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterPrivateLinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "ip_configuration": "ipConfiguration",
        "name": "name",
    },
)
class HdinsightInteractiveQueryClusterPrivateLinkConfiguration:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        ip_configuration: typing.Union["HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#group_id HdinsightInteractiveQueryCluster#group_id}.
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ip_configuration HdinsightInteractiveQueryCluster#ip_configuration}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        '''
        if isinstance(ip_configuration, dict):
            ip_configuration = HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration(**ip_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3823a1c29e8edf589be56af1701433efa0c9785b5ddebfe99b5550da67ae16ac)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#group_id HdinsightInteractiveQueryCluster#group_id}.'''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_configuration(
        self,
    ) -> "HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration":
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ip_configuration HdinsightInteractiveQueryCluster#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        assert result is not None, "Required property 'ip_configuration' is missing"
        return typing.cast("HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterPrivateLinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "primary": "primary",
        "private_ip_address": "privateIpAddress",
        "private_ip_allocation_method": "privateIpAllocationMethod",
        "subnet_id": "subnetId",
    },
)
class HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration:
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary HdinsightInteractiveQueryCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_ip_address HdinsightInteractiveQueryCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_ip_allocation_method HdinsightInteractiveQueryCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fca85c3f93c12c031e0287494385da74a2cd6eda3830d73b58180244f3f9482)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary HdinsightInteractiveQueryCluster#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_ip_address HdinsightInteractiveQueryCluster#private_ip_address}.'''
        result = self._values.get("private_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_allocation_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_ip_allocation_method HdinsightInteractiveQueryCluster#private_ip_allocation_method}.'''
        result = self._values.get("private_ip_allocation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bbee588a54de68f7a0cda7e0ff426f27e527d68e1d7c17bb580490d7b21f2e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa9b996730f8508421ca3d3f080a40cb0e79cd1c5af8eb7eb402c0add61eb33a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a9105d076ee6044aa87cac6de91fd3e77461264187cbed3af02877e239e95b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @private_ip_address.setter
    def private_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc38b6f507c7f1f80606885344996e25930947ec2c0cbbfd64bc2aa552f0b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpAllocationMethod")
    def private_ip_allocation_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAllocationMethod"))

    @private_ip_allocation_method.setter
    def private_ip_allocation_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6e024a2b9acdac451640cf2eac5bc8a17222bedf983e8bf7cb5d80be9e1835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpAllocationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ddc53e802da8c7623e330a8924ed31941c65beb7d2c5495a44daec0b8cafbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e298dcde30a0b39df656a309d470a0500b1a496a3d7114a72c7e7e6d74324a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterPrivateLinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterPrivateLinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6aaf6f177a190712e82140e2dd25aa2f3bf957a85ae8ddef0bc44119ef4333)
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#primary HdinsightInteractiveQueryCluster#primary}.
        :param private_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_ip_address HdinsightInteractiveQueryCluster#private_ip_address}.
        :param private_ip_allocation_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#private_ip_allocation_method HdinsightInteractiveQueryCluster#private_ip_allocation_method}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        '''
        value = HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration(
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
    ) -> HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfigurationOutputReference:
        return typing.cast(HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfigurationOutputReference, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration], jsii.get(self, "ipConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__482afe455d0987d037ef0feecdd26beddb2fab80f9ea67da64ff9d4a1893b673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124d0ab6e1206004620244cab86b1098dc33b8c6f0bba21f0050715bbe09fbb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfiguration]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c76740ce0ef9a73c20f250a995fd98851877c368ccccd4eabb9c05e27d9387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRoles",
    jsii_struct_bases=[],
    name_mapping={
        "head_node": "headNode",
        "worker_node": "workerNode",
        "zookeeper_node": "zookeeperNode",
    },
)
class HdinsightInteractiveQueryClusterRoles:
    def __init__(
        self,
        *,
        head_node: typing.Union["HdinsightInteractiveQueryClusterRolesHeadNode", typing.Dict[builtins.str, typing.Any]],
        worker_node: typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNode", typing.Dict[builtins.str, typing.Any]],
        zookeeper_node: typing.Union["HdinsightInteractiveQueryClusterRolesZookeeperNode", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param head_node: head_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#head_node HdinsightInteractiveQueryCluster#head_node}
        :param worker_node: worker_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#worker_node HdinsightInteractiveQueryCluster#worker_node}
        :param zookeeper_node: zookeeper_node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#zookeeper_node HdinsightInteractiveQueryCluster#zookeeper_node}
        '''
        if isinstance(head_node, dict):
            head_node = HdinsightInteractiveQueryClusterRolesHeadNode(**head_node)
        if isinstance(worker_node, dict):
            worker_node = HdinsightInteractiveQueryClusterRolesWorkerNode(**worker_node)
        if isinstance(zookeeper_node, dict):
            zookeeper_node = HdinsightInteractiveQueryClusterRolesZookeeperNode(**zookeeper_node)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d8be0c2eeba0f49e8337a47185e1f6f653be8b3ccea4ff5a7cc52310035c3a)
            check_type(argname="argument head_node", value=head_node, expected_type=type_hints["head_node"])
            check_type(argname="argument worker_node", value=worker_node, expected_type=type_hints["worker_node"])
            check_type(argname="argument zookeeper_node", value=zookeeper_node, expected_type=type_hints["zookeeper_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "head_node": head_node,
            "worker_node": worker_node,
            "zookeeper_node": zookeeper_node,
        }

    @builtins.property
    def head_node(self) -> "HdinsightInteractiveQueryClusterRolesHeadNode":
        '''head_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#head_node HdinsightInteractiveQueryCluster#head_node}
        '''
        result = self._values.get("head_node")
        assert result is not None, "Required property 'head_node' is missing"
        return typing.cast("HdinsightInteractiveQueryClusterRolesHeadNode", result)

    @builtins.property
    def worker_node(self) -> "HdinsightInteractiveQueryClusterRolesWorkerNode":
        '''worker_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#worker_node HdinsightInteractiveQueryCluster#worker_node}
        '''
        result = self._values.get("worker_node")
        assert result is not None, "Required property 'worker_node' is missing"
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNode", result)

    @builtins.property
    def zookeeper_node(self) -> "HdinsightInteractiveQueryClusterRolesZookeeperNode":
        '''zookeeper_node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#zookeeper_node HdinsightInteractiveQueryCluster#zookeeper_node}
        '''
        result = self._values.get("zookeeper_node")
        assert result is not None, "Required property 'zookeeper_node' is missing"
        return typing.cast("HdinsightInteractiveQueryClusterRolesZookeeperNode", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesHeadNode",
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
class HdinsightInteractiveQueryClusterRolesHeadNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2378201588b32c49f78526c545b9f53f0f06630abbc66eedeeb0060adb4823e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesHeadNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesHeadNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesHeadNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5931f1f091430e06337df7cdc70b022a0b5dfb7b28a2c96004784a4198af2048)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9b3178a191bd142efe860bd35fd0a63438768ce905ac56ed6551a41e003b2e)
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
    ) -> "HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsList":
        return typing.cast("HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c552b593a3d44571cd447a6fe68653355488b3e703139bf51a5c162a9220e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80331eb34e08a6cd43b711134dc0cfc8e9436d2424bdef9692dc8907bf50728a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c148c2d2617fbe163f9be058db6fd675140c9ccd84f32ec365a93ab46ff365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa8b4107072c5f4cbc85db91d8796c2fd7674b1b599e31834cdde9361ec5fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b7fad8b2d05ad51f24b791d860ce4796681aa831621f9cb1af3f22c556ac4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61b3931ba7e0aede53f38feb7bb888ef8162921a4de67710fa9e6d679493167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesHeadNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterRolesHeadNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da9a14d4fac417eb162dbaeb47ec8f476e92dff84ff7d3a9acf34699d76a884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#uri HdinsightInteractiveQueryCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#parameters HdinsightInteractiveQueryCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b499e588a5a677bb6f73c8a6faa869ca2190c2eaf756adcee8794fc25c74f98)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#uri HdinsightInteractiveQueryCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#parameters HdinsightInteractiveQueryCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89666f2fa43dfbcd1dae886771386c636400230c3ba45570f5d159e7476c3508)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731118c227f9db1e0cd5fad1f8d52db13e2c0fc4f34710dbafd51458314cf5b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dae7baf1e1e69caffa39d33e557280de75e19416a3c148916a704ad8ffa5de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e60d07a0d7c7f8b87d12f61fd259d6efd25c3a32e4dd72193895ab054f2e4eff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3abd121ab3dac803c0600cd4e0b087cd952580c52ccf2e069f9a6d7fcfab1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0d3442b32d6798516b23cc33ba7e51475f34c9b3be7b9aebf827f922aec288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8516cd000e2dd3b0a20884f0291b328b63bb52ae6d515293d736e9156fc45614)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21217c69c9b12f89e764be74b3c3d1a10ace9958cfab122cfce8d76b3ee8a82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5475e85176d1b57f3e8cfda617d42342dfd3411113cd22b1b3254a2187c0efa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06436ad69884b4ba22f93914ad117f60ff0598f52549219477d7569e44c155d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4269cd88368f20db2b3483238c44de021e7c543c8f38c2680bb72649ed0e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__005bf5a1d642ad2c9a544adb6488e8aa08242a501c0302184e94fb41f0be534a)
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
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.
        '''
        value = HdinsightInteractiveQueryClusterRolesHeadNode(
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
        autoscale: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#target_instance_count HdinsightInteractiveQueryCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#autoscale HdinsightInteractiveQueryCluster#autoscale}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.
        '''
        value = HdinsightInteractiveQueryClusterRolesWorkerNode(
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
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.
        '''
        value = HdinsightInteractiveQueryClusterRolesZookeeperNode(
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
    def head_node(self) -> HdinsightInteractiveQueryClusterRolesHeadNodeOutputReference:
        return typing.cast(HdinsightInteractiveQueryClusterRolesHeadNodeOutputReference, jsii.get(self, "headNode"))

    @builtins.property
    @jsii.member(jsii_name="workerNode")
    def worker_node(
        self,
    ) -> "HdinsightInteractiveQueryClusterRolesWorkerNodeOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNodeOutputReference", jsii.get(self, "workerNode"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNode")
    def zookeeper_node(
        self,
    ) -> "HdinsightInteractiveQueryClusterRolesZookeeperNodeOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterRolesZookeeperNodeOutputReference", jsii.get(self, "zookeeperNode"))

    @builtins.property
    @jsii.member(jsii_name="headNodeInput")
    def head_node_input(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesHeadNode]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesHeadNode], jsii.get(self, "headNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="workerNodeInput")
    def worker_node_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNode"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNode"], jsii.get(self, "workerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperNodeInput")
    def zookeeper_node_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterRolesZookeeperNode"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterRolesZookeeperNode"], jsii.get(self, "zookeeperNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HdinsightInteractiveQueryClusterRoles]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d763074a39071423ef7c11aa85b270a09f41aebbc91e21074f015904f4ccc6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNode",
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
class HdinsightInteractiveQueryClusterRolesWorkerNode:
    def __init__(
        self,
        *,
        target_instance_count: jsii.Number,
        username: builtins.str,
        vm_size: builtins.str,
        autoscale: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#target_instance_count HdinsightInteractiveQueryCluster#target_instance_count}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#autoscale HdinsightInteractiveQueryCluster#autoscale}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.
        '''
        if isinstance(autoscale, dict):
            autoscale = HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale(**autoscale)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ca734a7423c76cff4616b01dd76b85602c080ef796a18db394ac45967fc66e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#target_instance_count HdinsightInteractiveQueryCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscale(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale"]:
        '''autoscale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#autoscale HdinsightInteractiveQueryCluster#autoscale}
        '''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale"], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesWorkerNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale",
    jsii_struct_bases=[],
    name_mapping={"recurrence": "recurrence"},
)
class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale:
    def __init__(
        self,
        *,
        recurrence: typing.Optional[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#recurrence HdinsightInteractiveQueryCluster#recurrence}
        '''
        if isinstance(recurrence, dict):
            recurrence = HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815f65d35b3f61cb42951e36bffd9c3c22512d3d866c7a0821ed60f0e09fc8e7)
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recurrence is not None:
            self._values["recurrence"] = recurrence

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#recurrence HdinsightInteractiveQueryCluster#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7ef55a15fc03cb92044200387fd19cff9f0ac2430ae330c3abccc4b5d6e2e82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
        timezone: builtins.str,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#schedule HdinsightInteractiveQueryCluster#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#timezone HdinsightInteractiveQueryCluster#timezone}.
        '''
        value = HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence(
            schedule=schedule, timezone=timezone
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference":
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence"]:
        return typing.cast(typing.Optional["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0eed2ee1f5ff743fa712e5d77301c148c866f10de98847cfe3aaa73c3ad45bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule", "timezone": "timezone"},
)
class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence:
    def __init__(
        self,
        *,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
        timezone: builtins.str,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#schedule HdinsightInteractiveQueryCluster#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#timezone HdinsightInteractiveQueryCluster#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508e2ed70012ee5f7a72b1cf25a37cab6c0326226e8db7c613f3aee268836ab6)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
            "timezone": timezone,
        }

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#schedule HdinsightInteractiveQueryCluster#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]], result)

    @builtins.property
    def timezone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#timezone HdinsightInteractiveQueryCluster#timezone}.'''
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd2385bd283c08cf3f7136dceab3eabee6e1d2f545f7558722a176d8f64f3965)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cee58f422d6fb5459156ee632f231169f266b822eda816f90405b9f77c43ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList":
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule"]]], jsii.get(self, "scheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__308e8b47e28c0f3357f9916f21d7b0caca5e7e2c10c58a899fc2fde62e418e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__464f02124567723759f6cdda04b724282ee2714118a716a3e868ef9a7795f82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "days": "days",
        "target_instance_count": "targetInstanceCount",
        "time": "time",
    },
)
class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule:
    def __init__(
        self,
        *,
        days: typing.Sequence[builtins.str],
        target_instance_count: jsii.Number,
        time: builtins.str,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#days HdinsightInteractiveQueryCluster#days}.
        :param target_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#target_instance_count HdinsightInteractiveQueryCluster#target_instance_count}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#time HdinsightInteractiveQueryCluster#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3724d023eeec934c5da524a264182c4bca8d15105a885b473e49e5d99bf87a03)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#days HdinsightInteractiveQueryCluster#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#target_instance_count HdinsightInteractiveQueryCluster#target_instance_count}.'''
        result = self._values.get("target_instance_count")
        assert result is not None, "Required property 'target_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#time HdinsightInteractiveQueryCluster#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04de043bee70d40e88da6b6b255f49a6921d2e554880248ce76ee407bda1defb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7068cedd564cf744734fdf429d3200406ba6ae534432054842eb42ded34c36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af2872fd15067943a153a5463fbddc5ce93679496e93b3cee709893997d5053)
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
            type_hints = typing.get_type_hints(_typecheckingstub__000bb5d7eeb4449f19bfd9041829ce7e009a7536ffc9725c948cdccb3f46e2ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4535077b538d5f080356363989bdddf18d8a026a409ac09345563078d2d48dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19dbf4a33ae10ddac61a67fc8f1bcc19ce228b7dca761fcd90d9a8e176efc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8952b10dd917afa86d75ee026055ba62319d499e743aed3472223cea193108)
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
            type_hints = typing.get_type_hints(_typecheckingstub__963ffa9b0d574ec4660f8898c44fc97339be3b4a0e874db4f6fc49adef1be80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4379dfd9186403379ca9edb79bb2d46b7012712cd96f5a6da3bb37558344cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0facbecd73c0d1166f26226f9a6abfe73a79ae9563b4141fe11ab06edca34a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a4d79a44f6a80f0c9b1ad2a86773ef727380629d9a101f1e1975082f2bbc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterRolesWorkerNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__732bed4b2ab42d45444199106b29f9524bbeef0d6550b200d12a220e367f8405)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(
        self,
        *,
        recurrence: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#recurrence HdinsightInteractiveQueryCluster#recurrence}
        '''
        value = HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale(
            recurrence=recurrence
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a15acc14bec0edcdaf1f4bfa2e5bc4c76707968de0f644206018472592bd7c7)
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
    ) -> HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleOutputReference:
        return typing.cast(HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleOutputReference, jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="scriptActions")
    def script_actions(
        self,
    ) -> "HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsList":
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__61adae05046eb35304ec8bf953c3a502fbcc05c06180e4f1bd0ea5b751879b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2940cc8bf5a787a01fc5e01ec39544b5e0d7a35cb7499f6b8d28c20d9878c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bfb95ea01c5869d8677f53c8b34356f4655270340850693e05e737f5a20998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetInstanceCount")
    def target_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstanceCount"))

    @target_instance_count.setter
    def target_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08191df5239e2eae8ea1c5ede60eebd80b9f89d4c37fc212c16113e4d239ae5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697c15c7c778f05f43f7969df2de1c45159d91f3c81c593c81dd81ef8afd02a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b747a300acd9b9897e22a2e320920a537926dab02b402d371f746873cccabbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4087b00446b6e0013e8453057fc12b07b93088c23977ed4050e6f629334d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNode]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e0b5a1b2393573fa96441f4ff288105ad427cc7efe93a4087665d4026785ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#uri HdinsightInteractiveQueryCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#parameters HdinsightInteractiveQueryCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35de46770f21ecaea02aaf2a64e201f5ef183d0f5bb4fe63eeb9eb07ad537a61)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#uri HdinsightInteractiveQueryCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#parameters HdinsightInteractiveQueryCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98b276d930f134029d02024a77870af81aa188fbb0ef6a0fd3ab06f5951c251a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1dc79c1ee8b333718848d6c61c5705bff328175d91e02ecea0ad09e0f1dc06)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de5f714cb92261c34325e5ad6696078ea0b83659d7b1c95931de5bd49b36533)
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
            type_hints = typing.get_type_hints(_typecheckingstub__828790aa100fdbf2743cbf37c9015b1de8b06bbcfb4f752933f0908233e86c5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6c0911d6a3215bc6093730e4d13d86fffda1f3d36a4766da4f93b40cb24ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99c94abdc6665eacd2f70f58b0a01d084218fa2b9501dd567996a2da0ef829c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffac49f62ce0ab3420d4df49e9b72999ba643e969357c5ffe37c4b448d5916d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42b8217a99d43739d33db7f86ae23145446d7d9957c5fdf26eccd3992a1e8eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355dd3da937a805345f209c4e6e949f43aa886d157c4fe16b87f29015268aab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10db5d55c91792b70686815ebb789a896e4aad62f19d4a1094eb281f7901226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aefd30e6212b2ae8cd7818a3ac7205ba5e08605bbf6b73de234ed128aa33d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesZookeeperNode",
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
class HdinsightInteractiveQueryClusterRolesZookeeperNode:
    def __init__(
        self,
        *,
        username: builtins.str,
        vm_size: builtins.str,
        password: typing.Optional[builtins.str] = None,
        script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.
        :param script_actions: script_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        :param ssh_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bd7af7bc2c10465744a8e6ef301396e599727cc02c0af51017f2e52c005388)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#username HdinsightInteractiveQueryCluster#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#vm_size HdinsightInteractiveQueryCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#password HdinsightInteractiveQueryCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions"]]]:
        '''script_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#script_actions HdinsightInteractiveQueryCluster#script_actions}
        '''
        result = self._values.get("script_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions"]]], result)

    @builtins.property
    def ssh_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ssh_keys HdinsightInteractiveQueryCluster#ssh_keys}.'''
        result = self._values.get("ssh_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#subnet_id HdinsightInteractiveQueryCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#virtual_network_id HdinsightInteractiveQueryCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesZookeeperNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesZookeeperNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesZookeeperNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2479e6aa66ea73326b62d85ae14b89471205bcc61c195d9732c9c5fc3780e9d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScriptActions")
    def put_script_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa0fa46fb855ffed7180e26d1524b1a8f8e9afd73753893fcbf1f5e5f6c8520)
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
    ) -> "HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsList":
        return typing.cast("HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsList", jsii.get(self, "scriptActions"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptActionsInput")
    def script_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions"]]], jsii.get(self, "scriptActionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9fe6d7059fd17baefdab66dc3081b1339032a4734ea0631e850f9206193e34e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshKeys")
    def ssh_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshKeys"))

    @ssh_keys.setter
    def ssh_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7caa7f1d902743f3bcdcf052609a660e283fee7f4f2f702c888786acd1956c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd7f258defba4f5555f95ee52b387d0fca61bec768d8caf61a83d308ed131a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c51bb423c2b8a679cb90dff32ab87699b5f452ca41e82363c648007aaef1fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da08a90faeb38ab2d24224b8f86cec2808c007f2635b204846c8e10ea7b28bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751dc5fb13c09df411363b5b96c5b347d88319587c243e741e7bbea3d5f134a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterRolesZookeeperNode]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterRolesZookeeperNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterRolesZookeeperNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6453ce420498cdda0d21d9a97378ae84022234907136911249fcb51054daf623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uri": "uri", "parameters": "parameters"},
)
class HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#uri HdinsightInteractiveQueryCluster#uri}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#parameters HdinsightInteractiveQueryCluster#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe38d780a83f50b03d691df4e7b6ec35b55c05990ce330ef3447bf7de2e57f13)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#name HdinsightInteractiveQueryCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#uri HdinsightInteractiveQueryCluster#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#parameters HdinsightInteractiveQueryCluster#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c15c9f697372837ac5d3dc3e118379e53e8d274cc0f21d345318896d87b33cd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3b9449ab1ef176db6b994e4758c5ab07262ba6296e02caadbb8ae1fb763b80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ead467f8d6428dfb49710ca6fdbdf00a91bc4b0dc7e55cb89e78903355cd058)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e17f01c44a28d6bee0dcc43b11b1598e3ad83870a35d0ea9135c67c51736b1e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__401354bb56abbecf8df51981931a6301a87550549678dd9fb0bc78d6d04e5412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c9c5b5610f867c1b7c635c1d11ea665f4849174438b97623d3b18482c0e60b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d05605a376d4e936f9e2eeee12e5cf5b65f7dae77bc151647e35b2532db752f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a2a2be192be7b7631fede7858341afd1850ca8ea318119a380fe5e08b43cef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16020ef567ad11d2a0820c4cfa1ad8b7d5bc703582cef2ebdc73bfad9923878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0fdeef96ddbbaf2b5e7fce1dd13067e2002ce18269f2a8fe7a13b71c610611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b73cbd9200bc52539576d627f86fe7c4f57c0722a1c3d229a2c9dc09a7d163a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterSecurityProfile",
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
class HdinsightInteractiveQueryClusterSecurityProfile:
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
        :param aadds_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#aadds_resource_id HdinsightInteractiveQueryCluster#aadds_resource_id}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_name HdinsightInteractiveQueryCluster#domain_name}.
        :param domain_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_username HdinsightInteractiveQueryCluster#domain_username}.
        :param domain_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_user_password HdinsightInteractiveQueryCluster#domain_user_password}.
        :param ldaps_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ldaps_urls HdinsightInteractiveQueryCluster#ldaps_urls}.
        :param msi_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#msi_resource_id HdinsightInteractiveQueryCluster#msi_resource_id}.
        :param cluster_users_group_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#cluster_users_group_dns HdinsightInteractiveQueryCluster#cluster_users_group_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6d428149a00380467ad2677e655525f77e134e0726fa25d12acde6682a6a97)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#aadds_resource_id HdinsightInteractiveQueryCluster#aadds_resource_id}.'''
        result = self._values.get("aadds_resource_id")
        assert result is not None, "Required property 'aadds_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_name HdinsightInteractiveQueryCluster#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_username HdinsightInteractiveQueryCluster#domain_username}.'''
        result = self._values.get("domain_username")
        assert result is not None, "Required property 'domain_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_user_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#domain_user_password HdinsightInteractiveQueryCluster#domain_user_password}.'''
        result = self._values.get("domain_user_password")
        assert result is not None, "Required property 'domain_user_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ldaps_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#ldaps_urls HdinsightInteractiveQueryCluster#ldaps_urls}.'''
        result = self._values.get("ldaps_urls")
        assert result is not None, "Required property 'ldaps_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def msi_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#msi_resource_id HdinsightInteractiveQueryCluster#msi_resource_id}.'''
        result = self._values.get("msi_resource_id")
        assert result is not None, "Required property 'msi_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_users_group_dns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#cluster_users_group_dns HdinsightInteractiveQueryCluster#cluster_users_group_dns}.'''
        result = self._values.get("cluster_users_group_dns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterSecurityProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterSecurityProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterSecurityProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d0412ff932db514d7d7d048888e4a9ddcdd4b604a1b528f6af1a6076da2624a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f8b169e7f7ed0fa30b78b354fb02ea30e576e77507f926e00f11291ac5e9d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aaddsResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterUsersGroupDns")
    def cluster_users_group_dns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterUsersGroupDns"))

    @cluster_users_group_dns.setter
    def cluster_users_group_dns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aca18b3c844dac9662337c692877e69d5736161e18edfa682b844e0f267d07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterUsersGroupDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2382356537614877f3718057b7bf78e863f9fe240e5950fe41cccc1772a5c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUsername")
    def domain_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUsername"))

    @domain_username.setter
    def domain_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30aeb69ceb8fbda49dc8100a723685772959e9896db306ecd48e6e4caa96c4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainUserPassword")
    def domain_user_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainUserPassword"))

    @domain_user_password.setter
    def domain_user_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494efad50837dcb78eb875f3b781809b512d448df13dbf48ad361491245d1220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainUserPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapsUrls")
    def ldaps_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ldapsUrls"))

    @ldaps_urls.setter
    def ldaps_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551755c4215bfe8603a281ea67355504334d0b5433dcc4d59772d0eb0ad331de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapsUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiResourceId")
    def msi_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "msiResourceId"))

    @msi_resource_id.setter
    def msi_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5b423ab6d3c39aaf687dab0ad160bdaa81c1d549daddd4ea612263104f3d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterSecurityProfile]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterSecurityProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterSecurityProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8d8a1b3756a2a6246f3766468ec11a8475207db9e374d49e9c7bb48c5ac906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterStorageAccount",
    jsii_struct_bases=[],
    name_mapping={
        "is_default": "isDefault",
        "storage_account_key": "storageAccountKey",
        "storage_container_id": "storageContainerId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightInteractiveQueryClusterStorageAccount:
    def __init__(
        self,
        *,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_account_key: builtins.str,
        storage_container_id: builtins.str,
        storage_resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#is_default HdinsightInteractiveQueryCluster#is_default}.
        :param storage_account_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account_key HdinsightInteractiveQueryCluster#storage_account_key}.
        :param storage_container_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_container_id HdinsightInteractiveQueryCluster#storage_container_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_resource_id HdinsightInteractiveQueryCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f538408f146aedb64b0d026f2d9abfc7e5caeacdb4fdb4b388881aebf99635a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#is_default HdinsightInteractiveQueryCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_account_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_account_key HdinsightInteractiveQueryCluster#storage_account_key}.'''
        result = self._values.get("storage_account_key")
        assert result is not None, "Required property 'storage_account_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_container_id HdinsightInteractiveQueryCluster#storage_container_id}.'''
        result = self._values.get("storage_container_id")
        assert result is not None, "Required property 'storage_container_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_resource_id HdinsightInteractiveQueryCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterStorageAccountGen2",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem_id": "filesystemId",
        "is_default": "isDefault",
        "managed_identity_resource_id": "managedIdentityResourceId",
        "storage_resource_id": "storageResourceId",
    },
)
class HdinsightInteractiveQueryClusterStorageAccountGen2:
    def __init__(
        self,
        *,
        filesystem_id: builtins.str,
        is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        managed_identity_resource_id: builtins.str,
        storage_resource_id: builtins.str,
    ) -> None:
        '''
        :param filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#filesystem_id HdinsightInteractiveQueryCluster#filesystem_id}.
        :param is_default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#is_default HdinsightInteractiveQueryCluster#is_default}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#managed_identity_resource_id HdinsightInteractiveQueryCluster#managed_identity_resource_id}.
        :param storage_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_resource_id HdinsightInteractiveQueryCluster#storage_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ff86e2050ab24af8ac7b5f0a953e32fb3f3c15d1f2e93c7d06275362c4475e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#filesystem_id HdinsightInteractiveQueryCluster#filesystem_id}.'''
        result = self._values.get("filesystem_id")
        assert result is not None, "Required property 'filesystem_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#is_default HdinsightInteractiveQueryCluster#is_default}.'''
        result = self._values.get("is_default")
        assert result is not None, "Required property 'is_default' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def managed_identity_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#managed_identity_resource_id HdinsightInteractiveQueryCluster#managed_identity_resource_id}.'''
        result = self._values.get("managed_identity_resource_id")
        assert result is not None, "Required property 'managed_identity_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#storage_resource_id HdinsightInteractiveQueryCluster#storage_resource_id}.'''
        result = self._values.get("storage_resource_id")
        assert result is not None, "Required property 'storage_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterStorageAccountGen2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterStorageAccountGen2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterStorageAccountGen2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c4cd91a837fd3f13f5f0ca204bb1ecb84f7e3c614d325a5f91646141984594a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ece07a61ef488bbff33a3e4ac5a555847857de442f89aa321d75ccca2cba33a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58abc3c681c03eeb6adc7d38d6c8231647589e44f90dbaf8f0bf9200f4af4269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceId")
    def managed_identity_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityResourceId"))

    @managed_identity_resource_id.setter
    def managed_identity_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9d0afe6a30cb793c8b08cdb43a32ba593c4e6d5b1a3831da2e96c09bd49a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c94e30b6c95697cce67010ba9fc4d73ade2e614c1fd31485244e0002e1213bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[HdinsightInteractiveQueryClusterStorageAccountGen2]:
        return typing.cast(typing.Optional[HdinsightInteractiveQueryClusterStorageAccountGen2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HdinsightInteractiveQueryClusterStorageAccountGen2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a241cfe4dc2371bdaba2584da4f9bb2fddd3cf8759ebd46591f5d5007d93c4fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterStorageAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterStorageAccountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ca9db0fb0f06a8849edbfd27b4b4716aebd8c74f5d9e276f36a30afba0d5376)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HdinsightInteractiveQueryClusterStorageAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbbe9adc67b3050cb7229f9c64705e8662c25bafc8d091492d472506f363967)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HdinsightInteractiveQueryClusterStorageAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86d6c72926c39874c706d72ec039bae3ab627abb7206487c0bc33d04bcc962c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b25817882ee9dde7c836d7bdde1e72a2b4d34aab239b5dc41df6c3e52d468b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf442777b1a211caa8784b6d5029465e8d10fcf011d5eb69c3cf4938c51e49ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterStorageAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterStorageAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterStorageAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488edbd090982c73b43be524c963e7bccba3d81cbf8199042258fa2ffdcffa2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HdinsightInteractiveQueryClusterStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2a9f30c9d2a77eee71c9bb9afe55a2fe545524db812ba0ca05720b6eb74e6f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9154c2120fdc22ae867aa9426df9ce608bbc4de8ff58202a0ba7825b26f213ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountKey")
    def storage_account_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountKey"))

    @storage_account_key.setter
    def storage_account_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849fcc3a6828f9a35cc534bf7a68077c61dab390acd669e70ec6f63776e9f4fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerId")
    def storage_container_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerId"))

    @storage_container_id.setter
    def storage_container_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62d460f180ac0ab0d4293e70be1f36ad34f58c8fa4e2dc9d020c7047c494277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageResourceId")
    def storage_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageResourceId"))

    @storage_resource_id.setter
    def storage_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bcc1798076cc3165b77dffd92cde873f9e5ca008c1f4addea774048fdc75a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterStorageAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterStorageAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterStorageAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7605ef27a33e393a1f1268cc1cd8243b5ab0581b5700f93147c50816d49021d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class HdinsightInteractiveQueryClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#create HdinsightInteractiveQueryCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#delete HdinsightInteractiveQueryCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#read HdinsightInteractiveQueryCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#update HdinsightInteractiveQueryCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad15b535ea7214bda68e084f25a4c0ffafc0b90426ba80a0277ee52578b1fb3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#create HdinsightInteractiveQueryCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#delete HdinsightInteractiveQueryCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#read HdinsightInteractiveQueryCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hdinsight_interactive_query_cluster#update HdinsightInteractiveQueryCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HdinsightInteractiveQueryClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HdinsightInteractiveQueryClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hdinsightInteractiveQueryCluster.HdinsightInteractiveQueryClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c5f6f435d448fb2d483787047cd306548cf11530598f6247b77f66f0306e7b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bfcb07c85468bd978fc5f620c92ee89eec4a49dfb10fc5fd562f520694ad2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93fcc3b22fa4bfa80e46714f53bd8719291e3781a6e51cec9b600a8b80e5ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db82a27b27d34319372ec7f84d37c3177080b83449026a049c8fa0c42a2dd253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1ffe95dd474b35df89204ccf31ae56a81eb468c7c3f47cb934a455d7b93269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0870f52ae1999692a63265630d5eea1e9736cf14dc12455e610da01b2861bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HdinsightInteractiveQueryCluster",
    "HdinsightInteractiveQueryClusterComponentVersion",
    "HdinsightInteractiveQueryClusterComponentVersionOutputReference",
    "HdinsightInteractiveQueryClusterComputeIsolation",
    "HdinsightInteractiveQueryClusterComputeIsolationOutputReference",
    "HdinsightInteractiveQueryClusterConfig",
    "HdinsightInteractiveQueryClusterDiskEncryption",
    "HdinsightInteractiveQueryClusterDiskEncryptionList",
    "HdinsightInteractiveQueryClusterDiskEncryptionOutputReference",
    "HdinsightInteractiveQueryClusterExtension",
    "HdinsightInteractiveQueryClusterExtensionOutputReference",
    "HdinsightInteractiveQueryClusterGateway",
    "HdinsightInteractiveQueryClusterGatewayOutputReference",
    "HdinsightInteractiveQueryClusterMetastores",
    "HdinsightInteractiveQueryClusterMetastoresAmbari",
    "HdinsightInteractiveQueryClusterMetastoresAmbariOutputReference",
    "HdinsightInteractiveQueryClusterMetastoresHive",
    "HdinsightInteractiveQueryClusterMetastoresHiveOutputReference",
    "HdinsightInteractiveQueryClusterMetastoresOozie",
    "HdinsightInteractiveQueryClusterMetastoresOozieOutputReference",
    "HdinsightInteractiveQueryClusterMetastoresOutputReference",
    "HdinsightInteractiveQueryClusterMonitor",
    "HdinsightInteractiveQueryClusterMonitorOutputReference",
    "HdinsightInteractiveQueryClusterNetwork",
    "HdinsightInteractiveQueryClusterNetworkOutputReference",
    "HdinsightInteractiveQueryClusterPrivateLinkConfiguration",
    "HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration",
    "HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfigurationOutputReference",
    "HdinsightInteractiveQueryClusterPrivateLinkConfigurationOutputReference",
    "HdinsightInteractiveQueryClusterRoles",
    "HdinsightInteractiveQueryClusterRolesHeadNode",
    "HdinsightInteractiveQueryClusterRolesHeadNodeOutputReference",
    "HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions",
    "HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsList",
    "HdinsightInteractiveQueryClusterRolesHeadNodeScriptActionsOutputReference",
    "HdinsightInteractiveQueryClusterRolesOutputReference",
    "HdinsightInteractiveQueryClusterRolesWorkerNode",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleOutputReference",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceOutputReference",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleList",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceScheduleOutputReference",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeOutputReference",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsList",
    "HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActionsOutputReference",
    "HdinsightInteractiveQueryClusterRolesZookeeperNode",
    "HdinsightInteractiveQueryClusterRolesZookeeperNodeOutputReference",
    "HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions",
    "HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsList",
    "HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActionsOutputReference",
    "HdinsightInteractiveQueryClusterSecurityProfile",
    "HdinsightInteractiveQueryClusterSecurityProfileOutputReference",
    "HdinsightInteractiveQueryClusterStorageAccount",
    "HdinsightInteractiveQueryClusterStorageAccountGen2",
    "HdinsightInteractiveQueryClusterStorageAccountGen2OutputReference",
    "HdinsightInteractiveQueryClusterStorageAccountList",
    "HdinsightInteractiveQueryClusterStorageAccountOutputReference",
    "HdinsightInteractiveQueryClusterTimeouts",
    "HdinsightInteractiveQueryClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f89afd3d05fa80ad0488d2f49934ca37b6fb9756e840a8075c1c4c93e55f11c7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightInteractiveQueryClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightInteractiveQueryClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightInteractiveQueryClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extension: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bb6bdcb6d9f62a728598ce2365399b143df90e6fc8dd0d346db15b7382eb596b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5431b34c711f80d9cfb283ef736b7d4f1d02127acc91b8d883ba7995ae80c2a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d7bf56e4cd0343c693f57c37a5b58e975583bff53b1a237c1ae3c9e5ddffa9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b848c612d9404801ac762fa4c57977dbe701519d9fa239e1fa2a9496298428(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da165493bb58bdbb7058a062473e54f836b2a067351fecce2310e7cc52dd69ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7314af08240a8c129919ac8efa1d967fa011242e7a0d746cdf4dcc42bf72013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e1404787899200be84354fce0eb99138e038b9218db7a1b3ab0cb8be5b22ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68270cecaa94ba25df66cdda92c4099edf5b19b70fd1c715696f0239ba483652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3cb58499c41d698f0f7d799730f5cd121ab30857543b2240b30b298a83761b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4278c78c0b2d4d0930bbcd647bcc5ff7d9ffd9fe5dfa44eb4034eed82c7c13e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8427539cc51d23128e0e6907b8266b559c047e25d0f8ee35971557b1d877eb99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f509b9a9aacec691d5f34878aed64c7426a04c80bb46c1f79c1c4b92bb24f0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bd4d80c070e8f344a1d0de1c27b5db8f1b813d0d681ff60b74f22b55faed56(
    *,
    interactive_hive: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac47157365a7a1edb8a62455b77daaea5c9a705eabc20276505a47fcaa99837(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1edad14b073a35a280925e71b0855ef6a6909a63776bbe373df276c440b1d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44739d2384a4fc2ad3e7ecf026c0b4ce5095b7d84124e312a0f5e1799bbe79e(
    value: typing.Optional[HdinsightInteractiveQueryClusterComponentVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb02d02b6864a3dbe2a8906a28abd426ab9185b64e8b8fb3b39a16cb814a1ad(
    *,
    compute_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_sku: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b904886d5595b4775876dec981cd94981872c5f752ba815eca27b69c774c9490(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d66b16bf8be2e0564baeb464598a459892c25660407ab6832e3122a0b779ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3821250fe0e4da016686130c8a2d06ca230ea83e41eb7e1d50b799850e6f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83af40f83bee08bbc1f4355568e283d511ba588ea06326f0523866cd519d41a8(
    value: typing.Optional[HdinsightInteractiveQueryClusterComputeIsolation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd71ac3660fba0bbf641a41e01a2f599fe3aaec8aa4bf998af77f11bea901329(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_version: builtins.str,
    component_version: typing.Union[HdinsightInteractiveQueryClusterComponentVersion, typing.Dict[builtins.str, typing.Any]],
    gateway: typing.Union[HdinsightInteractiveQueryClusterGateway, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    roles: typing.Union[HdinsightInteractiveQueryClusterRoles, typing.Dict[builtins.str, typing.Any]],
    tier: builtins.str,
    compute_isolation: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterComputeIsolation, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_encryption: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterDiskEncryption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_in_transit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extension: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    metastores: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMetastores, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    private_link_configuration: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterPrivateLinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_profile: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterSecurityProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_gen2: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterStorageAccountGen2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_min_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dad84457ecbdbe016714c310680c7c6913aff92ed9e43002e4c9614b9930c4(
    *,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    key_vault_managed_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f8cee8f8495aae407cb12ced2b69a17fac4b02bcd151e62b16a065e35e461b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc4bedeae6f83caf1afdd9250cb224ddc67b1473ea17a09aa23f7c53ee0b8f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f360a316d1b7d30279d01a7206ccf65c2aaa626f3c984670e5e4a195a8bc41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6103ab35e837406fbb5738b189b0217b21c7f5330ebe008a5bc912c320b0a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ac05f4ddf835a364ecd050b2bfd2a5e2505436415f01affd56aba88648f0b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ceb0b5d25a2ee4fa526573a9ae4c979cd20f3a989aad3891d409292c90fe1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterDiskEncryption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5830dbd355763876a29ed4e8c65579b0ec421f49da57a6b095846ee9b82acab5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec4a3aeff8a85c0d19f9ab739be7505814b6b317e487a3cfc716148d031b6e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f8294bc838d84fa21a14ad46e8a7a1029daf76338aca4d27296b031e83eff3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56170ef994ee35e736401c9b2f1847f00573d9df806be5133586777f5bbceadd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6d1481a84738a969efc1e0b6027409eec4f7985d6c883bf39660e0bbc5be6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60743d8d4792b1c01fbac8c6fdfb9d89238ef5c3f2176427b35042feecf02337(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterDiskEncryption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba3200f575fbbcf99c33f9bef0ab3fbdaf4ee627aa106b5b36089a1aa81af11(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4bac2ea6873e61cb69e184df48bbcf45b349195b171cff6878c39643364c9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56df940b3324c5733d3914143eac566c4951306cb5a80da25b0678177effa62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68317d398896ed1e073f72beba8f659937751bd04d9eb619d1977ecc95e29f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1511353673fed4cc071e40fa7f8b1a176b8afbb3bb7d2005627f98780109beb5(
    value: typing.Optional[HdinsightInteractiveQueryClusterExtension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf713e76c9c48d3f8b07cb5df660fb6b50a35ba5772e16b68749626e18c3458(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7915f536e29caecdbdff220c9019609d690c1e012a48d6773952e7bade00fb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae3a1fcdc091fdf5afbf0eafddb0d19fcceb622b6a0cb18155bc8f51f89faed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e943446bc610a7a53ab1405ad880a8ea49a5e71c8ae70eee496bd9bcf3297215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e68a28d14b0620694efa89b20ead59bafa167ae0c63e1fa7361f45f059bdb7(
    value: typing.Optional[HdinsightInteractiveQueryClusterGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9a77fa4eb51d1634225c4ea30fb3aba9cd2bf23ec9c503b29d68e9275475c6(
    *,
    ambari: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMetastoresAmbari, typing.Dict[builtins.str, typing.Any]]] = None,
    hive: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMetastoresHive, typing.Dict[builtins.str, typing.Any]]] = None,
    oozie: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterMetastoresOozie, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88148511435c219d84a04e00ad574599606b51c0766973c2682c0fe114de4e88(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fc57ae55b2d8f2b079157415c075f91e908681ea6ae5aa273cb924984601e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13b466a9b03669a73235d1e97b553c6a72a874d659f490c0cb6f99085eb0341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bf6ac2f845d7bf04b8fb19f9c4842aa6c2157b961d2561612339093a7721f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dba585c6937c27ea652e95676c42b41149c0468538c0c01bda6fd21c165f4c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27885c63e018bd8149d7f4189cb5c43f1ad008bd888f7853de02c797f8f274c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10f9cd535cd88c64ebff2385c5cab98f4333a837b00e8ece94790664b7ad438(
    value: typing.Optional[HdinsightInteractiveQueryClusterMetastoresAmbari],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6750748e378d40db8fb7fb77663612ee65c1089129d186e537661cba5ea008(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8bccbc975eae8dca20f8ca2f87dd61af13e60a505ba689e48ff2e95b8c47da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e2ea80469b499abbf753131064ea300dbacd62e65bc5c40b6a8829a5b765c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a20d5bc1473d1fbb3714bcb6d1db75ef2395ffeed564cf79376fd95712b93bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b83d1d451227b81bdb799283ff44d08b807b26e692a7ad6915ede8009adbfa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7611ca0fbda369ef78a8f694ff411463b493660abb0f126351030515a8a6461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30012f67d63d9e579b3025676ade7e25535b9f39dce6f8110086f824ae2ab2b8(
    value: typing.Optional[HdinsightInteractiveQueryClusterMetastoresHive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b54f156ebe55ea22bcbabd58b6f733df70a810098d413535623449109f39c5(
    *,
    database_name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5519398b9c784a2d36d90fd373c997981725268c846413810b1655f5f6d22e05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622d7adf6ddcd5e3481beaa01d367807fade3202056cbc490ac336605f085900(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e7f8b7674e68ccd0b8b73a8ec5b7faec6be2d02461a51d75fb4f75b62b5656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e608ed6a71b72e02c6c39142f04c5425fad54f0487bbbd65f13a0586b4900ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3677a740b9d39c951fad1d6ac94f028b067cb350eb04e45e43b1041fc3f6616c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6bfba4e4d29f25391cbffa177dd478f114227f3a2131c664de9b48c56e2b01(
    value: typing.Optional[HdinsightInteractiveQueryClusterMetastoresOozie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89738712ce6d91ecda8186ec23f00be8d0f5a54e3d2d55776e194783f8fccdc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1708bf398c8692a7c29e30d1606600f2409326c56a3f5e542a57a7734b3a4480(
    value: typing.Optional[HdinsightInteractiveQueryClusterMetastores],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79731f5ddf63245c8960f0fa3f3fda73f2065206136d006163b032bcd7a5460(
    *,
    log_analytics_workspace_id: builtins.str,
    primary_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec1c32a68217efe29881bf88e11afab66778985272f725851aea7cb357915b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a701675e96d766d4e28a4e4f07fa875f7dc3c7e283b615fb8758cf6927f83d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6c47b8b3a3a64f588d057fd724d8042ac6a21b0d1d781f1ec1d698697e2305(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f2941d011917645bbd79cfdbd14a33f24156b0dc7d1a9e6c2ed70b3618d7fe(
    value: typing.Optional[HdinsightInteractiveQueryClusterMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8430fd20d6b16385a54fbffce37a57dcd21b416c745cd2e98b2c5f6114e2b14b(
    *,
    connection_direction: typing.Optional[builtins.str] = None,
    private_link_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73b968bf23d077ddabc899c69d15764d3df635ea9e002eb02d124b1696a840c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724ad5e1af999b4a3d0a40a8691ad880c4ac2d3b813a90dfddbe10642cec6cca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd17651ec02347d3dbf8551c2767ee05cfab33a946279bcb45bbfe33a692793a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bd4d2d561335663ade601a544d405950e54325f0b9a01ed041b09f348803ec(
    value: typing.Optional[HdinsightInteractiveQueryClusterNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3823a1c29e8edf589be56af1701433efa0c9785b5ddebfe99b5550da67ae16ac(
    *,
    group_id: builtins.str,
    ip_configuration: typing.Union[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fca85c3f93c12c031e0287494385da74a2cd6eda3830d73b58180244f3f9482(
    *,
    name: builtins.str,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    private_ip_allocation_method: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbee588a54de68f7a0cda7e0ff426f27e527d68e1d7c17bb580490d7b21f2e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9b996730f8508421ca3d3f080a40cb0e79cd1c5af8eb7eb402c0add61eb33a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a9105d076ee6044aa87cac6de91fd3e77461264187cbed3af02877e239e95b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc38b6f507c7f1f80606885344996e25930947ec2c0cbbfd64bc2aa552f0b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6e024a2b9acdac451640cf2eac5bc8a17222bedf983e8bf7cb5d80be9e1835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ddc53e802da8c7623e330a8924ed31941c65beb7d2c5495a44daec0b8cafbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e298dcde30a0b39df656a309d470a0500b1a496a3d7114a72c7e7e6d74324a7e(
    value: typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfigurationIpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6aaf6f177a190712e82140e2dd25aa2f3bf957a85ae8ddef0bc44119ef4333(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482afe455d0987d037ef0feecdd26beddb2fab80f9ea67da64ff9d4a1893b673(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124d0ab6e1206004620244cab86b1098dc33b8c6f0bba21f0050715bbe09fbb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c76740ce0ef9a73c20f250a995fd98851877c368ccccd4eabb9c05e27d9387(
    value: typing.Optional[HdinsightInteractiveQueryClusterPrivateLinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d8be0c2eeba0f49e8337a47185e1f6f653be8b3ccea4ff5a7cc52310035c3a(
    *,
    head_node: typing.Union[HdinsightInteractiveQueryClusterRolesHeadNode, typing.Dict[builtins.str, typing.Any]],
    worker_node: typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNode, typing.Dict[builtins.str, typing.Any]],
    zookeeper_node: typing.Union[HdinsightInteractiveQueryClusterRolesZookeeperNode, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2378201588b32c49f78526c545b9f53f0f06630abbc66eedeeb0060adb4823e(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5931f1f091430e06337df7cdc70b022a0b5dfb7b28a2c96004784a4198af2048(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9b3178a191bd142efe860bd35fd0a63438768ce905ac56ed6551a41e003b2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c552b593a3d44571cd447a6fe68653355488b3e703139bf51a5c162a9220e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80331eb34e08a6cd43b711134dc0cfc8e9436d2424bdef9692dc8907bf50728a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c148c2d2617fbe163f9be058db6fd675140c9ccd84f32ec365a93ab46ff365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa8b4107072c5f4cbc85db91d8796c2fd7674b1b599e31834cdde9361ec5fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b7fad8b2d05ad51f24b791d860ce4796681aa831621f9cb1af3f22c556ac4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61b3931ba7e0aede53f38feb7bb888ef8162921a4de67710fa9e6d679493167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da9a14d4fac417eb162dbaeb47ec8f476e92dff84ff7d3a9acf34699d76a884(
    value: typing.Optional[HdinsightInteractiveQueryClusterRolesHeadNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b499e588a5a677bb6f73c8a6faa869ca2190c2eaf756adcee8794fc25c74f98(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89666f2fa43dfbcd1dae886771386c636400230c3ba45570f5d159e7476c3508(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731118c227f9db1e0cd5fad1f8d52db13e2c0fc4f34710dbafd51458314cf5b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dae7baf1e1e69caffa39d33e557280de75e19416a3c148916a704ad8ffa5de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60d07a0d7c7f8b87d12f61fd259d6efd25c3a32e4dd72193895ab054f2e4eff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3abd121ab3dac803c0600cd4e0b087cd952580c52ccf2e069f9a6d7fcfab1b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0d3442b32d6798516b23cc33ba7e51475f34c9b3be7b9aebf827f922aec288(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8516cd000e2dd3b0a20884f0291b328b63bb52ae6d515293d736e9156fc45614(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21217c69c9b12f89e764be74b3c3d1a10ace9958cfab122cfce8d76b3ee8a82d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5475e85176d1b57f3e8cfda617d42342dfd3411113cd22b1b3254a2187c0efa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06436ad69884b4ba22f93914ad117f60ff0598f52549219477d7569e44c155d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4269cd88368f20db2b3483238c44de021e7c543c8f38c2680bb72649ed0e1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesHeadNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005bf5a1d642ad2c9a544adb6488e8aa08242a501c0302184e94fb41f0be534a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d763074a39071423ef7c11aa85b270a09f41aebbc91e21074f015904f4ccc6f(
    value: typing.Optional[HdinsightInteractiveQueryClusterRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ca734a7423c76cff4616b01dd76b85602c080ef796a18db394ac45967fc66e(
    *,
    target_instance_count: jsii.Number,
    username: builtins.str,
    vm_size: builtins.str,
    autoscale: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815f65d35b3f61cb42951e36bffd9c3c22512d3d866c7a0821ed60f0e09fc8e7(
    *,
    recurrence: typing.Optional[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ef55a15fc03cb92044200387fd19cff9f0ac2430ae330c3abccc4b5d6e2e82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0eed2ee1f5ff743fa712e5d77301c148c866f10de98847cfe3aaa73c3ad45bc(
    value: typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508e2ed70012ee5f7a72b1cf25a37cab6c0326226e8db7c613f3aee268836ab6(
    *,
    schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]]],
    timezone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2385bd283c08cf3f7136dceab3eabee6e1d2f545f7558722a176d8f64f3965(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cee58f422d6fb5459156ee632f231169f266b822eda816f90405b9f77c43ec1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308e8b47e28c0f3357f9916f21d7b0caca5e7e2c10c58a899fc2fde62e418e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464f02124567723759f6cdda04b724282ee2714118a716a3e868ef9a7795f82d(
    value: typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3724d023eeec934c5da524a264182c4bca8d15105a885b473e49e5d99bf87a03(
    *,
    days: typing.Sequence[builtins.str],
    target_instance_count: jsii.Number,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04de043bee70d40e88da6b6b255f49a6921d2e554880248ce76ee407bda1defb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7068cedd564cf744734fdf429d3200406ba6ae534432054842eb42ded34c36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af2872fd15067943a153a5463fbddc5ce93679496e93b3cee709893997d5053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000bb5d7eeb4449f19bfd9041829ce7e009a7536ffc9725c948cdccb3f46e2ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4535077b538d5f080356363989bdddf18d8a026a409ac09345563078d2d48dd0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19dbf4a33ae10ddac61a67fc8f1bcc19ce228b7dca761fcd90d9a8e176efc45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8952b10dd917afa86d75ee026055ba62319d499e743aed3472223cea193108(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963ffa9b0d574ec4660f8898c44fc97339be3b4a0e874db4f6fc49adef1be80a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4379dfd9186403379ca9edb79bb2d46b7012712cd96f5a6da3bb37558344cf1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0facbecd73c0d1166f26226f9a6abfe73a79ae9563b4141fe11ab06edca34a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a4d79a44f6a80f0c9b1ad2a86773ef727380629d9a101f1e1975082f2bbc3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeAutoscaleRecurrenceSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732bed4b2ab42d45444199106b29f9524bbeef0d6550b200d12a220e367f8405(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a15acc14bec0edcdaf1f4bfa2e5bc4c76707968de0f644206018472592bd7c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61adae05046eb35304ec8bf953c3a502fbcc05c06180e4f1bd0ea5b751879b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2940cc8bf5a787a01fc5e01ec39544b5e0d7a35cb7499f6b8d28c20d9878c62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bfb95ea01c5869d8677f53c8b34356f4655270340850693e05e737f5a20998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08191df5239e2eae8ea1c5ede60eebd80b9f89d4c37fc212c16113e4d239ae5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697c15c7c778f05f43f7969df2de1c45159d91f3c81c593c81dd81ef8afd02a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b747a300acd9b9897e22a2e320920a537926dab02b402d371f746873cccabbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4087b00446b6e0013e8453057fc12b07b93088c23977ed4050e6f629334d04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e0b5a1b2393573fa96441f4ff288105ad427cc7efe93a4087665d4026785ab(
    value: typing.Optional[HdinsightInteractiveQueryClusterRolesWorkerNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35de46770f21ecaea02aaf2a64e201f5ef183d0f5bb4fe63eeb9eb07ad537a61(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b276d930f134029d02024a77870af81aa188fbb0ef6a0fd3ab06f5951c251a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1dc79c1ee8b333718848d6c61c5705bff328175d91e02ecea0ad09e0f1dc06(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de5f714cb92261c34325e5ad6696078ea0b83659d7b1c95931de5bd49b36533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828790aa100fdbf2743cbf37c9015b1de8b06bbcfb4f752933f0908233e86c5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6c0911d6a3215bc6093730e4d13d86fffda1f3d36a4766da4f93b40cb24ab1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99c94abdc6665eacd2f70f58b0a01d084218fa2b9501dd567996a2da0ef829c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffac49f62ce0ab3420d4df49e9b72999ba643e969357c5ffe37c4b448d5916d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b8217a99d43739d33db7f86ae23145446d7d9957c5fdf26eccd3992a1e8eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355dd3da937a805345f209c4e6e949f43aa886d157c4fe16b87f29015268aab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10db5d55c91792b70686815ebb789a896e4aad62f19d4a1094eb281f7901226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aefd30e6212b2ae8cd7818a3ac7205ba5e08605bbf6b73de234ed128aa33d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesWorkerNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bd7af7bc2c10465744a8e6ef301396e599727cc02c0af51017f2e52c005388(
    *,
    username: builtins.str,
    vm_size: builtins.str,
    password: typing.Optional[builtins.str] = None,
    script_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2479e6aa66ea73326b62d85ae14b89471205bcc61c195d9732c9c5fc3780e9d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa0fa46fb855ffed7180e26d1524b1a8f8e9afd73753893fcbf1f5e5f6c8520(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe6d7059fd17baefdab66dc3081b1339032a4734ea0631e850f9206193e34e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7caa7f1d902743f3bcdcf052609a660e283fee7f4f2f702c888786acd1956c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd7f258defba4f5555f95ee52b387d0fca61bec768d8caf61a83d308ed131a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c51bb423c2b8a679cb90dff32ab87699b5f452ca41e82363c648007aaef1fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da08a90faeb38ab2d24224b8f86cec2808c007f2635b204846c8e10ea7b28bdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751dc5fb13c09df411363b5b96c5b347d88319587c243e741e7bbea3d5f134a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6453ce420498cdda0d21d9a97378ae84022234907136911249fcb51054daf623(
    value: typing.Optional[HdinsightInteractiveQueryClusterRolesZookeeperNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe38d780a83f50b03d691df4e7b6ec35b55c05990ce330ef3447bf7de2e57f13(
    *,
    name: builtins.str,
    uri: builtins.str,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15c9f697372837ac5d3dc3e118379e53e8d274cc0f21d345318896d87b33cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3b9449ab1ef176db6b994e4758c5ab07262ba6296e02caadbb8ae1fb763b80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ead467f8d6428dfb49710ca6fdbdf00a91bc4b0dc7e55cb89e78903355cd058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17f01c44a28d6bee0dcc43b11b1598e3ad83870a35d0ea9135c67c51736b1e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401354bb56abbecf8df51981931a6301a87550549678dd9fb0bc78d6d04e5412(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c9c5b5610f867c1b7c635c1d11ea665f4849174438b97623d3b18482c0e60b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05605a376d4e936f9e2eeee12e5cf5b65f7dae77bc151647e35b2532db752f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2a2be192be7b7631fede7858341afd1850ca8ea318119a380fe5e08b43cef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16020ef567ad11d2a0820c4cfa1ad8b7d5bc703582cef2ebdc73bfad9923878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0fdeef96ddbbaf2b5e7fce1dd13067e2002ce18269f2a8fe7a13b71c610611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b73cbd9200bc52539576d627f86fe7c4f57c0722a1c3d229a2c9dc09a7d163a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterRolesZookeeperNodeScriptActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6d428149a00380467ad2677e655525f77e134e0726fa25d12acde6682a6a97(
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

def _typecheckingstub__0d0412ff932db514d7d7d048888e4a9ddcdd4b604a1b528f6af1a6076da2624a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8b169e7f7ed0fa30b78b354fb02ea30e576e77507f926e00f11291ac5e9d39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aca18b3c844dac9662337c692877e69d5736161e18edfa682b844e0f267d07f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2382356537614877f3718057b7bf78e863f9fe240e5950fe41cccc1772a5c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30aeb69ceb8fbda49dc8100a723685772959e9896db306ecd48e6e4caa96c4d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494efad50837dcb78eb875f3b781809b512d448df13dbf48ad361491245d1220(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551755c4215bfe8603a281ea67355504334d0b5433dcc4d59772d0eb0ad331de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5b423ab6d3c39aaf687dab0ad160bdaa81c1d549daddd4ea612263104f3d2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8d8a1b3756a2a6246f3766468ec11a8475207db9e374d49e9c7bb48c5ac906(
    value: typing.Optional[HdinsightInteractiveQueryClusterSecurityProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f538408f146aedb64b0d026f2d9abfc7e5caeacdb4fdb4b388881aebf99635a(
    *,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_account_key: builtins.str,
    storage_container_id: builtins.str,
    storage_resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ff86e2050ab24af8ac7b5f0a953e32fb3f3c15d1f2e93c7d06275362c4475e(
    *,
    filesystem_id: builtins.str,
    is_default: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    managed_identity_resource_id: builtins.str,
    storage_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4cd91a837fd3f13f5f0ca204bb1ecb84f7e3c614d325a5f91646141984594a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece07a61ef488bbff33a3e4ac5a555847857de442f89aa321d75ccca2cba33a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58abc3c681c03eeb6adc7d38d6c8231647589e44f90dbaf8f0bf9200f4af4269(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9d0afe6a30cb793c8b08cdb43a32ba593c4e6d5b1a3831da2e96c09bd49a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c94e30b6c95697cce67010ba9fc4d73ade2e614c1fd31485244e0002e1213bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a241cfe4dc2371bdaba2584da4f9bb2fddd3cf8759ebd46591f5d5007d93c4fb(
    value: typing.Optional[HdinsightInteractiveQueryClusterStorageAccountGen2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca9db0fb0f06a8849edbfd27b4b4716aebd8c74f5d9e276f36a30afba0d5376(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbbe9adc67b3050cb7229f9c64705e8662c25bafc8d091492d472506f363967(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86d6c72926c39874c706d72ec039bae3ab627abb7206487c0bc33d04bcc962c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b25817882ee9dde7c836d7bdde1e72a2b4d34aab239b5dc41df6c3e52d468b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf442777b1a211caa8784b6d5029465e8d10fcf011d5eb69c3cf4938c51e49ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488edbd090982c73b43be524c963e7bccba3d81cbf8199042258fa2ffdcffa2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HdinsightInteractiveQueryClusterStorageAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a9f30c9d2a77eee71c9bb9afe55a2fe545524db812ba0ca05720b6eb74e6f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9154c2120fdc22ae867aa9426df9ce608bbc4de8ff58202a0ba7825b26f213ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849fcc3a6828f9a35cc534bf7a68077c61dab390acd669e70ec6f63776e9f4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62d460f180ac0ab0d4293e70be1f36ad34f58c8fa4e2dc9d020c7047c494277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bcc1798076cc3165b77dffd92cde873f9e5ca008c1f4addea774048fdc75a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7605ef27a33e393a1f1268cc1cd8243b5ab0581b5700f93147c50816d49021d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterStorageAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad15b535ea7214bda68e084f25a4c0ffafc0b90426ba80a0277ee52578b1fb3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5f6f435d448fb2d483787047cd306548cf11530598f6247b77f66f0306e7b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfcb07c85468bd978fc5f620c92ee89eec4a49dfb10fc5fd562f520694ad2e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93fcc3b22fa4bfa80e46714f53bd8719291e3781a6e51cec9b600a8b80e5ff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db82a27b27d34319372ec7f84d37c3177080b83449026a049c8fa0c42a2dd253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1ffe95dd474b35df89204ccf31ae56a81eb468c7c3f47cb934a455d7b93269(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0870f52ae1999692a63265630d5eea1e9736cf14dc12455e610da01b2861bca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HdinsightInteractiveQueryClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
