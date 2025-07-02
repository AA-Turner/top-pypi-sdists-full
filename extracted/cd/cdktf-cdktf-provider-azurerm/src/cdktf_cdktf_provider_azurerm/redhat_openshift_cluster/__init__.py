r'''
# `azurerm_redhat_openshift_cluster`

Refer to the Terraform Registry for docs: [`azurerm_redhat_openshift_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster).
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


class RedhatOpenshiftCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster azurerm_redhat_openshift_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_server_profile: typing.Union["RedhatOpenshiftClusterApiServerProfile", typing.Dict[builtins.str, typing.Any]],
        cluster_profile: typing.Union["RedhatOpenshiftClusterClusterProfile", typing.Dict[builtins.str, typing.Any]],
        ingress_profile: typing.Union["RedhatOpenshiftClusterIngressProfile", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        main_profile: typing.Union["RedhatOpenshiftClusterMainProfile", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network_profile: typing.Union["RedhatOpenshiftClusterNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        service_principal: typing.Union["RedhatOpenshiftClusterServicePrincipal", typing.Dict[builtins.str, typing.Any]],
        worker_profile: typing.Union["RedhatOpenshiftClusterWorkerProfile", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RedhatOpenshiftClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster azurerm_redhat_openshift_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_server_profile: api_server_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#api_server_profile RedhatOpenshiftCluster#api_server_profile}
        :param cluster_profile: cluster_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#cluster_profile RedhatOpenshiftCluster#cluster_profile}
        :param ingress_profile: ingress_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#ingress_profile RedhatOpenshiftCluster#ingress_profile}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#location RedhatOpenshiftCluster#location}.
        :param main_profile: main_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#main_profile RedhatOpenshiftCluster#main_profile}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#name RedhatOpenshiftCluster#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#network_profile RedhatOpenshiftCluster#network_profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#resource_group_name RedhatOpenshiftCluster#resource_group_name}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#service_principal RedhatOpenshiftCluster#service_principal}
        :param worker_profile: worker_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#worker_profile RedhatOpenshiftCluster#worker_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#id RedhatOpenshiftCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#tags RedhatOpenshiftCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#timeouts RedhatOpenshiftCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a393f34033b47918dc08be1edfc657bcbfa98df9a61904a173ed7e5659a3df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RedhatOpenshiftClusterConfig(
            api_server_profile=api_server_profile,
            cluster_profile=cluster_profile,
            ingress_profile=ingress_profile,
            location=location,
            main_profile=main_profile,
            name=name,
            network_profile=network_profile,
            resource_group_name=resource_group_name,
            service_principal=service_principal,
            worker_profile=worker_profile,
            id=id,
            tags=tags,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a RedhatOpenshiftCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RedhatOpenshiftCluster to import.
        :param import_from_id: The id of the existing RedhatOpenshiftCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RedhatOpenshiftCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0885cf4b5df447a2fbc1f83d773c33e0b5b3c3332ded1bd0c5a1f565256fb0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApiServerProfile")
    def put_api_server_profile(self, *, visibility: builtins.str) -> None:
        '''
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#visibility RedhatOpenshiftCluster#visibility}.
        '''
        value = RedhatOpenshiftClusterApiServerProfile(visibility=visibility)

        return typing.cast(None, jsii.invoke(self, "putApiServerProfile", [value]))

    @jsii.member(jsii_name="putClusterProfile")
    def put_cluster_profile(
        self,
        *,
        domain: builtins.str,
        version: builtins.str,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        pull_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#domain RedhatOpenshiftCluster#domain}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#version RedhatOpenshiftCluster#version}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#fips_enabled RedhatOpenshiftCluster#fips_enabled}.
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#managed_resource_group_name RedhatOpenshiftCluster#managed_resource_group_name}.
        :param pull_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#pull_secret RedhatOpenshiftCluster#pull_secret}.
        '''
        value = RedhatOpenshiftClusterClusterProfile(
            domain=domain,
            version=version,
            fips_enabled=fips_enabled,
            managed_resource_group_name=managed_resource_group_name,
            pull_secret=pull_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterProfile", [value]))

    @jsii.member(jsii_name="putIngressProfile")
    def put_ingress_profile(self, *, visibility: builtins.str) -> None:
        '''
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#visibility RedhatOpenshiftCluster#visibility}.
        '''
        value = RedhatOpenshiftClusterIngressProfile(visibility=visibility)

        return typing.cast(None, jsii.invoke(self, "putIngressProfile", [value]))

    @jsii.member(jsii_name="putMainProfile")
    def put_main_profile(
        self,
        *,
        subnet_id: builtins.str,
        vm_size: builtins.str,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#subnet_id RedhatOpenshiftCluster#subnet_id}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#vm_size RedhatOpenshiftCluster#vm_size}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_encryption_set_id RedhatOpenshiftCluster#disk_encryption_set_id}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#encryption_at_host_enabled RedhatOpenshiftCluster#encryption_at_host_enabled}.
        '''
        value = RedhatOpenshiftClusterMainProfile(
            subnet_id=subnet_id,
            vm_size=vm_size,
            disk_encryption_set_id=disk_encryption_set_id,
            encryption_at_host_enabled=encryption_at_host_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putMainProfile", [value]))

    @jsii.member(jsii_name="putNetworkProfile")
    def put_network_profile(
        self,
        *,
        pod_cidr: builtins.str,
        service_cidr: builtins.str,
        outbound_type: typing.Optional[builtins.str] = None,
        preconfigured_network_security_group_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pod_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#pod_cidr RedhatOpenshiftCluster#pod_cidr}.
        :param service_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#service_cidr RedhatOpenshiftCluster#service_cidr}.
        :param outbound_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#outbound_type RedhatOpenshiftCluster#outbound_type}.
        :param preconfigured_network_security_group_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#preconfigured_network_security_group_enabled RedhatOpenshiftCluster#preconfigured_network_security_group_enabled}.
        '''
        value = RedhatOpenshiftClusterNetworkProfile(
            pod_cidr=pod_cidr,
            service_cidr=service_cidr,
            outbound_type=outbound_type,
            preconfigured_network_security_group_enabled=preconfigured_network_security_group_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkProfile", [value]))

    @jsii.member(jsii_name="putServicePrincipal")
    def put_service_principal(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#client_id RedhatOpenshiftCluster#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#client_secret RedhatOpenshiftCluster#client_secret}.
        '''
        value = RedhatOpenshiftClusterServicePrincipal(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putServicePrincipal", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#create RedhatOpenshiftCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#delete RedhatOpenshiftCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#read RedhatOpenshiftCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#update RedhatOpenshiftCluster#update}.
        '''
        value = RedhatOpenshiftClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkerProfile")
    def put_worker_profile(
        self,
        *,
        disk_size_gb: jsii.Number,
        node_count: jsii.Number,
        subnet_id: builtins.str,
        vm_size: builtins.str,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_size_gb RedhatOpenshiftCluster#disk_size_gb}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#node_count RedhatOpenshiftCluster#node_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#subnet_id RedhatOpenshiftCluster#subnet_id}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#vm_size RedhatOpenshiftCluster#vm_size}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_encryption_set_id RedhatOpenshiftCluster#disk_encryption_set_id}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#encryption_at_host_enabled RedhatOpenshiftCluster#encryption_at_host_enabled}.
        '''
        value = RedhatOpenshiftClusterWorkerProfile(
            disk_size_gb=disk_size_gb,
            node_count=node_count,
            subnet_id=subnet_id,
            vm_size=vm_size,
            disk_encryption_set_id=disk_encryption_set_id,
            encryption_at_host_enabled=encryption_at_host_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerProfile", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="apiServerProfile")
    def api_server_profile(
        self,
    ) -> "RedhatOpenshiftClusterApiServerProfileOutputReference":
        return typing.cast("RedhatOpenshiftClusterApiServerProfileOutputReference", jsii.get(self, "apiServerProfile"))

    @builtins.property
    @jsii.member(jsii_name="clusterProfile")
    def cluster_profile(self) -> "RedhatOpenshiftClusterClusterProfileOutputReference":
        return typing.cast("RedhatOpenshiftClusterClusterProfileOutputReference", jsii.get(self, "clusterProfile"))

    @builtins.property
    @jsii.member(jsii_name="consoleUrl")
    def console_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consoleUrl"))

    @builtins.property
    @jsii.member(jsii_name="ingressProfile")
    def ingress_profile(self) -> "RedhatOpenshiftClusterIngressProfileOutputReference":
        return typing.cast("RedhatOpenshiftClusterIngressProfileOutputReference", jsii.get(self, "ingressProfile"))

    @builtins.property
    @jsii.member(jsii_name="mainProfile")
    def main_profile(self) -> "RedhatOpenshiftClusterMainProfileOutputReference":
        return typing.cast("RedhatOpenshiftClusterMainProfileOutputReference", jsii.get(self, "mainProfile"))

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(self) -> "RedhatOpenshiftClusterNetworkProfileOutputReference":
        return typing.cast("RedhatOpenshiftClusterNetworkProfileOutputReference", jsii.get(self, "networkProfile"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(
        self,
    ) -> "RedhatOpenshiftClusterServicePrincipalOutputReference":
        return typing.cast("RedhatOpenshiftClusterServicePrincipalOutputReference", jsii.get(self, "servicePrincipal"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RedhatOpenshiftClusterTimeoutsOutputReference":
        return typing.cast("RedhatOpenshiftClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workerProfile")
    def worker_profile(self) -> "RedhatOpenshiftClusterWorkerProfileOutputReference":
        return typing.cast("RedhatOpenshiftClusterWorkerProfileOutputReference", jsii.get(self, "workerProfile"))

    @builtins.property
    @jsii.member(jsii_name="apiServerProfileInput")
    def api_server_profile_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterApiServerProfile"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterApiServerProfile"], jsii.get(self, "apiServerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterProfileInput")
    def cluster_profile_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterClusterProfile"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterClusterProfile"], jsii.get(self, "clusterProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressProfileInput")
    def ingress_profile_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterIngressProfile"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterIngressProfile"], jsii.get(self, "ingressProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mainProfileInput")
    def main_profile_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterMainProfile"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterMainProfile"], jsii.get(self, "mainProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkProfileInput")
    def network_profile_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterNetworkProfile"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterNetworkProfile"], jsii.get(self, "networkProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalInput")
    def service_principal_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterServicePrincipal"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterServicePrincipal"], jsii.get(self, "servicePrincipalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedhatOpenshiftClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedhatOpenshiftClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workerProfileInput")
    def worker_profile_input(
        self,
    ) -> typing.Optional["RedhatOpenshiftClusterWorkerProfile"]:
        return typing.cast(typing.Optional["RedhatOpenshiftClusterWorkerProfile"], jsii.get(self, "workerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daea0639f35c7b54cf91416c0ffadd954a8383ab32e2fdbc38decb6600438a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2e059cd748fc399490db78169aed7f7ad9c5fe795a8679b72825d98f9b5f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9901da455c06e2fd8ec983cd5c1513dffebf1b1e8edb5d44644fed4d18c537b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a47deb333a251cfb0180d3008991b110eee841f2e4425a93bd17609a48d6a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8030d9783593a73446a1bb99635e61beba41b7602bf09fa57fbe6f1441860458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterApiServerProfile",
    jsii_struct_bases=[],
    name_mapping={"visibility": "visibility"},
)
class RedhatOpenshiftClusterApiServerProfile:
    def __init__(self, *, visibility: builtins.str) -> None:
        '''
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#visibility RedhatOpenshiftCluster#visibility}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554d188f501759bbc9bd72ee615b91714aa9bbe5d7e320e6a9181afc4df84238)
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "visibility": visibility,
        }

    @builtins.property
    def visibility(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#visibility RedhatOpenshiftCluster#visibility}.'''
        result = self._values.get("visibility")
        assert result is not None, "Required property 'visibility' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterApiServerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterApiServerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterApiServerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc723a3e2233e04b8b93423277d919e816daa5d9027fdc071080a2a12b37c883)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6498652767b1f1fc32340052d5bc714d083e995e09755717b1498dccf397365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterApiServerProfile]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterApiServerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterApiServerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001027c2de70ff0eba363924dfb0313a8fb2fd9e1d9a2b39f22e517b70fa7b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterClusterProfile",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "version": "version",
        "fips_enabled": "fipsEnabled",
        "managed_resource_group_name": "managedResourceGroupName",
        "pull_secret": "pullSecret",
    },
)
class RedhatOpenshiftClusterClusterProfile:
    def __init__(
        self,
        *,
        domain: builtins.str,
        version: builtins.str,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        pull_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#domain RedhatOpenshiftCluster#domain}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#version RedhatOpenshiftCluster#version}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#fips_enabled RedhatOpenshiftCluster#fips_enabled}.
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#managed_resource_group_name RedhatOpenshiftCluster#managed_resource_group_name}.
        :param pull_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#pull_secret RedhatOpenshiftCluster#pull_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2947add45d7d3e10fbc849adaaa1bce9aaed7b520f9f9a5567e8bf86aab47df1)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument fips_enabled", value=fips_enabled, expected_type=type_hints["fips_enabled"])
            check_type(argname="argument managed_resource_group_name", value=managed_resource_group_name, expected_type=type_hints["managed_resource_group_name"])
            check_type(argname="argument pull_secret", value=pull_secret, expected_type=type_hints["pull_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "version": version,
        }
        if fips_enabled is not None:
            self._values["fips_enabled"] = fips_enabled
        if managed_resource_group_name is not None:
            self._values["managed_resource_group_name"] = managed_resource_group_name
        if pull_secret is not None:
            self._values["pull_secret"] = pull_secret

    @builtins.property
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#domain RedhatOpenshiftCluster#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#version RedhatOpenshiftCluster#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fips_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#fips_enabled RedhatOpenshiftCluster#fips_enabled}.'''
        result = self._values.get("fips_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def managed_resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#managed_resource_group_name RedhatOpenshiftCluster#managed_resource_group_name}.'''
        result = self._values.get("managed_resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#pull_secret RedhatOpenshiftCluster#pull_secret}.'''
        result = self._values.get("pull_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterClusterProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterClusterProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterClusterProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55dc3d2632f8e8c04ffd474730a0c36009362d1eab90fec070127c6f12cfc6cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFipsEnabled")
    def reset_fips_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFipsEnabled", []))

    @jsii.member(jsii_name="resetManagedResourceGroupName")
    def reset_managed_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedResourceGroupName", []))

    @jsii.member(jsii_name="resetPullSecret")
    def reset_pull_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullSecret", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsEnabledInput")
    def fips_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fipsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupNameInput")
    def managed_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pullSecretInput")
    def pull_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pullSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7df1a408955634197bfccbb3627af3bda321fdc9d4cadd3b01130c8bd7cc4a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fipsEnabled"))

    @fips_enabled.setter
    def fips_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ced0bdc3d0463cc0571fc0ea7b9459461ea9777b0ccbf36f4ca0e4c0bc07390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fipsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupName")
    def managed_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourceGroupName"))

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63ef6fc1262e40efe483203820b85d9cbec67f79c348b9cd37aae95520b4110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pullSecret")
    def pull_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pullSecret"))

    @pull_secret.setter
    def pull_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14132a3664fc7ec862564c7c9616460b84d11e9ab98ff7b516359eedda770f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70981ca83eb703dc61e20bc084fc73240edba1c16b8258bbd867a995d83e8c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterClusterProfile]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterClusterProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterClusterProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8e08dbad31a9c088959764bb41ce5a3d34b55cb5d67ffbcaf493794c7b0873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_server_profile": "apiServerProfile",
        "cluster_profile": "clusterProfile",
        "ingress_profile": "ingressProfile",
        "location": "location",
        "main_profile": "mainProfile",
        "name": "name",
        "network_profile": "networkProfile",
        "resource_group_name": "resourceGroupName",
        "service_principal": "servicePrincipal",
        "worker_profile": "workerProfile",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class RedhatOpenshiftClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_server_profile: typing.Union[RedhatOpenshiftClusterApiServerProfile, typing.Dict[builtins.str, typing.Any]],
        cluster_profile: typing.Union[RedhatOpenshiftClusterClusterProfile, typing.Dict[builtins.str, typing.Any]],
        ingress_profile: typing.Union["RedhatOpenshiftClusterIngressProfile", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        main_profile: typing.Union["RedhatOpenshiftClusterMainProfile", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        network_profile: typing.Union["RedhatOpenshiftClusterNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        service_principal: typing.Union["RedhatOpenshiftClusterServicePrincipal", typing.Dict[builtins.str, typing.Any]],
        worker_profile: typing.Union["RedhatOpenshiftClusterWorkerProfile", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RedhatOpenshiftClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_server_profile: api_server_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#api_server_profile RedhatOpenshiftCluster#api_server_profile}
        :param cluster_profile: cluster_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#cluster_profile RedhatOpenshiftCluster#cluster_profile}
        :param ingress_profile: ingress_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#ingress_profile RedhatOpenshiftCluster#ingress_profile}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#location RedhatOpenshiftCluster#location}.
        :param main_profile: main_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#main_profile RedhatOpenshiftCluster#main_profile}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#name RedhatOpenshiftCluster#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#network_profile RedhatOpenshiftCluster#network_profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#resource_group_name RedhatOpenshiftCluster#resource_group_name}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#service_principal RedhatOpenshiftCluster#service_principal}
        :param worker_profile: worker_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#worker_profile RedhatOpenshiftCluster#worker_profile}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#id RedhatOpenshiftCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#tags RedhatOpenshiftCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#timeouts RedhatOpenshiftCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(api_server_profile, dict):
            api_server_profile = RedhatOpenshiftClusterApiServerProfile(**api_server_profile)
        if isinstance(cluster_profile, dict):
            cluster_profile = RedhatOpenshiftClusterClusterProfile(**cluster_profile)
        if isinstance(ingress_profile, dict):
            ingress_profile = RedhatOpenshiftClusterIngressProfile(**ingress_profile)
        if isinstance(main_profile, dict):
            main_profile = RedhatOpenshiftClusterMainProfile(**main_profile)
        if isinstance(network_profile, dict):
            network_profile = RedhatOpenshiftClusterNetworkProfile(**network_profile)
        if isinstance(service_principal, dict):
            service_principal = RedhatOpenshiftClusterServicePrincipal(**service_principal)
        if isinstance(worker_profile, dict):
            worker_profile = RedhatOpenshiftClusterWorkerProfile(**worker_profile)
        if isinstance(timeouts, dict):
            timeouts = RedhatOpenshiftClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e66fbb04929b6e3725e263b54959fe1620c6a4d497c8f70eee87664f265cfd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_server_profile", value=api_server_profile, expected_type=type_hints["api_server_profile"])
            check_type(argname="argument cluster_profile", value=cluster_profile, expected_type=type_hints["cluster_profile"])
            check_type(argname="argument ingress_profile", value=ingress_profile, expected_type=type_hints["ingress_profile"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument main_profile", value=main_profile, expected_type=type_hints["main_profile"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_profile", value=network_profile, expected_type=type_hints["network_profile"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument service_principal", value=service_principal, expected_type=type_hints["service_principal"])
            check_type(argname="argument worker_profile", value=worker_profile, expected_type=type_hints["worker_profile"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_server_profile": api_server_profile,
            "cluster_profile": cluster_profile,
            "ingress_profile": ingress_profile,
            "location": location,
            "main_profile": main_profile,
            "name": name,
            "network_profile": network_profile,
            "resource_group_name": resource_group_name,
            "service_principal": service_principal,
            "worker_profile": worker_profile,
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
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def api_server_profile(self) -> RedhatOpenshiftClusterApiServerProfile:
        '''api_server_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#api_server_profile RedhatOpenshiftCluster#api_server_profile}
        '''
        result = self._values.get("api_server_profile")
        assert result is not None, "Required property 'api_server_profile' is missing"
        return typing.cast(RedhatOpenshiftClusterApiServerProfile, result)

    @builtins.property
    def cluster_profile(self) -> RedhatOpenshiftClusterClusterProfile:
        '''cluster_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#cluster_profile RedhatOpenshiftCluster#cluster_profile}
        '''
        result = self._values.get("cluster_profile")
        assert result is not None, "Required property 'cluster_profile' is missing"
        return typing.cast(RedhatOpenshiftClusterClusterProfile, result)

    @builtins.property
    def ingress_profile(self) -> "RedhatOpenshiftClusterIngressProfile":
        '''ingress_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#ingress_profile RedhatOpenshiftCluster#ingress_profile}
        '''
        result = self._values.get("ingress_profile")
        assert result is not None, "Required property 'ingress_profile' is missing"
        return typing.cast("RedhatOpenshiftClusterIngressProfile", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#location RedhatOpenshiftCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def main_profile(self) -> "RedhatOpenshiftClusterMainProfile":
        '''main_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#main_profile RedhatOpenshiftCluster#main_profile}
        '''
        result = self._values.get("main_profile")
        assert result is not None, "Required property 'main_profile' is missing"
        return typing.cast("RedhatOpenshiftClusterMainProfile", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#name RedhatOpenshiftCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_profile(self) -> "RedhatOpenshiftClusterNetworkProfile":
        '''network_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#network_profile RedhatOpenshiftCluster#network_profile}
        '''
        result = self._values.get("network_profile")
        assert result is not None, "Required property 'network_profile' is missing"
        return typing.cast("RedhatOpenshiftClusterNetworkProfile", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#resource_group_name RedhatOpenshiftCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_principal(self) -> "RedhatOpenshiftClusterServicePrincipal":
        '''service_principal block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#service_principal RedhatOpenshiftCluster#service_principal}
        '''
        result = self._values.get("service_principal")
        assert result is not None, "Required property 'service_principal' is missing"
        return typing.cast("RedhatOpenshiftClusterServicePrincipal", result)

    @builtins.property
    def worker_profile(self) -> "RedhatOpenshiftClusterWorkerProfile":
        '''worker_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#worker_profile RedhatOpenshiftCluster#worker_profile}
        '''
        result = self._values.get("worker_profile")
        assert result is not None, "Required property 'worker_profile' is missing"
        return typing.cast("RedhatOpenshiftClusterWorkerProfile", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#id RedhatOpenshiftCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#tags RedhatOpenshiftCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RedhatOpenshiftClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#timeouts RedhatOpenshiftCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RedhatOpenshiftClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterIngressProfile",
    jsii_struct_bases=[],
    name_mapping={"visibility": "visibility"},
)
class RedhatOpenshiftClusterIngressProfile:
    def __init__(self, *, visibility: builtins.str) -> None:
        '''
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#visibility RedhatOpenshiftCluster#visibility}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada627e7846564293a3cebaf1e6d3dcba55b3e7dc1da68e18462cef393a5aea5)
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "visibility": visibility,
        }

    @builtins.property
    def visibility(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#visibility RedhatOpenshiftCluster#visibility}.'''
        result = self._values.get("visibility")
        assert result is not None, "Required property 'visibility' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterIngressProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterIngressProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterIngressProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b990be044b823374d5567bb1b6ad0944d17fa306d9bdad53c10fa42dd433b29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d98c108074c5ad6879864dd2b2a886814468258a1a3c74c48909651edab73d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterIngressProfile]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterIngressProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterIngressProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f25027e579a45441afaa3735c061f84ed83eea239ac5351678125b0e5efba66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterMainProfile",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_id": "subnetId",
        "vm_size": "vmSize",
        "disk_encryption_set_id": "diskEncryptionSetId",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
    },
)
class RedhatOpenshiftClusterMainProfile:
    def __init__(
        self,
        *,
        subnet_id: builtins.str,
        vm_size: builtins.str,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#subnet_id RedhatOpenshiftCluster#subnet_id}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#vm_size RedhatOpenshiftCluster#vm_size}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_encryption_set_id RedhatOpenshiftCluster#disk_encryption_set_id}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#encryption_at_host_enabled RedhatOpenshiftCluster#encryption_at_host_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34ca33ad147d2547e59da832f5f38cc2f83315aa438485a605db6175b61ae71)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument disk_encryption_set_id", value=disk_encryption_set_id, expected_type=type_hints["disk_encryption_set_id"])
            check_type(argname="argument encryption_at_host_enabled", value=encryption_at_host_enabled, expected_type=type_hints["encryption_at_host_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
            "vm_size": vm_size,
        }
        if disk_encryption_set_id is not None:
            self._values["disk_encryption_set_id"] = disk_encryption_set_id
        if encryption_at_host_enabled is not None:
            self._values["encryption_at_host_enabled"] = encryption_at_host_enabled

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#subnet_id RedhatOpenshiftCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#vm_size RedhatOpenshiftCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_encryption_set_id RedhatOpenshiftCluster#disk_encryption_set_id}.'''
        result = self._values.get("disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#encryption_at_host_enabled RedhatOpenshiftCluster#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterMainProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterMainProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterMainProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a41a6a002f179aa27d73c6c57bf3a17aa246fed52a01a04b6de14d462b274d85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskEncryptionSetId")
    def reset_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetEncryptionAtHostEnabled")
    def reset_encryption_at_host_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAtHostEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetIdInput")
    def disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAtHostEnabledInput")
    def encryption_at_host_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionAtHostEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionSetId"))

    @disk_encryption_set_id.setter
    def disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0aa208ab6b89951f60dda8be7e41cbf684cbc0c9007a66eddc208de918dc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c5b8eb043c3f9ee0f1d2fee392470debc29bf42d62c87d6158dfa43874965d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25101f99ddd4476c8c192b450e84c101971c932d2e0cf24fe0e273ed233d61c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c2bd130cc5acd6e43e1f1816b3f6bfcf392b568cceff978574acb79611e69c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterMainProfile]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterMainProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterMainProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4709bfe9ba2fd14f65a1e2c5af31bbacf86dc7e8b4916547a1c5a20a0e5a3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "pod_cidr": "podCidr",
        "service_cidr": "serviceCidr",
        "outbound_type": "outboundType",
        "preconfigured_network_security_group_enabled": "preconfiguredNetworkSecurityGroupEnabled",
    },
)
class RedhatOpenshiftClusterNetworkProfile:
    def __init__(
        self,
        *,
        pod_cidr: builtins.str,
        service_cidr: builtins.str,
        outbound_type: typing.Optional[builtins.str] = None,
        preconfigured_network_security_group_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pod_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#pod_cidr RedhatOpenshiftCluster#pod_cidr}.
        :param service_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#service_cidr RedhatOpenshiftCluster#service_cidr}.
        :param outbound_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#outbound_type RedhatOpenshiftCluster#outbound_type}.
        :param preconfigured_network_security_group_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#preconfigured_network_security_group_enabled RedhatOpenshiftCluster#preconfigured_network_security_group_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b09edd7bb8090c8494ac6a152f94970d120aae5084e69c0e7fb7216bbbcb15)
            check_type(argname="argument pod_cidr", value=pod_cidr, expected_type=type_hints["pod_cidr"])
            check_type(argname="argument service_cidr", value=service_cidr, expected_type=type_hints["service_cidr"])
            check_type(argname="argument outbound_type", value=outbound_type, expected_type=type_hints["outbound_type"])
            check_type(argname="argument preconfigured_network_security_group_enabled", value=preconfigured_network_security_group_enabled, expected_type=type_hints["preconfigured_network_security_group_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pod_cidr": pod_cidr,
            "service_cidr": service_cidr,
        }
        if outbound_type is not None:
            self._values["outbound_type"] = outbound_type
        if preconfigured_network_security_group_enabled is not None:
            self._values["preconfigured_network_security_group_enabled"] = preconfigured_network_security_group_enabled

    @builtins.property
    def pod_cidr(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#pod_cidr RedhatOpenshiftCluster#pod_cidr}.'''
        result = self._values.get("pod_cidr")
        assert result is not None, "Required property 'pod_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_cidr(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#service_cidr RedhatOpenshiftCluster#service_cidr}.'''
        result = self._values.get("service_cidr")
        assert result is not None, "Required property 'service_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def outbound_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#outbound_type RedhatOpenshiftCluster#outbound_type}.'''
        result = self._values.get("outbound_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preconfigured_network_security_group_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#preconfigured_network_security_group_enabled RedhatOpenshiftCluster#preconfigured_network_security_group_enabled}.'''
        result = self._values.get("preconfigured_network_security_group_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f73564c47e089f7a7d2dd6152c052dc557009d8c4065d105015a45658e81cd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOutboundType")
    def reset_outbound_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundType", []))

    @jsii.member(jsii_name="resetPreconfiguredNetworkSecurityGroupEnabled")
    def reset_preconfigured_network_security_group_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreconfiguredNetworkSecurityGroupEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="outboundTypeInput")
    def outbound_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outboundTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="podCidrInput")
    def pod_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredNetworkSecurityGroupEnabledInput")
    def preconfigured_network_security_group_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preconfiguredNetworkSecurityGroupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceCidrInput")
    def service_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundType")
    def outbound_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundType"))

    @outbound_type.setter
    def outbound_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9e84b034d5bfabdd0104bd7682b59a82e38232d79ec429e6b770e2e2125632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podCidr")
    def pod_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podCidr"))

    @pod_cidr.setter
    def pod_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40caf2ddbb8412c64e3f6935a31d736cc1229e1b230200a60197931de2ba2721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preconfiguredNetworkSecurityGroupEnabled")
    def preconfigured_network_security_group_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preconfiguredNetworkSecurityGroupEnabled"))

    @preconfigured_network_security_group_enabled.setter
    def preconfigured_network_security_group_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958a7d777b77d3d84fa2fcc900c0507b0bdbadea539fc95487f526c21342a5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preconfiguredNetworkSecurityGroupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceCidr")
    def service_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceCidr"))

    @service_cidr.setter
    def service_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ae7612b1bff98989735c7ed6b89f5f34daf01082e868899bd6931fa9d7a6ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterNetworkProfile]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f9ec5b2347db4c516ab4888e2353ad901e89997b8f71436e98dcd17debdede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterServicePrincipal",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class RedhatOpenshiftClusterServicePrincipal:
    def __init__(self, *, client_id: builtins.str, client_secret: builtins.str) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#client_id RedhatOpenshiftCluster#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#client_secret RedhatOpenshiftCluster#client_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7027fca082f6b392c7cce951aeb3ddf662c7851915408787e939d9a19cc08d)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#client_id RedhatOpenshiftCluster#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#client_secret RedhatOpenshiftCluster#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterServicePrincipal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterServicePrincipalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterServicePrincipalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82f0deca5d932329c5b0a20a0870acba7a8a58f0a3b245a052d52335369285ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee352b3601d21f847ea1cf323e2b60a2c96abbb4cd63e5fc96b7e04198434a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0551e9d4c7182305773b9833baf6ffb93bcec4ac82698f02bfecf0e849e87bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterServicePrincipal]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterServicePrincipal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterServicePrincipal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c580c69795fdc63a393ed8a87b15ce90eb3ddf2ac6c074a9ea5d96826958c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class RedhatOpenshiftClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#create RedhatOpenshiftCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#delete RedhatOpenshiftCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#read RedhatOpenshiftCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#update RedhatOpenshiftCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a838ebc82fc4b628d44b9d35efd6990b19a1f8821839f5f04b3a3fbd7464bb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#create RedhatOpenshiftCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#delete RedhatOpenshiftCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#read RedhatOpenshiftCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#update RedhatOpenshiftCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e137e12b0bf4bc1cccf0ce92bba54d310fd1d86ce5b7156e83101f72e063290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c06facfff33193beea1c0d64fb2e77cd5a83e2c64e3140f22bf264e9194ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a013f661ca0652da962708e76c9122d5b08ebac1363743470f7dda1b34431b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c200ff3559a66acc846135d71760b23c50d7e5ab905519ba4ba16e4089350d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff77add677c70c13a015bbcf348c417bd49f7baa4fc26ef9d087bc950ba14ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedhatOpenshiftClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedhatOpenshiftClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedhatOpenshiftClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ba9c4664a3fee03776dcdba03f6e7a287dad58b94a15643a0d597d4b4e2532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterWorkerProfile",
    jsii_struct_bases=[],
    name_mapping={
        "disk_size_gb": "diskSizeGb",
        "node_count": "nodeCount",
        "subnet_id": "subnetId",
        "vm_size": "vmSize",
        "disk_encryption_set_id": "diskEncryptionSetId",
        "encryption_at_host_enabled": "encryptionAtHostEnabled",
    },
)
class RedhatOpenshiftClusterWorkerProfile:
    def __init__(
        self,
        *,
        disk_size_gb: jsii.Number,
        node_count: jsii.Number,
        subnet_id: builtins.str,
        vm_size: builtins.str,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_size_gb RedhatOpenshiftCluster#disk_size_gb}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#node_count RedhatOpenshiftCluster#node_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#subnet_id RedhatOpenshiftCluster#subnet_id}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#vm_size RedhatOpenshiftCluster#vm_size}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_encryption_set_id RedhatOpenshiftCluster#disk_encryption_set_id}.
        :param encryption_at_host_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#encryption_at_host_enabled RedhatOpenshiftCluster#encryption_at_host_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b316c8fb5c6b2e476272d85eb654bceb5a5f97c74e5d0f4a145205581fe11e7)
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument disk_encryption_set_id", value=disk_encryption_set_id, expected_type=type_hints["disk_encryption_set_id"])
            check_type(argname="argument encryption_at_host_enabled", value=encryption_at_host_enabled, expected_type=type_hints["encryption_at_host_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_size_gb": disk_size_gb,
            "node_count": node_count,
            "subnet_id": subnet_id,
            "vm_size": vm_size,
        }
        if disk_encryption_set_id is not None:
            self._values["disk_encryption_set_id"] = disk_encryption_set_id
        if encryption_at_host_enabled is not None:
            self._values["encryption_at_host_enabled"] = encryption_at_host_enabled

    @builtins.property
    def disk_size_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_size_gb RedhatOpenshiftCluster#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        assert result is not None, "Required property 'disk_size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#node_count RedhatOpenshiftCluster#node_count}.'''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#subnet_id RedhatOpenshiftCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#vm_size RedhatOpenshiftCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#disk_encryption_set_id RedhatOpenshiftCluster#disk_encryption_set_id}.'''
        result = self._values.get("disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_host_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redhat_openshift_cluster#encryption_at_host_enabled RedhatOpenshiftCluster#encryption_at_host_enabled}.'''
        result = self._values.get("encryption_at_host_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedhatOpenshiftClusterWorkerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedhatOpenshiftClusterWorkerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redhatOpenshiftCluster.RedhatOpenshiftClusterWorkerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8db0fc692ce8d3c5eaf211cccbd8a2931be80b3c45f13b0e91025dc51bafe27a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskEncryptionSetId")
    def reset_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetEncryptionAtHostEnabled")
    def reset_encryption_at_host_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAtHostEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetIdInput")
    def disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAtHostEnabledInput")
    def encryption_at_host_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionAtHostEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionSetId"))

    @disk_encryption_set_id.setter
    def disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b4b29a9ba0a178123367cc91facb61ecad287ad69f2b2dfa89dc72ce04b073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fef88a721b8d748cf9fc460ab0d75cc6b3ebeababa84baa615d1c35de3f5dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__682e5a48960b8b09e9bcedc93d66a06fd32ee90392b1f7fd6c498f87baf91842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtHostEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb4801a41f5b4aa96b117cb87fa038653b267774cc70e23e995f99c0fa35704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b518b456f5cd27a30da60024b7d3cd6e707e93f87c7069e037e9855af7b1c2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7aeed5c0282db8d2f7daa11b271a4d5ffd48639fe956a98206e92d1b1b6368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedhatOpenshiftClusterWorkerProfile]:
        return typing.cast(typing.Optional[RedhatOpenshiftClusterWorkerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedhatOpenshiftClusterWorkerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5c77e414aec6451bec639f93621b855f776cc0dfd65f6cf92e8daaf73ca02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RedhatOpenshiftCluster",
    "RedhatOpenshiftClusterApiServerProfile",
    "RedhatOpenshiftClusterApiServerProfileOutputReference",
    "RedhatOpenshiftClusterClusterProfile",
    "RedhatOpenshiftClusterClusterProfileOutputReference",
    "RedhatOpenshiftClusterConfig",
    "RedhatOpenshiftClusterIngressProfile",
    "RedhatOpenshiftClusterIngressProfileOutputReference",
    "RedhatOpenshiftClusterMainProfile",
    "RedhatOpenshiftClusterMainProfileOutputReference",
    "RedhatOpenshiftClusterNetworkProfile",
    "RedhatOpenshiftClusterNetworkProfileOutputReference",
    "RedhatOpenshiftClusterServicePrincipal",
    "RedhatOpenshiftClusterServicePrincipalOutputReference",
    "RedhatOpenshiftClusterTimeouts",
    "RedhatOpenshiftClusterTimeoutsOutputReference",
    "RedhatOpenshiftClusterWorkerProfile",
    "RedhatOpenshiftClusterWorkerProfileOutputReference",
]

publication.publish()

def _typecheckingstub__07a393f34033b47918dc08be1edfc657bcbfa98df9a61904a173ed7e5659a3df(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_server_profile: typing.Union[RedhatOpenshiftClusterApiServerProfile, typing.Dict[builtins.str, typing.Any]],
    cluster_profile: typing.Union[RedhatOpenshiftClusterClusterProfile, typing.Dict[builtins.str, typing.Any]],
    ingress_profile: typing.Union[RedhatOpenshiftClusterIngressProfile, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    main_profile: typing.Union[RedhatOpenshiftClusterMainProfile, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network_profile: typing.Union[RedhatOpenshiftClusterNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    service_principal: typing.Union[RedhatOpenshiftClusterServicePrincipal, typing.Dict[builtins.str, typing.Any]],
    worker_profile: typing.Union[RedhatOpenshiftClusterWorkerProfile, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RedhatOpenshiftClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ac0885cf4b5df447a2fbc1f83d773c33e0b5b3c3332ded1bd0c5a1f565256fb0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daea0639f35c7b54cf91416c0ffadd954a8383ab32e2fdbc38decb6600438a61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2e059cd748fc399490db78169aed7f7ad9c5fe795a8679b72825d98f9b5f79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9901da455c06e2fd8ec983cd5c1513dffebf1b1e8edb5d44644fed4d18c537b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a47deb333a251cfb0180d3008991b110eee841f2e4425a93bd17609a48d6a80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8030d9783593a73446a1bb99635e61beba41b7602bf09fa57fbe6f1441860458(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554d188f501759bbc9bd72ee615b91714aa9bbe5d7e320e6a9181afc4df84238(
    *,
    visibility: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc723a3e2233e04b8b93423277d919e816daa5d9027fdc071080a2a12b37c883(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6498652767b1f1fc32340052d5bc714d083e995e09755717b1498dccf397365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001027c2de70ff0eba363924dfb0313a8fb2fd9e1d9a2b39f22e517b70fa7b1d(
    value: typing.Optional[RedhatOpenshiftClusterApiServerProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2947add45d7d3e10fbc849adaaa1bce9aaed7b520f9f9a5567e8bf86aab47df1(
    *,
    domain: builtins.str,
    version: builtins.str,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    pull_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55dc3d2632f8e8c04ffd474730a0c36009362d1eab90fec070127c6f12cfc6cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7df1a408955634197bfccbb3627af3bda321fdc9d4cadd3b01130c8bd7cc4a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ced0bdc3d0463cc0571fc0ea7b9459461ea9777b0ccbf36f4ca0e4c0bc07390(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63ef6fc1262e40efe483203820b85d9cbec67f79c348b9cd37aae95520b4110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14132a3664fc7ec862564c7c9616460b84d11e9ab98ff7b516359eedda770f30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70981ca83eb703dc61e20bc084fc73240edba1c16b8258bbd867a995d83e8c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8e08dbad31a9c088959764bb41ce5a3d34b55cb5d67ffbcaf493794c7b0873(
    value: typing.Optional[RedhatOpenshiftClusterClusterProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e66fbb04929b6e3725e263b54959fe1620c6a4d497c8f70eee87664f265cfd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_server_profile: typing.Union[RedhatOpenshiftClusterApiServerProfile, typing.Dict[builtins.str, typing.Any]],
    cluster_profile: typing.Union[RedhatOpenshiftClusterClusterProfile, typing.Dict[builtins.str, typing.Any]],
    ingress_profile: typing.Union[RedhatOpenshiftClusterIngressProfile, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    main_profile: typing.Union[RedhatOpenshiftClusterMainProfile, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    network_profile: typing.Union[RedhatOpenshiftClusterNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    service_principal: typing.Union[RedhatOpenshiftClusterServicePrincipal, typing.Dict[builtins.str, typing.Any]],
    worker_profile: typing.Union[RedhatOpenshiftClusterWorkerProfile, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RedhatOpenshiftClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada627e7846564293a3cebaf1e6d3dcba55b3e7dc1da68e18462cef393a5aea5(
    *,
    visibility: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b990be044b823374d5567bb1b6ad0944d17fa306d9bdad53c10fa42dd433b29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d98c108074c5ad6879864dd2b2a886814468258a1a3c74c48909651edab73d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f25027e579a45441afaa3735c061f84ed83eea239ac5351678125b0e5efba66(
    value: typing.Optional[RedhatOpenshiftClusterIngressProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34ca33ad147d2547e59da832f5f38cc2f83315aa438485a605db6175b61ae71(
    *,
    subnet_id: builtins.str,
    vm_size: builtins.str,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41a6a002f179aa27d73c6c57bf3a17aa246fed52a01a04b6de14d462b274d85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0aa208ab6b89951f60dda8be7e41cbf684cbc0c9007a66eddc208de918dc9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c5b8eb043c3f9ee0f1d2fee392470debc29bf42d62c87d6158dfa43874965d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25101f99ddd4476c8c192b450e84c101971c932d2e0cf24fe0e273ed233d61c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c2bd130cc5acd6e43e1f1816b3f6bfcf392b568cceff978574acb79611e69c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4709bfe9ba2fd14f65a1e2c5af31bbacf86dc7e8b4916547a1c5a20a0e5a3fd(
    value: typing.Optional[RedhatOpenshiftClusterMainProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b09edd7bb8090c8494ac6a152f94970d120aae5084e69c0e7fb7216bbbcb15(
    *,
    pod_cidr: builtins.str,
    service_cidr: builtins.str,
    outbound_type: typing.Optional[builtins.str] = None,
    preconfigured_network_security_group_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f73564c47e089f7a7d2dd6152c052dc557009d8c4065d105015a45658e81cd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9e84b034d5bfabdd0104bd7682b59a82e38232d79ec429e6b770e2e2125632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40caf2ddbb8412c64e3f6935a31d736cc1229e1b230200a60197931de2ba2721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958a7d777b77d3d84fa2fcc900c0507b0bdbadea539fc95487f526c21342a5ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ae7612b1bff98989735c7ed6b89f5f34daf01082e868899bd6931fa9d7a6ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f9ec5b2347db4c516ab4888e2353ad901e89997b8f71436e98dcd17debdede(
    value: typing.Optional[RedhatOpenshiftClusterNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7027fca082f6b392c7cce951aeb3ddf662c7851915408787e939d9a19cc08d(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f0deca5d932329c5b0a20a0870acba7a8a58f0a3b245a052d52335369285ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee352b3601d21f847ea1cf323e2b60a2c96abbb4cd63e5fc96b7e04198434a08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0551e9d4c7182305773b9833baf6ffb93bcec4ac82698f02bfecf0e849e87bbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c580c69795fdc63a393ed8a87b15ce90eb3ddf2ac6c074a9ea5d96826958c1(
    value: typing.Optional[RedhatOpenshiftClusterServicePrincipal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a838ebc82fc4b628d44b9d35efd6990b19a1f8821839f5f04b3a3fbd7464bb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e137e12b0bf4bc1cccf0ce92bba54d310fd1d86ce5b7156e83101f72e063290(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c06facfff33193beea1c0d64fb2e77cd5a83e2c64e3140f22bf264e9194ca2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a013f661ca0652da962708e76c9122d5b08ebac1363743470f7dda1b34431b59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c200ff3559a66acc846135d71760b23c50d7e5ab905519ba4ba16e4089350d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff77add677c70c13a015bbcf348c417bd49f7baa4fc26ef9d087bc950ba14ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ba9c4664a3fee03776dcdba03f6e7a287dad58b94a15643a0d597d4b4e2532(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedhatOpenshiftClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b316c8fb5c6b2e476272d85eb654bceb5a5f97c74e5d0f4a145205581fe11e7(
    *,
    disk_size_gb: jsii.Number,
    node_count: jsii.Number,
    subnet_id: builtins.str,
    vm_size: builtins.str,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    encryption_at_host_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db0fc692ce8d3c5eaf211cccbd8a2931be80b3c45f13b0e91025dc51bafe27a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b4b29a9ba0a178123367cc91facb61ecad287ad69f2b2dfa89dc72ce04b073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fef88a721b8d748cf9fc460ab0d75cc6b3ebeababa84baa615d1c35de3f5dfb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682e5a48960b8b09e9bcedc93d66a06fd32ee90392b1f7fd6c498f87baf91842(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb4801a41f5b4aa96b117cb87fa038653b267774cc70e23e995f99c0fa35704(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b518b456f5cd27a30da60024b7d3cd6e707e93f87c7069e037e9855af7b1c2f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7aeed5c0282db8d2f7daa11b271a4d5ffd48639fe956a98206e92d1b1b6368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5c77e414aec6451bec639f93621b855f776cc0dfd65f6cf92e8daaf73ca02d(
    value: typing.Optional[RedhatOpenshiftClusterWorkerProfile],
) -> None:
    """Type checking stubs"""
    pass
