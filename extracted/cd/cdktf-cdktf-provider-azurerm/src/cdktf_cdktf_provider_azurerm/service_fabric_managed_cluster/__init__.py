r'''
# `azurerm_service_fabric_managed_cluster`

Refer to the Terraform Registry for docs: [`azurerm_service_fabric_managed_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster).
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


class ServiceFabricManagedCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster azurerm_service_fabric_managed_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        client_connection_port: jsii.Number,
        http_gateway_port: jsii.Number,
        lb_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterLbRule", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        authentication: typing.Optional[typing.Union["ServiceFabricManagedClusterAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_fabric_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterCustomFabricSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_name: typing.Optional[builtins.str] = None,
        dns_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterNodeType", typing.Dict[builtins.str, typing.Any]]]]] = None,
        password: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ServiceFabricManagedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_wave: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster azurerm_service_fabric_managed_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_connection_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#client_connection_port ServiceFabricManagedCluster#client_connection_port}.
        :param http_gateway_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#http_gateway_port ServiceFabricManagedCluster#http_gateway_port}.
        :param lb_rule: lb_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#lb_rule ServiceFabricManagedCluster#lb_rule}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#location ServiceFabricManagedCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#name ServiceFabricManagedCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#resource_group_name ServiceFabricManagedCluster#resource_group_name}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#authentication ServiceFabricManagedCluster#authentication}
        :param backup_service_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#backup_service_enabled ServiceFabricManagedCluster#backup_service_enabled}.
        :param custom_fabric_setting: custom_fabric_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#custom_fabric_setting ServiceFabricManagedCluster#custom_fabric_setting}
        :param dns_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#dns_name ServiceFabricManagedCluster#dns_name}.
        :param dns_service_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#dns_service_enabled ServiceFabricManagedCluster#dns_service_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#id ServiceFabricManagedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_type: node_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#node_type ServiceFabricManagedCluster#node_type}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#password ServiceFabricManagedCluster#password}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#sku ServiceFabricManagedCluster#sku}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#subnet_id ServiceFabricManagedCluster#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#tags ServiceFabricManagedCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#timeouts ServiceFabricManagedCluster#timeouts}
        :param upgrade_wave: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#upgrade_wave ServiceFabricManagedCluster#upgrade_wave}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#username ServiceFabricManagedCluster#username}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4bded4d0b410ddea933427da1948d57b33860350daf743e35a5a6e8f7886e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceFabricManagedClusterConfig(
            client_connection_port=client_connection_port,
            http_gateway_port=http_gateway_port,
            lb_rule=lb_rule,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            authentication=authentication,
            backup_service_enabled=backup_service_enabled,
            custom_fabric_setting=custom_fabric_setting,
            dns_name=dns_name,
            dns_service_enabled=dns_service_enabled,
            id=id,
            node_type=node_type,
            password=password,
            sku=sku,
            subnet_id=subnet_id,
            tags=tags,
            timeouts=timeouts,
            upgrade_wave=upgrade_wave,
            username=username,
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
        '''Generates CDKTF code for importing a ServiceFabricManagedCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceFabricManagedCluster to import.
        :param import_from_id: The id of the existing ServiceFabricManagedCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceFabricManagedCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcc2e081386bf02d8717cd4f45db1f27757e9434c8a18ba9a3c7d90d4a69653)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        *,
        active_directory: typing.Optional[typing.Union["ServiceFabricManagedClusterAuthenticationActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterAuthenticationCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#active_directory ServiceFabricManagedCluster#active_directory}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#certificate ServiceFabricManagedCluster#certificate}
        '''
        value = ServiceFabricManagedClusterAuthentication(
            active_directory=active_directory, certificate=certificate
        )

        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="putCustomFabricSetting")
    def put_custom_fabric_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterCustomFabricSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03025382ca59460e5cd88042f4d6e766bda030603f18c846b238dcb6eb9d7f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomFabricSetting", [value]))

    @jsii.member(jsii_name="putLbRule")
    def put_lb_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterLbRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d77ebd00dec3d20db6122d322e436cd1d2a12df83c1f86a349a02f6a7bb724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLbRule", [value]))

    @jsii.member(jsii_name="putNodeType")
    def put_node_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterNodeType", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a09500851e7cc390f03b4b8885499250e2b4cedca31c0918edf45dc17804c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeType", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#create ServiceFabricManagedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#delete ServiceFabricManagedCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#read ServiceFabricManagedCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#update ServiceFabricManagedCluster#update}.
        '''
        value = ServiceFabricManagedClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @jsii.member(jsii_name="resetBackupServiceEnabled")
    def reset_backup_service_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupServiceEnabled", []))

    @jsii.member(jsii_name="resetCustomFabricSetting")
    def reset_custom_fabric_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomFabricSetting", []))

    @jsii.member(jsii_name="resetDnsName")
    def reset_dns_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsName", []))

    @jsii.member(jsii_name="resetDnsServiceEnabled")
    def reset_dns_service_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServiceEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetSku")
    def reset_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSku", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpgradeWave")
    def reset_upgrade_wave(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeWave", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

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
    @jsii.member(jsii_name="authentication")
    def authentication(
        self,
    ) -> "ServiceFabricManagedClusterAuthenticationOutputReference":
        return typing.cast("ServiceFabricManagedClusterAuthenticationOutputReference", jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="customFabricSetting")
    def custom_fabric_setting(
        self,
    ) -> "ServiceFabricManagedClusterCustomFabricSettingList":
        return typing.cast("ServiceFabricManagedClusterCustomFabricSettingList", jsii.get(self, "customFabricSetting"))

    @builtins.property
    @jsii.member(jsii_name="lbRule")
    def lb_rule(self) -> "ServiceFabricManagedClusterLbRuleList":
        return typing.cast("ServiceFabricManagedClusterLbRuleList", jsii.get(self, "lbRule"))

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> "ServiceFabricManagedClusterNodeTypeList":
        return typing.cast("ServiceFabricManagedClusterNodeTypeList", jsii.get(self, "nodeType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServiceFabricManagedClusterTimeoutsOutputReference":
        return typing.cast("ServiceFabricManagedClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional["ServiceFabricManagedClusterAuthentication"]:
        return typing.cast(typing.Optional["ServiceFabricManagedClusterAuthentication"], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="backupServiceEnabledInput")
    def backup_service_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backupServiceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientConnectionPortInput")
    def client_connection_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientConnectionPortInput"))

    @builtins.property
    @jsii.member(jsii_name="customFabricSettingInput")
    def custom_fabric_setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterCustomFabricSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterCustomFabricSetting"]]], jsii.get(self, "customFabricSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNameInput")
    def dns_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServiceEnabledInput")
    def dns_service_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dnsServiceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGatewayPortInput")
    def http_gateway_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpGatewayPortInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lbRuleInput")
    def lb_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterLbRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterLbRule"]]], jsii.get(self, "lbRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeType"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeType"]]], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceFabricManagedClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceFabricManagedClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeWaveInput")
    def upgrade_wave_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "upgradeWaveInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="backupServiceEnabled")
    def backup_service_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backupServiceEnabled"))

    @backup_service_enabled.setter
    def backup_service_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d79a1636da5d0dd58480096f42fa4ce303fedf678e978596e7eeb86713042cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupServiceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientConnectionPort")
    def client_connection_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientConnectionPort"))

    @client_connection_port.setter
    def client_connection_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca941098fb29e9439971131d1a9ee572eca0fd746fb09f7bfe8a4268c5bcbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientConnectionPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @dns_name.setter
    def dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02f019ccb42f09ac5b53b425968b33e8fee2627fd777e5c52229af589944591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsServiceEnabled")
    def dns_service_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dnsServiceEnabled"))

    @dns_service_enabled.setter
    def dns_service_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93042936b195b9c974ada4f7ad026aef4e9b7488b11c973c91dfa771f07ce9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServiceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpGatewayPort")
    def http_gateway_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpGatewayPort"))

    @http_gateway_port.setter
    def http_gateway_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab8329d6156cdc4262cdb0e6639a0b535fe9bfb5473c3779fc322bb8d24e1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpGatewayPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a18044346d2464ed1e1f0a04fb7e932676e71c9a7066a5c944241e01ba238bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8a970b0bf20f35b8de55d3d2f11d0bd2ab33f1a3fa361e86d36d495d9cb45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b78f388cfdd3fc0235439c76cbe5ee9da862638642ef0f0c184f84c9bd5d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc977824348a6b27fc9897dd93885e96e115736c7163bcd7f7a28d786fe0ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86470a7364547e7afa6bcb4302b32232f127b8580b14ff1b2566f7d37a32b965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f2b0c408f6921acbf1bbbf752fb66fad2f3d43ab6f9449938a78b5b21672de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cbefe4708e8c3f6f3b5f1100544f351a70e078c19168dc5d801b0a1acba7c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193434f637862cd2c6348424631d0bcc6bf80bcb37c8d7e649a0997450b8b442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upgradeWave")
    def upgrade_wave(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeWave"))

    @upgrade_wave.setter
    def upgrade_wave(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc10d2b9242a1bf18f6246af91a53d7f73a295099f2e91d1cdd04c18207f00d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upgradeWave", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b31ee344fa7a19853a2a953f326b898777c7ead00103aa304faaa0c0087372e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthentication",
    jsii_struct_bases=[],
    name_mapping={"active_directory": "activeDirectory", "certificate": "certificate"},
)
class ServiceFabricManagedClusterAuthentication:
    def __init__(
        self,
        *,
        active_directory: typing.Optional[typing.Union["ServiceFabricManagedClusterAuthenticationActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterAuthenticationCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#active_directory ServiceFabricManagedCluster#active_directory}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#certificate ServiceFabricManagedCluster#certificate}
        '''
        if isinstance(active_directory, dict):
            active_directory = ServiceFabricManagedClusterAuthenticationActiveDirectory(**active_directory)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620c8e8d9dc0741b99f3a8bad99c0ac9ea61cef05b5bb292169a114583ff309c)
            check_type(argname="argument active_directory", value=active_directory, expected_type=type_hints["active_directory"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_directory is not None:
            self._values["active_directory"] = active_directory
        if certificate is not None:
            self._values["certificate"] = certificate

    @builtins.property
    def active_directory(
        self,
    ) -> typing.Optional["ServiceFabricManagedClusterAuthenticationActiveDirectory"]:
        '''active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#active_directory ServiceFabricManagedCluster#active_directory}
        '''
        result = self._values.get("active_directory")
        return typing.cast(typing.Optional["ServiceFabricManagedClusterAuthenticationActiveDirectory"], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterAuthenticationCertificate"]]]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#certificate ServiceFabricManagedCluster#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterAuthenticationCertificate"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthenticationActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "client_application_id": "clientApplicationId",
        "cluster_application_id": "clusterApplicationId",
        "tenant_id": "tenantId",
    },
)
class ServiceFabricManagedClusterAuthenticationActiveDirectory:
    def __init__(
        self,
        *,
        client_application_id: builtins.str,
        cluster_application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param client_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#client_application_id ServiceFabricManagedCluster#client_application_id}.
        :param cluster_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#cluster_application_id ServiceFabricManagedCluster#cluster_application_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#tenant_id ServiceFabricManagedCluster#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf09d4c04329a479ba31cf431329ac6164fdea58dc77dc8b213a3e2e5b7a5d3)
            check_type(argname="argument client_application_id", value=client_application_id, expected_type=type_hints["client_application_id"])
            check_type(argname="argument cluster_application_id", value=cluster_application_id, expected_type=type_hints["cluster_application_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_application_id": client_application_id,
            "cluster_application_id": cluster_application_id,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def client_application_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#client_application_id ServiceFabricManagedCluster#client_application_id}.'''
        result = self._values.get("client_application_id")
        assert result is not None, "Required property 'client_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_application_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#cluster_application_id ServiceFabricManagedCluster#cluster_application_id}.'''
        result = self._values.get("cluster_application_id")
        assert result is not None, "Required property 'cluster_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#tenant_id ServiceFabricManagedCluster#tenant_id}.'''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterAuthenticationActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterAuthenticationActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthenticationActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d2e0d977025c9d6bb34e79d6e21bebdf1bbb216bae1394c2ad2cb835dbc4361)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientApplicationIdInput")
    def client_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterApplicationIdInput")
    def cluster_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientApplicationId")
    def client_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientApplicationId"))

    @client_application_id.setter
    def client_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d424c35b473a67327b62a96bdaeb4039a1e85a418a0d3f5f8ab78ca88d2efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterApplicationId")
    def cluster_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterApplicationId"))

    @cluster_application_id.setter
    def cluster_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f7a8caeae31109bfd1c9b27d7a2d568791b051370b6262168608cc0bacdd18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d32a37fd174abcea4475e1589ab52d6622fd17186e412066ba6d6b2147c30e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricManagedClusterAuthenticationActiveDirectory]:
        return typing.cast(typing.Optional[ServiceFabricManagedClusterAuthenticationActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricManagedClusterAuthenticationActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599be36ec3bbf28f5357fe2923ef2d38bc3f1fe19db268d3ae764c0f1580f7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthenticationCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "thumbprint": "thumbprint",
        "type": "type",
        "common_name": "commonName",
    },
)
class ServiceFabricManagedClusterAuthenticationCertificate:
    def __init__(
        self,
        *,
        thumbprint: builtins.str,
        type: builtins.str,
        common_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#thumbprint ServiceFabricManagedCluster#thumbprint}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#type ServiceFabricManagedCluster#type}.
        :param common_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#common_name ServiceFabricManagedCluster#common_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3713d1925e869802e00087b8fdc20a0d2a933c6fbaa1d4d1b14a8dd37833164)
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thumbprint": thumbprint,
            "type": type,
        }
        if common_name is not None:
            self._values["common_name"] = common_name

    @builtins.property
    def thumbprint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#thumbprint ServiceFabricManagedCluster#thumbprint}.'''
        result = self._values.get("thumbprint")
        assert result is not None, "Required property 'thumbprint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#type ServiceFabricManagedCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#common_name ServiceFabricManagedCluster#common_name}.'''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterAuthenticationCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterAuthenticationCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthenticationCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fefd10c66133ec8710c7d154c4e6fb1e43b8d29533adb32761be385db9508c6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricManagedClusterAuthenticationCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b2e5154ea78fc8ac8091be3622113573352592de418bbc28226edca7d2b3f8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricManagedClusterAuthenticationCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbee88948cf022266c2e93ef891ee74558ff5ea9507c40d96f3f36d7638f6e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2ba7a967cc6add1e0383cbc8c7fbec8861d1dc8745d6db84792b9b5f6507c02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fb137673a560dbf5cdf4194316a43b523b4883c6db1f98cf67181bb8d67227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterAuthenticationCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterAuthenticationCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterAuthenticationCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2433cbec0477397442fb8ee1bfed535b222f0b0c14088afd325fa9a6cfeb237d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterAuthenticationCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthenticationCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f765817a36806e9fd980238f0422f859aec3557ab6e2177de2caad1e636ec8fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa91cc9a6a118faa8dc16c9bf768e7952e3993326c50f3b2f7cb881fa10bc646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204d485e5f99d5b0015fb0b389ca7c7c04c215017eab56bd1aef5ee4553d8dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5fc0ce4cef4fb35ca983006e614248c5d88720a1a3f5725cb142073c0ba15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterAuthenticationCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterAuthenticationCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterAuthenticationCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd54f7c5dae5f26c321b26b792b80db8cb569d936dd0d0c340fd05828faf4d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__000faa6a6624386d39b7d9ec9dd3dcec7a32f46a6736f796475e1dad2fe60119)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectory")
    def put_active_directory(
        self,
        *,
        client_application_id: builtins.str,
        cluster_application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param client_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#client_application_id ServiceFabricManagedCluster#client_application_id}.
        :param cluster_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#cluster_application_id ServiceFabricManagedCluster#cluster_application_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#tenant_id ServiceFabricManagedCluster#tenant_id}.
        '''
        value = ServiceFabricManagedClusterAuthenticationActiveDirectory(
            client_application_id=client_application_id,
            cluster_application_id=cluster_application_id,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDirectory", [value]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c65ace1ba86e2537b077644fbcb079acf6e6d930793389fd041d280abc89db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="resetActiveDirectory")
    def reset_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectory", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(
        self,
    ) -> ServiceFabricManagedClusterAuthenticationActiveDirectoryOutputReference:
        return typing.cast(ServiceFabricManagedClusterAuthenticationActiveDirectoryOutputReference, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> ServiceFabricManagedClusterAuthenticationCertificateList:
        return typing.cast(ServiceFabricManagedClusterAuthenticationCertificateList, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryInput")
    def active_directory_input(
        self,
    ) -> typing.Optional[ServiceFabricManagedClusterAuthenticationActiveDirectory]:
        return typing.cast(typing.Optional[ServiceFabricManagedClusterAuthenticationActiveDirectory], jsii.get(self, "activeDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterAuthenticationCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterAuthenticationCertificate]]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceFabricManagedClusterAuthentication]:
        return typing.cast(typing.Optional[ServiceFabricManagedClusterAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFabricManagedClusterAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abe0f2366dd6e732e5a9b530d464706851d522cf82750d3751f87a4b2837112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_connection_port": "clientConnectionPort",
        "http_gateway_port": "httpGatewayPort",
        "lb_rule": "lbRule",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "authentication": "authentication",
        "backup_service_enabled": "backupServiceEnabled",
        "custom_fabric_setting": "customFabricSetting",
        "dns_name": "dnsName",
        "dns_service_enabled": "dnsServiceEnabled",
        "id": "id",
        "node_type": "nodeType",
        "password": "password",
        "sku": "sku",
        "subnet_id": "subnetId",
        "tags": "tags",
        "timeouts": "timeouts",
        "upgrade_wave": "upgradeWave",
        "username": "username",
    },
)
class ServiceFabricManagedClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_connection_port: jsii.Number,
        http_gateway_port: jsii.Number,
        lb_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterLbRule", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        authentication: typing.Optional[typing.Union[ServiceFabricManagedClusterAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_fabric_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterCustomFabricSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_name: typing.Optional[builtins.str] = None,
        dns_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterNodeType", typing.Dict[builtins.str, typing.Any]]]]] = None,
        password: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ServiceFabricManagedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        upgrade_wave: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_connection_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#client_connection_port ServiceFabricManagedCluster#client_connection_port}.
        :param http_gateway_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#http_gateway_port ServiceFabricManagedCluster#http_gateway_port}.
        :param lb_rule: lb_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#lb_rule ServiceFabricManagedCluster#lb_rule}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#location ServiceFabricManagedCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#name ServiceFabricManagedCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#resource_group_name ServiceFabricManagedCluster#resource_group_name}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#authentication ServiceFabricManagedCluster#authentication}
        :param backup_service_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#backup_service_enabled ServiceFabricManagedCluster#backup_service_enabled}.
        :param custom_fabric_setting: custom_fabric_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#custom_fabric_setting ServiceFabricManagedCluster#custom_fabric_setting}
        :param dns_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#dns_name ServiceFabricManagedCluster#dns_name}.
        :param dns_service_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#dns_service_enabled ServiceFabricManagedCluster#dns_service_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#id ServiceFabricManagedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_type: node_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#node_type ServiceFabricManagedCluster#node_type}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#password ServiceFabricManagedCluster#password}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#sku ServiceFabricManagedCluster#sku}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#subnet_id ServiceFabricManagedCluster#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#tags ServiceFabricManagedCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#timeouts ServiceFabricManagedCluster#timeouts}
        :param upgrade_wave: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#upgrade_wave ServiceFabricManagedCluster#upgrade_wave}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#username ServiceFabricManagedCluster#username}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authentication, dict):
            authentication = ServiceFabricManagedClusterAuthentication(**authentication)
        if isinstance(timeouts, dict):
            timeouts = ServiceFabricManagedClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f40ebb0f9d80a61a402cde89fd6eeccb7f5a9c7ad033cc83bc9a0e47ad6e04)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_connection_port", value=client_connection_port, expected_type=type_hints["client_connection_port"])
            check_type(argname="argument http_gateway_port", value=http_gateway_port, expected_type=type_hints["http_gateway_port"])
            check_type(argname="argument lb_rule", value=lb_rule, expected_type=type_hints["lb_rule"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument backup_service_enabled", value=backup_service_enabled, expected_type=type_hints["backup_service_enabled"])
            check_type(argname="argument custom_fabric_setting", value=custom_fabric_setting, expected_type=type_hints["custom_fabric_setting"])
            check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
            check_type(argname="argument dns_service_enabled", value=dns_service_enabled, expected_type=type_hints["dns_service_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument upgrade_wave", value=upgrade_wave, expected_type=type_hints["upgrade_wave"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_connection_port": client_connection_port,
            "http_gateway_port": http_gateway_port,
            "lb_rule": lb_rule,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if authentication is not None:
            self._values["authentication"] = authentication
        if backup_service_enabled is not None:
            self._values["backup_service_enabled"] = backup_service_enabled
        if custom_fabric_setting is not None:
            self._values["custom_fabric_setting"] = custom_fabric_setting
        if dns_name is not None:
            self._values["dns_name"] = dns_name
        if dns_service_enabled is not None:
            self._values["dns_service_enabled"] = dns_service_enabled
        if id is not None:
            self._values["id"] = id
        if node_type is not None:
            self._values["node_type"] = node_type
        if password is not None:
            self._values["password"] = password
        if sku is not None:
            self._values["sku"] = sku
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if upgrade_wave is not None:
            self._values["upgrade_wave"] = upgrade_wave
        if username is not None:
            self._values["username"] = username

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
    def client_connection_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#client_connection_port ServiceFabricManagedCluster#client_connection_port}.'''
        result = self._values.get("client_connection_port")
        assert result is not None, "Required property 'client_connection_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def http_gateway_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#http_gateway_port ServiceFabricManagedCluster#http_gateway_port}.'''
        result = self._values.get("http_gateway_port")
        assert result is not None, "Required property 'http_gateway_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def lb_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterLbRule"]]:
        '''lb_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#lb_rule ServiceFabricManagedCluster#lb_rule}
        '''
        result = self._values.get("lb_rule")
        assert result is not None, "Required property 'lb_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterLbRule"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#location ServiceFabricManagedCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#name ServiceFabricManagedCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#resource_group_name ServiceFabricManagedCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional[ServiceFabricManagedClusterAuthentication]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#authentication ServiceFabricManagedCluster#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[ServiceFabricManagedClusterAuthentication], result)

    @builtins.property
    def backup_service_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#backup_service_enabled ServiceFabricManagedCluster#backup_service_enabled}.'''
        result = self._values.get("backup_service_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_fabric_setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterCustomFabricSetting"]]]:
        '''custom_fabric_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#custom_fabric_setting ServiceFabricManagedCluster#custom_fabric_setting}
        '''
        result = self._values.get("custom_fabric_setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterCustomFabricSetting"]]], result)

    @builtins.property
    def dns_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#dns_name ServiceFabricManagedCluster#dns_name}.'''
        result = self._values.get("dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_service_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#dns_service_enabled ServiceFabricManagedCluster#dns_service_enabled}.'''
        result = self._values.get("dns_service_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#id ServiceFabricManagedCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeType"]]]:
        '''node_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#node_type ServiceFabricManagedCluster#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeType"]]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#password ServiceFabricManagedCluster#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#sku ServiceFabricManagedCluster#sku}.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#subnet_id ServiceFabricManagedCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#tags ServiceFabricManagedCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServiceFabricManagedClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#timeouts ServiceFabricManagedCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServiceFabricManagedClusterTimeouts"], result)

    @builtins.property
    def upgrade_wave(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#upgrade_wave ServiceFabricManagedCluster#upgrade_wave}.'''
        result = self._values.get("upgrade_wave")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#username ServiceFabricManagedCluster#username}.'''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterCustomFabricSetting",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "section": "section", "value": "value"},
)
class ServiceFabricManagedClusterCustomFabricSetting:
    def __init__(
        self,
        *,
        parameter: builtins.str,
        section: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#parameter ServiceFabricManagedCluster#parameter}.
        :param section: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#section ServiceFabricManagedCluster#section}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#value ServiceFabricManagedCluster#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad9be0419b85bff9c67fc7844d344a436faa480fefda2f388e2b5531865f80b)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument section", value=section, expected_type=type_hints["section"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter": parameter,
            "section": section,
            "value": value,
        }

    @builtins.property
    def parameter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#parameter ServiceFabricManagedCluster#parameter}.'''
        result = self._values.get("parameter")
        assert result is not None, "Required property 'parameter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def section(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#section ServiceFabricManagedCluster#section}.'''
        result = self._values.get("section")
        assert result is not None, "Required property 'section' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#value ServiceFabricManagedCluster#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterCustomFabricSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterCustomFabricSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterCustomFabricSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ccfd5e72b78cc4d481a49779b9789190fcf87b7b66e158c451b2eca4dcea3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricManagedClusterCustomFabricSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1eb66d270f357549a1c228451152cb72b098046d5f0f880bd64270fc711e1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricManagedClusterCustomFabricSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7171d38cc5b90edbfaddbdd7f67000ac6b19fa9bc824bb86b448963bd2cf194c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef6502f83a04b6ff9cdaaa7a4b8c6e37bfef438e337b1aeb516bc89a26f9daff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41cb29eb5a6634201e6b339f3b2b7116fd0b0d2ea9d45e11b72384e543916a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterCustomFabricSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterCustomFabricSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterCustomFabricSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bede82a8f3932e1d84cf52608c18b78b84a22e573c7dab58068e638638009cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterCustomFabricSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterCustomFabricSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70922a04b6c5fcb72819c9b353f749717ce919a784eb422bc37bd990ee126858)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="sectionInput")
    def section_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sectionInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameter"))

    @parameter.setter
    def parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa3a8e0a7be2a31e23690395dfd5719e93f3f496f7ea2cce2c89aed3bb3850a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="section")
    def section(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "section"))

    @section.setter
    def section(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa292c9e125501cdc82ebd3bedd632f0c5d63f1b53bc22ca72847dd0e25e2179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "section", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d13598aa9f9cf4b8436e927658c83f75b31dcce4a7887ae530c0cc9f4838803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterCustomFabricSetting]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterCustomFabricSetting]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterCustomFabricSetting]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757ebca9bdc9b94d300e9fd5f2e403d3c914fbe353926cf8588a1c382ebb470e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterLbRule",
    jsii_struct_bases=[],
    name_mapping={
        "backend_port": "backendPort",
        "frontend_port": "frontendPort",
        "probe_protocol": "probeProtocol",
        "protocol": "protocol",
        "probe_request_path": "probeRequestPath",
    },
)
class ServiceFabricManagedClusterLbRule:
    def __init__(
        self,
        *,
        backend_port: jsii.Number,
        frontend_port: jsii.Number,
        probe_protocol: builtins.str,
        protocol: builtins.str,
        probe_request_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#backend_port ServiceFabricManagedCluster#backend_port}.
        :param frontend_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#frontend_port ServiceFabricManagedCluster#frontend_port}.
        :param probe_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#probe_protocol ServiceFabricManagedCluster#probe_protocol}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#protocol ServiceFabricManagedCluster#protocol}.
        :param probe_request_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#probe_request_path ServiceFabricManagedCluster#probe_request_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d402f75f9b84b3599a4af4b710c2a2dd4842d5de479c7768800010416f35d8b)
            check_type(argname="argument backend_port", value=backend_port, expected_type=type_hints["backend_port"])
            check_type(argname="argument frontend_port", value=frontend_port, expected_type=type_hints["frontend_port"])
            check_type(argname="argument probe_protocol", value=probe_protocol, expected_type=type_hints["probe_protocol"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument probe_request_path", value=probe_request_path, expected_type=type_hints["probe_request_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend_port": backend_port,
            "frontend_port": frontend_port,
            "probe_protocol": probe_protocol,
            "protocol": protocol,
        }
        if probe_request_path is not None:
            self._values["probe_request_path"] = probe_request_path

    @builtins.property
    def backend_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#backend_port ServiceFabricManagedCluster#backend_port}.'''
        result = self._values.get("backend_port")
        assert result is not None, "Required property 'backend_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frontend_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#frontend_port ServiceFabricManagedCluster#frontend_port}.'''
        result = self._values.get("frontend_port")
        assert result is not None, "Required property 'frontend_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def probe_protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#probe_protocol ServiceFabricManagedCluster#probe_protocol}.'''
        result = self._values.get("probe_protocol")
        assert result is not None, "Required property 'probe_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#protocol ServiceFabricManagedCluster#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def probe_request_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#probe_request_path ServiceFabricManagedCluster#probe_request_path}.'''
        result = self._values.get("probe_request_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterLbRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterLbRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterLbRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcdfbda00c43b1dc01b23246747cf215f3fc687f5d6a8d3770105913d6379033)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricManagedClusterLbRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8057c46772e20f01f5806aced163a0b5ea85df78cc7b10d73b6e47966f3767)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricManagedClusterLbRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162d4a092f61053fda63b41d31c6f98ae261cfd2c09dfd453e0f35a0f5b940a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4557fe40d16259e332e83ce368b8854fb43d052a7af21141afee98421050fae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5a569bb7dc330e6bebfe98f448a0f2994adbefd4657635b7a2d9cc512b759c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterLbRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterLbRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterLbRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fdbc7f5c841a0be3780aeeca7a6b7d270149b733d72d0da205dd668cee80ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterLbRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterLbRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5ea34fe05b47ff495cbc82e02ea43cb2f32f6e126966a14d6009fea0857960)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProbeRequestPath")
    def reset_probe_request_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProbeRequestPath", []))

    @builtins.property
    @jsii.member(jsii_name="backendPortInput")
    def backend_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backendPortInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendPortInput")
    def frontend_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frontendPortInput"))

    @builtins.property
    @jsii.member(jsii_name="probeProtocolInput")
    def probe_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "probeProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="probeRequestPathInput")
    def probe_request_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "probeRequestPathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPort")
    def backend_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backendPort"))

    @backend_port.setter
    def backend_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d05cd6d6eba543b42c75f31b28c0d70a1f08fb80db529910a16b68b0efe91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendPort")
    def frontend_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frontendPort"))

    @frontend_port.setter
    def frontend_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1683cb2f1f6f40351289874d999cfa30da87c39f2ea5e4bfe9f89559bc77f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="probeProtocol")
    def probe_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probeProtocol"))

    @probe_protocol.setter
    def probe_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a61bf9f1d3f6f55db6b85683166c4e0fc2f8f002de0f7fb01eaea1a80fc716a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probeProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="probeRequestPath")
    def probe_request_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "probeRequestPath"))

    @probe_request_path.setter
    def probe_request_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbb0b80ab474417d735e39ee704120ac23c96a5dedccb57708eda24ed42086a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "probeRequestPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95443504f06424d181544e813bc3ff84be33f8dd9d01b54d8a8aa15986c1c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterLbRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterLbRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterLbRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97e66f097ad3ef7077b90d10b579138f90b447580f437a96c6f13a37a0722b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeType",
    jsii_struct_bases=[],
    name_mapping={
        "application_port_range": "applicationPortRange",
        "data_disk_size_gb": "dataDiskSizeGb",
        "ephemeral_port_range": "ephemeralPortRange",
        "name": "name",
        "vm_image_offer": "vmImageOffer",
        "vm_image_publisher": "vmImagePublisher",
        "vm_image_sku": "vmImageSku",
        "vm_image_version": "vmImageVersion",
        "vm_instance_count": "vmInstanceCount",
        "vm_size": "vmSize",
        "capacities": "capacities",
        "data_disk_type": "dataDiskType",
        "multiple_placement_groups_enabled": "multiplePlacementGroupsEnabled",
        "placement_properties": "placementProperties",
        "primary": "primary",
        "stateless": "stateless",
        "vm_secrets": "vmSecrets",
    },
)
class ServiceFabricManagedClusterNodeType:
    def __init__(
        self,
        *,
        application_port_range: builtins.str,
        data_disk_size_gb: jsii.Number,
        ephemeral_port_range: builtins.str,
        name: builtins.str,
        vm_image_offer: builtins.str,
        vm_image_publisher: builtins.str,
        vm_image_sku: builtins.str,
        vm_image_version: builtins.str,
        vm_instance_count: jsii.Number,
        vm_size: builtins.str,
        capacities: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data_disk_type: typing.Optional[builtins.str] = None,
        multiple_placement_groups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        placement_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stateless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vm_secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterNodeTypeVmSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param application_port_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#application_port_range ServiceFabricManagedCluster#application_port_range}.
        :param data_disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#data_disk_size_gb ServiceFabricManagedCluster#data_disk_size_gb}.
        :param ephemeral_port_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#ephemeral_port_range ServiceFabricManagedCluster#ephemeral_port_range}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#name ServiceFabricManagedCluster#name}.
        :param vm_image_offer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_offer ServiceFabricManagedCluster#vm_image_offer}.
        :param vm_image_publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_publisher ServiceFabricManagedCluster#vm_image_publisher}.
        :param vm_image_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_sku ServiceFabricManagedCluster#vm_image_sku}.
        :param vm_image_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_version ServiceFabricManagedCluster#vm_image_version}.
        :param vm_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_instance_count ServiceFabricManagedCluster#vm_instance_count}.
        :param vm_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_size ServiceFabricManagedCluster#vm_size}.
        :param capacities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#capacities ServiceFabricManagedCluster#capacities}.
        :param data_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#data_disk_type ServiceFabricManagedCluster#data_disk_type}.
        :param multiple_placement_groups_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#multiple_placement_groups_enabled ServiceFabricManagedCluster#multiple_placement_groups_enabled}.
        :param placement_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#placement_properties ServiceFabricManagedCluster#placement_properties}.
        :param primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#primary ServiceFabricManagedCluster#primary}.
        :param stateless: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#stateless ServiceFabricManagedCluster#stateless}.
        :param vm_secrets: vm_secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_secrets ServiceFabricManagedCluster#vm_secrets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32151f4732b336a0a2effb7f03ca6578b152098e8717ffeaf82c3ef0430e4e7)
            check_type(argname="argument application_port_range", value=application_port_range, expected_type=type_hints["application_port_range"])
            check_type(argname="argument data_disk_size_gb", value=data_disk_size_gb, expected_type=type_hints["data_disk_size_gb"])
            check_type(argname="argument ephemeral_port_range", value=ephemeral_port_range, expected_type=type_hints["ephemeral_port_range"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vm_image_offer", value=vm_image_offer, expected_type=type_hints["vm_image_offer"])
            check_type(argname="argument vm_image_publisher", value=vm_image_publisher, expected_type=type_hints["vm_image_publisher"])
            check_type(argname="argument vm_image_sku", value=vm_image_sku, expected_type=type_hints["vm_image_sku"])
            check_type(argname="argument vm_image_version", value=vm_image_version, expected_type=type_hints["vm_image_version"])
            check_type(argname="argument vm_instance_count", value=vm_instance_count, expected_type=type_hints["vm_instance_count"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument capacities", value=capacities, expected_type=type_hints["capacities"])
            check_type(argname="argument data_disk_type", value=data_disk_type, expected_type=type_hints["data_disk_type"])
            check_type(argname="argument multiple_placement_groups_enabled", value=multiple_placement_groups_enabled, expected_type=type_hints["multiple_placement_groups_enabled"])
            check_type(argname="argument placement_properties", value=placement_properties, expected_type=type_hints["placement_properties"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument stateless", value=stateless, expected_type=type_hints["stateless"])
            check_type(argname="argument vm_secrets", value=vm_secrets, expected_type=type_hints["vm_secrets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_port_range": application_port_range,
            "data_disk_size_gb": data_disk_size_gb,
            "ephemeral_port_range": ephemeral_port_range,
            "name": name,
            "vm_image_offer": vm_image_offer,
            "vm_image_publisher": vm_image_publisher,
            "vm_image_sku": vm_image_sku,
            "vm_image_version": vm_image_version,
            "vm_instance_count": vm_instance_count,
            "vm_size": vm_size,
        }
        if capacities is not None:
            self._values["capacities"] = capacities
        if data_disk_type is not None:
            self._values["data_disk_type"] = data_disk_type
        if multiple_placement_groups_enabled is not None:
            self._values["multiple_placement_groups_enabled"] = multiple_placement_groups_enabled
        if placement_properties is not None:
            self._values["placement_properties"] = placement_properties
        if primary is not None:
            self._values["primary"] = primary
        if stateless is not None:
            self._values["stateless"] = stateless
        if vm_secrets is not None:
            self._values["vm_secrets"] = vm_secrets

    @builtins.property
    def application_port_range(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#application_port_range ServiceFabricManagedCluster#application_port_range}.'''
        result = self._values.get("application_port_range")
        assert result is not None, "Required property 'application_port_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_disk_size_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#data_disk_size_gb ServiceFabricManagedCluster#data_disk_size_gb}.'''
        result = self._values.get("data_disk_size_gb")
        assert result is not None, "Required property 'data_disk_size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ephemeral_port_range(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#ephemeral_port_range ServiceFabricManagedCluster#ephemeral_port_range}.'''
        result = self._values.get("ephemeral_port_range")
        assert result is not None, "Required property 'ephemeral_port_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#name ServiceFabricManagedCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_image_offer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_offer ServiceFabricManagedCluster#vm_image_offer}.'''
        result = self._values.get("vm_image_offer")
        assert result is not None, "Required property 'vm_image_offer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_image_publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_publisher ServiceFabricManagedCluster#vm_image_publisher}.'''
        result = self._values.get("vm_image_publisher")
        assert result is not None, "Required property 'vm_image_publisher' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_image_sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_sku ServiceFabricManagedCluster#vm_image_sku}.'''
        result = self._values.get("vm_image_sku")
        assert result is not None, "Required property 'vm_image_sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_image_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_image_version ServiceFabricManagedCluster#vm_image_version}.'''
        result = self._values.get("vm_image_version")
        assert result is not None, "Required property 'vm_image_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_instance_count ServiceFabricManagedCluster#vm_instance_count}.'''
        result = self._values.get("vm_instance_count")
        assert result is not None, "Required property 'vm_instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_size ServiceFabricManagedCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacities(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#capacities ServiceFabricManagedCluster#capacities}.'''
        result = self._values.get("capacities")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def data_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#data_disk_type ServiceFabricManagedCluster#data_disk_type}.'''
        result = self._values.get("data_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multiple_placement_groups_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#multiple_placement_groups_enabled ServiceFabricManagedCluster#multiple_placement_groups_enabled}.'''
        result = self._values.get("multiple_placement_groups_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def placement_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#placement_properties ServiceFabricManagedCluster#placement_properties}.'''
        result = self._values.get("placement_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#primary ServiceFabricManagedCluster#primary}.'''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def stateless(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#stateless ServiceFabricManagedCluster#stateless}.'''
        result = self._values.get("stateless")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vm_secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeTypeVmSecrets"]]]:
        '''vm_secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vm_secrets ServiceFabricManagedCluster#vm_secrets}
        '''
        result = self._values.get("vm_secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeTypeVmSecrets"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterNodeType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterNodeTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e97c74bdcb263b660ac77e541594eef61deeee6415bc02371d927d7ec901f9c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricManagedClusterNodeTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea09b4bde364620d18fecc626a23e650b96cbc0f6d583aa8180403c973bc568c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricManagedClusterNodeTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7440be6de2db4e4ebc4279934bd2ebb88c4770119748b38a9a3e96c81c6cd234)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2342a12b508c68127eef643377162c6f70d54362fb501890e4efae2399267ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5bf66884dce08a1fd8f9bbef90047c1984252b453a18cf4dc19c1ae48545c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3aa724beb6759e0eb8c9397cb98eb7e2f92936a06c62f1cb0cd6e6452db0cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterNodeTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb36fa41abb0793ad5bc383b16a18116fdb02a1d117f1ccbc690726e666313e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVmSecrets")
    def put_vm_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterNodeTypeVmSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98043425462d0e4e97e1d17511af6ae358aadd51490ad55e80d1e34eaa7822fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVmSecrets", [value]))

    @jsii.member(jsii_name="resetCapacities")
    def reset_capacities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacities", []))

    @jsii.member(jsii_name="resetDataDiskType")
    def reset_data_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskType", []))

    @jsii.member(jsii_name="resetMultiplePlacementGroupsEnabled")
    def reset_multiple_placement_groups_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiplePlacementGroupsEnabled", []))

    @jsii.member(jsii_name="resetPlacementProperties")
    def reset_placement_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementProperties", []))

    @jsii.member(jsii_name="resetPrimary")
    def reset_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimary", []))

    @jsii.member(jsii_name="resetStateless")
    def reset_stateless(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStateless", []))

    @jsii.member(jsii_name="resetVmSecrets")
    def reset_vm_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSecrets", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="vmSecrets")
    def vm_secrets(self) -> "ServiceFabricManagedClusterNodeTypeVmSecretsList":
        return typing.cast("ServiceFabricManagedClusterNodeTypeVmSecretsList", jsii.get(self, "vmSecrets"))

    @builtins.property
    @jsii.member(jsii_name="applicationPortRangeInput")
    def application_port_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationPortRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="capacitiesInput")
    def capacities_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "capacitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGbInput")
    def data_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskTypeInput")
    def data_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralPortRangeInput")
    def ephemeral_port_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ephemeralPortRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="multiplePlacementGroupsEnabledInput")
    def multiple_placement_groups_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multiplePlacementGroupsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="placementPropertiesInput")
    def placement_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "placementPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="statelessInput")
    def stateless_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "statelessInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageOfferInput")
    def vm_image_offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmImageOfferInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImagePublisherInput")
    def vm_image_publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmImagePublisherInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageSkuInput")
    def vm_image_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmImageSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageVersionInput")
    def vm_image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmImageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="vmInstanceCountInput")
    def vm_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSecretsInput")
    def vm_secrets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeTypeVmSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeTypeVmSecrets"]]], jsii.get(self, "vmSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationPortRange")
    def application_port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationPortRange"))

    @application_port_range.setter
    def application_port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a992d55a1fb64c6eaa344307d911e17e88b442aac5bedf0dd3e625f343c7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationPortRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacities")
    def capacities(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "capacities"))

    @capacities.setter
    def capacities(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6befb086cb76a6103eb9f736165300c52c9e9f787ca2c2f71467d62c73fa81c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGb")
    def data_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataDiskSizeGb"))

    @data_disk_size_gb.setter
    def data_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c9d6184138a9bb410b7c7117c22f67f0a81b3b418b93700bb1400da97955f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskType")
    def data_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskType"))

    @data_disk_type.setter
    def data_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7da4a9b82f76ed26a577f4b391a7d83ccdafc6bcdfb68c13878d3666a4e33d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ephemeralPortRange")
    def ephemeral_port_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralPortRange"))

    @ephemeral_port_range.setter
    def ephemeral_port_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486ac3c46a6514b2f27837aa57fa5f10e43b19bbdb72cae56f12c1a0695f1bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ephemeralPortRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiplePlacementGroupsEnabled")
    def multiple_placement_groups_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multiplePlacementGroupsEnabled"))

    @multiple_placement_groups_enabled.setter
    def multiple_placement_groups_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65660f489d156a8791e550edeb742bbc3626d0411c40195cebd3a6486ed9d6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiplePlacementGroupsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a21307eaa0e246ea9ddcf6361f53026c7dca2d997793891850fd14ed9d50fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="placementProperties")
    def placement_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "placementProperties"))

    @placement_properties.setter
    def placement_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b093e3e2546d6030dcc1e231009efb0f0ae24de64c28e802ba0275363843a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementProperties", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0f1aa807fa9fd4f1f2909101d9de8debc7ba1b0a9f1c0b2f53e6d095c80574a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateless")
    def stateless(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stateless"))

    @stateless.setter
    def stateless(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857bb7a9630baa9146a128d34b43a17caf383a25387ec913ddec7f160845a0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateless", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmImageOffer")
    def vm_image_offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmImageOffer"))

    @vm_image_offer.setter
    def vm_image_offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff4b1295be0c03e2a48870faf2f533c5d80f1a3477e263a0f932302901a0851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmImageOffer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmImagePublisher")
    def vm_image_publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmImagePublisher"))

    @vm_image_publisher.setter
    def vm_image_publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbb28584705351e917714e8e3c0606ccbf5a9a3da981d30180c8a428982ed9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmImagePublisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmImageSku")
    def vm_image_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmImageSku"))

    @vm_image_sku.setter
    def vm_image_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc933f835fc8486ef2cee81c98a3d0939c462d8f133b260bd4a359466d6f9747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmImageSku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmImageVersion")
    def vm_image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmImageVersion"))

    @vm_image_version.setter
    def vm_image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593c08884dc495faaf395b255f152e4c8dbd7cf6338049919b9284f52e734ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmImageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmInstanceCount")
    def vm_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmInstanceCount"))

    @vm_instance_count.setter
    def vm_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31709b17cbad9acaf20ce1112170cdfe9f8a7abfcf6988d355fa1e89e892c69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f96a46f901044a201eb582410ca3feb563e68c7c1ccfe322255e2a554f744d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4c59425797d25faf3141c2fb2d48cebeefd7c43fe5490ca5741911f9b18cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeVmSecrets",
    jsii_struct_bases=[],
    name_mapping={"certificates": "certificates", "vault_id": "vaultId"},
)
class ServiceFabricManagedClusterNodeTypeVmSecrets:
    def __init__(
        self,
        *,
        certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFabricManagedClusterNodeTypeVmSecretsCertificates", typing.Dict[builtins.str, typing.Any]]]],
        vault_id: builtins.str,
    ) -> None:
        '''
        :param certificates: certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#certificates ServiceFabricManagedCluster#certificates}
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vault_id ServiceFabricManagedCluster#vault_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef56c659d1a195020143a95da6242d19792a6655c5627aed7505a9a7653b06b)
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificates": certificates,
            "vault_id": vault_id,
        }

    @builtins.property
    def certificates(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeTypeVmSecretsCertificates"]]:
        '''certificates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#certificates ServiceFabricManagedCluster#certificates}
        '''
        result = self._values.get("certificates")
        assert result is not None, "Required property 'certificates' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFabricManagedClusterNodeTypeVmSecretsCertificates"]], result)

    @builtins.property
    def vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#vault_id ServiceFabricManagedCluster#vault_id}.'''
        result = self._values.get("vault_id")
        assert result is not None, "Required property 'vault_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterNodeTypeVmSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeVmSecretsCertificates",
    jsii_struct_bases=[],
    name_mapping={"store": "store", "url": "url"},
)
class ServiceFabricManagedClusterNodeTypeVmSecretsCertificates:
    def __init__(self, *, store: builtins.str, url: builtins.str) -> None:
        '''
        :param store: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#store ServiceFabricManagedCluster#store}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#url ServiceFabricManagedCluster#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacc3846174d7584cee76559834d6663c02709b41feedecca5073ff75cbe3dd3)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "store": store,
            "url": url,
        }

    @builtins.property
    def store(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#store ServiceFabricManagedCluster#store}.'''
        result = self._values.get("store")
        assert result is not None, "Required property 'store' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#url ServiceFabricManagedCluster#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterNodeTypeVmSecretsCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ccb9da901ee2a64c8cfe7d2c669c291498a3b994e04d08c8c4d957b95b5e795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749f3d3de75b07b8cd1f677de36de8fcedf675e5ebb9037c64b004b5227cffd1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e76e730183ee2e5eb8a959812614e872c213f21e97af978ed31b2a1f9ad312f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c489ee78b9ccd55ca0421891e5b31b4c32bb05d6db2f421471c4dfad3ee290d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfe5e6a32924d07dc2153ad44e5e06cb660e4df91073cf1cb6f180c1dc0fb04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e2a9ae29e57de46c6ef7cd93edc846bb9bd183ae90297257b3e34f361d7147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be450f98b108b641489116b1a5a6236ab4dc26086bfd1bd095dc0e5cfc7193df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="storeInput")
    def store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storeInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "store"))

    @store.setter
    def store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b09ad4c260bd56c5271e439960c37d95f2f9002e0332110b4b3bf65439cc21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "store", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff36baf1715d1dab745e0fbcccb34c02386c7fd003d2e9468d767929dd242c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2421b757d3ea1061f27628aef09b7499da52337da48b887f76e73b16cc6e0afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterNodeTypeVmSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeVmSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03b0bcb445b487a46abd841c8ffb0a95ce409eed8e59ad4cffb645397adc391e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFabricManagedClusterNodeTypeVmSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0338fa6b3f86c405f57f51cc54618c5e90fcd3725ed8a53768ce1040161f84a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFabricManagedClusterNodeTypeVmSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e0b8d0a89eccb1d4165952eb50e583f32ba553ea661a4d77cd5010de4ed864)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a172d2612fd67332c4890308251a6fa4d610aa630f7b29bd9f81f9ff82bb23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b34fbd063d695213580ac3594fc3a9c6a5025beb735a561f247928fb42823a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7390698aa082e07e1a79eba72241a33a28377144e48cae65dacccdc1a90bf474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFabricManagedClusterNodeTypeVmSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterNodeTypeVmSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e46f75b10726678e546363c42ef9647b97bf744a361bb4ae9f38d39912cd6d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCertificates")
    def put_certificates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2ce5b10d0727bc01b6b48e6c55f3e1c654c46ae4cd7cea4adc5433b0d6ff55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertificates", [value]))

    @builtins.property
    @jsii.member(jsii_name="certificates")
    def certificates(
        self,
    ) -> ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesList:
        return typing.cast(ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesList, jsii.get(self, "certificates"))

    @builtins.property
    @jsii.member(jsii_name="certificatesInput")
    def certificates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]], jsii.get(self, "certificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2eb90b6f3518e05e86d37db735e1cdd97ea668731ad07b9fdb9349b8c47a64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ce67e4d9d49f627099108de34e3a90adb736598253ccd4c5cda42f7e3c34c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServiceFabricManagedClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#create ServiceFabricManagedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#delete ServiceFabricManagedCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#read ServiceFabricManagedCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#update ServiceFabricManagedCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b963419f21b23acc705e79789f872de5c63209709864385fe1eeb814f8d0c70)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#create ServiceFabricManagedCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#delete ServiceFabricManagedCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#read ServiceFabricManagedCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/service_fabric_managed_cluster#update ServiceFabricManagedCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFabricManagedClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFabricManagedClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.serviceFabricManagedCluster.ServiceFabricManagedClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f866c52fcfbea6de89a7f5dc26c333da2e7e541e6ab7c05d800c4c0c13c1ab3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d998fa8ee18b16a43de28e1435b506a2d5c21d8d9186e7a0cda075916b9f9a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ef64c528c944f71a59c5b0cc0f445f2e084b3e0203d1e0bf879f0b07ea076b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada3a3cc306a6e2608eeb231eba6df02ec621754259b188038306a4c5bcc5d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9551241b3675224d553c271c2e2edc769449b574c2dc5b8ccf16186bf24f07d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205f95c6035f424d85e84ef09ce2378e95747b8a620ae20f1ce05e340b83334c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceFabricManagedCluster",
    "ServiceFabricManagedClusterAuthentication",
    "ServiceFabricManagedClusterAuthenticationActiveDirectory",
    "ServiceFabricManagedClusterAuthenticationActiveDirectoryOutputReference",
    "ServiceFabricManagedClusterAuthenticationCertificate",
    "ServiceFabricManagedClusterAuthenticationCertificateList",
    "ServiceFabricManagedClusterAuthenticationCertificateOutputReference",
    "ServiceFabricManagedClusterAuthenticationOutputReference",
    "ServiceFabricManagedClusterConfig",
    "ServiceFabricManagedClusterCustomFabricSetting",
    "ServiceFabricManagedClusterCustomFabricSettingList",
    "ServiceFabricManagedClusterCustomFabricSettingOutputReference",
    "ServiceFabricManagedClusterLbRule",
    "ServiceFabricManagedClusterLbRuleList",
    "ServiceFabricManagedClusterLbRuleOutputReference",
    "ServiceFabricManagedClusterNodeType",
    "ServiceFabricManagedClusterNodeTypeList",
    "ServiceFabricManagedClusterNodeTypeOutputReference",
    "ServiceFabricManagedClusterNodeTypeVmSecrets",
    "ServiceFabricManagedClusterNodeTypeVmSecretsCertificates",
    "ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesList",
    "ServiceFabricManagedClusterNodeTypeVmSecretsCertificatesOutputReference",
    "ServiceFabricManagedClusterNodeTypeVmSecretsList",
    "ServiceFabricManagedClusterNodeTypeVmSecretsOutputReference",
    "ServiceFabricManagedClusterTimeouts",
    "ServiceFabricManagedClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7d4bded4d0b410ddea933427da1948d57b33860350daf743e35a5a6e8f7886e9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    client_connection_port: jsii.Number,
    http_gateway_port: jsii.Number,
    lb_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterLbRule, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    authentication: typing.Optional[typing.Union[ServiceFabricManagedClusterAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_fabric_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterCustomFabricSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_name: typing.Optional[builtins.str] = None,
    dns_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ServiceFabricManagedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_wave: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4bcc2e081386bf02d8717cd4f45db1f27757e9434c8a18ba9a3c7d90d4a69653(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03025382ca59460e5cd88042f4d6e766bda030603f18c846b238dcb6eb9d7f1e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterCustomFabricSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d77ebd00dec3d20db6122d322e436cd1d2a12df83c1f86a349a02f6a7bb724(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterLbRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a09500851e7cc390f03b4b8885499250e2b4cedca31c0918edf45dc17804c64(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d79a1636da5d0dd58480096f42fa4ce303fedf678e978596e7eeb86713042cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca941098fb29e9439971131d1a9ee572eca0fd746fb09f7bfe8a4268c5bcbc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02f019ccb42f09ac5b53b425968b33e8fee2627fd777e5c52229af589944591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93042936b195b9c974ada4f7ad026aef4e9b7488b11c973c91dfa771f07ce9aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab8329d6156cdc4262cdb0e6639a0b535fe9bfb5473c3779fc322bb8d24e1f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a18044346d2464ed1e1f0a04fb7e932676e71c9a7066a5c944241e01ba238bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8a970b0bf20f35b8de55d3d2f11d0bd2ab33f1a3fa361e86d36d495d9cb45b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b78f388cfdd3fc0235439c76cbe5ee9da862638642ef0f0c184f84c9bd5d12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc977824348a6b27fc9897dd93885e96e115736c7163bcd7f7a28d786fe0ab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86470a7364547e7afa6bcb4302b32232f127b8580b14ff1b2566f7d37a32b965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f2b0c408f6921acbf1bbbf752fb66fad2f3d43ab6f9449938a78b5b21672de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cbefe4708e8c3f6f3b5f1100544f351a70e078c19168dc5d801b0a1acba7c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193434f637862cd2c6348424631d0bcc6bf80bcb37c8d7e649a0997450b8b442(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc10d2b9242a1bf18f6246af91a53d7f73a295099f2e91d1cdd04c18207f00d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b31ee344fa7a19853a2a953f326b898777c7ead00103aa304faaa0c0087372e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620c8e8d9dc0741b99f3a8bad99c0ac9ea61cef05b5bb292169a114583ff309c(
    *,
    active_directory: typing.Optional[typing.Union[ServiceFabricManagedClusterAuthenticationActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf09d4c04329a479ba31cf431329ac6164fdea58dc77dc8b213a3e2e5b7a5d3(
    *,
    client_application_id: builtins.str,
    cluster_application_id: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2e0d977025c9d6bb34e79d6e21bebdf1bbb216bae1394c2ad2cb835dbc4361(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d424c35b473a67327b62a96bdaeb4039a1e85a418a0d3f5f8ab78ca88d2efd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f7a8caeae31109bfd1c9b27d7a2d568791b051370b6262168608cc0bacdd18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d32a37fd174abcea4475e1589ab52d6622fd17186e412066ba6d6b2147c30e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599be36ec3bbf28f5357fe2923ef2d38bc3f1fe19db268d3ae764c0f1580f7a5(
    value: typing.Optional[ServiceFabricManagedClusterAuthenticationActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3713d1925e869802e00087b8fdc20a0d2a933c6fbaa1d4d1b14a8dd37833164(
    *,
    thumbprint: builtins.str,
    type: builtins.str,
    common_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefd10c66133ec8710c7d154c4e6fb1e43b8d29533adb32761be385db9508c6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b2e5154ea78fc8ac8091be3622113573352592de418bbc28226edca7d2b3f8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbee88948cf022266c2e93ef891ee74558ff5ea9507c40d96f3f36d7638f6e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ba7a967cc6add1e0383cbc8c7fbec8861d1dc8745d6db84792b9b5f6507c02(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fb137673a560dbf5cdf4194316a43b523b4883c6db1f98cf67181bb8d67227(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2433cbec0477397442fb8ee1bfed535b222f0b0c14088afd325fa9a6cfeb237d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterAuthenticationCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f765817a36806e9fd980238f0422f859aec3557ab6e2177de2caad1e636ec8fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa91cc9a6a118faa8dc16c9bf768e7952e3993326c50f3b2f7cb881fa10bc646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204d485e5f99d5b0015fb0b389ca7c7c04c215017eab56bd1aef5ee4553d8dd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5fc0ce4cef4fb35ca983006e614248c5d88720a1a3f5725cb142073c0ba15e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd54f7c5dae5f26c321b26b792b80db8cb569d936dd0d0c340fd05828faf4d84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterAuthenticationCertificate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000faa6a6624386d39b7d9ec9dd3dcec7a32f46a6736f796475e1dad2fe60119(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c65ace1ba86e2537b077644fbcb079acf6e6d930793389fd041d280abc89db2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterAuthenticationCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abe0f2366dd6e732e5a9b530d464706851d522cf82750d3751f87a4b2837112(
    value: typing.Optional[ServiceFabricManagedClusterAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f40ebb0f9d80a61a402cde89fd6eeccb7f5a9c7ad033cc83bc9a0e47ad6e04(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_connection_port: jsii.Number,
    http_gateway_port: jsii.Number,
    lb_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterLbRule, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    authentication: typing.Optional[typing.Union[ServiceFabricManagedClusterAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_fabric_setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterCustomFabricSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_name: typing.Optional[builtins.str] = None,
    dns_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    password: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ServiceFabricManagedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    upgrade_wave: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad9be0419b85bff9c67fc7844d344a436faa480fefda2f388e2b5531865f80b(
    *,
    parameter: builtins.str,
    section: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ccfd5e72b78cc4d481a49779b9789190fcf87b7b66e158c451b2eca4dcea3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1eb66d270f357549a1c228451152cb72b098046d5f0f880bd64270fc711e1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7171d38cc5b90edbfaddbdd7f67000ac6b19fa9bc824bb86b448963bd2cf194c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6502f83a04b6ff9cdaaa7a4b8c6e37bfef438e337b1aeb516bc89a26f9daff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cb29eb5a6634201e6b339f3b2b7116fd0b0d2ea9d45e11b72384e543916a38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bede82a8f3932e1d84cf52608c18b78b84a22e573c7dab58068e638638009cad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterCustomFabricSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70922a04b6c5fcb72819c9b353f749717ce919a784eb422bc37bd990ee126858(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa3a8e0a7be2a31e23690395dfd5719e93f3f496f7ea2cce2c89aed3bb3850a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa292c9e125501cdc82ebd3bedd632f0c5d63f1b53bc22ca72847dd0e25e2179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d13598aa9f9cf4b8436e927658c83f75b31dcce4a7887ae530c0cc9f4838803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757ebca9bdc9b94d300e9fd5f2e403d3c914fbe353926cf8588a1c382ebb470e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterCustomFabricSetting]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d402f75f9b84b3599a4af4b710c2a2dd4842d5de479c7768800010416f35d8b(
    *,
    backend_port: jsii.Number,
    frontend_port: jsii.Number,
    probe_protocol: builtins.str,
    protocol: builtins.str,
    probe_request_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdfbda00c43b1dc01b23246747cf215f3fc687f5d6a8d3770105913d6379033(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8057c46772e20f01f5806aced163a0b5ea85df78cc7b10d73b6e47966f3767(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162d4a092f61053fda63b41d31c6f98ae261cfd2c09dfd453e0f35a0f5b940a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4557fe40d16259e332e83ce368b8854fb43d052a7af21141afee98421050fae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a569bb7dc330e6bebfe98f448a0f2994adbefd4657635b7a2d9cc512b759c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fdbc7f5c841a0be3780aeeca7a6b7d270149b733d72d0da205dd668cee80ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterLbRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5ea34fe05b47ff495cbc82e02ea43cb2f32f6e126966a14d6009fea0857960(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d05cd6d6eba543b42c75f31b28c0d70a1f08fb80db529910a16b68b0efe91e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1683cb2f1f6f40351289874d999cfa30da87c39f2ea5e4bfe9f89559bc77f1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a61bf9f1d3f6f55db6b85683166c4e0fc2f8f002de0f7fb01eaea1a80fc716a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbb0b80ab474417d735e39ee704120ac23c96a5dedccb57708eda24ed42086a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95443504f06424d181544e813bc3ff84be33f8dd9d01b54d8a8aa15986c1c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97e66f097ad3ef7077b90d10b579138f90b447580f437a96c6f13a37a0722b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterLbRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32151f4732b336a0a2effb7f03ca6578b152098e8717ffeaf82c3ef0430e4e7(
    *,
    application_port_range: builtins.str,
    data_disk_size_gb: jsii.Number,
    ephemeral_port_range: builtins.str,
    name: builtins.str,
    vm_image_offer: builtins.str,
    vm_image_publisher: builtins.str,
    vm_image_sku: builtins.str,
    vm_image_version: builtins.str,
    vm_instance_count: jsii.Number,
    vm_size: builtins.str,
    capacities: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    data_disk_type: typing.Optional[builtins.str] = None,
    multiple_placement_groups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    placement_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stateless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vm_secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeTypeVmSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97c74bdcb263b660ac77e541594eef61deeee6415bc02371d927d7ec901f9c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea09b4bde364620d18fecc626a23e650b96cbc0f6d583aa8180403c973bc568c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7440be6de2db4e4ebc4279934bd2ebb88c4770119748b38a9a3e96c81c6cd234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2342a12b508c68127eef643377162c6f70d54362fb501890e4efae2399267ea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bf66884dce08a1fd8f9bbef90047c1984252b453a18cf4dc19c1ae48545c19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3aa724beb6759e0eb8c9397cb98eb7e2f92936a06c62f1cb0cd6e6452db0cb7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb36fa41abb0793ad5bc383b16a18116fdb02a1d117f1ccbc690726e666313e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98043425462d0e4e97e1d17511af6ae358aadd51490ad55e80d1e34eaa7822fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeTypeVmSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a992d55a1fb64c6eaa344307d911e17e88b442aac5bedf0dd3e625f343c7a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6befb086cb76a6103eb9f736165300c52c9e9f787ca2c2f71467d62c73fa81c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c9d6184138a9bb410b7c7117c22f67f0a81b3b418b93700bb1400da97955f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7da4a9b82f76ed26a577f4b391a7d83ccdafc6bcdfb68c13878d3666a4e33d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486ac3c46a6514b2f27837aa57fa5f10e43b19bbdb72cae56f12c1a0695f1bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65660f489d156a8791e550edeb742bbc3626d0411c40195cebd3a6486ed9d6bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a21307eaa0e246ea9ddcf6361f53026c7dca2d997793891850fd14ed9d50fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b093e3e2546d6030dcc1e231009efb0f0ae24de64c28e802ba0275363843a2a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1aa807fa9fd4f1f2909101d9de8debc7ba1b0a9f1c0b2f53e6d095c80574a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857bb7a9630baa9146a128d34b43a17caf383a25387ec913ddec7f160845a0f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff4b1295be0c03e2a48870faf2f533c5d80f1a3477e263a0f932302901a0851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbb28584705351e917714e8e3c0606ccbf5a9a3da981d30180c8a428982ed9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc933f835fc8486ef2cee81c98a3d0939c462d8f133b260bd4a359466d6f9747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593c08884dc495faaf395b255f152e4c8dbd7cf6338049919b9284f52e734ead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31709b17cbad9acaf20ce1112170cdfe9f8a7abfcf6988d355fa1e89e892c69e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f96a46f901044a201eb582410ca3feb563e68c7c1ccfe322255e2a554f744d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4c59425797d25faf3141c2fb2d48cebeefd7c43fe5490ca5741911f9b18cc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef56c659d1a195020143a95da6242d19792a6655c5627aed7505a9a7653b06b(
    *,
    certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates, typing.Dict[builtins.str, typing.Any]]]],
    vault_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacc3846174d7584cee76559834d6663c02709b41feedecca5073ff75cbe3dd3(
    *,
    store: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccb9da901ee2a64c8cfe7d2c669c291498a3b994e04d08c8c4d957b95b5e795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749f3d3de75b07b8cd1f677de36de8fcedf675e5ebb9037c64b004b5227cffd1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e76e730183ee2e5eb8a959812614e872c213f21e97af978ed31b2a1f9ad312f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c489ee78b9ccd55ca0421891e5b31b4c32bb05d6db2f421471c4dfad3ee290d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe5e6a32924d07dc2153ad44e5e06cb660e4df91073cf1cb6f180c1dc0fb04b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e2a9ae29e57de46c6ef7cd93edc846bb9bd183ae90297257b3e34f361d7147(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be450f98b108b641489116b1a5a6236ab4dc26086bfd1bd095dc0e5cfc7193df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b09ad4c260bd56c5271e439960c37d95f2f9002e0332110b4b3bf65439cc21f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff36baf1715d1dab745e0fbcccb34c02386c7fd003d2e9468d767929dd242c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2421b757d3ea1061f27628aef09b7499da52337da48b887f76e73b16cc6e0afd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecretsCertificates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b0bcb445b487a46abd841c8ffb0a95ce409eed8e59ad4cffb645397adc391e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0338fa6b3f86c405f57f51cc54618c5e90fcd3725ed8a53768ce1040161f84a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e0b8d0a89eccb1d4165952eb50e583f32ba553ea661a4d77cd5010de4ed864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a172d2612fd67332c4890308251a6fa4d610aa630f7b29bd9f81f9ff82bb23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34fbd063d695213580ac3594fc3a9c6a5025beb735a561f247928fb42823a00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7390698aa082e07e1a79eba72241a33a28377144e48cae65dacccdc1a90bf474(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFabricManagedClusterNodeTypeVmSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e46f75b10726678e546363c42ef9647b97bf744a361bb4ae9f38d39912cd6d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2ce5b10d0727bc01b6b48e6c55f3e1c654c46ae4cd7cea4adc5433b0d6ff55(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFabricManagedClusterNodeTypeVmSecretsCertificates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2eb90b6f3518e05e86d37db735e1cdd97ea668731ad07b9fdb9349b8c47a64c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ce67e4d9d49f627099108de34e3a90adb736598253ccd4c5cda42f7e3c34c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterNodeTypeVmSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b963419f21b23acc705e79789f872de5c63209709864385fe1eeb814f8d0c70(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f866c52fcfbea6de89a7f5dc26c333da2e7e541e6ab7c05d800c4c0c13c1ab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d998fa8ee18b16a43de28e1435b506a2d5c21d8d9186e7a0cda075916b9f9a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ef64c528c944f71a59c5b0cc0f445f2e084b3e0203d1e0bf879f0b07ea076b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada3a3cc306a6e2608eeb231eba6df02ec621754259b188038306a4c5bcc5d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9551241b3675224d553c271c2e2edc769449b574c2dc5b8ccf16186bf24f07d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205f95c6035f424d85e84ef09ce2378e95747b8a620ae20f1ce05e340b83334c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFabricManagedClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
