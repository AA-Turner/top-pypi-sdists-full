r'''
# `opentelekomcloud_cfw_acl_rule_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cfw_acl_rule_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1).
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


class CfwAclRuleV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1 opentelekomcloud_cfw_acl_rule_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        action_type: jsii.Number,
        address_type: jsii.Number,
        destination: typing.Union["CfwAclRuleV1Destination", typing.Dict[builtins.str, typing.Any]],
        long_connect_enable: jsii.Number,
        name: builtins.str,
        object_id: builtins.str,
        sequence: typing.Union["CfwAclRuleV1Sequence", typing.Dict[builtins.str, typing.Any]],
        service: typing.Union["CfwAclRuleV1Service", typing.Dict[builtins.str, typing.Any]],
        source: typing.Union["CfwAclRuleV1Source", typing.Dict[builtins.str, typing.Any]],
        status: jsii.Number,
        type: jsii.Number,
        applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        applications_json_string: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        direction: typing.Optional[jsii.Number] = None,
        long_connect_time: typing.Optional[jsii.Number] = None,
        long_connect_time_hour: typing.Optional[jsii.Number] = None,
        long_connect_time_minute: typing.Optional[jsii.Number] = None,
        long_connect_time_second: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CfwAclRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1 opentelekomcloud_cfw_acl_rule_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#action_type CfwAclRuleV1#action_type}.
        :param address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#destination CfwAclRuleV1#destination}
        :param long_connect_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_enable CfwAclRuleV1#long_connect_enable}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#object_id CfwAclRuleV1#object_id}.
        :param sequence: sequence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#sequence CfwAclRuleV1#sequence}
        :param service: service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service CfwAclRuleV1#service}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source CfwAclRuleV1#source}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#status CfwAclRuleV1#status}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param applications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#applications CfwAclRuleV1#applications}.
        :param applications_json_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#applications_json_string CfwAclRuleV1#applications_json_string}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#description CfwAclRuleV1#description}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#direction CfwAclRuleV1#direction}.
        :param long_connect_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time CfwAclRuleV1#long_connect_time}.
        :param long_connect_time_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_hour CfwAclRuleV1#long_connect_time_hour}.
        :param long_connect_time_minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_minute CfwAclRuleV1#long_connect_time_minute}.
        :param long_connect_time_second: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_second CfwAclRuleV1#long_connect_time_second}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#timeouts CfwAclRuleV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7455662b104acab54a488fc9b68bf91b7c280d598fb288c7b5b785fb7f31939)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CfwAclRuleV1Config(
            action_type=action_type,
            address_type=address_type,
            destination=destination,
            long_connect_enable=long_connect_enable,
            name=name,
            object_id=object_id,
            sequence=sequence,
            service=service,
            source=source,
            status=status,
            type=type,
            applications=applications,
            applications_json_string=applications_json_string,
            description=description,
            direction=direction,
            long_connect_time=long_connect_time,
            long_connect_time_hour=long_connect_time_hour,
            long_connect_time_minute=long_connect_time_minute,
            long_connect_time_second=long_connect_time_second,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a CfwAclRuleV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CfwAclRuleV1 to import.
        :param import_from_id: The id of the existing CfwAclRuleV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CfwAclRuleV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a872de92daab0f46cce615975e5eb5e9a57d4a7c7b23e81996635e0b20f463)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        type: jsii.Number,
        address: typing.Optional[builtins.str] = None,
        address_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        address_set_id: typing.Optional[builtins.str] = None,
        address_set_name: typing.Optional[builtins.str] = None,
        address_set_type: typing.Optional[jsii.Number] = None,
        address_type: typing.Optional[jsii.Number] = None,
        domain_address_name: typing.Optional[builtins.str] = None,
        domain_set_id: typing.Optional[builtins.str] = None,
        domain_set_name: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1DestinationRegionListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_list_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address CfwAclRuleV1#address}.
        :param address_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_group CfwAclRuleV1#address_group}.
        :param address_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_id CfwAclRuleV1#address_set_id}.
        :param address_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_name CfwAclRuleV1#address_set_name}.
        :param address_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_type CfwAclRuleV1#address_set_type}.
        :param address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.
        :param domain_address_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_address_name CfwAclRuleV1#domain_address_name}.
        :param domain_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_id CfwAclRuleV1#domain_set_id}.
        :param domain_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_name CfwAclRuleV1#domain_set_name}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#ip_address CfwAclRuleV1#ip_address}.
        :param predefined_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.
        :param region_list: region_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list CfwAclRuleV1#region_list}
        :param region_list_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list_json CfwAclRuleV1#region_list_json}.
        '''
        value = CfwAclRuleV1Destination(
            type=type,
            address=address,
            address_group=address_group,
            address_set_id=address_set_id,
            address_set_name=address_set_name,
            address_set_type=address_set_type,
            address_type=address_type,
            domain_address_name=domain_address_name,
            domain_set_id=domain_set_id,
            domain_set_name=domain_set_name,
            ip_address=ip_address,
            predefined_group=predefined_group,
            region_list=region_list,
            region_list_json=region_list_json,
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="putSequence")
    def put_sequence(
        self,
        *,
        bottom: typing.Optional[jsii.Number] = None,
        dest_rule_id: typing.Optional[builtins.str] = None,
        top: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bottom: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#bottom CfwAclRuleV1#bottom}.
        :param dest_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_rule_id CfwAclRuleV1#dest_rule_id}.
        :param top: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#top CfwAclRuleV1#top}.
        '''
        value = CfwAclRuleV1Sequence(bottom=bottom, dest_rule_id=dest_rule_id, top=top)

        return typing.cast(None, jsii.invoke(self, "putSequence", [value]))

    @jsii.member(jsii_name="putService")
    def put_service(
        self,
        *,
        type: jsii.Number,
        custom_service: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1ServiceCustomService", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dest_port: typing.Optional[builtins.str] = None,
        predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        protocol: typing.Optional[jsii.Number] = None,
        protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
        service_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_group_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1ServiceServiceGroupNames", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_set_id: typing.Optional[builtins.str] = None,
        service_set_name: typing.Optional[builtins.str] = None,
        service_set_type: typing.Optional[jsii.Number] = None,
        source_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param custom_service: custom_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#custom_service CfwAclRuleV1#custom_service}
        :param dest_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_port CfwAclRuleV1#dest_port}.
        :param predefined_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocol CfwAclRuleV1#protocol}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocols CfwAclRuleV1#protocols}.
        :param service_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_group CfwAclRuleV1#service_group}.
        :param service_group_names: service_group_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_group_names CfwAclRuleV1#service_group_names}
        :param service_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_id CfwAclRuleV1#service_set_id}.
        :param service_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_name CfwAclRuleV1#service_set_name}.
        :param service_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_type CfwAclRuleV1#service_set_type}.
        :param source_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source_port CfwAclRuleV1#source_port}.
        '''
        value = CfwAclRuleV1Service(
            type=type,
            custom_service=custom_service,
            dest_port=dest_port,
            predefined_group=predefined_group,
            protocol=protocol,
            protocols=protocols,
            service_group=service_group,
            service_group_names=service_group_names,
            service_set_id=service_set_id,
            service_set_name=service_set_name,
            service_set_type=service_set_type,
            source_port=source_port,
        )

        return typing.cast(None, jsii.invoke(self, "putService", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        type: jsii.Number,
        address: typing.Optional[builtins.str] = None,
        address_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        address_set_id: typing.Optional[builtins.str] = None,
        address_set_name: typing.Optional[builtins.str] = None,
        address_set_type: typing.Optional[jsii.Number] = None,
        address_type: typing.Optional[jsii.Number] = None,
        domain_address_name: typing.Optional[builtins.str] = None,
        domain_set_id: typing.Optional[builtins.str] = None,
        domain_set_name: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1SourceRegionListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_list_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address CfwAclRuleV1#address}.
        :param address_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_group CfwAclRuleV1#address_group}.
        :param address_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_id CfwAclRuleV1#address_set_id}.
        :param address_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_name CfwAclRuleV1#address_set_name}.
        :param address_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_type CfwAclRuleV1#address_set_type}.
        :param address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.
        :param domain_address_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_address_name CfwAclRuleV1#domain_address_name}.
        :param domain_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_id CfwAclRuleV1#domain_set_id}.
        :param domain_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_name CfwAclRuleV1#domain_set_name}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#ip_address CfwAclRuleV1#ip_address}.
        :param predefined_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.
        :param region_list: region_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list CfwAclRuleV1#region_list}
        :param region_list_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list_json CfwAclRuleV1#region_list_json}.
        '''
        value = CfwAclRuleV1Source(
            type=type,
            address=address,
            address_group=address_group,
            address_set_id=address_set_id,
            address_set_name=address_set_name,
            address_set_type=address_set_type,
            address_type=address_type,
            domain_address_name=domain_address_name,
            domain_set_id=domain_set_id,
            domain_set_name=domain_set_name,
            ip_address=ip_address,
            predefined_group=predefined_group,
            region_list=region_list,
            region_list_json=region_list_json,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#create CfwAclRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#delete CfwAclRuleV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#update CfwAclRuleV1#update}.
        '''
        value = CfwAclRuleV1Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApplications")
    def reset_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplications", []))

    @jsii.member(jsii_name="resetApplicationsJsonString")
    def reset_applications_json_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationsJsonString", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetLongConnectTime")
    def reset_long_connect_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongConnectTime", []))

    @jsii.member(jsii_name="resetLongConnectTimeHour")
    def reset_long_connect_time_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongConnectTimeHour", []))

    @jsii.member(jsii_name="resetLongConnectTimeMinute")
    def reset_long_connect_time_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongConnectTimeMinute", []))

    @jsii.member(jsii_name="resetLongConnectTimeSecond")
    def reset_long_connect_time_second(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongConnectTimeSecond", []))

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
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> "CfwAclRuleV1DestinationOutputReference":
        return typing.cast("CfwAclRuleV1DestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastOpenTime")
    def last_open_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastOpenTime"))

    @builtins.property
    @jsii.member(jsii_name="sequence")
    def sequence(self) -> "CfwAclRuleV1SequenceOutputReference":
        return typing.cast("CfwAclRuleV1SequenceOutputReference", jsii.get(self, "sequence"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "CfwAclRuleV1ServiceOutputReference":
        return typing.cast("CfwAclRuleV1ServiceOutputReference", jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "CfwAclRuleV1SourceOutputReference":
        return typing.cast("CfwAclRuleV1SourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CfwAclRuleV1TimeoutsOutputReference":
        return typing.cast("CfwAclRuleV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionTypeInput")
    def action_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "actionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressTypeInput")
    def address_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationsInput")
    def applications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationsJsonStringInput")
    def applications_json_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationsJsonStringInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional["CfwAclRuleV1Destination"]:
        return typing.cast(typing.Optional["CfwAclRuleV1Destination"], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="longConnectEnableInput")
    def long_connect_enable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longConnectEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeHourInput")
    def long_connect_time_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longConnectTimeHourInput"))

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeInput")
    def long_connect_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longConnectTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeMinuteInput")
    def long_connect_time_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longConnectTimeMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeSecondInput")
    def long_connect_time_second_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longConnectTimeSecondInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sequenceInput")
    def sequence_input(self) -> typing.Optional["CfwAclRuleV1Sequence"]:
        return typing.cast(typing.Optional["CfwAclRuleV1Sequence"], jsii.get(self, "sequenceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional["CfwAclRuleV1Service"]:
        return typing.cast(typing.Optional["CfwAclRuleV1Service"], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["CfwAclRuleV1Source"]:
        return typing.cast(typing.Optional["CfwAclRuleV1Source"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CfwAclRuleV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CfwAclRuleV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "actionType"))

    @action_type.setter
    def action_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e795bd9a9b6147933a660ca1ad66fe6a111260cfd7b7d2b2f1b3c8a48e97f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressType")
    def address_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addressType"))

    @address_type.setter
    def address_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2122230a80d238d589ab4adf6b05326924a80618711ebc50961bc7f34d2f70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applications")
    def applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applications"))

    @applications.setter
    def applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6332553f41793ea4d9bf34919dcae669ce71512598fb4cf48745e2c8180b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationsJsonString")
    def applications_json_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationsJsonString"))

    @applications_json_string.setter
    def applications_json_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811b8c5ddd4086a2aef9c81e905204fa458569ebea6df4b3f276b74eaa283d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationsJsonString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3619a00cf25ebba8dd4924c3e57ae10019df064008933efec761c9b38fa02fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff1567a43ef45cb77102ee76112acf2271ae34be772416fb3954f627d847bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longConnectEnable")
    def long_connect_enable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longConnectEnable"))

    @long_connect_enable.setter
    def long_connect_enable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e64a8bfb1957fc060ce63aee298335012f1eb43d663f490f0e450e9eb43ec99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longConnectEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longConnectTime")
    def long_connect_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longConnectTime"))

    @long_connect_time.setter
    def long_connect_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e8ace50c439af3877848841746d9f70eb3441054cc1ed113eb6c652606326e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longConnectTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeHour")
    def long_connect_time_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longConnectTimeHour"))

    @long_connect_time_hour.setter
    def long_connect_time_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e94d92d8a6a7bbb00185bd94c02b424d3ee590fb1998ce3d77066cd6d091f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longConnectTimeHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeMinute")
    def long_connect_time_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longConnectTimeMinute"))

    @long_connect_time_minute.setter
    def long_connect_time_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1021e88774c97bc714d44d2b59006240b577f3991e3a1e8286f55953413de36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longConnectTimeMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longConnectTimeSecond")
    def long_connect_time_second(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longConnectTimeSecond"))

    @long_connect_time_second.setter
    def long_connect_time_second(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2003b9125569f61f21ba16191bea4099c68df095dea92ff7ee9746dc1aed5507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longConnectTimeSecond", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87ffd084f05823237c3aa951867cc92c3d9f932f1f8b43d9d65520ed0dc9607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e43a6f95cc837c1a0d2f0c6253a278bcf8a41da3b8dfd4432b2752f8a2554e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @status.setter
    def status(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e6e9be2c8082c8080b16798182d03d5cb9e0b87110adf3e0ac01f0e92ffa70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @type.setter
    def type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1da57b4206dbc492a166cb7e4a04a1daa040ebb5110f144ed5a45ff507fa336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_type": "actionType",
        "address_type": "addressType",
        "destination": "destination",
        "long_connect_enable": "longConnectEnable",
        "name": "name",
        "object_id": "objectId",
        "sequence": "sequence",
        "service": "service",
        "source": "source",
        "status": "status",
        "type": "type",
        "applications": "applications",
        "applications_json_string": "applicationsJsonString",
        "description": "description",
        "direction": "direction",
        "long_connect_time": "longConnectTime",
        "long_connect_time_hour": "longConnectTimeHour",
        "long_connect_time_minute": "longConnectTimeMinute",
        "long_connect_time_second": "longConnectTimeSecond",
        "timeouts": "timeouts",
    },
)
class CfwAclRuleV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action_type: jsii.Number,
        address_type: jsii.Number,
        destination: typing.Union["CfwAclRuleV1Destination", typing.Dict[builtins.str, typing.Any]],
        long_connect_enable: jsii.Number,
        name: builtins.str,
        object_id: builtins.str,
        sequence: typing.Union["CfwAclRuleV1Sequence", typing.Dict[builtins.str, typing.Any]],
        service: typing.Union["CfwAclRuleV1Service", typing.Dict[builtins.str, typing.Any]],
        source: typing.Union["CfwAclRuleV1Source", typing.Dict[builtins.str, typing.Any]],
        status: jsii.Number,
        type: jsii.Number,
        applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        applications_json_string: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        direction: typing.Optional[jsii.Number] = None,
        long_connect_time: typing.Optional[jsii.Number] = None,
        long_connect_time_hour: typing.Optional[jsii.Number] = None,
        long_connect_time_minute: typing.Optional[jsii.Number] = None,
        long_connect_time_second: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CfwAclRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#action_type CfwAclRuleV1#action_type}.
        :param address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#destination CfwAclRuleV1#destination}
        :param long_connect_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_enable CfwAclRuleV1#long_connect_enable}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#object_id CfwAclRuleV1#object_id}.
        :param sequence: sequence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#sequence CfwAclRuleV1#sequence}
        :param service: service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service CfwAclRuleV1#service}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source CfwAclRuleV1#source}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#status CfwAclRuleV1#status}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param applications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#applications CfwAclRuleV1#applications}.
        :param applications_json_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#applications_json_string CfwAclRuleV1#applications_json_string}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#description CfwAclRuleV1#description}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#direction CfwAclRuleV1#direction}.
        :param long_connect_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time CfwAclRuleV1#long_connect_time}.
        :param long_connect_time_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_hour CfwAclRuleV1#long_connect_time_hour}.
        :param long_connect_time_minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_minute CfwAclRuleV1#long_connect_time_minute}.
        :param long_connect_time_second: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_second CfwAclRuleV1#long_connect_time_second}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#timeouts CfwAclRuleV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = CfwAclRuleV1Destination(**destination)
        if isinstance(sequence, dict):
            sequence = CfwAclRuleV1Sequence(**sequence)
        if isinstance(service, dict):
            service = CfwAclRuleV1Service(**service)
        if isinstance(source, dict):
            source = CfwAclRuleV1Source(**source)
        if isinstance(timeouts, dict):
            timeouts = CfwAclRuleV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb91efdaf0795d2b0907a0f321fe0d5b1784ec536e2e7fdfb276288e9e877fb7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument address_type", value=address_type, expected_type=type_hints["address_type"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument long_connect_enable", value=long_connect_enable, expected_type=type_hints["long_connect_enable"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument sequence", value=sequence, expected_type=type_hints["sequence"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument applications_json_string", value=applications_json_string, expected_type=type_hints["applications_json_string"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument long_connect_time", value=long_connect_time, expected_type=type_hints["long_connect_time"])
            check_type(argname="argument long_connect_time_hour", value=long_connect_time_hour, expected_type=type_hints["long_connect_time_hour"])
            check_type(argname="argument long_connect_time_minute", value=long_connect_time_minute, expected_type=type_hints["long_connect_time_minute"])
            check_type(argname="argument long_connect_time_second", value=long_connect_time_second, expected_type=type_hints["long_connect_time_second"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_type": action_type,
            "address_type": address_type,
            "destination": destination,
            "long_connect_enable": long_connect_enable,
            "name": name,
            "object_id": object_id,
            "sequence": sequence,
            "service": service,
            "source": source,
            "status": status,
            "type": type,
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
        if applications is not None:
            self._values["applications"] = applications
        if applications_json_string is not None:
            self._values["applications_json_string"] = applications_json_string
        if description is not None:
            self._values["description"] = description
        if direction is not None:
            self._values["direction"] = direction
        if long_connect_time is not None:
            self._values["long_connect_time"] = long_connect_time
        if long_connect_time_hour is not None:
            self._values["long_connect_time_hour"] = long_connect_time_hour
        if long_connect_time_minute is not None:
            self._values["long_connect_time_minute"] = long_connect_time_minute
        if long_connect_time_second is not None:
            self._values["long_connect_time_second"] = long_connect_time_second
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
    def action_type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#action_type CfwAclRuleV1#action_type}.'''
        result = self._values.get("action_type")
        assert result is not None, "Required property 'action_type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def address_type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.'''
        result = self._values.get("address_type")
        assert result is not None, "Required property 'address_type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def destination(self) -> "CfwAclRuleV1Destination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#destination CfwAclRuleV1#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("CfwAclRuleV1Destination", result)

    @builtins.property
    def long_connect_enable(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_enable CfwAclRuleV1#long_connect_enable}.'''
        result = self._values.get("long_connect_enable")
        assert result is not None, "Required property 'long_connect_enable' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#object_id CfwAclRuleV1#object_id}.'''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sequence(self) -> "CfwAclRuleV1Sequence":
        '''sequence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#sequence CfwAclRuleV1#sequence}
        '''
        result = self._values.get("sequence")
        assert result is not None, "Required property 'sequence' is missing"
        return typing.cast("CfwAclRuleV1Sequence", result)

    @builtins.property
    def service(self) -> "CfwAclRuleV1Service":
        '''service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service CfwAclRuleV1#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast("CfwAclRuleV1Service", result)

    @builtins.property
    def source(self) -> "CfwAclRuleV1Source":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source CfwAclRuleV1#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("CfwAclRuleV1Source", result)

    @builtins.property
    def status(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#status CfwAclRuleV1#status}.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#applications CfwAclRuleV1#applications}.'''
        result = self._values.get("applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def applications_json_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#applications_json_string CfwAclRuleV1#applications_json_string}.'''
        result = self._values.get("applications_json_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#description CfwAclRuleV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#direction CfwAclRuleV1#direction}.'''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_connect_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time CfwAclRuleV1#long_connect_time}.'''
        result = self._values.get("long_connect_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_connect_time_hour(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_hour CfwAclRuleV1#long_connect_time_hour}.'''
        result = self._values.get("long_connect_time_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_connect_time_minute(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_minute CfwAclRuleV1#long_connect_time_minute}.'''
        result = self._values.get("long_connect_time_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def long_connect_time_second(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#long_connect_time_second CfwAclRuleV1#long_connect_time_second}.'''
        result = self._values.get("long_connect_time_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CfwAclRuleV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#timeouts CfwAclRuleV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CfwAclRuleV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1Destination",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "address": "address",
        "address_group": "addressGroup",
        "address_set_id": "addressSetId",
        "address_set_name": "addressSetName",
        "address_set_type": "addressSetType",
        "address_type": "addressType",
        "domain_address_name": "domainAddressName",
        "domain_set_id": "domainSetId",
        "domain_set_name": "domainSetName",
        "ip_address": "ipAddress",
        "predefined_group": "predefinedGroup",
        "region_list": "regionList",
        "region_list_json": "regionListJson",
    },
)
class CfwAclRuleV1Destination:
    def __init__(
        self,
        *,
        type: jsii.Number,
        address: typing.Optional[builtins.str] = None,
        address_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        address_set_id: typing.Optional[builtins.str] = None,
        address_set_name: typing.Optional[builtins.str] = None,
        address_set_type: typing.Optional[jsii.Number] = None,
        address_type: typing.Optional[jsii.Number] = None,
        domain_address_name: typing.Optional[builtins.str] = None,
        domain_set_id: typing.Optional[builtins.str] = None,
        domain_set_name: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1DestinationRegionListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_list_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address CfwAclRuleV1#address}.
        :param address_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_group CfwAclRuleV1#address_group}.
        :param address_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_id CfwAclRuleV1#address_set_id}.
        :param address_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_name CfwAclRuleV1#address_set_name}.
        :param address_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_type CfwAclRuleV1#address_set_type}.
        :param address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.
        :param domain_address_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_address_name CfwAclRuleV1#domain_address_name}.
        :param domain_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_id CfwAclRuleV1#domain_set_id}.
        :param domain_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_name CfwAclRuleV1#domain_set_name}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#ip_address CfwAclRuleV1#ip_address}.
        :param predefined_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.
        :param region_list: region_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list CfwAclRuleV1#region_list}
        :param region_list_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list_json CfwAclRuleV1#region_list_json}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f344338afb7232500637ff33ee441f6108bdb28c0424e4761c1dac83a34eba)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument address_group", value=address_group, expected_type=type_hints["address_group"])
            check_type(argname="argument address_set_id", value=address_set_id, expected_type=type_hints["address_set_id"])
            check_type(argname="argument address_set_name", value=address_set_name, expected_type=type_hints["address_set_name"])
            check_type(argname="argument address_set_type", value=address_set_type, expected_type=type_hints["address_set_type"])
            check_type(argname="argument address_type", value=address_type, expected_type=type_hints["address_type"])
            check_type(argname="argument domain_address_name", value=domain_address_name, expected_type=type_hints["domain_address_name"])
            check_type(argname="argument domain_set_id", value=domain_set_id, expected_type=type_hints["domain_set_id"])
            check_type(argname="argument domain_set_name", value=domain_set_name, expected_type=type_hints["domain_set_name"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument predefined_group", value=predefined_group, expected_type=type_hints["predefined_group"])
            check_type(argname="argument region_list", value=region_list, expected_type=type_hints["region_list"])
            check_type(argname="argument region_list_json", value=region_list_json, expected_type=type_hints["region_list_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if address is not None:
            self._values["address"] = address
        if address_group is not None:
            self._values["address_group"] = address_group
        if address_set_id is not None:
            self._values["address_set_id"] = address_set_id
        if address_set_name is not None:
            self._values["address_set_name"] = address_set_name
        if address_set_type is not None:
            self._values["address_set_type"] = address_set_type
        if address_type is not None:
            self._values["address_type"] = address_type
        if domain_address_name is not None:
            self._values["domain_address_name"] = domain_address_name
        if domain_set_id is not None:
            self._values["domain_set_id"] = domain_set_id
        if domain_set_name is not None:
            self._values["domain_set_name"] = domain_set_name
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if predefined_group is not None:
            self._values["predefined_group"] = predefined_group
        if region_list is not None:
            self._values["region_list"] = region_list
        if region_list_json is not None:
            self._values["region_list_json"] = region_list_json

    @builtins.property
    def type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address CfwAclRuleV1#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_group CfwAclRuleV1#address_group}.'''
        result = self._values.get("address_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def address_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_id CfwAclRuleV1#address_set_id}.'''
        result = self._values.get("address_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_name CfwAclRuleV1#address_set_name}.'''
        result = self._values.get("address_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_set_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_type CfwAclRuleV1#address_set_type}.'''
        result = self._values.get("address_set_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def address_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.'''
        result = self._values.get("address_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_address_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_address_name CfwAclRuleV1#domain_address_name}.'''
        result = self._values.get("domain_address_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_id CfwAclRuleV1#domain_set_id}.'''
        result = self._values.get("domain_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_name CfwAclRuleV1#domain_set_name}.'''
        result = self._values.get("domain_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#ip_address CfwAclRuleV1#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def predefined_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.'''
        result = self._values.get("predefined_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1DestinationRegionListStruct"]]]:
        '''region_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list CfwAclRuleV1#region_list}
        '''
        result = self._values.get("region_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1DestinationRegionListStruct"]]], result)

    @builtins.property
    def region_list_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list_json CfwAclRuleV1#region_list_json}.'''
        result = self._values.get("region_list_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1Destination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1DestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1DestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5d31a474e7773bfc97d5d002f33fd7190dd496d0ad64b8d729d54ef0c39ff96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRegionList")
    def put_region_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1DestinationRegionListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae0079b151e9ebf155f2f9a98d3cb843da33621d80df51e5c2ed3466f7218e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegionList", [value]))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetAddressGroup")
    def reset_address_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressGroup", []))

    @jsii.member(jsii_name="resetAddressSetId")
    def reset_address_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressSetId", []))

    @jsii.member(jsii_name="resetAddressSetName")
    def reset_address_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressSetName", []))

    @jsii.member(jsii_name="resetAddressSetType")
    def reset_address_set_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressSetType", []))

    @jsii.member(jsii_name="resetAddressType")
    def reset_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressType", []))

    @jsii.member(jsii_name="resetDomainAddressName")
    def reset_domain_address_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainAddressName", []))

    @jsii.member(jsii_name="resetDomainSetId")
    def reset_domain_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainSetId", []))

    @jsii.member(jsii_name="resetDomainSetName")
    def reset_domain_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainSetName", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetPredefinedGroup")
    def reset_predefined_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredefinedGroup", []))

    @jsii.member(jsii_name="resetRegionList")
    def reset_region_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionList", []))

    @jsii.member(jsii_name="resetRegionListJson")
    def reset_region_list_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionListJson", []))

    @builtins.property
    @jsii.member(jsii_name="regionList")
    def region_list(self) -> "CfwAclRuleV1DestinationRegionListStructList":
        return typing.cast("CfwAclRuleV1DestinationRegionListStructList", jsii.get(self, "regionList"))

    @builtins.property
    @jsii.member(jsii_name="addressGroupInput")
    def address_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSetIdInput")
    def address_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSetNameInput")
    def address_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSetTypeInput")
    def address_set_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addressSetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressTypeInput")
    def address_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="domainAddressNameInput")
    def domain_address_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainAddressNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainSetIdInput")
    def domain_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainSetNameInput")
    def domain_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="predefinedGroupInput")
    def predefined_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "predefinedGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="regionListInput")
    def region_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1DestinationRegionListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1DestinationRegionListStruct"]]], jsii.get(self, "regionListInput"))

    @builtins.property
    @jsii.member(jsii_name="regionListJsonInput")
    def region_list_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionListJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec1fc8f24a77425f94fca1617624540d7281897dbe3072aee43b9e174191a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressGroup")
    def address_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressGroup"))

    @address_group.setter
    def address_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5801756fe48f04629aad71e1124f6b162e3aea2d2589b14d9ad21297d9878c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSetId")
    def address_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressSetId"))

    @address_set_id.setter
    def address_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8773b9c66d59764f6d647e76de94541dc0cfb70b5d30bd388d7fb377e48d2a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSetName")
    def address_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressSetName"))

    @address_set_name.setter
    def address_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfe9bb6788baf644a818b90c562b2df4a11a2a49c3771035cdeac316a202098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSetType")
    def address_set_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addressSetType"))

    @address_set_type.setter
    def address_set_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced876fe316e9d2a0656f068bdae37d58d06a2010198f5990577484f5a89cd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressType")
    def address_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addressType"))

    @address_type.setter
    def address_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88405c7b7ccb71f42762ff8602781e62352433d2dab6d1f53f41d0ef730ce3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainAddressName")
    def domain_address_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainAddressName"))

    @domain_address_name.setter
    def domain_address_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d07e609df55849bf9ff76aafd67c44e827c18b1b7b9369a7ee34ea6d56672e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainAddressName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainSetId")
    def domain_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainSetId"))

    @domain_set_id.setter
    def domain_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc775623ead2796b0ce5e05157a108aac84c5e90838b350c2cfecec35297068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainSetName")
    def domain_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainSetName"))

    @domain_set_name.setter
    def domain_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3153504eff05972b7375e1b99fe0b8fc40edc7cafce698fedb94fc8c54e96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424354e36f7556a4ea3e89a45d1b0ad5d69ce3f7aaad64e2f362fda1ab3822d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predefinedGroup")
    def predefined_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "predefinedGroup"))

    @predefined_group.setter
    def predefined_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c1e7f9225012bd6c6f26edc3205f2af344e9cddbaada93568f7dc819eb59e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predefinedGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionListJson")
    def region_list_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionListJson"))

    @region_list_json.setter
    def region_list_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6bc4ca2c0b73b0c309bf23e5e53dc9ee24daacae53db1264e9a16361b8f2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionListJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @type.setter
    def type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c50dfbd12676da07bb9cd79ff387a0c18ae511b6d140a66863d4df5744546f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwAclRuleV1Destination]:
        return typing.cast(typing.Optional[CfwAclRuleV1Destination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwAclRuleV1Destination]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693cde54e06e5610941c7094946747db08bc1c511d5abdce7b27bd6d1a262bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1DestinationRegionListStruct",
    jsii_struct_bases=[],
    name_mapping={"region_id": "regionId", "region_type": "regionType"},
)
class CfwAclRuleV1DestinationRegionListStruct:
    def __init__(
        self,
        *,
        region_id: typing.Optional[builtins.str] = None,
        region_type: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param region_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_id CfwAclRuleV1#region_id}.
        :param region_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_type CfwAclRuleV1#region_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed3068714278f30f222b2263a6468b55ab33dc50f6e5ed4f4ead5325b629cb6)
            check_type(argname="argument region_id", value=region_id, expected_type=type_hints["region_id"])
            check_type(argname="argument region_type", value=region_type, expected_type=type_hints["region_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if region_id is not None:
            self._values["region_id"] = region_id
        if region_type is not None:
            self._values["region_type"] = region_type

    @builtins.property
    def region_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_id CfwAclRuleV1#region_id}.'''
        result = self._values.get("region_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_type CfwAclRuleV1#region_type}.'''
        result = self._values.get("region_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1DestinationRegionListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1DestinationRegionListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1DestinationRegionListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6c31d33a4c5ca543b6bbc88e862e9289c885e666f197aec7dd6fbc8d8224a29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CfwAclRuleV1DestinationRegionListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18532fe01ba7fab1d7947527128e032fa7e7eca0c7ef364e543d488a55dfe34a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CfwAclRuleV1DestinationRegionListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84abb1c7d778db5d9ff056e2931efd3ad911331ac2a5c06bf351855dd66f0234)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5228192e6edbbce4d9c402163a5d0abe53e34178fb83994fbaf1f263682b3ed7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d51430e38d4dc33c783aa7f1bff043c5cfc222714823d075c33ef28aac3bd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1DestinationRegionListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1DestinationRegionListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1DestinationRegionListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29efc687ecbc0377ea9e1a05b2e367a572a332d47a2dfb94203198aa8c0dcf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CfwAclRuleV1DestinationRegionListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1DestinationRegionListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__514e72f570340bbf629af3edabe8fbf45eed4bf1ba61ea5a733c6634676b1b2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRegionId")
    def reset_region_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionId", []))

    @jsii.member(jsii_name="resetRegionType")
    def reset_region_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionType", []))

    @builtins.property
    @jsii.member(jsii_name="regionIdInput")
    def region_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionTypeInput")
    def region_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "regionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionId")
    def region_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionId"))

    @region_id.setter
    def region_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb63bdde3e2afb0c2d4fd215f3b9fcfb9da99244705c66c6710f13963bf506d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionType")
    def region_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "regionType"))

    @region_type.setter
    def region_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b483b2399db095af02f053aa98dde80b9a122ce9ab486fd6670b1de055f63f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1DestinationRegionListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1DestinationRegionListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1DestinationRegionListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39cbdd52c3c60fcb0cf86ed64c06e1a32b964f37801f8ef8f117e9a424c9c5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1Sequence",
    jsii_struct_bases=[],
    name_mapping={"bottom": "bottom", "dest_rule_id": "destRuleId", "top": "top"},
)
class CfwAclRuleV1Sequence:
    def __init__(
        self,
        *,
        bottom: typing.Optional[jsii.Number] = None,
        dest_rule_id: typing.Optional[builtins.str] = None,
        top: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bottom: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#bottom CfwAclRuleV1#bottom}.
        :param dest_rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_rule_id CfwAclRuleV1#dest_rule_id}.
        :param top: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#top CfwAclRuleV1#top}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e58a26a095b71057718837a7c8a6156ddc5867e4cfae9c0cb30b79e9b30a795)
            check_type(argname="argument bottom", value=bottom, expected_type=type_hints["bottom"])
            check_type(argname="argument dest_rule_id", value=dest_rule_id, expected_type=type_hints["dest_rule_id"])
            check_type(argname="argument top", value=top, expected_type=type_hints["top"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bottom is not None:
            self._values["bottom"] = bottom
        if dest_rule_id is not None:
            self._values["dest_rule_id"] = dest_rule_id
        if top is not None:
            self._values["top"] = top

    @builtins.property
    def bottom(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#bottom CfwAclRuleV1#bottom}.'''
        result = self._values.get("bottom")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dest_rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_rule_id CfwAclRuleV1#dest_rule_id}.'''
        result = self._values.get("dest_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def top(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#top CfwAclRuleV1#top}.'''
        result = self._values.get("top")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1Sequence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1SequenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1SequenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79341aa09d528f842473b3a5b095dc5ff849f22499f797f1dba1ccdc8098e693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBottom")
    def reset_bottom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBottom", []))

    @jsii.member(jsii_name="resetDestRuleId")
    def reset_dest_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestRuleId", []))

    @jsii.member(jsii_name="resetTop")
    def reset_top(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTop", []))

    @builtins.property
    @jsii.member(jsii_name="bottomInput")
    def bottom_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bottomInput"))

    @builtins.property
    @jsii.member(jsii_name="destRuleIdInput")
    def dest_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="topInput")
    def top_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "topInput"))

    @builtins.property
    @jsii.member(jsii_name="bottom")
    def bottom(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bottom"))

    @bottom.setter
    def bottom(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4297344fc1c5023248c299dc536031bdfc586240ddb1e2128ab171aac678819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bottom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destRuleId")
    def dest_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destRuleId"))

    @dest_rule_id.setter
    def dest_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e1009e0dd4d7079f7c4fb7d38a9310f0251d1caf98e9b86d7be694fb1b333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destRuleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="top")
    def top(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "top"))

    @top.setter
    def top(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fcdac6bf2ac6b81b03cc346d8e69db04b3605d2f2be55f15865eeb66db6c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "top", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwAclRuleV1Sequence]:
        return typing.cast(typing.Optional[CfwAclRuleV1Sequence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwAclRuleV1Sequence]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc22deeeffdb5deb072610079c74a6108eca933d1f3921121fc6cb889d3cf11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1Service",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "custom_service": "customService",
        "dest_port": "destPort",
        "predefined_group": "predefinedGroup",
        "protocol": "protocol",
        "protocols": "protocols",
        "service_group": "serviceGroup",
        "service_group_names": "serviceGroupNames",
        "service_set_id": "serviceSetId",
        "service_set_name": "serviceSetName",
        "service_set_type": "serviceSetType",
        "source_port": "sourcePort",
    },
)
class CfwAclRuleV1Service:
    def __init__(
        self,
        *,
        type: jsii.Number,
        custom_service: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1ServiceCustomService", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dest_port: typing.Optional[builtins.str] = None,
        predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        protocol: typing.Optional[jsii.Number] = None,
        protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
        service_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_group_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1ServiceServiceGroupNames", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_set_id: typing.Optional[builtins.str] = None,
        service_set_name: typing.Optional[builtins.str] = None,
        service_set_type: typing.Optional[jsii.Number] = None,
        source_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param custom_service: custom_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#custom_service CfwAclRuleV1#custom_service}
        :param dest_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_port CfwAclRuleV1#dest_port}.
        :param predefined_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocol CfwAclRuleV1#protocol}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocols CfwAclRuleV1#protocols}.
        :param service_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_group CfwAclRuleV1#service_group}.
        :param service_group_names: service_group_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_group_names CfwAclRuleV1#service_group_names}
        :param service_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_id CfwAclRuleV1#service_set_id}.
        :param service_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_name CfwAclRuleV1#service_set_name}.
        :param service_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_type CfwAclRuleV1#service_set_type}.
        :param source_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source_port CfwAclRuleV1#source_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced2d83007200504a651675014643d87064a033d128db0c7a1d75d91edab0b9b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument custom_service", value=custom_service, expected_type=type_hints["custom_service"])
            check_type(argname="argument dest_port", value=dest_port, expected_type=type_hints["dest_port"])
            check_type(argname="argument predefined_group", value=predefined_group, expected_type=type_hints["predefined_group"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument service_group", value=service_group, expected_type=type_hints["service_group"])
            check_type(argname="argument service_group_names", value=service_group_names, expected_type=type_hints["service_group_names"])
            check_type(argname="argument service_set_id", value=service_set_id, expected_type=type_hints["service_set_id"])
            check_type(argname="argument service_set_name", value=service_set_name, expected_type=type_hints["service_set_name"])
            check_type(argname="argument service_set_type", value=service_set_type, expected_type=type_hints["service_set_type"])
            check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if custom_service is not None:
            self._values["custom_service"] = custom_service
        if dest_port is not None:
            self._values["dest_port"] = dest_port
        if predefined_group is not None:
            self._values["predefined_group"] = predefined_group
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocols is not None:
            self._values["protocols"] = protocols
        if service_group is not None:
            self._values["service_group"] = service_group
        if service_group_names is not None:
            self._values["service_group_names"] = service_group_names
        if service_set_id is not None:
            self._values["service_set_id"] = service_set_id
        if service_set_name is not None:
            self._values["service_set_name"] = service_set_name
        if service_set_type is not None:
            self._values["service_set_type"] = service_set_type
        if source_port is not None:
            self._values["source_port"] = source_port

    @builtins.property
    def type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def custom_service(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1ServiceCustomService"]]]:
        '''custom_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#custom_service CfwAclRuleV1#custom_service}
        '''
        result = self._values.get("custom_service")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1ServiceCustomService"]]], result)

    @builtins.property
    def dest_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_port CfwAclRuleV1#dest_port}.'''
        result = self._values.get("dest_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predefined_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.'''
        result = self._values.get("predefined_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocol CfwAclRuleV1#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocols CfwAclRuleV1#protocols}.'''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def service_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_group CfwAclRuleV1#service_group}.'''
        result = self._values.get("service_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_group_names(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1ServiceServiceGroupNames"]]]:
        '''service_group_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_group_names CfwAclRuleV1#service_group_names}
        '''
        result = self._values.get("service_group_names")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1ServiceServiceGroupNames"]]], result)

    @builtins.property
    def service_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_id CfwAclRuleV1#service_set_id}.'''
        result = self._values.get("service_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_name CfwAclRuleV1#service_set_name}.'''
        result = self._values.get("service_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_set_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_type CfwAclRuleV1#service_set_type}.'''
        result = self._values.get("service_set_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source_port CfwAclRuleV1#source_port}.'''
        result = self._values.get("source_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1Service(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceCustomService",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "dest_port": "destPort",
        "name": "name",
        "protocol": "protocol",
        "source_port": "sourcePort",
    },
)
class CfwAclRuleV1ServiceCustomService:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        dest_port: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[jsii.Number] = None,
        source_port: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#description CfwAclRuleV1#description}.
        :param dest_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_port CfwAclRuleV1#dest_port}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocol CfwAclRuleV1#protocol}.
        :param source_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source_port CfwAclRuleV1#source_port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51face4c318ad2514eb30c26ac280e4bcd9489ebe27c9882371a267c424ce857)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dest_port", value=dest_port, expected_type=type_hints["dest_port"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if dest_port is not None:
            self._values["dest_port"] = dest_port
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if source_port is not None:
            self._values["source_port"] = source_port

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#description CfwAclRuleV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dest_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#dest_port CfwAclRuleV1#dest_port}.'''
        result = self._values.get("dest_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocol CfwAclRuleV1#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#source_port CfwAclRuleV1#source_port}.'''
        result = self._values.get("source_port")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1ServiceCustomService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1ServiceCustomServiceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceCustomServiceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92cac2a31b58b94eab71637b7159761c1e20037a69cc8d4a0dad6829d7a97a58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CfwAclRuleV1ServiceCustomServiceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f795262365552cb8be3f633bbdbc5392c49250a5d92241a466564821c767c30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CfwAclRuleV1ServiceCustomServiceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4cb0205f85110a73db4c2550b7418cbac19da41fb4eedaa8b0820d1317de623)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4da40e988b8757990eeebe7e4707fd32337cb246021fe9a293fbcf768074ce8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6200abda10629c1d76fbf027d3cc10ab1da293a1f9c42c92d47e3682069c0ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceCustomService]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceCustomService]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceCustomService]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2d1dd9a8c2b00920369f2a662adfe7fe1ce8db1542d3902b52c0f424fda6c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CfwAclRuleV1ServiceCustomServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceCustomServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__769796d8e7ea2d9a238da6bb2f9c921e8b6faa63717c03efdc6f03f93ba9e2d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestPort")
    def reset_dest_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestPort", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetSourcePort")
    def reset_source_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcePort", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destPortInput")
    def dest_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortInput")
    def source_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePortInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb3bfdd00fc2cf9adbf52b8e29919982100bcc70e340b82ff50f93c7179b2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destPort")
    def dest_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destPort"))

    @dest_port.setter
    def dest_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f58f37fb590105436533da0ab119e303265cc033b4f2cfbeac224a8fd30d817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ff6afed09a1f11f63f161c9caddfca72b0d9a6661f7d18e09629a263b337a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1adf2929e477b9fd25e8f12dbc1bee47e288194b9f8c2564d13ff7c5d7b4f648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePort")
    def source_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePort"))

    @source_port.setter
    def source_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524a72e1c210675eb0e0136f8f112b314b137d7e7afbe3495fa892aadd634734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceCustomService]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceCustomService]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceCustomService]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a5520746313fe7c07bf01f270a267f71a2847e9259a8ac48e25b309d579434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CfwAclRuleV1ServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b65495273dba720b0588bb9789639db436a52593c6aa864854ed0cb06e6575a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomService")
    def put_custom_service(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1ServiceCustomService, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0507ee01bd67d3e6691fdc151997907556bde686f6ebae9e8e5eff40f15d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomService", [value]))

    @jsii.member(jsii_name="putServiceGroupNames")
    def put_service_group_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1ServiceServiceGroupNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58884c685f321007614e0378c59db3d1048dc38b9e2002b1de2ff85f3dd9021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceGroupNames", [value]))

    @jsii.member(jsii_name="resetCustomService")
    def reset_custom_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomService", []))

    @jsii.member(jsii_name="resetDestPort")
    def reset_dest_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestPort", []))

    @jsii.member(jsii_name="resetPredefinedGroup")
    def reset_predefined_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredefinedGroup", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetServiceGroup")
    def reset_service_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceGroup", []))

    @jsii.member(jsii_name="resetServiceGroupNames")
    def reset_service_group_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceGroupNames", []))

    @jsii.member(jsii_name="resetServiceSetId")
    def reset_service_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceSetId", []))

    @jsii.member(jsii_name="resetServiceSetName")
    def reset_service_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceSetName", []))

    @jsii.member(jsii_name="resetServiceSetType")
    def reset_service_set_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceSetType", []))

    @jsii.member(jsii_name="resetSourcePort")
    def reset_source_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcePort", []))

    @builtins.property
    @jsii.member(jsii_name="customService")
    def custom_service(self) -> CfwAclRuleV1ServiceCustomServiceList:
        return typing.cast(CfwAclRuleV1ServiceCustomServiceList, jsii.get(self, "customService"))

    @builtins.property
    @jsii.member(jsii_name="serviceGroupNames")
    def service_group_names(self) -> "CfwAclRuleV1ServiceServiceGroupNamesList":
        return typing.cast("CfwAclRuleV1ServiceServiceGroupNamesList", jsii.get(self, "serviceGroupNames"))

    @builtins.property
    @jsii.member(jsii_name="customServiceInput")
    def custom_service_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceCustomService]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceCustomService]]], jsii.get(self, "customServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="destPortInput")
    def dest_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destPortInput"))

    @builtins.property
    @jsii.member(jsii_name="predefinedGroupInput")
    def predefined_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "predefinedGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceGroupInput")
    def service_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceGroupNamesInput")
    def service_group_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1ServiceServiceGroupNames"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1ServiceServiceGroupNames"]]], jsii.get(self, "serviceGroupNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceSetIdInput")
    def service_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceSetNameInput")
    def service_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceSetTypeInput")
    def service_set_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serviceSetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePortInput")
    def source_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePortInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="destPort")
    def dest_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destPort"))

    @dest_port.setter
    def dest_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e575e2b675ccf54dbb310ee2dd7e610425033e16cf1073cb8f0f6f2074c6b6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predefinedGroup")
    def predefined_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "predefinedGroup"))

    @predefined_group.setter
    def predefined_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557015768b127dc6239ac42ab5bd8db57fd0c8d066bce7a4b2a40233d1bea24a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predefinedGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899b877df5f4e21fabbf196bd33a235cc931908ac321b54c9086993e9b87c11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65aecc27335b86a9cd04a92a6d7c1ead5ec470b6b9518561a27f97f129b29dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceGroup")
    def service_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceGroup"))

    @service_group.setter
    def service_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73acf07d76c84081eb17eba6d35e8cba071dda24cc4aaf96dd20682e139c1298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceSetId")
    def service_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceSetId"))

    @service_set_id.setter
    def service_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e24e10b5c90c85e9f61cddbb595340e59d086e94da3ed2d894d146aabfec44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceSetName")
    def service_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceSetName"))

    @service_set_name.setter
    def service_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292a38983643c78191dbed87f8841cad25b133c9873665e8e313254fe37f227e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceSetType")
    def service_set_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serviceSetType"))

    @service_set_type.setter
    def service_set_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c6282aab229599dd05858efb8a8c42969b5d93ce09e2d67dedef8f4a51afd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceSetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePort")
    def source_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePort"))

    @source_port.setter
    def source_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56839f7a3babc152cdd4175d69d2a7e4f2233e7484d741e86337e105852dddf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @type.setter
    def type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee10ab2b3eeddb5cf43351d5c764aa042efcd0670ddb9fedf201fb6e56d6b0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwAclRuleV1Service]:
        return typing.cast(typing.Optional[CfwAclRuleV1Service], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwAclRuleV1Service]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6a6fbacacf5f85f6557236c22782cd778ee2eaa0dff1205734f27d701197fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceServiceGroupNames",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocols": "protocols",
        "service_set_type": "serviceSetType",
        "set_id": "setId",
    },
)
class CfwAclRuleV1ServiceServiceGroupNames:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
        service_set_type: typing.Optional[jsii.Number] = None,
        set_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocols CfwAclRuleV1#protocols}.
        :param service_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_type CfwAclRuleV1#service_set_type}.
        :param set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#set_id CfwAclRuleV1#set_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458f1ac96ca3422467162a548ec790c57068c498a3d3575eb347737001c94b34)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument service_set_type", value=service_set_type, expected_type=type_hints["service_set_type"])
            check_type(argname="argument set_id", value=set_id, expected_type=type_hints["set_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if protocols is not None:
            self._values["protocols"] = protocols
        if service_set_type is not None:
            self._values["service_set_type"] = service_set_type
        if set_id is not None:
            self._values["set_id"] = set_id

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#name CfwAclRuleV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#protocols CfwAclRuleV1#protocols}.'''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def service_set_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#service_set_type CfwAclRuleV1#service_set_type}.'''
        result = self._values.get("service_set_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#set_id CfwAclRuleV1#set_id}.'''
        result = self._values.get("set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1ServiceServiceGroupNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1ServiceServiceGroupNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceServiceGroupNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9e39cd3e3d98b0f0bf2bbfb11498671c838f6fddcb21b00717e43d34d0709b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CfwAclRuleV1ServiceServiceGroupNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae11d7d98206e8ced10091d609d0f94b068108e2d51548ac8053750868da06d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CfwAclRuleV1ServiceServiceGroupNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37bdd4f37af6de6ca9169ffd33555a9b5e5a6e5d19f38003c80948cac89990d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e206cb0f69c538378c2b813d320a0b62859990b894128f1e92819ddaaac05c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a452f345540285bc7d13c5f20346d18c8be57d09773bb03f1f28ade9303d83d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceServiceGroupNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceServiceGroupNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceServiceGroupNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee67f3beb394206f3b08df1acc6bb6ac884f6037a2d0fe5e97c5e769ccc0e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CfwAclRuleV1ServiceServiceGroupNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1ServiceServiceGroupNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23b18b901ec23a1aadd1bb96a7e5ce224eaf4b39e3cee14f05196861110cc24a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetServiceSetType")
    def reset_service_set_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceSetType", []))

    @jsii.member(jsii_name="resetSetId")
    def reset_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetId", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceSetTypeInput")
    def service_set_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serviceSetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="setIdInput")
    def set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "setIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578b7c143132e05892834169909e86636032f89657615b4772845b5f36b2c964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175fdbfb18704577cc8504fefa7afd02cfdbe5559907e4b00f89537a075d36d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceSetType")
    def service_set_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serviceSetType"))

    @service_set_type.setter
    def service_set_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358bba1bfc8ecd97f74ae7b9b761c9926f89cfd53d8b50ffcd3103c038b26980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceSetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="setId")
    def set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "setId"))

    @set_id.setter
    def set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9e813d3749d41923c18cf30a922e7fd8280bea50fa67531826c7edf2c79b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceServiceGroupNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceServiceGroupNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceServiceGroupNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d89f904c99027f4b75d8647ebd17d1639e948895c4ce750c589e99400c12ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1Source",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "address": "address",
        "address_group": "addressGroup",
        "address_set_id": "addressSetId",
        "address_set_name": "addressSetName",
        "address_set_type": "addressSetType",
        "address_type": "addressType",
        "domain_address_name": "domainAddressName",
        "domain_set_id": "domainSetId",
        "domain_set_name": "domainSetName",
        "ip_address": "ipAddress",
        "predefined_group": "predefinedGroup",
        "region_list": "regionList",
        "region_list_json": "regionListJson",
    },
)
class CfwAclRuleV1Source:
    def __init__(
        self,
        *,
        type: jsii.Number,
        address: typing.Optional[builtins.str] = None,
        address_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        address_set_id: typing.Optional[builtins.str] = None,
        address_set_name: typing.Optional[builtins.str] = None,
        address_set_type: typing.Optional[jsii.Number] = None,
        address_type: typing.Optional[jsii.Number] = None,
        domain_address_name: typing.Optional[builtins.str] = None,
        domain_set_id: typing.Optional[builtins.str] = None,
        domain_set_name: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1SourceRegionListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region_list_json: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address CfwAclRuleV1#address}.
        :param address_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_group CfwAclRuleV1#address_group}.
        :param address_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_id CfwAclRuleV1#address_set_id}.
        :param address_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_name CfwAclRuleV1#address_set_name}.
        :param address_set_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_type CfwAclRuleV1#address_set_type}.
        :param address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.
        :param domain_address_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_address_name CfwAclRuleV1#domain_address_name}.
        :param domain_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_id CfwAclRuleV1#domain_set_id}.
        :param domain_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_name CfwAclRuleV1#domain_set_name}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#ip_address CfwAclRuleV1#ip_address}.
        :param predefined_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.
        :param region_list: region_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list CfwAclRuleV1#region_list}
        :param region_list_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list_json CfwAclRuleV1#region_list_json}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a4ca0c50230c0bf320bfeb974b898effe165b272aaa4506cfc070f63633d50)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument address_group", value=address_group, expected_type=type_hints["address_group"])
            check_type(argname="argument address_set_id", value=address_set_id, expected_type=type_hints["address_set_id"])
            check_type(argname="argument address_set_name", value=address_set_name, expected_type=type_hints["address_set_name"])
            check_type(argname="argument address_set_type", value=address_set_type, expected_type=type_hints["address_set_type"])
            check_type(argname="argument address_type", value=address_type, expected_type=type_hints["address_type"])
            check_type(argname="argument domain_address_name", value=domain_address_name, expected_type=type_hints["domain_address_name"])
            check_type(argname="argument domain_set_id", value=domain_set_id, expected_type=type_hints["domain_set_id"])
            check_type(argname="argument domain_set_name", value=domain_set_name, expected_type=type_hints["domain_set_name"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument predefined_group", value=predefined_group, expected_type=type_hints["predefined_group"])
            check_type(argname="argument region_list", value=region_list, expected_type=type_hints["region_list"])
            check_type(argname="argument region_list_json", value=region_list_json, expected_type=type_hints["region_list_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if address is not None:
            self._values["address"] = address
        if address_group is not None:
            self._values["address_group"] = address_group
        if address_set_id is not None:
            self._values["address_set_id"] = address_set_id
        if address_set_name is not None:
            self._values["address_set_name"] = address_set_name
        if address_set_type is not None:
            self._values["address_set_type"] = address_set_type
        if address_type is not None:
            self._values["address_type"] = address_type
        if domain_address_name is not None:
            self._values["domain_address_name"] = domain_address_name
        if domain_set_id is not None:
            self._values["domain_set_id"] = domain_set_id
        if domain_set_name is not None:
            self._values["domain_set_name"] = domain_set_name
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if predefined_group is not None:
            self._values["predefined_group"] = predefined_group
        if region_list is not None:
            self._values["region_list"] = region_list
        if region_list_json is not None:
            self._values["region_list_json"] = region_list_json

    @builtins.property
    def type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#type CfwAclRuleV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address CfwAclRuleV1#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_group CfwAclRuleV1#address_group}.'''
        result = self._values.get("address_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def address_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_id CfwAclRuleV1#address_set_id}.'''
        result = self._values.get("address_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_name CfwAclRuleV1#address_set_name}.'''
        result = self._values.get("address_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def address_set_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_set_type CfwAclRuleV1#address_set_type}.'''
        result = self._values.get("address_set_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def address_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#address_type CfwAclRuleV1#address_type}.'''
        result = self._values.get("address_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_address_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_address_name CfwAclRuleV1#domain_address_name}.'''
        result = self._values.get("domain_address_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_id CfwAclRuleV1#domain_set_id}.'''
        result = self._values.get("domain_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_set_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#domain_set_name CfwAclRuleV1#domain_set_name}.'''
        result = self._values.get("domain_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#ip_address CfwAclRuleV1#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def predefined_group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#predefined_group CfwAclRuleV1#predefined_group}.'''
        result = self._values.get("predefined_group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1SourceRegionListStruct"]]]:
        '''region_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list CfwAclRuleV1#region_list}
        '''
        result = self._values.get("region_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1SourceRegionListStruct"]]], result)

    @builtins.property
    def region_list_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_list_json CfwAclRuleV1#region_list_json}.'''
        result = self._values.get("region_list_json")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1Source(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1SourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1SourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d53d6eb5a32343475aa8592eb53322605df902a4aa18826c3022e8de4d6fa42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRegionList")
    def put_region_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CfwAclRuleV1SourceRegionListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991a60d937b385d8704406aacab78c5f4da877f8b252f7a478940c5f4b4b293b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegionList", [value]))

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetAddressGroup")
    def reset_address_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressGroup", []))

    @jsii.member(jsii_name="resetAddressSetId")
    def reset_address_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressSetId", []))

    @jsii.member(jsii_name="resetAddressSetName")
    def reset_address_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressSetName", []))

    @jsii.member(jsii_name="resetAddressSetType")
    def reset_address_set_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressSetType", []))

    @jsii.member(jsii_name="resetAddressType")
    def reset_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressType", []))

    @jsii.member(jsii_name="resetDomainAddressName")
    def reset_domain_address_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainAddressName", []))

    @jsii.member(jsii_name="resetDomainSetId")
    def reset_domain_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainSetId", []))

    @jsii.member(jsii_name="resetDomainSetName")
    def reset_domain_set_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainSetName", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetPredefinedGroup")
    def reset_predefined_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredefinedGroup", []))

    @jsii.member(jsii_name="resetRegionList")
    def reset_region_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionList", []))

    @jsii.member(jsii_name="resetRegionListJson")
    def reset_region_list_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionListJson", []))

    @builtins.property
    @jsii.member(jsii_name="regionList")
    def region_list(self) -> "CfwAclRuleV1SourceRegionListStructList":
        return typing.cast("CfwAclRuleV1SourceRegionListStructList", jsii.get(self, "regionList"))

    @builtins.property
    @jsii.member(jsii_name="addressGroupInput")
    def address_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSetIdInput")
    def address_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSetNameInput")
    def address_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="addressSetTypeInput")
    def address_set_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addressSetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="addressTypeInput")
    def address_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "addressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="domainAddressNameInput")
    def domain_address_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainAddressNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainSetIdInput")
    def domain_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainSetNameInput")
    def domain_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="predefinedGroupInput")
    def predefined_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "predefinedGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="regionListInput")
    def region_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1SourceRegionListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CfwAclRuleV1SourceRegionListStruct"]]], jsii.get(self, "regionListInput"))

    @builtins.property
    @jsii.member(jsii_name="regionListJsonInput")
    def region_list_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionListJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660ca77535ca1e4c95ec1f9053c61f3fb72d5d1c88a8eb95ba2f127b939ba28e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressGroup")
    def address_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressGroup"))

    @address_group.setter
    def address_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57dcf0e36b591f3e1a4c5d491e09ce7d9a16a01305763c710c1e6e9cd32138fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSetId")
    def address_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressSetId"))

    @address_set_id.setter
    def address_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281cdeaf25b0b9a77ff6d98b29ee8270bb3267662837708e55bab599a48260d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSetName")
    def address_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addressSetName"))

    @address_set_name.setter
    def address_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec765a48574faafca48ba27b0aabab93ef8aea7b6367f83a95e933198ae772cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressSetType")
    def address_set_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addressSetType"))

    @address_set_type.setter
    def address_set_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b25f48b71a37b9cf7281ae4234cf721f5eb43c68b501b2c62499aaa194c39e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressSetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addressType")
    def address_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "addressType"))

    @address_type.setter
    def address_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3d35aff6330b3618b349f23242218f1e39f49bb7295654d272815fa182ea5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainAddressName")
    def domain_address_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainAddressName"))

    @domain_address_name.setter
    def domain_address_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6633236675ab02e4071a4e42051c30ad1c0d6c2007f6c44c2a3ec06dbb87c4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainAddressName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainSetId")
    def domain_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainSetId"))

    @domain_set_id.setter
    def domain_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7980c449d623de755a5db9ddaca071c343d31cca5ea0805451695af0fbe5570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainSetName")
    def domain_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainSetName"))

    @domain_set_name.setter
    def domain_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9daee2c0126895d22d3d7225a8a56532d4aaa83bdf4ad3d8bf89a8dc98645978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f033c81621f000f65fca409465aa0fcc5d1ab3202d57ed1b113ba1814137cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predefinedGroup")
    def predefined_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "predefinedGroup"))

    @predefined_group.setter
    def predefined_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cc6bc42f62d53d5bab2fda543f3b23981b5305f61a30ff9720def1f0c48c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predefinedGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionListJson")
    def region_list_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionListJson"))

    @region_list_json.setter
    def region_list_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd4be9af6f7073f5a5dd72b96b9a17ef1e59ced1299fe93c27645897c62d7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionListJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @type.setter
    def type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf8466eb2997f924d19456e4572aa1d93746950d208abf2a95e50dc25b0bc23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwAclRuleV1Source]:
        return typing.cast(typing.Optional[CfwAclRuleV1Source], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwAclRuleV1Source]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197992054c60b0b7bcfc66170dc0aa4f32317ced0beb18979fb5a98d0d0fefab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1SourceRegionListStruct",
    jsii_struct_bases=[],
    name_mapping={"region_id": "regionId", "region_type": "regionType"},
)
class CfwAclRuleV1SourceRegionListStruct:
    def __init__(
        self,
        *,
        region_id: typing.Optional[builtins.str] = None,
        region_type: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param region_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_id CfwAclRuleV1#region_id}.
        :param region_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_type CfwAclRuleV1#region_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253b89e8260b6091f50f27c4705e0c9b894ad20e2f20f6e551afefa062076bc8)
            check_type(argname="argument region_id", value=region_id, expected_type=type_hints["region_id"])
            check_type(argname="argument region_type", value=region_type, expected_type=type_hints["region_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if region_id is not None:
            self._values["region_id"] = region_id
        if region_type is not None:
            self._values["region_type"] = region_type

    @builtins.property
    def region_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_id CfwAclRuleV1#region_id}.'''
        result = self._values.get("region_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#region_type CfwAclRuleV1#region_type}.'''
        result = self._values.get("region_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1SourceRegionListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1SourceRegionListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1SourceRegionListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1846f53e02c603a4329831274cf60ce29d952a1172e4f0d524264b7153a1686c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CfwAclRuleV1SourceRegionListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc159d947c056ee74a2ed48e319ea33c2e10beb55553ff038729116f0e04d87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CfwAclRuleV1SourceRegionListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb109b3a4bf68349750a63ffc128018cd1b2d4c95a55fc1cd96b711a58044b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d87e5a584fc62ad7211d6dbf076e54deb5c4618e6bf3c47fb2718fd0f93fcfd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6b3177d16cb1be9a2d1ace25b1d5f8544fc4fac3026e81e33b2afeab5ae3211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1SourceRegionListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1SourceRegionListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1SourceRegionListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356bd5ee42e2f1e6db7d112076d91ba781a2abae4051c4922a3a6671dee5562b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CfwAclRuleV1SourceRegionListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1SourceRegionListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab523b7cc2eac056355e6d4bcd6666024b222a29b781c9251d4d55eba3c4cf21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRegionId")
    def reset_region_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionId", []))

    @jsii.member(jsii_name="resetRegionType")
    def reset_region_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionType", []))

    @builtins.property
    @jsii.member(jsii_name="regionIdInput")
    def region_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionTypeInput")
    def region_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "regionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionId")
    def region_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionId"))

    @region_id.setter
    def region_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515b88b27193c0ea37e8e843ccc920e85c1ca0165d3669ba91a80f4fde6a3089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionType")
    def region_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "regionType"))

    @region_type.setter
    def region_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdb19e6284cfa696398ca4c33ddea7d4eda19404d46399297210037cd1d12b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1SourceRegionListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1SourceRegionListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1SourceRegionListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbc295118ab4b19869c755459654a5e5a8b9b074ae653571fdabdfdeb187086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CfwAclRuleV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#create CfwAclRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#delete CfwAclRuleV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#update CfwAclRuleV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eaedd6f7879f8d1466160a832ac132d41635953700f27c68ac93161796d913b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#create CfwAclRuleV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#delete CfwAclRuleV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_acl_rule_v1#update CfwAclRuleV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwAclRuleV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwAclRuleV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwAclRuleV1.CfwAclRuleV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9acd54fc193e431e2abc3f0a61fb9025239a0c5789d26b6e8adff17d2a9c1da4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c94c50c485e41bb7cf136ca0f1c0dd827a2c41232c8a3812ab97b439dbe9f76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e563873cdc8483bd26f1fea950797b4f48c415fae0debf3d6e3f9140e21201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab436c9f91d98afc7841da36aa594d6041fb7bf2cf1391a382385fe7956ec100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7b9eb93123f1ce4086cbf3b1bbd2a095212d67c5c1aa92ac58f2d32316dc84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CfwAclRuleV1",
    "CfwAclRuleV1Config",
    "CfwAclRuleV1Destination",
    "CfwAclRuleV1DestinationOutputReference",
    "CfwAclRuleV1DestinationRegionListStruct",
    "CfwAclRuleV1DestinationRegionListStructList",
    "CfwAclRuleV1DestinationRegionListStructOutputReference",
    "CfwAclRuleV1Sequence",
    "CfwAclRuleV1SequenceOutputReference",
    "CfwAclRuleV1Service",
    "CfwAclRuleV1ServiceCustomService",
    "CfwAclRuleV1ServiceCustomServiceList",
    "CfwAclRuleV1ServiceCustomServiceOutputReference",
    "CfwAclRuleV1ServiceOutputReference",
    "CfwAclRuleV1ServiceServiceGroupNames",
    "CfwAclRuleV1ServiceServiceGroupNamesList",
    "CfwAclRuleV1ServiceServiceGroupNamesOutputReference",
    "CfwAclRuleV1Source",
    "CfwAclRuleV1SourceOutputReference",
    "CfwAclRuleV1SourceRegionListStruct",
    "CfwAclRuleV1SourceRegionListStructList",
    "CfwAclRuleV1SourceRegionListStructOutputReference",
    "CfwAclRuleV1Timeouts",
    "CfwAclRuleV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e7455662b104acab54a488fc9b68bf91b7c280d598fb288c7b5b785fb7f31939(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    action_type: jsii.Number,
    address_type: jsii.Number,
    destination: typing.Union[CfwAclRuleV1Destination, typing.Dict[builtins.str, typing.Any]],
    long_connect_enable: jsii.Number,
    name: builtins.str,
    object_id: builtins.str,
    sequence: typing.Union[CfwAclRuleV1Sequence, typing.Dict[builtins.str, typing.Any]],
    service: typing.Union[CfwAclRuleV1Service, typing.Dict[builtins.str, typing.Any]],
    source: typing.Union[CfwAclRuleV1Source, typing.Dict[builtins.str, typing.Any]],
    status: jsii.Number,
    type: jsii.Number,
    applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    applications_json_string: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    direction: typing.Optional[jsii.Number] = None,
    long_connect_time: typing.Optional[jsii.Number] = None,
    long_connect_time_hour: typing.Optional[jsii.Number] = None,
    long_connect_time_minute: typing.Optional[jsii.Number] = None,
    long_connect_time_second: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CfwAclRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a1a872de92daab0f46cce615975e5eb5e9a57d4a7c7b23e81996635e0b20f463(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e795bd9a9b6147933a660ca1ad66fe6a111260cfd7b7d2b2f1b3c8a48e97f33(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2122230a80d238d589ab4adf6b05326924a80618711ebc50961bc7f34d2f70d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6332553f41793ea4d9bf34919dcae669ce71512598fb4cf48745e2c8180b7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811b8c5ddd4086a2aef9c81e905204fa458569ebea6df4b3f276b74eaa283d51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3619a00cf25ebba8dd4924c3e57ae10019df064008933efec761c9b38fa02fd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff1567a43ef45cb77102ee76112acf2271ae34be772416fb3954f627d847bfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e64a8bfb1957fc060ce63aee298335012f1eb43d663f490f0e450e9eb43ec99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e8ace50c439af3877848841746d9f70eb3441054cc1ed113eb6c652606326e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e94d92d8a6a7bbb00185bd94c02b424d3ee590fb1998ce3d77066cd6d091f75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1021e88774c97bc714d44d2b59006240b577f3991e3a1e8286f55953413de36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2003b9125569f61f21ba16191bea4099c68df095dea92ff7ee9746dc1aed5507(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87ffd084f05823237c3aa951867cc92c3d9f932f1f8b43d9d65520ed0dc9607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e43a6f95cc837c1a0d2f0c6253a278bcf8a41da3b8dfd4432b2752f8a2554e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e6e9be2c8082c8080b16798182d03d5cb9e0b87110adf3e0ac01f0e92ffa70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1da57b4206dbc492a166cb7e4a04a1daa040ebb5110f144ed5a45ff507fa336(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb91efdaf0795d2b0907a0f321fe0d5b1784ec536e2e7fdfb276288e9e877fb7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_type: jsii.Number,
    address_type: jsii.Number,
    destination: typing.Union[CfwAclRuleV1Destination, typing.Dict[builtins.str, typing.Any]],
    long_connect_enable: jsii.Number,
    name: builtins.str,
    object_id: builtins.str,
    sequence: typing.Union[CfwAclRuleV1Sequence, typing.Dict[builtins.str, typing.Any]],
    service: typing.Union[CfwAclRuleV1Service, typing.Dict[builtins.str, typing.Any]],
    source: typing.Union[CfwAclRuleV1Source, typing.Dict[builtins.str, typing.Any]],
    status: jsii.Number,
    type: jsii.Number,
    applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    applications_json_string: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    direction: typing.Optional[jsii.Number] = None,
    long_connect_time: typing.Optional[jsii.Number] = None,
    long_connect_time_hour: typing.Optional[jsii.Number] = None,
    long_connect_time_minute: typing.Optional[jsii.Number] = None,
    long_connect_time_second: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CfwAclRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f344338afb7232500637ff33ee441f6108bdb28c0424e4761c1dac83a34eba(
    *,
    type: jsii.Number,
    address: typing.Optional[builtins.str] = None,
    address_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    address_set_id: typing.Optional[builtins.str] = None,
    address_set_name: typing.Optional[builtins.str] = None,
    address_set_type: typing.Optional[jsii.Number] = None,
    address_type: typing.Optional[jsii.Number] = None,
    domain_address_name: typing.Optional[builtins.str] = None,
    domain_set_id: typing.Optional[builtins.str] = None,
    domain_set_name: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    region_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1DestinationRegionListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region_list_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d31a474e7773bfc97d5d002f33fd7190dd496d0ad64b8d729d54ef0c39ff96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae0079b151e9ebf155f2f9a98d3cb843da33621d80df51e5c2ed3466f7218e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1DestinationRegionListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec1fc8f24a77425f94fca1617624540d7281897dbe3072aee43b9e174191a24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5801756fe48f04629aad71e1124f6b162e3aea2d2589b14d9ad21297d9878c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8773b9c66d59764f6d647e76de94541dc0cfb70b5d30bd388d7fb377e48d2a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfe9bb6788baf644a818b90c562b2df4a11a2a49c3771035cdeac316a202098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced876fe316e9d2a0656f068bdae37d58d06a2010198f5990577484f5a89cd0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88405c7b7ccb71f42762ff8602781e62352433d2dab6d1f53f41d0ef730ce3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d07e609df55849bf9ff76aafd67c44e827c18b1b7b9369a7ee34ea6d56672e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc775623ead2796b0ce5e05157a108aac84c5e90838b350c2cfecec35297068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3153504eff05972b7375e1b99fe0b8fc40edc7cafce698fedb94fc8c54e96b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424354e36f7556a4ea3e89a45d1b0ad5d69ce3f7aaad64e2f362fda1ab3822d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c1e7f9225012bd6c6f26edc3205f2af344e9cddbaada93568f7dc819eb59e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6bc4ca2c0b73b0c309bf23e5e53dc9ee24daacae53db1264e9a16361b8f2c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c50dfbd12676da07bb9cd79ff387a0c18ae511b6d140a66863d4df5744546f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693cde54e06e5610941c7094946747db08bc1c511d5abdce7b27bd6d1a262bf6(
    value: typing.Optional[CfwAclRuleV1Destination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed3068714278f30f222b2263a6468b55ab33dc50f6e5ed4f4ead5325b629cb6(
    *,
    region_id: typing.Optional[builtins.str] = None,
    region_type: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c31d33a4c5ca543b6bbc88e862e9289c885e666f197aec7dd6fbc8d8224a29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18532fe01ba7fab1d7947527128e032fa7e7eca0c7ef364e543d488a55dfe34a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84abb1c7d778db5d9ff056e2931efd3ad911331ac2a5c06bf351855dd66f0234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5228192e6edbbce4d9c402163a5d0abe53e34178fb83994fbaf1f263682b3ed7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d51430e38d4dc33c783aa7f1bff043c5cfc222714823d075c33ef28aac3bd70(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29efc687ecbc0377ea9e1a05b2e367a572a332d47a2dfb94203198aa8c0dcf30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1DestinationRegionListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514e72f570340bbf629af3edabe8fbf45eed4bf1ba61ea5a733c6634676b1b2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb63bdde3e2afb0c2d4fd215f3b9fcfb9da99244705c66c6710f13963bf506d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b483b2399db095af02f053aa98dde80b9a122ce9ab486fd6670b1de055f63f79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cbdd52c3c60fcb0cf86ed64c06e1a32b964f37801f8ef8f117e9a424c9c5d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1DestinationRegionListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e58a26a095b71057718837a7c8a6156ddc5867e4cfae9c0cb30b79e9b30a795(
    *,
    bottom: typing.Optional[jsii.Number] = None,
    dest_rule_id: typing.Optional[builtins.str] = None,
    top: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79341aa09d528f842473b3a5b095dc5ff849f22499f797f1dba1ccdc8098e693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4297344fc1c5023248c299dc536031bdfc586240ddb1e2128ab171aac678819(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e1009e0dd4d7079f7c4fb7d38a9310f0251d1caf98e9b86d7be694fb1b333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fcdac6bf2ac6b81b03cc346d8e69db04b3605d2f2be55f15865eeb66db6c69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc22deeeffdb5deb072610079c74a6108eca933d1f3921121fc6cb889d3cf11(
    value: typing.Optional[CfwAclRuleV1Sequence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced2d83007200504a651675014643d87064a033d128db0c7a1d75d91edab0b9b(
    *,
    type: jsii.Number,
    custom_service: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1ServiceCustomService, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dest_port: typing.Optional[builtins.str] = None,
    predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol: typing.Optional[jsii.Number] = None,
    protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
    service_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_group_names: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1ServiceServiceGroupNames, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_set_id: typing.Optional[builtins.str] = None,
    service_set_name: typing.Optional[builtins.str] = None,
    service_set_type: typing.Optional[jsii.Number] = None,
    source_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51face4c318ad2514eb30c26ac280e4bcd9489ebe27c9882371a267c424ce857(
    *,
    description: typing.Optional[builtins.str] = None,
    dest_port: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[jsii.Number] = None,
    source_port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cac2a31b58b94eab71637b7159761c1e20037a69cc8d4a0dad6829d7a97a58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f795262365552cb8be3f633bbdbc5392c49250a5d92241a466564821c767c30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cb0205f85110a73db4c2550b7418cbac19da41fb4eedaa8b0820d1317de623(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4da40e988b8757990eeebe7e4707fd32337cb246021fe9a293fbcf768074ce8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6200abda10629c1d76fbf027d3cc10ab1da293a1f9c42c92d47e3682069c0ce3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2d1dd9a8c2b00920369f2a662adfe7fe1ce8db1542d3902b52c0f424fda6c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceCustomService]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769796d8e7ea2d9a238da6bb2f9c921e8b6faa63717c03efdc6f03f93ba9e2d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb3bfdd00fc2cf9adbf52b8e29919982100bcc70e340b82ff50f93c7179b2c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f58f37fb590105436533da0ab119e303265cc033b4f2cfbeac224a8fd30d817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ff6afed09a1f11f63f161c9caddfca72b0d9a6661f7d18e09629a263b337a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1adf2929e477b9fd25e8f12dbc1bee47e288194b9f8c2564d13ff7c5d7b4f648(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524a72e1c210675eb0e0136f8f112b314b137d7e7afbe3495fa892aadd634734(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a5520746313fe7c07bf01f270a267f71a2847e9259a8ac48e25b309d579434(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceCustomService]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b65495273dba720b0588bb9789639db436a52593c6aa864854ed0cb06e6575a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0507ee01bd67d3e6691fdc151997907556bde686f6ebae9e8e5eff40f15d02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1ServiceCustomService, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58884c685f321007614e0378c59db3d1048dc38b9e2002b1de2ff85f3dd9021(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1ServiceServiceGroupNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e575e2b675ccf54dbb310ee2dd7e610425033e16cf1073cb8f0f6f2074c6b6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557015768b127dc6239ac42ab5bd8db57fd0c8d066bce7a4b2a40233d1bea24a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899b877df5f4e21fabbf196bd33a235cc931908ac321b54c9086993e9b87c11f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65aecc27335b86a9cd04a92a6d7c1ead5ec470b6b9518561a27f97f129b29dc5(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73acf07d76c84081eb17eba6d35e8cba071dda24cc4aaf96dd20682e139c1298(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e24e10b5c90c85e9f61cddbb595340e59d086e94da3ed2d894d146aabfec44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292a38983643c78191dbed87f8841cad25b133c9873665e8e313254fe37f227e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c6282aab229599dd05858efb8a8c42969b5d93ce09e2d67dedef8f4a51afd4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56839f7a3babc152cdd4175d69d2a7e4f2233e7484d741e86337e105852dddf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee10ab2b3eeddb5cf43351d5c764aa042efcd0670ddb9fedf201fb6e56d6b0af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6a6fbacacf5f85f6557236c22782cd778ee2eaa0dff1205734f27d701197fc(
    value: typing.Optional[CfwAclRuleV1Service],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458f1ac96ca3422467162a548ec790c57068c498a3d3575eb347737001c94b34(
    *,
    name: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[jsii.Number]] = None,
    service_set_type: typing.Optional[jsii.Number] = None,
    set_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e39cd3e3d98b0f0bf2bbfb11498671c838f6fddcb21b00717e43d34d0709b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae11d7d98206e8ced10091d609d0f94b068108e2d51548ac8053750868da06d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37bdd4f37af6de6ca9169ffd33555a9b5e5a6e5d19f38003c80948cac89990d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e206cb0f69c538378c2b813d320a0b62859990b894128f1e92819ddaaac05c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a452f345540285bc7d13c5f20346d18c8be57d09773bb03f1f28ade9303d83d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee67f3beb394206f3b08df1acc6bb6ac884f6037a2d0fe5e97c5e769ccc0e9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1ServiceServiceGroupNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b18b901ec23a1aadd1bb96a7e5ce224eaf4b39e3cee14f05196861110cc24a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578b7c143132e05892834169909e86636032f89657615b4772845b5f36b2c964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175fdbfb18704577cc8504fefa7afd02cfdbe5559907e4b00f89537a075d36d4(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358bba1bfc8ecd97f74ae7b9b761c9926f89cfd53d8b50ffcd3103c038b26980(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9e813d3749d41923c18cf30a922e7fd8280bea50fa67531826c7edf2c79b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d89f904c99027f4b75d8647ebd17d1639e948895c4ce750c589e99400c12ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1ServiceServiceGroupNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a4ca0c50230c0bf320bfeb974b898effe165b272aaa4506cfc070f63633d50(
    *,
    type: jsii.Number,
    address: typing.Optional[builtins.str] = None,
    address_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    address_set_id: typing.Optional[builtins.str] = None,
    address_set_name: typing.Optional[builtins.str] = None,
    address_set_type: typing.Optional[jsii.Number] = None,
    address_type: typing.Optional[jsii.Number] = None,
    domain_address_name: typing.Optional[builtins.str] = None,
    domain_set_id: typing.Optional[builtins.str] = None,
    domain_set_name: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    predefined_group: typing.Optional[typing.Sequence[builtins.str]] = None,
    region_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1SourceRegionListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region_list_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d53d6eb5a32343475aa8592eb53322605df902a4aa18826c3022e8de4d6fa42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991a60d937b385d8704406aacab78c5f4da877f8b252f7a478940c5f4b4b293b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CfwAclRuleV1SourceRegionListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660ca77535ca1e4c95ec1f9053c61f3fb72d5d1c88a8eb95ba2f127b939ba28e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57dcf0e36b591f3e1a4c5d491e09ce7d9a16a01305763c710c1e6e9cd32138fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281cdeaf25b0b9a77ff6d98b29ee8270bb3267662837708e55bab599a48260d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec765a48574faafca48ba27b0aabab93ef8aea7b6367f83a95e933198ae772cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b25f48b71a37b9cf7281ae4234cf721f5eb43c68b501b2c62499aaa194c39e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3d35aff6330b3618b349f23242218f1e39f49bb7295654d272815fa182ea5b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6633236675ab02e4071a4e42051c30ad1c0d6c2007f6c44c2a3ec06dbb87c4d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7980c449d623de755a5db9ddaca071c343d31cca5ea0805451695af0fbe5570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daee2c0126895d22d3d7225a8a56532d4aaa83bdf4ad3d8bf89a8dc98645978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f033c81621f000f65fca409465aa0fcc5d1ab3202d57ed1b113ba1814137cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cc6bc42f62d53d5bab2fda543f3b23981b5305f61a30ff9720def1f0c48c02(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd4be9af6f7073f5a5dd72b96b9a17ef1e59ced1299fe93c27645897c62d7e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf8466eb2997f924d19456e4572aa1d93746950d208abf2a95e50dc25b0bc23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197992054c60b0b7bcfc66170dc0aa4f32317ced0beb18979fb5a98d0d0fefab(
    value: typing.Optional[CfwAclRuleV1Source],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253b89e8260b6091f50f27c4705e0c9b894ad20e2f20f6e551afefa062076bc8(
    *,
    region_id: typing.Optional[builtins.str] = None,
    region_type: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1846f53e02c603a4329831274cf60ce29d952a1172e4f0d524264b7153a1686c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc159d947c056ee74a2ed48e319ea33c2e10beb55553ff038729116f0e04d87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb109b3a4bf68349750a63ffc128018cd1b2d4c95a55fc1cd96b711a58044b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87e5a584fc62ad7211d6dbf076e54deb5c4618e6bf3c47fb2718fd0f93fcfd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b3177d16cb1be9a2d1ace25b1d5f8544fc4fac3026e81e33b2afeab5ae3211(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356bd5ee42e2f1e6db7d112076d91ba781a2abae4051c4922a3a6671dee5562b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CfwAclRuleV1SourceRegionListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab523b7cc2eac056355e6d4bcd6666024b222a29b781c9251d4d55eba3c4cf21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515b88b27193c0ea37e8e843ccc920e85c1ca0165d3669ba91a80f4fde6a3089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdb19e6284cfa696398ca4c33ddea7d4eda19404d46399297210037cd1d12b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbc295118ab4b19869c755459654a5e5a8b9b074ae653571fdabdfdeb187086(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1SourceRegionListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eaedd6f7879f8d1466160a832ac132d41635953700f27c68ac93161796d913b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acd54fc193e431e2abc3f0a61fb9025239a0c5789d26b6e8adff17d2a9c1da4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94c50c485e41bb7cf136ca0f1c0dd827a2c41232c8a3812ab97b439dbe9f76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e563873cdc8483bd26f1fea950797b4f48c415fae0debf3d6e3f9140e21201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab436c9f91d98afc7841da36aa594d6041fb7bf2cf1391a382385fe7956ec100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7b9eb93123f1ce4086cbf3b1bbd2a095212d67c5c1aa92ac58f2d32316dc84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwAclRuleV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
