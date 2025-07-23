r'''
# `google_dns_record_set`

Refer to the Terraform Registry for docs: [`google_dns_record_set`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set).
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


class DnsRecordSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set google_dns_record_set}.'''

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
        routing_policy: typing.Optional[typing.Union["DnsRecordSetRoutingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set google_dns_record_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param managed_zone: The name of the zone in which this record set will reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#managed_zone DnsRecordSet#managed_zone}
        :param name: The DNS name this record set will apply to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#name DnsRecordSet#name}
        :param type: The DNS record set type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#type DnsRecordSet#type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#id DnsRecordSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        :param routing_policy: routing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#routing_policy DnsRecordSet#routing_policy}
        :param rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}
        :param ttl: The time-to-live of this record set (seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ttl DnsRecordSet#ttl}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc80a5b5fa7ebaac7357ab91688e2c9551dd1b3ace8607f53bfd18fad3c9fb3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DnsRecordSetConfig(
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
        '''Generates CDKTF code for importing a DnsRecordSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DnsRecordSet to import.
        :param import_from_id: The id of the existing DnsRecordSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DnsRecordSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b283fe049031d9086d1ce5d7bd70e4ebca2538155f71e1c2b976f7c6a48e875)
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
        geo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyGeo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_check: typing.Optional[builtins.str] = None,
        primary_backup: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        wrr: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrr", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable_geo_fencing: Specifies whether to enable fencing for geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#enable_geo_fencing DnsRecordSet#enable_geo_fencing}
        :param geo: geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#geo DnsRecordSet#geo}
        :param health_check: Specifies the health check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_check DnsRecordSet#health_check}
        :param primary_backup: primary_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#primary_backup DnsRecordSet#primary_backup}
        :param wrr: wrr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#wrr DnsRecordSet#wrr}
        '''
        value = DnsRecordSetRoutingPolicy(
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
    def routing_policy(self) -> "DnsRecordSetRoutingPolicyOutputReference":
        return typing.cast("DnsRecordSetRoutingPolicyOutputReference", jsii.get(self, "routingPolicy"))

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
    def routing_policy_input(self) -> typing.Optional["DnsRecordSetRoutingPolicy"]:
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicy"], jsii.get(self, "routingPolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__050a9500c570031429c3bb80ff8573b1bb6317894a9f97607e59bede72e7fb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedZone")
    def managed_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedZone"))

    @managed_zone.setter
    def managed_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfb6f990de9acbd036628da3a90c663a00cad31617cd0a1a1e52043d3018ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d52d993d10753cdeadad995fc9b8f89a8a4ff36d0562ba52236511027181b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e56248dff56bd3df564920096e01a73832203d11b36565efea9a9457a52eb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe85caef8010e8a17393180701ff35c38ce6a3d257cbde19b916d5df2fa646e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517269ec34358cda924a62221bf552e56d893a4d5db126ab0a0a164326ac8fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79eb3afe959908e588498a8db46baff558a85ab11f5a2693422c4b89ce3913c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetConfig",
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
class DnsRecordSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        routing_policy: typing.Optional[typing.Union["DnsRecordSetRoutingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param managed_zone: The name of the zone in which this record set will reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#managed_zone DnsRecordSet#managed_zone}
        :param name: The DNS name this record set will apply to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#name DnsRecordSet#name}
        :param type: The DNS record set type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#type DnsRecordSet#type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#id DnsRecordSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        :param routing_policy: routing_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#routing_policy DnsRecordSet#routing_policy}
        :param rrdatas: The string data for the records in this record set whose meaning depends on the DNS type. For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}
        :param ttl: The time-to-live of this record set (seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ttl DnsRecordSet#ttl}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(routing_policy, dict):
            routing_policy = DnsRecordSetRoutingPolicy(**routing_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8298b7750ae475388725d4ab10c48ee5478e537a4fcf002f8ffea0c638c52c8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#managed_zone DnsRecordSet#managed_zone}
        '''
        result = self._values.get("managed_zone")
        assert result is not None, "Required property 'managed_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The DNS name this record set will apply to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#name DnsRecordSet#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The DNS record set type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#type DnsRecordSet#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#id DnsRecordSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_policy(self) -> typing.Optional["DnsRecordSetRoutingPolicy"]:
        '''routing_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#routing_policy DnsRecordSet#routing_policy}
        '''
        result = self._values.get("routing_policy")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicy"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The string data for the records in this record set whose meaning depends on the DNS type.

        For TXT record, if the string data contains spaces, add surrounding " if you don't want your string to get split on spaces. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the Terraform configuration string (e.g. "first255characters""morecharacters").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}
        '''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The time-to-live of this record set (seconds).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ttl DnsRecordSet#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "enable_geo_fencing": "enableGeoFencing",
        "geo": "geo",
        "health_check": "healthCheck",
        "primary_backup": "primaryBackup",
        "wrr": "wrr",
    },
)
class DnsRecordSetRoutingPolicy:
    def __init__(
        self,
        *,
        enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        geo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyGeo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_check: typing.Optional[builtins.str] = None,
        primary_backup: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        wrr: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrr", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enable_geo_fencing: Specifies whether to enable fencing for geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#enable_geo_fencing DnsRecordSet#enable_geo_fencing}
        :param geo: geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#geo DnsRecordSet#geo}
        :param health_check: Specifies the health check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_check DnsRecordSet#health_check}
        :param primary_backup: primary_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#primary_backup DnsRecordSet#primary_backup}
        :param wrr: wrr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#wrr DnsRecordSet#wrr}
        '''
        if isinstance(primary_backup, dict):
            primary_backup = DnsRecordSetRoutingPolicyPrimaryBackup(**primary_backup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f732d616e785af192ec01da07894101c28e293ad4565b6ec334e51e0bc77110)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#enable_geo_fencing DnsRecordSet#enable_geo_fencing}
        '''
        result = self._values.get("enable_geo_fencing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def geo(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeo"]]]:
        '''geo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#geo DnsRecordSet#geo}
        '''
        result = self._values.get("geo")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeo"]]], result)

    @builtins.property
    def health_check(self) -> typing.Optional[builtins.str]:
        '''Specifies the health check.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_check DnsRecordSet#health_check}
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_backup(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"]:
        '''primary_backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#primary_backup DnsRecordSet#primary_backup}
        '''
        result = self._values.get("primary_backup")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"], result)

    @builtins.property
    def wrr(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]]:
        '''wrr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#wrr DnsRecordSet#wrr}
        '''
        result = self._values.get("wrr")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeo",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class DnsRecordSetRoutingPolicyGeo:
    def __init__(
        self,
        *,
        location: builtins.str,
        health_checked_targets: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyGeoHealthCheckedTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: The location name defined in Google Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#location DnsRecordSet#location}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = DnsRecordSetRoutingPolicyGeoHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f7bf95a1e64cf70490ed35d29a32b547e372d249c6657d5b5374b7c5e9ebe4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#location DnsRecordSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyGeoHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyGeoHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyGeo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class DnsRecordSetRoutingPolicyGeoHealthCheckedTargets:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c27151c6a1da6d067c1e7127f245274e783144931c1bd277aad8bbb49d45084)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyGeoHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers",
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
class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers:
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
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f018ef8cf4c295e895ff632dfbedb97f8826556a7ebf56ecfadd9dd2670eec4e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0755fe14da6c3213e1cca6c470e01749160a74c097b44d5ad901b189cef6dd09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0d4a66a7e22677adcbe06188113facdc5983f8f1cfc6e70bd9b96d899c4eb8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93c6450afe7b395b00c97c64756bc344d04d63b7e071a7c341b8179ed4fa583)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46cb73d2f209d00968189aa2b8b3e6cf7c7c450a7476682c3f35ab05ebcf68cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c971cdadd5eca710b52f642d83e982323882481dc2ac1eedfeba48ec10437190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08cc80206256c2a66b008f7266948cdbf31e9fd040bc286f7cd6dac55fcbf27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6749fc2544033550e8c827ea23909a1c661bcc0b4d773b72bb1314c3f0a75c3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d49527424997791735f7800c978ab2ffb553eed668f4343137134154fb02321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d967648f8f92e6528a0c70490bdf419d0e276bd89d7e388db4ac065e089d763b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f2bae4cc8d5b0b27daba8c4a70d7d445f1dffc477119b1a3f2d139bc5a3f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8ee0ae35a0e6046770c545945235450035b6b3a52e2800acadeffbbe47e0ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39873638b5a5468b97618cc441ccd5c8ccf0137111f743fda034b31d9ce6cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bf083d6287578c30d1b622893938f800ada13c4cf8cb695d7633fad7c8f828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e97284c2519f6f2278e09cc0a4bd8e5ee61b82264fbf97eafe6b8c53fb8ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb5fcd5c852aeb24886029d2f3dc8029750d4617fa8bc25b533192f56b17fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d555e2de6f265c210f45fbb704f811a4acd6e9331184f374e1c5e842f905eda7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a5d2b11a3677b213e2b18375ea2a7e77e4ff56ce781660625514597e26b279)
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
    ) -> DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df75efcc59e5b3a1db34457266897a817f63dfb1f3ebc0d94cdb2924ab1ef4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e5d6fd22bfa57f8ca8906eb72fcc9b9139480fe941406a167e503059311d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyGeoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d4e196a13f50ec5428088a5bc38f586dfbfa76b3e6da9a88f46264f9093d13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DnsRecordSetRoutingPolicyGeoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1afffb6af8763167bc2bc61b04c4f30120d2c73e69f113f95b2f4605a5a6359)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyGeoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80689996a1c3904d9f6c0028270a90c577c2296eeb7988a467c1e94ecaf9eee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ef3789d05c8d3476b8f0d6b67a8ad4c07448833673367c0ca1ec199ed642389)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d93a1679b7a06c9154f1253c2b9037ce7293758562a0d477f80d07f0b4d616c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008e391abad0133dab77beb5ee943d93cd5b94be8b133621823d7e0e49b24fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyGeoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyGeoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20b8ee0db31d6952292ea49a2ed570dc882244c3b78b8daf6a2d9b57f9e533d2)
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
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyGeoHealthCheckedTargets(
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
    ) -> DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference:
        return typing.cast(DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b0658e6882b6e2c9ca9fecc640547d4cff796e526ac4761af9ec2d8171ed58cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2074cdaacfdd795954485823408de8ebf577a8efed107e2056990cde018d228b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b10ab4b699841fa71ae9b022e5b8f4c6d0b9b37a92fdb6f0626e1a3e662cde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b892adadc86e297d302e0b0e5f73b8e6a5787a5dddde67e73b8a25060ec3161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGeo")
    def put_geo(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832308d273a442fa8861171f65f979e78c82a02a241baea6f510c3d8d8a0b047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeo", [value]))

    @jsii.member(jsii_name="putPrimaryBackup")
    def put_primary_backup(
        self,
        *,
        backup_geo: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo", typing.Dict[builtins.str, typing.Any]]]],
        primary: typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimary", typing.Dict[builtins.str, typing.Any]],
        enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trickle_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_geo: backup_geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#backup_geo DnsRecordSet#backup_geo}
        :param primary: primary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#primary DnsRecordSet#primary}
        :param enable_geo_fencing_for_backups: Specifies whether to enable fencing for backup geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#enable_geo_fencing_for_backups DnsRecordSet#enable_geo_fencing_for_backups}
        :param trickle_ratio: Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#trickle_ratio DnsRecordSet#trickle_ratio}
        '''
        value = DnsRecordSetRoutingPolicyPrimaryBackup(
            backup_geo=backup_geo,
            primary=primary,
            enable_geo_fencing_for_backups=enable_geo_fencing_for_backups,
            trickle_ratio=trickle_ratio,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryBackup", [value]))

    @jsii.member(jsii_name="putWrr")
    def put_wrr(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrr", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__365c85f310db5ae97ee89350b0bd10d653676a3cbe6187fb2f23453a357bffa3)
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
    def geo(self) -> DnsRecordSetRoutingPolicyGeoList:
        return typing.cast(DnsRecordSetRoutingPolicyGeoList, jsii.get(self, "geo"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackup")
    def primary_backup(self) -> "DnsRecordSetRoutingPolicyPrimaryBackupOutputReference":
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupOutputReference", jsii.get(self, "primaryBackup"))

    @builtins.property
    @jsii.member(jsii_name="wrr")
    def wrr(self) -> "DnsRecordSetRoutingPolicyWrrList":
        return typing.cast("DnsRecordSetRoutingPolicyWrrList", jsii.get(self, "wrr"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]], jsii.get(self, "geoInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckInput")
    def health_check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryBackupInput")
    def primary_backup_input(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"]:
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackup"], jsii.get(self, "primaryBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="wrrInput")
    def wrr_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrr"]]], jsii.get(self, "wrrInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e2bc632d6c6e816846c0345ff991a4c1448408c1fd0c62b1dd3d9b3d83d2a334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGeoFencing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheck"))

    @health_check.setter
    def health_check(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ff61f2e7ddc049637ed366be9a2dd597fa5ca907788323c7ec9b6ebf5f7581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsRecordSetRoutingPolicy]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DnsRecordSetRoutingPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcc0d39996472754acaa4a8d92eb49549d89feefa8666b56fb109095561a910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackup",
    jsii_struct_bases=[],
    name_mapping={
        "backup_geo": "backupGeo",
        "primary": "primary",
        "enable_geo_fencing_for_backups": "enableGeoFencingForBackups",
        "trickle_ratio": "trickleRatio",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackup:
    def __init__(
        self,
        *,
        backup_geo: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo", typing.Dict[builtins.str, typing.Any]]]],
        primary: typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimary", typing.Dict[builtins.str, typing.Any]],
        enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trickle_ratio: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_geo: backup_geo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#backup_geo DnsRecordSet#backup_geo}
        :param primary: primary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#primary DnsRecordSet#primary}
        :param enable_geo_fencing_for_backups: Specifies whether to enable fencing for backup geo queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#enable_geo_fencing_for_backups DnsRecordSet#enable_geo_fencing_for_backups}
        :param trickle_ratio: Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#trickle_ratio DnsRecordSet#trickle_ratio}
        '''
        if isinstance(primary, dict):
            primary = DnsRecordSetRoutingPolicyPrimaryBackupPrimary(**primary)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23212610ae285d98bec0608b759130bf5122645ebafbe71c58b15076b3f873a)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo"]]:
        '''backup_geo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#backup_geo DnsRecordSet#backup_geo}
        '''
        result = self._values.get("backup_geo")
        assert result is not None, "Required property 'backup_geo' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo"]], result)

    @builtins.property
    def primary(self) -> "DnsRecordSetRoutingPolicyPrimaryBackupPrimary":
        '''primary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#primary DnsRecordSet#primary}
        '''
        result = self._values.get("primary")
        assert result is not None, "Required property 'primary' is missing"
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupPrimary", result)

    @builtins.property
    def enable_geo_fencing_for_backups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable fencing for backup geo queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#enable_geo_fencing_for_backups DnsRecordSet#enable_geo_fencing_for_backups}
        '''
        result = self._values.get("enable_geo_fencing_for_backups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trickle_ratio(self) -> typing.Optional[jsii.Number]:
        '''Specifies the percentage of traffic to send to the backup targets even when the primary targets are healthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#trickle_ratio DnsRecordSet#trickle_ratio}
        '''
        result = self._values.get("trickle_ratio")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo:
    def __init__(
        self,
        *,
        location: builtins.str,
        health_checked_targets: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: The location name defined in Google Cloud. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#location DnsRecordSet#location}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0077678ddbca2ebdd5657ffb55d2502872b3319e4decf1333d4a7abb6ee3012)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#location DnsRecordSet#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5e59b5ba540d8fd616d342b38c932487a0bf1c3089c18ac55475389304d3ab)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers",
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
class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers:
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
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9f707a825ca7a1ed76b25d016af3e39165a1b6514dcfba679e95af76d5ef02)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__073cce1bf851de4e9d2f6bb0730b10a8c09070d06457db918668af5d1ccf96ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec91bd1735534e22e8f6b2eecc75b18df3df51aae8f669e9fdf609ceded1c658)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce2f9a84754302d47610c578e2ebee0ca217dd8dd3b4f1a7d66bf37f3eb6de9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8df8aaf65d4e601b2318196762ee829ccba6b4ac30d2bcb2ef4ede6e7e1108a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74449ca4f11a6c6155b17a7d599c86862f745a8c379707ef478b7d733ec1a53a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf32b0a12e0e74a8ae0e5eb9a6d15352b710f66f86a07bab92a8cd87164f6a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2835a2fde630c1a6b25e52306b2c4c50ee8e1f8b9b9d5220ddd8211ecd9e3f27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__298708f437a5c7eac5b16095b9d16ef11e26dd9e50dc28539a241d4c2392348f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414ce257106f2811545945e8c0686c6a896a5de4d4b368ecaab09990bcf52abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e8a1fbef77ec5175163dc50f04ef74380bf8fef31658e1026a7ba4d79c07e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4461fe78ef9c895c3666f624b77dcc5572c240f9917de0ea873824e2ec7af10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98c85726a4ce2d68994c5d75cd727320fca28a6fdda200666616b8030f851fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd431bb2eb88294a97735eecbe6a21da69e94670aebdfcbc3777f7df785d6d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5a47d820b8f7cad09443184b6044b2a9e3524f061db3a0d0180b4935bd6ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25faaf3acc83f03bbbe639866cf427d5b53e1169bb7ae7f75faccb257b46c722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0590f53143722090173eae6e6a1128a1b67a4c8cf6a1d53cb3fb3a14df63a76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c56aaef9714c74fd67c5bd8817f8e0e3eb166b3930b61f290bef933febf87ed)
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
    ) -> DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625908e2fe7218fd1653592183eafc7da6e7b263b0b5dfbffc98de411d10b124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3350f8393d4feb30abf0c15323e62e06422fe2ba262b902e19f13ebc9b04c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e36e8553954ff88fcd2b00d5101625b1329fcf780746884de14f9616d6e2559c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256077eb4912952a1a2b33f888bfa485b09163262bf7966600eaa863c3a45f0a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a30fcd19d35b5c3d1628a5cf9df696952bc47bd10961d3e6659becb3c16cb91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9db656d086315851fe97e79e58aa0ae102734795a73e157f55624e90d19a7cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf20b5ad3e61083d1edb691ae2c48a5ee28dc58d676fed354c1e7d7acb42cb51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dcfc4c2884fb678e23cba566790ddc67393eb8d441963ffc3a80d4adbac333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a37d74aa42f918cbdc6a5096d47410f3ab1b0def4c3877ea16552fa0d375b07)
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
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets(
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
    ) -> DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__17fc3860a6231abca00fdc2e1faea3378ee2a5b15ab139d0a06a357737552eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rrdatas")
    def rrdatas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rrdatas"))

    @rrdatas.setter
    def rrdatas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc89b69795c820935de3cc4651ece59ec31e8cd78610c75922ca03661fca6fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51094923e04814474bb4106fde02bfbc8b8ef587f374248a2a79c6f8790cac82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb47532b5c28bf1811a985b4d8b87f3cf5dff5ec139fe3c238e68eaf09dfd300)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBackupGeo")
    def put_backup_geo(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c4994a92696d14a8db6f715c6fdb87b50bfe3a888cbba1f5914b2855d71eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackupGeo", [value]))

    @jsii.member(jsii_name="putPrimary")
    def put_primary(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyPrimaryBackupPrimary(
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
    def backup_geo(self) -> DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList, jsii.get(self, "backupGeo"))

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference":
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference", jsii.get(self, "primary"))

    @builtins.property
    @jsii.member(jsii_name="backupGeoInput")
    def backup_geo_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]], jsii.get(self, "backupGeoInput"))

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
    ) -> typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupPrimary"]:
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyPrimaryBackupPrimary"], jsii.get(self, "primaryInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a3f2db58a040e942410515880d926c66d5f2cca66558a3ed88a5ca1ba36a1e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGeoFencingForBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trickleRatio")
    def trickle_ratio(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "trickleRatio"))

    @trickle_ratio.setter
    def trickle_ratio(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c12c8f4de3348fa8a9109c128e5a1dd588dc9a265a388505699f613cf439948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trickleRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1e93d42e80b430ccc6b533eed97ebd965ffe4bc551c74555b283e06145cded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimary",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class DnsRecordSetRoutingPolicyPrimaryBackupPrimary:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd427925c6907b1bc75cc9983a428093611aee986ed133e1bfa608ca56246ed0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupPrimary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers",
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
class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers:
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
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cc893deb4aab23148afa5fa081ab7869f48de5bb1e8bac744f5013fe89bfcc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__820fd56d78308ed0087e13d3c91666ff62c4f6d211de35f1200f4118233d6430)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f6f9af2b69e6a5568e35af0e732f885641d737b454b4704515c9da151a1237)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1647ac8a61c98d352f051c9dda8f5eb1db075fe56b35bb26adb780715fc66ccd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e7056c7d081ab0e5d3369f6645195acbcf3f1b6d45876f004bdd003750d8b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f17ea5c3e98f74c294d8a7e4f793d4a0be172d47e4f3c568cffb18cab697fdf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47138a81422443cf51bf731c6fc8299da08cbc3b2f2d9fd9b5351c36648dfd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edb618d010338dc83c91e0c34abd0b9c7fdb55930b6ea5c2501304123a8cc236)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b63ef1de51003ceed628b8910c9d5732b2830602f57c072b3fdc83f484885dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866fcaa99e921236a46d44256e14689b22d59e35de5aa166004f24ec8865c9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7be3b621f753d1a6f98db79411b1fe664512beaba6e057d7579dec4dddcb043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adce2404c9f9e3af108d66f9b7b607f10ace441bd50aaa4f861e2420eac8592d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9c863f714c06213674f9efb4615f9cd74fa6fa89fd975ccb0059e4e029efc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ade44b7270d824b51854b642640dc59156447d0cb6eec72e269cc479849114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7a6f903e2eaa92eb1922d8e0918248e353f76d646efba4a239e663d91ef6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd070654a4d6530f0fe414ded0dc5fb4a76ddb45a3bb7a3bdf610d15debbbc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e75e80ce28a0a72b828cb24dfac5a40fef6831f794453d2c372899c675d2b9f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d1889a380f69273c69f6b3a1fd86127d0d9c6c2383ea208050d146dd6f715e)
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
    ) -> DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31195b16413231ce484c91223653ca73032d49caca40d07bdd9d68c9f9193b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49992dddb547c43deb593f3861bbb1a8d6be692e4024e4e4de60eeca9a66b643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrr",
    jsii_struct_bases=[],
    name_mapping={
        "weight": "weight",
        "health_checked_targets": "healthCheckedTargets",
        "rrdatas": "rrdatas",
    },
)
class DnsRecordSetRoutingPolicyWrr:
    def __init__(
        self,
        *,
        weight: jsii.Number,
        health_checked_targets: typing.Optional[typing.Union["DnsRecordSetRoutingPolicyWrrHealthCheckedTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param weight: The ratio of traffic routed to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#weight DnsRecordSet#weight}
        :param health_checked_targets: health_checked_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        :param rrdatas: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}.
        '''
        if isinstance(health_checked_targets, dict):
            health_checked_targets = DnsRecordSetRoutingPolicyWrrHealthCheckedTargets(**health_checked_targets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7e35a41e501ffbc848172e70e4ed9a8f962bd90787d7de398025dbaee30a36)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#weight DnsRecordSet#weight}
        '''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def health_checked_targets(
        self,
    ) -> typing.Optional["DnsRecordSetRoutingPolicyWrrHealthCheckedTargets"]:
        '''health_checked_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#health_checked_targets DnsRecordSet#health_checked_targets}
        '''
        result = self._values.get("health_checked_targets")
        return typing.cast(typing.Optional["DnsRecordSetRoutingPolicyWrrHealthCheckedTargets"], result)

    @builtins.property
    def rrdatas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#rrdatas DnsRecordSet#rrdatas}.'''
        result = self._values.get("rrdatas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyWrr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargets",
    jsii_struct_bases=[],
    name_mapping={
        "external_endpoints": "externalEndpoints",
        "internal_load_balancers": "internalLoadBalancers",
    },
)
class DnsRecordSetRoutingPolicyWrrHealthCheckedTargets:
    def __init__(
        self,
        *,
        external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c0a912130c7d1900085cf03419fae3e121f71b2bc6bd3d70f1ef18b1df84bd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        '''
        result = self._values.get("external_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def internal_load_balancers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers"]]]:
        '''internal_load_balancers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        result = self._values.get("internal_load_balancers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyWrrHealthCheckedTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers",
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
class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers:
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
        :param ip_address: The frontend IP address of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        :param ip_protocol: The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        :param network_url: The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        :param port: The configured port of the load balancer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        :param project: The ID of the project in which the load balancer belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        :param load_balancer_type: The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        :param region: The region of the load balancer. Only needed for regional load balancers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61496f9cfffbf035c86b80e2cc4fa1687c991c20d9727ec506fbf2a72ae14c8e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_address DnsRecordSet#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_protocol(self) -> builtins.str:
        '''The configured IP protocol of the load balancer. This value is case-sensitive. Possible values: ["tcp", "udp"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#ip_protocol DnsRecordSet#ip_protocol}
        '''
        result = self._values.get("ip_protocol")
        assert result is not None, "Required property 'ip_protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_url(self) -> builtins.str:
        '''The fully qualified url of the network in which the load balancer belongs. This should be formatted like ``https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#network_url DnsRecordSet#network_url}
        '''
        result = self._values.get("network_url")
        assert result is not None, "Required property 'network_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''The configured port of the load balancer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#port DnsRecordSet#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''The ID of the project in which the load balancer belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#project DnsRecordSet#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer. This value is case-sensitive. Possible values: ["regionalL4ilb", "regionalL7ilb", "globalL7ilb"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#load_balancer_type DnsRecordSet#load_balancer_type}
        '''
        result = self._values.get("load_balancer_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the load balancer. Only needed for regional load balancers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#region DnsRecordSet#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47575c8af9841a9f5d27ec19cd1c104f52be26c1b1fd9f7a2da049638e50ca70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2b8003608c91df4e42314b14bd1d13e5e47bac582d4dadb6a607e630990ea2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4faaa40b9da50b2ad096a9c46ceb507df4ecf1060565e4b6f42f1d60b5678df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18361646deb7543337f84e17f828749f41a97e2c04110c11b11d471de3b9ced1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c583359dfeecf1977f5b22d9b5036fac713777f55578ff287f45ac1cff8f873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54529741fb648b8ebcd4d74f713ef86e33e43308b757e83dcc39ce916a404aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87b7958ce921af08a8638b3167621dcfab1625031fcf4321b921b0691184f7d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__423c541ee371fdd20f19889b593c02cc39c812f9f6c0f1042949b5cfca22a115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocol")
    def ip_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipProtocol"))

    @ip_protocol.setter
    def ip_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da4b81b9c4f551398bbb2ffd8d7865a2083c8b6d92bd559576529fd7f49e005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42298204eac59c5004d21070ac35f081ec54c277ffdf4f081ba234d85e9de73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUrl")
    def network_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUrl"))

    @network_url.setter
    def network_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0440392339f4ebf2f09baff961f08b5fadac61ffea0f5f0ed3d024f572c1b1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb6d4a9937ee769777a93cac2e9969636216804c281d3ae1bdd5d48f5aa69f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a51b30b850e719c784a81667f5eb719d9b621b4d5d527d3cc483bfee392ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030ff227907a8a06bdaea53b8bf5b0f8159da757e9f64df7ff842792028849a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7416b55fa9de990f7b84bd2e74c6a897e31e6a0b12ef8e7b03f85bbf8e4db8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__485433eacb3043c6f69bd2237897c3ecbfde35e1ed65353b3b286d74d123e8f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalLoadBalancers")
    def put_internal_load_balancers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea880b4e8297d2164b4405e621bfdbc46a062cca9b4e53d3290985ead2e30501)
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
    ) -> DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList:
        return typing.cast(DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList, jsii.get(self, "internalLoadBalancers"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpointsInput")
    def external_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancersInput")
    def internal_load_balancers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]], jsii.get(self, "internalLoadBalancersInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEndpoints")
    def external_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalEndpoints"))

    @external_endpoints.setter
    def external_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848bbe15e01d86e748f1d7407c893810b33a5db1f9d0ad79b036d4dc4f72ec6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf2c656df42a4ce718e8a36649e57dbbc82cf987de6a92869d6fd51936be9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyWrrList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa2e00156a258cebbc4b646ac3e9b526d82881bf1debb7c7f38b0cea8ab900d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DnsRecordSetRoutingPolicyWrrOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4358f792741802a552c277fedad4af1a7f1170686c9bee9e6e7881217eb8c1fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DnsRecordSetRoutingPolicyWrrOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81e1740f40d0b6937d2e2fbb6d2a35e7637f44ce27b19b11cf93f11c8f83db3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c81ea1ad6a436a095c1082f457310c3030b9038abb77f60f2cc8fada265f338a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1109047249b060ec692304060b3a9313da706b57e37f1a9f5f0c720438aaaca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d55d4d91c32af0a9dd2270dd1fbfe9849dc0545962c3edd2a45434d3e74dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DnsRecordSetRoutingPolicyWrrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dnsRecordSet.DnsRecordSetRoutingPolicyWrrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c38bcdef0fae1346f54903913f169e194a3bc67deefdfae4075e5a27e5b65dc1)
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
        internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param external_endpoints: The Internet IP addresses to be health checked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#external_endpoints DnsRecordSet#external_endpoints}
        :param internal_load_balancers: internal_load_balancers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dns_record_set#internal_load_balancers DnsRecordSet#internal_load_balancers}
        '''
        value = DnsRecordSetRoutingPolicyWrrHealthCheckedTargets(
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
    ) -> DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference:
        return typing.cast(DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference, jsii.get(self, "healthCheckedTargets"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckedTargetsInput")
    def health_checked_targets_input(
        self,
    ) -> typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets]:
        return typing.cast(typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets], jsii.get(self, "healthCheckedTargetsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a2b0f7b9760a98474fc205a1417b03c65d0b0c9e39c5769e200e329f13027bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rrdatas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc6dc4ba3061ef093ba7ef93b64a502467b6de4a1deee5b618098d702bf22a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrr]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrr]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrr]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ffc70373c20a7e65fa24dda2d3991704a96b8657336e9e92d6ae562160795a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DnsRecordSet",
    "DnsRecordSetConfig",
    "DnsRecordSetRoutingPolicy",
    "DnsRecordSetRoutingPolicyGeo",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargets",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsOutputReference",
    "DnsRecordSetRoutingPolicyGeoList",
    "DnsRecordSetRoutingPolicyGeoOutputReference",
    "DnsRecordSetRoutingPolicyOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackup",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoList",
    "DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimary",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyPrimaryBackupPrimaryOutputReference",
    "DnsRecordSetRoutingPolicyWrr",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargets",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersList",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancersOutputReference",
    "DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsOutputReference",
    "DnsRecordSetRoutingPolicyWrrList",
    "DnsRecordSetRoutingPolicyWrrOutputReference",
]

publication.publish()

def _typecheckingstub__6dc80a5b5fa7ebaac7357ab91688e2c9551dd1b3ace8607f53bfd18fad3c9fb3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    managed_zone: builtins.str,
    name: builtins.str,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    routing_policy: typing.Optional[typing.Union[DnsRecordSetRoutingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7b283fe049031d9086d1ce5d7bd70e4ebca2538155f71e1c2b976f7c6a48e875(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050a9500c570031429c3bb80ff8573b1bb6317894a9f97607e59bede72e7fb74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfb6f990de9acbd036628da3a90c663a00cad31617cd0a1a1e52043d3018ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d52d993d10753cdeadad995fc9b8f89a8a4ff36d0562ba52236511027181b14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e56248dff56bd3df564920096e01a73832203d11b36565efea9a9457a52eb17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe85caef8010e8a17393180701ff35c38ce6a3d257cbde19b916d5df2fa646e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517269ec34358cda924a62221bf552e56d893a4d5db126ab0a0a164326ac8fe6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79eb3afe959908e588498a8db46baff558a85ab11f5a2693422c4b89ce3913c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8298b7750ae475388725d4ab10c48ee5478e537a4fcf002f8ffea0c638c52c8b(
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
    routing_policy: typing.Optional[typing.Union[DnsRecordSetRoutingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f732d616e785af192ec01da07894101c28e293ad4565b6ec334e51e0bc77110(
    *,
    enable_geo_fencing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    geo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health_check: typing.Optional[builtins.str] = None,
    primary_backup: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    wrr: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrr, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f7bf95a1e64cf70490ed35d29a32b547e372d249c6657d5b5374b7c5e9ebe4(
    *,
    location: builtins.str,
    health_checked_targets: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c27151c6a1da6d067c1e7127f245274e783144931c1bd277aad8bbb49d45084(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f018ef8cf4c295e895ff632dfbedb97f8826556a7ebf56ecfadd9dd2670eec4e(
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

def _typecheckingstub__0755fe14da6c3213e1cca6c470e01749160a74c097b44d5ad901b189cef6dd09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0d4a66a7e22677adcbe06188113facdc5983f8f1cfc6e70bd9b96d899c4eb8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93c6450afe7b395b00c97c64756bc344d04d63b7e071a7c341b8179ed4fa583(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cb73d2f209d00968189aa2b8b3e6cf7c7c450a7476682c3f35ab05ebcf68cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c971cdadd5eca710b52f642d83e982323882481dc2ac1eedfeba48ec10437190(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08cc80206256c2a66b008f7266948cdbf31e9fd040bc286f7cd6dac55fcbf27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6749fc2544033550e8c827ea23909a1c661bcc0b4d773b72bb1314c3f0a75c3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d49527424997791735f7800c978ab2ffb553eed668f4343137134154fb02321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d967648f8f92e6528a0c70490bdf419d0e276bd89d7e388db4ac065e089d763b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f2bae4cc8d5b0b27daba8c4a70d7d445f1dffc477119b1a3f2d139bc5a3f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8ee0ae35a0e6046770c545945235450035b6b3a52e2800acadeffbbe47e0ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39873638b5a5468b97618cc441ccd5c8ccf0137111f743fda034b31d9ce6cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bf083d6287578c30d1b622893938f800ada13c4cf8cb695d7633fad7c8f828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e97284c2519f6f2278e09cc0a4bd8e5ee61b82264fbf97eafe6b8c53fb8ffc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb5fcd5c852aeb24886029d2f3dc8029750d4617fa8bc25b533192f56b17fbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d555e2de6f265c210f45fbb704f811a4acd6e9331184f374e1c5e842f905eda7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a5d2b11a3677b213e2b18375ea2a7e77e4ff56ce781660625514597e26b279(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df75efcc59e5b3a1db34457266897a817f63dfb1f3ebc0d94cdb2924ab1ef4b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e5d6fd22bfa57f8ca8906eb72fcc9b9139480fe941406a167e503059311d87(
    value: typing.Optional[DnsRecordSetRoutingPolicyGeoHealthCheckedTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d4e196a13f50ec5428088a5bc38f586dfbfa76b3e6da9a88f46264f9093d13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1afffb6af8763167bc2bc61b04c4f30120d2c73e69f113f95b2f4605a5a6359(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80689996a1c3904d9f6c0028270a90c577c2296eeb7988a467c1e94ecaf9eee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef3789d05c8d3476b8f0d6b67a8ad4c07448833673367c0ca1ec199ed642389(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d93a1679b7a06c9154f1253c2b9037ce7293758562a0d477f80d07f0b4d616c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008e391abad0133dab77beb5ee943d93cd5b94be8b133621823d7e0e49b24fb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyGeo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b8ee0db31d6952292ea49a2ed570dc882244c3b78b8daf6a2d9b57f9e533d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0658e6882b6e2c9ca9fecc640547d4cff796e526ac4761af9ec2d8171ed58cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2074cdaacfdd795954485823408de8ebf577a8efed107e2056990cde018d228b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b10ab4b699841fa71ae9b022e5b8f4c6d0b9b37a92fdb6f0626e1a3e662cde0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyGeo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b892adadc86e297d302e0b0e5f73b8e6a5787a5dddde67e73b8a25060ec3161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832308d273a442fa8861171f65f979e78c82a02a241baea6f510c3d8d8a0b047(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyGeo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365c85f310db5ae97ee89350b0bd10d653676a3cbe6187fb2f23453a357bffa3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrr, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bc632d6c6e816846c0345ff991a4c1448408c1fd0c62b1dd3d9b3d83d2a334(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ff61f2e7ddc049637ed366be9a2dd597fa5ca907788323c7ec9b6ebf5f7581(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcc0d39996472754acaa4a8d92eb49549d89feefa8666b56fb109095561a910(
    value: typing.Optional[DnsRecordSetRoutingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23212610ae285d98bec0608b759130bf5122645ebafbe71c58b15076b3f873a(
    *,
    backup_geo: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[builtins.str, typing.Any]]]],
    primary: typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimary, typing.Dict[builtins.str, typing.Any]],
    enable_geo_fencing_for_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trickle_ratio: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0077678ddbca2ebdd5657ffb55d2502872b3319e4decf1333d4a7abb6ee3012(
    *,
    location: builtins.str,
    health_checked_targets: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5e59b5ba540d8fd616d342b38c932487a0bf1c3089c18ac55475389304d3ab(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9f707a825ca7a1ed76b25d016af3e39165a1b6514dcfba679e95af76d5ef02(
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

def _typecheckingstub__073cce1bf851de4e9d2f6bb0730b10a8c09070d06457db918668af5d1ccf96ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec91bd1735534e22e8f6b2eecc75b18df3df51aae8f669e9fdf609ceded1c658(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce2f9a84754302d47610c578e2ebee0ca217dd8dd3b4f1a7d66bf37f3eb6de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8df8aaf65d4e601b2318196762ee829ccba6b4ac30d2bcb2ef4ede6e7e1108a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74449ca4f11a6c6155b17a7d599c86862f745a8c379707ef478b7d733ec1a53a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf32b0a12e0e74a8ae0e5eb9a6d15352b710f66f86a07bab92a8cd87164f6a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2835a2fde630c1a6b25e52306b2c4c50ee8e1f8b9b9d5220ddd8211ecd9e3f27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298708f437a5c7eac5b16095b9d16ef11e26dd9e50dc28539a241d4c2392348f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414ce257106f2811545945e8c0686c6a896a5de4d4b368ecaab09990bcf52abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e8a1fbef77ec5175163dc50f04ef74380bf8fef31658e1026a7ba4d79c07e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4461fe78ef9c895c3666f624b77dcc5572c240f9917de0ea873824e2ec7af10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98c85726a4ce2d68994c5d75cd727320fca28a6fdda200666616b8030f851fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd431bb2eb88294a97735eecbe6a21da69e94670aebdfcbc3777f7df785d6d95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5a47d820b8f7cad09443184b6044b2a9e3524f061db3a0d0180b4935bd6ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25faaf3acc83f03bbbe639866cf427d5b53e1169bb7ae7f75faccb257b46c722(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0590f53143722090173eae6e6a1128a1b67a4c8cf6a1d53cb3fb3a14df63a76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c56aaef9714c74fd67c5bd8817f8e0e3eb166b3930b61f290bef933febf87ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625908e2fe7218fd1653592183eafc7da6e7b263b0b5dfbffc98de411d10b124(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3350f8393d4feb30abf0c15323e62e06422fe2ba262b902e19f13ebc9b04c7(
    value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeoHealthCheckedTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36e8553954ff88fcd2b00d5101625b1329fcf780746884de14f9616d6e2559c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256077eb4912952a1a2b33f888bfa485b09163262bf7966600eaa863c3a45f0a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a30fcd19d35b5c3d1628a5cf9df696952bc47bd10961d3e6659becb3c16cb91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9db656d086315851fe97e79e58aa0ae102734795a73e157f55624e90d19a7cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf20b5ad3e61083d1edb691ae2c48a5ee28dc58d676fed354c1e7d7acb42cb51(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dcfc4c2884fb678e23cba566790ddc67393eb8d441963ffc3a80d4adbac333(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a37d74aa42f918cbdc6a5096d47410f3ab1b0def4c3877ea16552fa0d375b07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fc3860a6231abca00fdc2e1faea3378ee2a5b15ab139d0a06a357737552eef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc89b69795c820935de3cc4651ece59ec31e8cd78610c75922ca03661fca6fb1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51094923e04814474bb4106fde02bfbc8b8ef587f374248a2a79c6f8790cac82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb47532b5c28bf1811a985b4d8b87f3cf5dff5ec139fe3c238e68eaf09dfd300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c4994a92696d14a8db6f715c6fdb87b50bfe3a888cbba1f5914b2855d71eaf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupBackupGeo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3f2db58a040e942410515880d926c66d5f2cca66558a3ed88a5ca1ba36a1e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c12c8f4de3348fa8a9109c128e5a1dd588dc9a265a388505699f613cf439948(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1e93d42e80b430ccc6b533eed97ebd965ffe4bc551c74555b283e06145cded(
    value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd427925c6907b1bc75cc9983a428093611aee986ed133e1bfa608ca56246ed0(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cc893deb4aab23148afa5fa081ab7869f48de5bb1e8bac744f5013fe89bfcc(
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

def _typecheckingstub__820fd56d78308ed0087e13d3c91666ff62c4f6d211de35f1200f4118233d6430(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f6f9af2b69e6a5568e35af0e732f885641d737b454b4704515c9da151a1237(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1647ac8a61c98d352f051c9dda8f5eb1db075fe56b35bb26adb780715fc66ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e7056c7d081ab0e5d3369f6645195acbcf3f1b6d45876f004bdd003750d8b0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17ea5c3e98f74c294d8a7e4f793d4a0be172d47e4f3c568cffb18cab697fdf9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47138a81422443cf51bf731c6fc8299da08cbc3b2f2d9fd9b5351c36648dfd7c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb618d010338dc83c91e0c34abd0b9c7fdb55930b6ea5c2501304123a8cc236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b63ef1de51003ceed628b8910c9d5732b2830602f57c072b3fdc83f484885dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866fcaa99e921236a46d44256e14689b22d59e35de5aa166004f24ec8865c9f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7be3b621f753d1a6f98db79411b1fe664512beaba6e057d7579dec4dddcb043(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adce2404c9f9e3af108d66f9b7b607f10ace441bd50aaa4f861e2420eac8592d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9c863f714c06213674f9efb4615f9cd74fa6fa89fd975ccb0059e4e029efc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ade44b7270d824b51854b642640dc59156447d0cb6eec72e269cc479849114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7a6f903e2eaa92eb1922d8e0918248e353f76d646efba4a239e663d91ef6f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd070654a4d6530f0fe414ded0dc5fb4a76ddb45a3bb7a3bdf610d15debbbc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75e80ce28a0a72b828cb24dfac5a40fef6831f794453d2c372899c675d2b9f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d1889a380f69273c69f6b3a1fd86127d0d9c6c2383ea208050d146dd6f715e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyPrimaryBackupPrimaryInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31195b16413231ce484c91223653ca73032d49caca40d07bdd9d68c9f9193b25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49992dddb547c43deb593f3861bbb1a8d6be692e4024e4e4de60eeca9a66b643(
    value: typing.Optional[DnsRecordSetRoutingPolicyPrimaryBackupPrimary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7e35a41e501ffbc848172e70e4ed9a8f962bd90787d7de398025dbaee30a36(
    *,
    weight: jsii.Number,
    health_checked_targets: typing.Optional[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    rrdatas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c0a912130c7d1900085cf03419fae3e121f71b2bc6bd3d70f1ef18b1df84bd(
    *,
    external_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    internal_load_balancers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61496f9cfffbf035c86b80e2cc4fa1687c991c20d9727ec506fbf2a72ae14c8e(
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

def _typecheckingstub__47575c8af9841a9f5d27ec19cd1c104f52be26c1b1fd9f7a2da049638e50ca70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2b8003608c91df4e42314b14bd1d13e5e47bac582d4dadb6a607e630990ea2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4faaa40b9da50b2ad096a9c46ceb507df4ecf1060565e4b6f42f1d60b5678df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18361646deb7543337f84e17f828749f41a97e2c04110c11b11d471de3b9ced1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c583359dfeecf1977f5b22d9b5036fac713777f55578ff287f45ac1cff8f873(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54529741fb648b8ebcd4d74f713ef86e33e43308b757e83dcc39ce916a404aa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b7958ce921af08a8638b3167621dcfab1625031fcf4321b921b0691184f7d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423c541ee371fdd20f19889b593c02cc39c812f9f6c0f1042949b5cfca22a115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da4b81b9c4f551398bbb2ffd8d7865a2083c8b6d92bd559576529fd7f49e005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42298204eac59c5004d21070ac35f081ec54c277ffdf4f081ba234d85e9de73e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0440392339f4ebf2f09baff961f08b5fadac61ffea0f5f0ed3d024f572c1b1aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb6d4a9937ee769777a93cac2e9969636216804c281d3ae1bdd5d48f5aa69f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a51b30b850e719c784a81667f5eb719d9b621b4d5d527d3cc483bfee392ca7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030ff227907a8a06bdaea53b8bf5b0f8159da757e9f64df7ff842792028849a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7416b55fa9de990f7b84bd2e74c6a897e31e6a0b12ef8e7b03f85bbf8e4db8f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485433eacb3043c6f69bd2237897c3ecbfde35e1ed65353b3b286d74d123e8f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea880b4e8297d2164b4405e621bfdbc46a062cca9b4e53d3290985ead2e30501(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DnsRecordSetRoutingPolicyWrrHealthCheckedTargetsInternalLoadBalancers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848bbe15e01d86e748f1d7407c893810b33a5db1f9d0ad79b036d4dc4f72ec6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf2c656df42a4ce718e8a36649e57dbbc82cf987de6a92869d6fd51936be9ec(
    value: typing.Optional[DnsRecordSetRoutingPolicyWrrHealthCheckedTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2e00156a258cebbc4b646ac3e9b526d82881bf1debb7c7f38b0cea8ab900d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4358f792741802a552c277fedad4af1a7f1170686c9bee9e6e7881217eb8c1fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81e1740f40d0b6937d2e2fbb6d2a35e7637f44ce27b19b11cf93f11c8f83db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81ea1ad6a436a095c1082f457310c3030b9038abb77f60f2cc8fada265f338a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1109047249b060ec692304060b3a9313da706b57e37f1a9f5f0c720438aaaca0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d55d4d91c32af0a9dd2270dd1fbfe9849dc0545962c3edd2a45434d3e74dfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DnsRecordSetRoutingPolicyWrr]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38bcdef0fae1346f54903913f169e194a3bc67deefdfae4075e5a27e5b65dc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b0f7b9760a98474fc205a1417b03c65d0b0c9e39c5769e200e329f13027bd1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc6dc4ba3061ef093ba7ef93b64a502467b6de4a1deee5b618098d702bf22a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ffc70373c20a7e65fa24dda2d3991704a96b8657336e9e92d6ae562160795a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DnsRecordSetRoutingPolicyWrr]],
) -> None:
    """Type checking stubs"""
    pass
