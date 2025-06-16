r'''
# `google_dns_record_set`

Refer to the Terraform Registry for docs: [`google_dns_record_set`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set).
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


class GoogleDnsRecordSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set google_dns_record_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        managed_zone: builtins.str,
        name: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        routing_policy: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
        ttl: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set google_dns_record_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param managed_zone: The name of the zone in which this record set will reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#managed_zone GoogleDnsRecordSet#managed_zone}
        :param name: The DNS name this record set will apply to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#name GoogleDnsRecordSet#name}
        :param type: The DNS record set type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#type GoogleDnsRecordSet#type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#id GoogleDnsRecordSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        :param routing_policy: routing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#routing_policy GoogleDnsRecordSet#routing_policy}
        :param rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}
        :param ttl: The time-to-live of this record set (seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ttl GoogleDnsRecordSet#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d768d15018537ceede9e2d941aa12f4d9f41fb150c001f4aa1f998d4856048)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDnsRecordSetConfig(
            managed_zone=managed_zone,
            name=name,
            type=type,
            id=id,
            project=project,
            routing_policy=routing_policy,
            rrdatas=rrdatas,
            ttl=ttl,
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
        '''Generates CDKTF code for importing a GoogleDnsRecordSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDnsRecordSet to import.
        :param import_from_id: The id of the existing GoogleDnsRecordSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDnsRecordSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2740c90b6e5a5d8739db37e4f73efe5ddaf4e20c784bdefdf87905ab2950669)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRoutingPolicy")
    def put_routing_policy(
        self,
        *,
        enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        geo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyGeo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_check: typing.Optional[builtins.str] = None,
        primary_backup: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        wrr: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyWrr", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable_geo_fencing: Specifies whether to enable fencing for geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#enable_geo_fencing GoogleDnsRecordSet#enable_geo_fencing}
        :param geo: geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#geo GoogleDnsRecordSet#geo}
        :param health_check: Specifies the health check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_check GoogleDnsRecordSet#health_check}
        :param primary_backup: primary_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#primary_backup GoogleDnsRecordSet#primary_backup}
        :param wrr: wrr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#wrr GoogleDnsRecordSet#wrr}
        '''
        value = GoogleDnsRecordSetRoutingPolicy(
            enable_geo_fencing=enable_geo_fencing,
            geo=geo,
            health_check=health_check,
            primary_backup=primary_backup,
            wrr=wrr,
        )

        return typing.cast(None, jsii.invoke(self, "putRoutingPolicy", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRoutingPolicy")
    def reset_routing_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingPolicy", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

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
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "GoogleDnsRecordSetRoutingPolicyOutputReference":
        return typing.cast("GoogleDnsRecordSetRoutingPolicyOutputReference", jsii.get(self, "routingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managedZoneInput")
    def managed_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="routingPolicyInput")
    def routing_policy_input(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicy"]:
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicy"], jsii.get(self, "routingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddd7440ba541a74eca2f383295b8be3cb2f1f8b0ab446c924118fded2c5c9e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedZone")
    def managed_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedZone"))

    @managed_zone.setter
    def managed_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e64b2c623b10db694811811ff7b93f6b5fc17acba90d03448d058984bf1c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a12d8901b95fd2585e77be8fa7d48eb31c77c321c4ba7f2cab4a7b2595ef517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cad695f34ddb591ed3b1f0ae0f8c69495535d25e6724f9065ace665727f2190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d1ddda375c27b52c6563eeb42e1a036dde5e00ddf72d7b2eb23b2b4669be2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35349c09d0504c829cdda67f0dbef8cc1829ecaf1ef1e1e5b909cf2c53bc42e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e4ce1c5a733a2345119b36450135ac0e7d190bea98d3fd9eee321b4b84cd94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "managed_zone": "managedZone",
        "name": "name",
        "type": "type",
        "id": "id",
        "project": "project",
        "routing_policy": "routingPolicy",
        "rrdatas": "rrdatas",
        "ttl": "ttl",
    },
)
class GoogleDnsRecordSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        managed_zone: builtins.str,
        name: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        routing_policy: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param managed_zone: The name of the zone in which this record set will reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#managed_zone GoogleDnsRecordSet#managed_zone}
        :param name: The DNS name this record set will apply to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#name GoogleDnsRecordSet#name}
        :param type: The DNS record set type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#type GoogleDnsRecordSet#type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#id GoogleDnsRecordSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        :param routing_policy: routing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#routing_policy GoogleDnsRecordSet#routing_policy}
        :param rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}
        :param ttl: The time-to-live of this record set (seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ttl GoogleDnsRecordSet#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing_policy, dict):
            routing_policy = GoogleDnsRecordSetRoutingPolicy(**routing_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2b27506331dd8f5f50d09549265cd6e4fb1e700ea977bff39c317a157060e2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument managed_zone", value=managed_zone, expected_type=type_hints["managed_zone"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "managed_zone": managed_zone,
            "name": name,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if routing_policy is not None:
            self._values["routing_policy"] = routing_policy
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas
        if ttl is not None:
            self._values["ttl"] = ttl

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
    def managed_zone(self) -> builtins.str:
        '''The name of the zone in which this record set will reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#managed_zone GoogleDnsRecordSet#managed_zone}
        '''
        result = self._values.get("managed_zone")
        assert result is not None, "Required property 'managed_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The DNS name this record set will apply to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#name GoogleDnsRecordSet#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The DNS record set type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#type GoogleDnsRecordSet#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#id GoogleDnsRecordSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_policy(self) -> typing.Optional["GoogleDnsRecordSetRoutingPolicy"]:
        '''routing_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#routing_policy GoogleDnsRecordSet#routing_policy}
        '''
        result = self._values.get("routing_policy")
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicy"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The string data for the records in this record set whose meaning depends on the DNS type.

        For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}
        '''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The time-to-live of this record set (seconds).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ttl GoogleDnsRecordSet#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "enable_geo_fencing": "enableGeoFencing",
        "geo": "geo",
        "health_check": "healthCheck",
        "primary_backup": "primaryBackup",
        "wrr": "wrr",
    },
)
class GoogleDnsRecordSetRoutingPolicy:
    def __init__(
        self,
        *,
        enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        geo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyGeo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_check: typing.Optional[builtins.str] = None,
        primary_backup: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        wrr: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyWrr", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable_geo_fencing: Specifies whether to enable fencing for geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#enable_geo_fencing GoogleDnsRecordSet#enable_geo_fencing}
        :param geo: geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#geo GoogleDnsRecordSet#geo}
        :param health_check: Specifies the health check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_check GoogleDnsRecordSet#health_check}
        :param primary_backup: primary_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#primary_backup GoogleDnsRecordSet#primary_backup}
        :param wrr: wrr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#wrr GoogleDnsRecordSet#wrr}
        '''
        if isinstance(primary_backup, dict):
            primary_backup = GoogleDnsRecordSetRoutingPolicyPrimaryBackup(**primary_backup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f137acf7257bef1cf64bacd80e862ced61ea17b4072dbcd06cc964f0287601b9)
            check_type(argname="argument enable_geo_fencing", value=enable_geo_fencing, expected_type=type_hints["enable_geo_fencing"])
            check_type(argname="argument geo", value=geo, expected_type=type_hints["geo"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument primary_backup", value=primary_backup, expected_type=type_hints["primary_backup"])
            check_type(argname="argument wrr", value=wrr, expected_type=type_hints["wrr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_geo_fencing is not None:
            self._values["enable_geo_fencing"] = enable_geo_fencing
        if geo is not None:
            self._values["geo"] = geo
        if health_check is not None:
            self._values["health_check"] = health_check
        if primary_backup is not None:
            self._values["primary_backup"] = primary_backup
        if wrr is not None:
            self._values["wrr"] = wrr

    @builtins.property
    def enable_geo_fencing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable fencing for geo queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#enable_geo_fencing GoogleDnsRecordSet#enable_geo_fencing}
        '''
        result = self._values.get("enable_geo_fencing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def geo(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyGeo"]]]:
        '''geo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#geo GoogleDnsRecordSet#geo}
        '''
        result = self._values.get("geo")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyGeo"]]], result)

    @builtins.property
    def health_check(self) -> typing.Optional[builtins.str]:
        '''Specifies the health check.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_check GoogleDnsRecordSet#health_check}
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_backup(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackup"]:
        '''primary_backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#primary_backup GoogleDnsRecordSet#primary_backup}
        '''
        result = self._values.get("primary_backup")
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackup"], result)

    @builtins.property
    def wrr(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyWrr"]]]:
        '''wrr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#wrr GoogleDnsRecordSet#wrr}
        '''
        result = self._values.get("wrr")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyWrr"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeo",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class GoogleDnsRecordSetRoutingPolicyGeo:
    def __init__(
        self,
        *,
        location: builtins.str,
        health_checked_targets: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: The location name defined in Google Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#location GoogleDnsRecordSet#location}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_checked_targets GoogleDnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ca662e7fcbaa508b76472632d37c1b884655786731d3e3ca8da1c32db5acb5)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument health_checked_targets", value=health_checked_targets, expected_type=type_hints["health_checked_targets"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if health_checked_targets is not None:
            self._values["health_checked_targets"] = health_checked_targets
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas

    @builtins.property
    def location(self) -> builtins.str:
        '''The location name defined in Google Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#location GoogleDnsRecordSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_checked_targets GoogleDnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyGeo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230c6d65c222b850aeab24644dd96cb40a56cecd8d222ae589c3f7be68a9fa45)
            check_type(argname="argument external_endpoints", value=external_endpoints, expected_type=type_hints["external_endpoints"])
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_endpoints is not None:
            self._values["external_endpoints"] = external_endpoints
        if internal_load_balancers is not None:
            self._values["internal_load_balancers"] = internal_load_balancers

    @builtins.property
    def external_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Internet IP addresses to be health checked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "load_balancer_type": "loadBalancerType",
        "region": "region",
    },
)
class GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        load_balancer_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0469b84094a38d7787e483be6e9c9e5c9d63774cadbc15652b1549e677b74662)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if load_balancer_type is not None:
            self._values["load_balancer_type"] = load_balancer_type
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3894b89e3247a1117f11084f23dc190cf545a09a636f9c225c96a5ad1f174ed7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ae14f43a73f4902041f1a9c3f6f7b826dbe445f00497f55c7f545430e7e971)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903e7652ac09717b8d022432a25f2928fcf7709572b491887fe945d259f686be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__990f192b8f81fd02c4d76b88cc4b849a922f2520266c21f0cf244d2b7b4c12ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d70c2f7c134e06dc2e63568e6e4f18fa5a9ae770074cb39a19d8b49c118fb02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fed351f261882c795c9a4a06410af17e42df3598a4682770d017dde417794d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b87f62dac8a0cedc1b79213e8b9e95886e6835afef90435e2691be3f22b584ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLoadBalancerType")
    def reset_load_balancer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367255f4fd93aeda1758882df77705e37cf5d3f483444053d31cfd18e699604c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b809b3c945c1df229367a78e6d9952042d72f599397a0f505a749a71979ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec096c50399532ea13ff8e9521fdae7bdd02df6159de1ff26d04e0b828c81ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae3017dab724f8895ff1d355b790d4997deee36712488a4750a153aa079eaa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155c6b1a93e3e503532bb84ad6bad0f296c279c8e07010e1f426c43833722898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e96cb81e36245bfbfd9a313930a2e0a64068c84b9a884370524cc9e3bff11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0ebcfde3c36babcc194a9a9d9ff689caf55f98d6f464cd53e0996a8c4de463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9621e825afd5b6ae1b2801f42e3e997333493bbee24d2467a8e3734685eeb187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48c093cef366dc9023c4d45fcd8e9cb49701e12899cedfb0f7698b4fcf9d038)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7ad3cb5b2888cee075a165ade85e22686e2cbf1eb1dbb2d2ee8431584f785c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @jsii.member(jsii_name="resetExternalEndpoints")
    def reset_external_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEndpoints", []))

    @jsii.member(jsii_name="resetInternalLoadBalancers")
    def reset_internal_load_balancers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalLoadBalancers", []))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a7991acdde33090ac806e7d14fa1cd1795cc3658d48daa6946a6d3b77cae0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d74b4d4fb4da7483fdb92646f439bd4f63d12563bf355f275ca640b46721fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyGeoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0933eb8153fd28b20d21530767b9c87748cd460ff9495f87311d2b4c6c20f089)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyGeoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7ea743dcd1732d85728d01d4b4f3bb3e13c04b73bb0b03f358d359b5bcb6b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyGeoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcaa6cc9fb9dae5da20d57ead4b1011964f6ccbfe6019dcd1de30837c282eb56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47ab710a6c4e9eca8a53b6aa28d341fe38048749de3c0ff87933ac51a9998094)
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
            type_hints = typing.get_type_hints(_typecheckingstub__503c7c85f3b2bc341e858a9eb0094b4d5ea34650ffc9628456a2041985c6d13b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3947f41d64c18652ef2588986329ad8ce2d7fed14c548884656e82c428025606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyGeoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyGeoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e83650efaed6593671cbb793c8da71e957aa30d1fb4334ddf74e3bc7047bcb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHealthCheckedTargets")
    def put_health_checked_targets(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        value = GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets(
            external_endpoints=external_endpoints,
            internal_load_balancers=internal_load_balancers,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckedTargets", [value]))

    @jsii.member(jsii_name="resetHealthCheckedTargets")
    def reset_health_checked_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckedTargets", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargets")
    def health_checked_targets(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8802e11f8d7be90a5f06eb2bdf515f3e54db7d9c25eeb9cdfd1b7b5d80fc85b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f023b696b08e48c562c8632a36d835edd86d77aee42fc90f5a64615d01d175e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3ca16d0c246edf5fa62d27718f5ac58fc4dba2f6f6aff2fe0e4b8ea1f8c5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b3ab74eb2a204fe4b9a79a0779a94d5a17978542a5cee9be9851a59cdd329bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGeo")
    def put_geo(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec29098ebb9367d4f72e611f823a2dbc33fe16773b9af097542ded5bf2bd62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeo", [value]))

    @jsii.member(jsii_name="putPrimaryBackup")
    def put_primary_backup(
        self,
        *,
        backup_geo: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo", typing.Dict[builtins.str, typing.Any]]]],
        primary: typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary", typing.Dict[builtins.str, typing.Any]],
        enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trickle_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_geo: backup_geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#backup_geo GoogleDnsRecordSet#backup_geo}
        :param primary: primary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#primary GoogleDnsRecordSet#primary}
        :param enable_geo_fencing_for_backups: Specifies whether to enable fencing for backup geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#enable_geo_fencing_for_backups GoogleDnsRecordSet#enable_geo_fencing_for_backups}
        :param trickle_ratio: Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#trickle_ratio GoogleDnsRecordSet#trickle_ratio}
        '''
        value = GoogleDnsRecordSetRoutingPolicyPrimaryBackup(
            backup_geo=backup_geo,
            primary=primary,
            enable_geo_fencing_for_backups=enable_geo_fencing_for_backups,
            trickle_ratio=trickle_ratio,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryBackup", [value]))

    @jsii.member(jsii_name="putWrr")
    def put_wrr(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyWrr", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb7c5a0016bf9e67f50776c0c932dff57336a07164cb69107e5cc2f50f7bac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWrr", [value]))

    @jsii.member(jsii_name="resetEnableGeoFencing")
    def reset_enable_geo_fencing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGeoFencing", []))

    @jsii.member(jsii_name="resetGeo")
    def reset_geo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeo", []))

    @jsii.member(jsii_name="resetHealthCheck")
    def reset_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheck", []))

    @jsii.member(jsii_name="resetPrimaryBackup")
    def reset_primary_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryBackup", []))

    @jsii.member(jsii_name="resetWrr")
    def reset_wrr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWrr", []))

    @builtins.property
    @jsii.member(jsii_name="geo")
    def geo(self) -> GoogleDnsRecordSetRoutingPolicyGeoList:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyGeoList, jsii.get(self, "geo"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackup")
    def primary_backup(
        self,
    ) -> "GoogleDnsRecordSetRoutingPolicyPrimaryBackupOutputReference":
        return typing.cast("GoogleDnsRecordSetRoutingPolicyPrimaryBackupOutputReference", jsii.get(self, "primaryBackup"))

    @builtins.property
    @jsii.member(jsii_name="wrr")
    def wrr(self) -> "GoogleDnsRecordSetRoutingPolicyWrrList":
        return typing.cast("GoogleDnsRecordSetRoutingPolicyWrrList", jsii.get(self, "wrr"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencingInput")
    def enable_geo_fencing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableGeoFencingInput"))

    @builtins.property
    @jsii.member(jsii_name="geoInput")
    def geo_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeo]]], jsii.get(self, "geoInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckInput")
    def health_check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackupInput")
    def primary_backup_input(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackup"]:
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackup"], jsii.get(self, "primaryBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="wrrInput")
    def wrr_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyWrr"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyWrr"]]], jsii.get(self, "wrrInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencing")
    def enable_geo_fencing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableGeoFencing"))

    @enable_geo_fencing.setter
    def enable_geo_fencing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebf317fa6005b1691395b0d1b6b18654763a9c336855bee7e4d2e2028390d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGeoFencing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheck"))

    @health_check.setter
    def health_check(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fef4a1007e0baa07176c57e70e07a07567a76c2ac7287be3d9fe5046d7787d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDnsRecordSetRoutingPolicy]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsRecordSetRoutingPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730870648af74c19a285755223cff90f5b657cc677e956834ab2467b66b23801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackup",
    jsii_struct_bases=[],
    name_mapping={
        "backup_geo": "backupGeo",
        "primary": "primary",
        "enable_geo_fencing_for_backups": "enableGeoFencingForBackups",
        "trickle_ratio": "trickleRatio",
    },
)
class GoogleDnsRecordSetRoutingPolicyPrimaryBackup:
    def __init__(
        self,
        *,
        backup_geo: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo", typing.Dict[builtins.str, typing.Any]]]],
        primary: typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary", typing.Dict[builtins.str, typing.Any]],
        enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trickle_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_geo: backup_geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#backup_geo GoogleDnsRecordSet#backup_geo}
        :param primary: primary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#primary GoogleDnsRecordSet#primary}
        :param enable_geo_fencing_for_backups: Specifies whether to enable fencing for backup geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#enable_geo_fencing_for_backups GoogleDnsRecordSet#enable_geo_fencing_for_backups}
        :param trickle_ratio: Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#trickle_ratio GoogleDnsRecordSet#trickle_ratio}
        '''
        if isinstance(primary, dict):
            primary = GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary(**primary)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c19b95669d93a623f2f52f3cf49f53d2b79ef95dd2a39d9fa9fbcfda6ec650)
            check_type(argname="argument backup_geo", value=backup_geo, expected_type=type_hints["backup_geo"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument enable_geo_fencing_for_backups", value=enable_geo_fencing_for_backups, expected_type=type_hints["enable_geo_fencing_for_backups"])
            check_type(argname="argument trickle_ratio", value=trickle_ratio, expected_type=type_hints["trickle_ratio"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_geo": backup_geo,
            "primary": primary,
        }
        if enable_geo_fencing_for_backups is not None:
            self._values["enable_geo_fencing_for_backups"] = enable_geo_fencing_for_backups
        if trickle_ratio is not None:
            self._values["trickle_ratio"] = trickle_ratio

    @builtins.property
    def backup_geo(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo"]]:
        '''backup_geo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#backup_geo GoogleDnsRecordSet#backup_geo}
        '''
        result = self._values.get("backup_geo")
        assert result is not None, "Required property 'backup_geo' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo"]], result)

    @builtins.property
    def primary(self) -> "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary":
        '''primary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#primary GoogleDnsRecordSet#primary}
        '''
        result = self._values.get("primary")
        assert result is not None, "Required property 'primary' is missing"
        return typing.cast("GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary", result)

    @builtins.property
    def enable_geo_fencing_for_backups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable fencing for backup geo queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#enable_geo_fencing_for_backups GoogleDnsRecordSet#enable_geo_fencing_for_backups}
        '''
        result = self._values.get("enable_geo_fencing_for_backups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trickle_ratio(self) -> typing.Optional[jsii.Number]:
        '''Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#trickle_ratio GoogleDnsRecordSet#trickle_ratio}
        '''
        result = self._values.get("trickle_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyPrimaryBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo:
    def __init__(
        self,
        *,
        location: builtins.str,
        health_checked_targets: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: The location name defined in Google Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#location GoogleDnsRecordSet#location}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_checked_targets GoogleDnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242b28bf01338ac2a20bedfe720df5dea5f701cfdf10ef10ca28a9859c483080)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument health_checked_targets", value=health_checked_targets, expected_type=type_hints["health_checked_targets"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if health_checked_targets is not None:
            self._values["health_checked_targets"] = health_checked_targets
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas

    @builtins.property
    def location(self) -> builtins.str:
        '''The location name defined in Google Cloud.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#location GoogleDnsRecordSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_checked_targets GoogleDnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93edbf7547c8be6baa4a3a3dd3cff798681900f004e08bc06b7e1af3a389d63)
            check_type(argname="argument external_endpoints", value=external_endpoints, expected_type=type_hints["external_endpoints"])
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_endpoints is not None:
            self._values["external_endpoints"] = external_endpoints
        if internal_load_balancers is not None:
            self._values["internal_load_balancers"] = internal_load_balancers

    @builtins.property
    def external_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Internet IP addresses to be health checked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "load_balancer_type": "loadBalancerType",
        "region": "region",
    },
)
class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        load_balancer_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b6841702de5627cb89f098ddb7a6b12f59484f27428a18b8916f63604cbddc)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if load_balancer_type is not None:
            self._values["load_balancer_type"] = load_balancer_type
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5980123b1cf626b0be6e0c998b7b2c92c2fd96dd32f1cefd19af34587903a0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d698ed584c143341f73b34ffd70bd3a6741d8df00ccda33c3e7e8c64d2d0fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956fe616a178670421e6bd53290219b38ec1532392c322e9a313ef3b2fbdeec6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52df072edba8a89022d2302e007fdd7c4c18db321207fb647fbf817514786931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc9686c71a25abe0fb830dbaff0bfd4dd03ca1dc5b57c6318812a60aab30c4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b793ead816d41cf9b5e06b63054a57cd13a209bd07fa0858d8b68f7f8e2d0c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__493d6c365b2f4415b3888da6c5e63ad5eea4818bb002d6283bdc41fc46fd6c67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLoadBalancerType")
    def reset_load_balancer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44643df0e0ea1d6788925ecc6c4b73efe5ceb0b01d297ce89f64f9b592a75a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208672187ab86ff68604cd3c2f6f373cbfb00b7fb471837fcee189eb165ab59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063225929e9828073142cf8f764fb28af19af151647b4f3b4f165f13e719b4c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da8f2a2212730ccb3812a2f5d44dc6b69dc1630f22c40b5f87093541e1aebd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546903e66f1df05787d69fbe2ed6b8d9da095972867928c78e9feb1dc2f9fe1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3832e4fb564578bb92442de7a433fc290f356d81a8b60cc266f2e5992fcc132f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026bce62fafc66d5c7f235baa49f8ecf3508f71d667d526d3484a5671e4808bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9f1f338721fc4aae1cb6d02a2a126ad6265ac14463466cb13ce3249a9dfc89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6b7b67578bb3cc96ac6b466136affd4be339d337f1d3ed04dec13fcdaed387f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a58852418280da718ef7fce2d0d4441bd9049ce82282e109e3130e53bffa0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @jsii.member(jsii_name="resetExternalEndpoints")
    def reset_external_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEndpoints", []))

    @jsii.member(jsii_name="resetInternalLoadBalancers")
    def reset_internal_load_balancers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalLoadBalancers", []))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a23310cd1fe97519c1e2068fcc884d559409d46ef0a6644764a4a8dd3487e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c461080dc6f75a15511ce68c5b14565c53bcae314b562987cb9dd1258e88ab88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddb83cf67699417299c765d905a79ce6c197876d773af8e915978add4cd0d6e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37c7a3ea96b42bdc1612dcf0a7a7e2f302ab84296cae5b0228e93280c615769)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7849355ac238c9075ccee6dc65cd56eed67b6292c54515629493ec462a0f582e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6522f8f07669a54ba7e7cae5ea6f9c4f6fc2f636d12f690674094a5c47cbb593)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f057cb710e3c45c1b3c41ed5b85e733248f0a1dfc466faadc4b86353a0a545c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb00c697fca0b70f963c07c501ac6eb8081d231e4bb3107d8344e1562d16342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddd763b9492c1602e3d46a6ff4f0c069f21f61baeaa4ebda5ae2d5b937f73f01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHealthCheckedTargets")
    def put_health_checked_targets(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        value = GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(
            external_endpoints=external_endpoints,
            internal_load_balancers=internal_load_balancers,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckedTargets", [value]))

    @jsii.member(jsii_name="resetHealthCheckedTargets")
    def reset_health_checked_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckedTargets", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargets")
    def health_checked_targets(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81ea8c3fd89bee847abd8874f080d61606c90b62a3a72734deb071c6697ca2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8881f932445e147745c8438c83cfe8ce51b64b2edc2584e7c47e30b791bca627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99b5160f7937a6101c56a2bab4aee8088a0394c29ba5969502cd88ba0572046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b499785d8b2685e86d14f1e0d22caa65aaa707bbd0a71ce732f531d3d688b98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBackupGeo")
    def put_backup_geo(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b722ecb5bb8f29c878dde1afc140edb8ac0c7f1d017e31810712871aacdcd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackupGeo", [value]))

    @jsii.member(jsii_name="putPrimary")
    def put_primary(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        value = GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary(
            external_endpoints=external_endpoints,
            internal_load_balancers=internal_load_balancers,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimary", [value]))

    @jsii.member(jsii_name="resetEnableGeoFencingForBackups")
    def reset_enable_geo_fencing_for_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGeoFencingForBackups", []))

    @jsii.member(jsii_name="resetTrickleRatio")
    def reset_trickle_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrickleRatio", []))

    @builtins.property
    @jsii.member(jsii_name="backupGeo")
    def backup_geo(self) -> GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList, jsii.get(self, "backupGeo"))

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(
        self,
    ) -> "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference":
        return typing.cast("GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference", jsii.get(self, "primary"))

    @builtins.property
    @jsii.member(jsii_name="backupGeoInput")
    def backup_geo_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]], jsii.get(self, "backupGeoInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencingForBackupsInput")
    def enable_geo_fencing_for_backups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableGeoFencingForBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInput")
    def primary_input(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary"]:
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary"], jsii.get(self, "primaryInput"))

    @builtins.property
    @jsii.member(jsii_name="trickleRatioInput")
    def trickle_ratio_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "trickleRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGeoFencingForBackups")
    def enable_geo_fencing_for_backups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableGeoFencingForBackups"))

    @enable_geo_fencing_for_backups.setter
    def enable_geo_fencing_for_backups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0027d683fdc7465ec23bd9efac7fb2e65dc6109e5cba1230d8c48b8f49b5d4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGeoFencingForBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trickleRatio")
    def trickle_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "trickleRatio"))

    @trickle_ratio.setter
    def trickle_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878e7feac86ef514c90a64f41f31fb8f8fa9463e8a3e0bac8ca8070fe72861ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trickleRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackup]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686e468c905631908f2a945c3d649127ad3512f0942f975c3b4384acb827a608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f6be770b5dbc411785f7e26e61336268bb55b90f2490d562b53ccd62f50aeb)
            check_type(argname="argument external_endpoints", value=external_endpoints, expected_type=type_hints["external_endpoints"])
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_endpoints is not None:
            self._values["external_endpoints"] = external_endpoints
        if internal_load_balancers is not None:
            self._values["internal_load_balancers"] = internal_load_balancers

    @builtins.property
    def external_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Internet IP addresses to be health checked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "load_balancer_type": "loadBalancerType",
        "region": "region",
    },
)
class GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        load_balancer_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95c25ea5c9173b5ef663c7da97af529085468400674d9dda96bec5d257317eb)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if load_balancer_type is not None:
            self._values["load_balancer_type"] = load_balancer_type
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd4399631ebe313a33a9d4be778abd8a5cfbb2c6abc56e58e650bb6e9224a76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c658ec77eb8d8974b80b3085ef4ab5574df72c305b2163a28e350c49a9a7b5ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b511abf656a4839b0d9643c66e72922b86aec6b6683775855d5cd9048c6300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22942569f8c4f2519c10cd8ab8744005c92f8299de528b8b2bff8c50f9a153d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae677d3962e984be8ee15bd69bbef06b0ef64610bc6a57739e9e90ecd30cec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc02f22845b1028132a8f186b4fe74d26b058856358861185445d78e8adbd7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c11e03eb7b33e35deb992b02118e49766b269eeaa1bbce753e96af88f2e7b644)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLoadBalancerType")
    def reset_load_balancer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204232e8cf2b9f536c03aa7c390500ee8b58e0faf17f9dd32374115cf3b4ad82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff178c20b16e8cf6622060fe2004c9ea7ee9afc8966ad7ab705ddf0280e6282e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eae18b906ebe33a11d727db15d37cd75341697114e7cf68f62b51dd18e34c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842b567db6962ab47386fc262ebeb175e7d2b780afbf44555f1da614488dafac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d28ffabbaa07f431a7e4271135fd801e5dae08c4c34d88336a38e1d5cd608f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007c68977324529dbe3a96ff9a5bef4db009f52aded3d68fb73d790b40c2ac3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7866cbef29c97f00277e1532ef3643b942b3436840f5a2d70eb0a08ab513e28d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae15dcbcacf5b67ef4583cd3418b0845753fd06f9ac4ca8634a1fde82595671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22543b9415f271d550145bafceef23f3a577ecd4fa871e34daee9b0cf13cc160)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a1eba93159484c263654519f6ba4663e6d5f2b07cf9d6f71022ee3b2db791e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @jsii.member(jsii_name="resetExternalEndpoints")
    def reset_external_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEndpoints", []))

    @jsii.member(jsii_name="resetInternalLoadBalancers")
    def reset_internal_load_balancers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalLoadBalancers", []))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0bf9fa632befa965e5e2c12bfa7104bb713dfcbbeb140ba5b04d7b588c0c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd056e2e726d33e9c36dab88ec4d3c31826a7cb90400f6993f86d41c698ffd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrr",
    jsii_struct_bases=[],
    name_mapping={
        "weight": "weight",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class GoogleDnsRecordSetRoutingPolicyWrr:
    def __init__(
        self,
        *,
        weight: jsii.Number,
        health_checked_targets: typing.Optional[typing.Union["GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param weight: The ratio of traffic routed to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#weight GoogleDnsRecordSet#weight}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_checked_targets GoogleDnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e4d07f8ad73e2c32458d0df5688e12395cf420c92ba9912b86596bad79a65d9)
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument health_checked_targets", value=health_checked_targets, expected_type=type_hints["health_checked_targets"])
            check_type(argname="argument rrdatas", value=rrdatas, expected_type=type_hints["rrdatas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weight": weight,
        }
        if health_checked_targets is not None:
            self._values["health_checked_targets"] = health_checked_targets
        if rrdatas is not None:
            self._values["rrdatas"] = rrdatas

    @builtins.property
    def weight(self) -> jsii.Number:
        '''The ratio of traffic routed to the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#weight GoogleDnsRecordSet#weight}
        '''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#health_checked_targets GoogleDnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#rrdatas GoogleDnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyWrr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60b83f67f9b848cc24a0359e1edcc6fe2b1b9cdee8fd2b0b0a7168bc2901de9)
            check_type(argname="argument external_endpoints", value=external_endpoints, expected_type=type_hints["external_endpoints"])
            check_type(argname="argument internal_load_balancers", value=internal_load_balancers, expected_type=type_hints["internal_load_balancers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_endpoints is not None:
            self._values["external_endpoints"] = external_endpoints
        if internal_load_balancers is not None:
            self._values["internal_load_balancers"] = internal_load_balancers

    @builtins.property
    def external_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Internet IP addresses to be health checked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address": "ipAddress",
        "ip_protocol": "ipProtocol",
        "network_url": "networkUrl",
        "port": "port",
        "project": "project",
        "load_balancer_type": "loadBalancerType",
        "region": "region",
    },
)
class GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers:
    def __init__(
        self,
        *,
        ip_address: builtins.str,
        ip_protocol: builtins.str,
        network_url: builtins.str,
        port: builtins.str,
        project: builtins.str,
        load_balancer_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18121d26de8ada3d9a06e4545b20f6ff5ba7d627fa7fb13aaee148cd066179a9)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ip_protocol", value=ip_protocol, expected_type=type_hints["ip_protocol"])
            check_type(argname="argument network_url", value=network_url, expected_type=type_hints["network_url"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
            "ip_protocol": ip_protocol,
            "network_url": network_url,
            "port": port,
            "project": project,
        }
        if load_balancer_type is not None:
            self._values["load_balancer_type"] = load_balancer_type
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The frontend IP address of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_address GoogleDnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#ip_protocol GoogleDnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#network_url GoogleDnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#port GoogleDnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#project GoogleDnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#load_balancer_type GoogleDnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#region GoogleDnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__327e8c9019414ad24239e2358a8028006b59ddc406f247f3937ef131db6c7aa6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e133092648c7b2bef9b09895e25c1b99dbdce0afdabc29d7ab4f30c5a90f74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fbd23830fc885dd9e8ec19f05d683db6f34731961558dfb59ec9d17a16ce47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94e9d6fad7bf32d160147b9cfd23d4d20fa3d8d2591f76cda1e39305efc7c491)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae8e7c69a20270a064a101beffe016772a9b3a7ee4dda4c7e10fd3af074623e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7905f402482a1f87b7f75854f61d76ed7069dd6a19fd10865459cfa87aad068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddfe50b0b192562caabe428edaa9518b4a20b7d6c9b25b38a4d6be10b327815d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLoadBalancerType")
    def reset_load_balancer_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolInput")
    def ip_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUrlInput")
    def network_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79c90dd047c169d6101ef8960fb0aa32be0be9325b757a51ef5afe9fb6295d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0132a3240810eeb2a94057196b029d7af43714f6dac20eed5bcb8154cc287b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ae5fbf4844690502a5d3680038f144b1da6464b04e30ab2b91a1bc1c57053a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bb71b548d8f727e7869ab3a8a9873ea62a574ca34dbff4b98888ae13f0f609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa05eb34490cc20790e6770093cbfe7c673690bbd9fdc67869c57cebce18758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f03b6dc189043fe88ce6df9947597f141b74c8ad786e24d895adda89230b14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9692262fc79a0cf4841f0dc00c167dcc386438809506f906ea75bc5036fed0bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2be318a19b8ad94ec49b6517b80fa48da1696a09c5ee67895d8f0cb1562f44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec6ab25fa7c63e37a73e23545d3c100f799beb43dbed5e7ce2911b1dbe4f74c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0440b6ed0b40b694320bb2728dfe612ff11d2a4285fdc7cb51306ec4db2e294b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInternalLoadBalancers", [value]))

    @jsii.member(jsii_name="resetExternalEndpoints")
    def reset_external_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEndpoints", []))

    @jsii.member(jsii_name="resetInternalLoadBalancers")
    def reset_internal_load_balancers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalLoadBalancers", []))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancers")
    def internal_load_balancers(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b492ce1141cf1d74d432e326924ef66fa3d6b2610f22b2cefc3160d31d031611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d013889db349434cc2fff9d040e057f697171fa5b3c9cd9733c99e4c30a123e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyWrrList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd6ca45387e431b4b4b3a423f8986c2b3c8c556ba2493c50d0dd51e80ba4ba43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDnsRecordSetRoutingPolicyWrrOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030265c8f6c37e784e8a0125e599ae5729c7a775a1599ee8d28fb19e5ac44a1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDnsRecordSetRoutingPolicyWrrOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f856a1cec4229dd544f231b32c90ad1eada0e2fa7e5dfcb6ff363f7d1a53953)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69aa67e314ad4ec2ee0cfa16b6e94f29f42ceb37029c48aa32d59a2ddbd43b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99367cfa739b982170167b2d097d96adc63c2d4727eb3ce485f7a8fe9049bdca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrr]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrr]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrr]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac4f7bac78de2d9aa14ebf0d8d9b38e16dfd4ffd5f12c6cf9fdc6807a5114cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDnsRecordSetRoutingPolicyWrrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDnsRecordSet.GoogleDnsRecordSetRoutingPolicyWrrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2627b92a0bf818cb235c098b6814211251cc85b101f6285faa7d02ee7d44b63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHealthCheckedTargets")
    def put_health_checked_targets(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#external_endpoints GoogleDnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dns_record_set#internal_load_balancers GoogleDnsRecordSet#internal_load_balancers}
        '''
        value = GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets(
            external_endpoints=external_endpoints,
            internal_load_balancers=internal_load_balancers,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheckedTargets", [value]))

    @jsii.member(jsii_name="resetHealthCheckedTargets")
    def reset_health_checked_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckedTargets", []))

    @jsii.member(jsii_name="resetRrdatas")
    def reset_rrdatas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRrdatas", []))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargets")
    def health_checked_targets(
        self,
    ) -> GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference:
        return typing.cast(GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets]:
        return typing.cast(typing.Optional[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatasInput")
    def rrdatas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rrdatasInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ffa8c43460ed5b2116bd3eff189a910c521189ee2b7dd4b922a93922c507315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3ba3ea25b3f147a92ef4d127a352d4aaac7ded970288946c3b519c8d7279a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrr]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrr]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrr]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1976b0fcaf75cc34f1f12d89167240794d5386767ac14804b4a9ecaadd5a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDnsRecordSet",
    "GoogleDnsRecordSetConfig",
    "GoogleDnsRecordSetRoutingPolicy",
    "GoogleDnsRecordSetRoutingPolicyGeo",
    "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets",
    "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers",
    "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList",
    "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference",
    "GoogleDnsRecordSetRoutingPolicyGeoList",
    "GoogleDnsRecordSetRoutingPolicyGeoOutputReference",
    "GoogleDnsRecordSetRoutingPolicyOutputReference",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackup",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupOutputReference",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference",
    "GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference",
    "GoogleDnsRecordSetRoutingPolicyWrr",
    "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets",
    "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers",
    "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList",
    "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference",
    "GoogleDnsRecordSetRoutingPolicyWrrList",
    "GoogleDnsRecordSetRoutingPolicyWrrOutputReference",
]

publication.publish()

def _typecheckingstub__61d768d15018537ceede9e2d941aa12f4d9f41fb150c001f4aa1f998d4856048(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    managed_zone: builtins.str,
    name: builtins.str,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    routing_policy: typing.Optional[typing.Union[GoogleDnsRecordSetRoutingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ttl: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__c2740c90b6e5a5d8739db37e4f73efe5ddaf4e20c784bdefdf87905ab2950669(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddd7440ba541a74eca2f383295b8be3cb2f1f8b0ab446c924118fded2c5c9e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e64b2c623b10db694811811ff7b93f6b5fc17acba90d03448d058984bf1c58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a12d8901b95fd2585e77be8fa7d48eb31c77c321c4ba7f2cab4a7b2595ef517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cad695f34ddb591ed3b1f0ae0f8c69495535d25e6724f9065ace665727f2190(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d1ddda375c27b52c6563eeb42e1a036dde5e00ddf72d7b2eb23b2b4669be2d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35349c09d0504c829cdda67f0dbef8cc1829ecaf1ef1e1e5b909cf2c53bc42e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e4ce1c5a733a2345119b36450135ac0e7d190bea98d3fd9eee321b4b84cd94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2b27506331dd8f5f50d09549265cd6e4fb1e700ea977bff39c317a157060e2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_zone: builtins.str,
    name: builtins.str,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    routing_policy: typing.Optional[typing.Union[GoogleDnsRecordSetRoutingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f137acf7257bef1cf64bacd80e862ced61ea17b4072dbcd06cc964f0287601b9(
    *,
    enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    geo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health_check: typing.Optional[builtins.str] = None,
    primary_backup: typing.Optional[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    wrr: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyWrr, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ca662e7fcbaa508b76472632d37c1b884655786731d3e3ca8da1c32db5acb5(
    *,
    location: builtins.str,
    health_checked_targets: typing.Optional[typing.Union[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230c6d65c222b850aeab24644dd96cb40a56cecd8d222ae589c3f7be68a9fa45(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0469b84094a38d7787e483be6e9c9e5c9d63774cadbc15652b1549e677b74662(
    *,
    ip_address: builtins.str,
    ip_protocol: builtins.str,
    network_url: builtins.str,
    port: builtins.str,
    project: builtins.str,
    load_balancer_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3894b89e3247a1117f11084f23dc190cf545a09a636f9c225c96a5ad1f174ed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ae14f43a73f4902041f1a9c3f6f7b826dbe445f00497f55c7f545430e7e971(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903e7652ac09717b8d022432a25f2928fcf7709572b491887fe945d259f686be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990f192b8f81fd02c4d76b88cc4b849a922f2520266c21f0cf244d2b7b4c12ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d70c2f7c134e06dc2e63568e6e4f18fa5a9ae770074cb39a19d8b49c118fb02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fed351f261882c795c9a4a06410af17e42df3598a4682770d017dde417794d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87f62dac8a0cedc1b79213e8b9e95886e6835afef90435e2691be3f22b584ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367255f4fd93aeda1758882df77705e37cf5d3f483444053d31cfd18e699604c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b809b3c945c1df229367a78e6d9952042d72f599397a0f505a749a71979ba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec096c50399532ea13ff8e9521fdae7bdd02df6159de1ff26d04e0b828c81ef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae3017dab724f8895ff1d355b790d4997deee36712488a4750a153aa079eaa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155c6b1a93e3e503532bb84ad6bad0f296c279c8e07010e1f426c43833722898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e96cb81e36245bfbfd9a313930a2e0a64068c84b9a884370524cc9e3bff11c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0ebcfde3c36babcc194a9a9d9ff689caf55f98d6f464cd53e0996a8c4de463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9621e825afd5b6ae1b2801f42e3e997333493bbee24d2467a8e3734685eeb187(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48c093cef366dc9023c4d45fcd8e9cb49701e12899cedfb0f7698b4fcf9d038(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7ad3cb5b2888cee075a165ade85e22686e2cbf1eb1dbb2d2ee8431584f785c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a7991acdde33090ac806e7d14fa1cd1795cc3658d48daa6946a6d3b77cae0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d74b4d4fb4da7483fdb92646f439bd4f63d12563bf355f275ca640b46721fc(
    value: typing.Optional[GoogleDnsRecordSetRoutingPolicyGeoHealthCheckedTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0933eb8153fd28b20d21530767b9c87748cd460ff9495f87311d2b4c6c20f089(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7ea743dcd1732d85728d01d4b4f3bb3e13c04b73bb0b03f358d359b5bcb6b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcaa6cc9fb9dae5da20d57ead4b1011964f6ccbfe6019dcd1de30837c282eb56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ab710a6c4e9eca8a53b6aa28d341fe38048749de3c0ff87933ac51a9998094(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503c7c85f3b2bc341e858a9eb0094b4d5ea34650ffc9628456a2041985c6d13b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3947f41d64c18652ef2588986329ad8ce2d7fed14c548884656e82c428025606(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyGeo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e83650efaed6593671cbb793c8da71e957aa30d1fb4334ddf74e3bc7047bcb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8802e11f8d7be90a5f06eb2bdf515f3e54db7d9c25eeb9cdfd1b7b5d80fc85b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f023b696b08e48c562c8632a36d835edd86d77aee42fc90f5a64615d01d175e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3ca16d0c246edf5fa62d27718f5ac58fc4dba2f6f6aff2fe0e4b8ea1f8c5cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyGeo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3ab74eb2a204fe4b9a79a0779a94d5a17978542a5cee9be9851a59cdd329bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec29098ebb9367d4f72e611f823a2dbc33fe16773b9af097542ded5bf2bd62a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyGeo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb7c5a0016bf9e67f50776c0c932dff57336a07164cb69107e5cc2f50f7bac2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyWrr, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebf317fa6005b1691395b0d1b6b18654763a9c336855bee7e4d2e2028390d76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fef4a1007e0baa07176c57e70e07a07567a76c2ac7287be3d9fe5046d7787d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730870648af74c19a285755223cff90f5b657cc677e956834ab2467b66b23801(
    value: typing.Optional[GoogleDnsRecordSetRoutingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c19b95669d93a623f2f52f3cf49f53d2b79ef95dd2a39d9fa9fbcfda6ec650(
    *,
    backup_geo: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[builtins.str, typing.Any]]]],
    primary: typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary, typing.Dict[builtins.str, typing.Any]],
    enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trickle_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242b28bf01338ac2a20bedfe720df5dea5f701cfdf10ef10ca28a9859c483080(
    *,
    location: builtins.str,
    health_checked_targets: typing.Optional[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93edbf7547c8be6baa4a3a3dd3cff798681900f004e08bc06b7e1af3a389d63(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b6841702de5627cb89f098ddb7a6b12f59484f27428a18b8916f63604cbddc(
    *,
    ip_address: builtins.str,
    ip_protocol: builtins.str,
    network_url: builtins.str,
    port: builtins.str,
    project: builtins.str,
    load_balancer_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5980123b1cf626b0be6e0c998b7b2c92c2fd96dd32f1cefd19af34587903a0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d698ed584c143341f73b34ffd70bd3a6741d8df00ccda33c3e7e8c64d2d0fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956fe616a178670421e6bd53290219b38ec1532392c322e9a313ef3b2fbdeec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52df072edba8a89022d2302e007fdd7c4c18db321207fb647fbf817514786931(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9686c71a25abe0fb830dbaff0bfd4dd03ca1dc5b57c6318812a60aab30c4bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b793ead816d41cf9b5e06b63054a57cd13a209bd07fa0858d8b68f7f8e2d0c17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493d6c365b2f4415b3888da6c5e63ad5eea4818bb002d6283bdc41fc46fd6c67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44643df0e0ea1d6788925ecc6c4b73efe5ceb0b01d297ce89f64f9b592a75a59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208672187ab86ff68604cd3c2f6f373cbfb00b7fb471837fcee189eb165ab59d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063225929e9828073142cf8f764fb28af19af151647b4f3b4f165f13e719b4c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da8f2a2212730ccb3812a2f5d44dc6b69dc1630f22c40b5f87093541e1aebd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546903e66f1df05787d69fbe2ed6b8d9da095972867928c78e9feb1dc2f9fe1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3832e4fb564578bb92442de7a433fc290f356d81a8b60cc266f2e5992fcc132f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026bce62fafc66d5c7f235baa49f8ecf3508f71d667d526d3484a5671e4808bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9f1f338721fc4aae1cb6d02a2a126ad6265ac14463466cb13ce3249a9dfc89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b7b67578bb3cc96ac6b466136affd4be339d337f1d3ed04dec13fcdaed387f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a58852418280da718ef7fce2d0d4441bd9049ce82282e109e3130e53bffa0d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a23310cd1fe97519c1e2068fcc884d559409d46ef0a6644764a4a8dd3487e48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c461080dc6f75a15511ce68c5b14565c53bcae314b562987cb9dd1258e88ab88(
    value: typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb83cf67699417299c765d905a79ce6c197876d773af8e915978add4cd0d6e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37c7a3ea96b42bdc1612dcf0a7a7e2f302ab84296cae5b0228e93280c615769(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849355ac238c9075ccee6dc65cd56eed67b6292c54515629493ec462a0f582e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6522f8f07669a54ba7e7cae5ea6f9c4f6fc2f636d12f690674094a5c47cbb593(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f057cb710e3c45c1b3c41ed5b85e733248f0a1dfc466faadc4b86353a0a545c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb00c697fca0b70f963c07c501ac6eb8081d231e4bb3107d8344e1562d16342(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd763b9492c1602e3d46a6ff4f0c069f21f61baeaa4ebda5ae2d5b937f73f01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81ea8c3fd89bee847abd8874f080d61606c90b62a3a72734deb071c6697ca2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8881f932445e147745c8438c83cfe8ce51b64b2edc2584e7c47e30b791bca627(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99b5160f7937a6101c56a2bab4aee8088a0394c29ba5969502cd88ba0572046(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b499785d8b2685e86d14f1e0d22caa65aaa707bbd0a71ce732f531d3d688b98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b722ecb5bb8f29c878dde1afc140edb8ac0c7f1d017e31810712871aacdcd9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0027d683fdc7465ec23bd9efac7fb2e65dc6109e5cba1230d8c48b8f49b5d4eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878e7feac86ef514c90a64f41f31fb8f8fa9463e8a3e0bac8ca8070fe72861ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686e468c905631908f2a945c3d649127ad3512f0942f975c3b4384acb827a608(
    value: typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f6be770b5dbc411785f7e26e61336268bb55b90f2490d562b53ccd62f50aeb(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95c25ea5c9173b5ef663c7da97af529085468400674d9dda96bec5d257317eb(
    *,
    ip_address: builtins.str,
    ip_protocol: builtins.str,
    network_url: builtins.str,
    port: builtins.str,
    project: builtins.str,
    load_balancer_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd4399631ebe313a33a9d4be778abd8a5cfbb2c6abc56e58e650bb6e9224a76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c658ec77eb8d8974b80b3085ef4ab5574df72c305b2163a28e350c49a9a7b5ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b511abf656a4839b0d9643c66e72922b86aec6b6683775855d5cd9048c6300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22942569f8c4f2519c10cd8ab8744005c92f8299de528b8b2bff8c50f9a153d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae677d3962e984be8ee15bd69bbef06b0ef64610bc6a57739e9e90ecd30cec0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc02f22845b1028132a8f186b4fe74d26b058856358861185445d78e8adbd7e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11e03eb7b33e35deb992b02118e49766b269eeaa1bbce753e96af88f2e7b644(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204232e8cf2b9f536c03aa7c390500ee8b58e0faf17f9dd32374115cf3b4ad82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff178c20b16e8cf6622060fe2004c9ea7ee9afc8966ad7ab705ddf0280e6282e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eae18b906ebe33a11d727db15d37cd75341697114e7cf68f62b51dd18e34c93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842b567db6962ab47386fc262ebeb175e7d2b780afbf44555f1da614488dafac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d28ffabbaa07f431a7e4271135fd801e5dae08c4c34d88336a38e1d5cd608f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007c68977324529dbe3a96ff9a5bef4db009f52aded3d68fb73d790b40c2ac3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7866cbef29c97f00277e1532ef3643b942b3436840f5a2d70eb0a08ab513e28d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae15dcbcacf5b67ef4583cd3418b0845753fd06f9ac4ca8634a1fde82595671(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22543b9415f271d550145bafceef23f3a577ecd4fa871e34daee9b0cf13cc160(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a1eba93159484c263654519f6ba4663e6d5f2b07cf9d6f71022ee3b2db791e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0bf9fa632befa965e5e2c12bfa7104bb713dfcbbeb140ba5b04d7b588c0c5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd056e2e726d33e9c36dab88ec4d3c31826a7cb90400f6993f86d41c698ffd4(
    value: typing.Optional[GoogleDnsRecordSetRoutingPolicyPrimaryBackupPrimary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4d07f8ad73e2c32458d0df5688e12395cf420c92ba9912b86596bad79a65d9(
    *,
    weight: jsii.Number,
    health_checked_targets: typing.Optional[typing.Union[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60b83f67f9b848cc24a0359e1edcc6fe2b1b9cdee8fd2b0b0a7168bc2901de9(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18121d26de8ada3d9a06e4545b20f6ff5ba7d627fa7fb13aaee148cd066179a9(
    *,
    ip_address: builtins.str,
    ip_protocol: builtins.str,
    network_url: builtins.str,
    port: builtins.str,
    project: builtins.str,
    load_balancer_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327e8c9019414ad24239e2358a8028006b59ddc406f247f3937ef131db6c7aa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e133092648c7b2bef9b09895e25c1b99dbdce0afdabc29d7ab4f30c5a90f74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fbd23830fc885dd9e8ec19f05d683db6f34731961558dfb59ec9d17a16ce47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e9d6fad7bf32d160147b9cfd23d4d20fa3d8d2591f76cda1e39305efc7c491(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8e7c69a20270a064a101beffe016772a9b3a7ee4dda4c7e10fd3af074623e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7905f402482a1f87b7f75854f61d76ed7069dd6a19fd10865459cfa87aad068(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfe50b0b192562caabe428edaa9518b4a20b7d6c9b25b38a4d6be10b327815d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79c90dd047c169d6101ef8960fb0aa32be0be9325b757a51ef5afe9fb6295d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0132a3240810eeb2a94057196b029d7af43714f6dac20eed5bcb8154cc287b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ae5fbf4844690502a5d3680038f144b1da6464b04e30ab2b91a1bc1c57053a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bb71b548d8f727e7869ab3a8a9873ea62a574ca34dbff4b98888ae13f0f609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa05eb34490cc20790e6770093cbfe7c673690bbd9fdc67869c57cebce18758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f03b6dc189043fe88ce6df9947597f141b74c8ad786e24d895adda89230b14a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9692262fc79a0cf4841f0dc00c167dcc386438809506f906ea75bc5036fed0bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2be318a19b8ad94ec49b6517b80fa48da1696a09c5ee67895d8f0cb1562f44e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6ab25fa7c63e37a73e23545d3c100f799beb43dbed5e7ce2911b1dbe4f74c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0440b6ed0b40b694320bb2728dfe612ff11d2a4285fdc7cb51306ec4db2e294b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b492ce1141cf1d74d432e326924ef66fa3d6b2610f22b2cefc3160d31d031611(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d013889db349434cc2fff9d040e057f697171fa5b3c9cd9733c99e4c30a123e5(
    value: typing.Optional[GoogleDnsRecordSetRoutingPolicyWrrHealthCheckedTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6ca45387e431b4b4b3a423f8986c2b3c8c556ba2493c50d0dd51e80ba4ba43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030265c8f6c37e784e8a0125e599ae5729c7a775a1599ee8d28fb19e5ac44a1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f856a1cec4229dd544f231b32c90ad1eada0e2fa7e5dfcb6ff363f7d1a53953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69aa67e314ad4ec2ee0cfa16b6e94f29f42ceb37029c48aa32d59a2ddbd43b0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99367cfa739b982170167b2d097d96adc63c2d4727eb3ce485f7a8fe9049bdca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac4f7bac78de2d9aa14ebf0d8d9b38e16dfd4ffd5f12c6cf9fdc6807a5114cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDnsRecordSetRoutingPolicyWrr]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2627b92a0bf818cb235c098b6814211251cc85b101f6285faa7d02ee7d44b63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffa8c43460ed5b2116bd3eff189a910c521189ee2b7dd4b922a93922c507315(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3ba3ea25b3f147a92ef4d127a352d4aaac7ded970288946c3b519c8d7279a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1976b0fcaf75cc34f1f12d89167240794d5386767ac14804b4a9ecaadd5a0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDnsRecordSetRoutingPolicyWrr]],
) -> None:
    """Type checking stubs"""
    pass
