r'''
# `opentelekomcloud_lts_cross_account_access_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lts_cross_account_access_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2).
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


class LtsCrossAccountAccessV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCrossAccountAccessV2.LtsCrossAccountAccessV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2 opentelekomcloud_lts_cross_account_access_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        agency_domain_name: builtins.str,
        agency_name: builtins.str,
        agency_project_id: builtins.str,
        log_agency_group_id: builtins.str,
        log_agency_group_name: builtins.str,
        log_agency_stream_id: builtins.str,
        log_agency_stream_name: builtins.str,
        log_group_id: builtins.str,
        log_group_name: builtins.str,
        log_stream_id: builtins.str,
        log_stream_name: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2 opentelekomcloud_lts_cross_account_access_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param agency_domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_domain_name LtsCrossAccountAccessV2#agency_domain_name}.
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_name LtsCrossAccountAccessV2#agency_name}.
        :param agency_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_project_id LtsCrossAccountAccessV2#agency_project_id}.
        :param log_agency_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_group_id LtsCrossAccountAccessV2#log_agency_group_id}.
        :param log_agency_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_group_name LtsCrossAccountAccessV2#log_agency_group_name}.
        :param log_agency_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_stream_id LtsCrossAccountAccessV2#log_agency_stream_id}.
        :param log_agency_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_stream_name LtsCrossAccountAccessV2#log_agency_stream_name}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_group_id LtsCrossAccountAccessV2#log_group_id}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_group_name LtsCrossAccountAccessV2#log_group_name}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_stream_id LtsCrossAccountAccessV2#log_stream_id}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_stream_name LtsCrossAccountAccessV2#log_stream_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#name LtsCrossAccountAccessV2#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#id LtsCrossAccountAccessV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#tags LtsCrossAccountAccessV2#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a47a7fc2cb516ab82f5842dd230f1899ef6a0af97c5802f5a027500fbaceeb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LtsCrossAccountAccessV2Config(
            agency_domain_name=agency_domain_name,
            agency_name=agency_name,
            agency_project_id=agency_project_id,
            log_agency_group_id=log_agency_group_id,
            log_agency_group_name=log_agency_group_name,
            log_agency_stream_id=log_agency_stream_id,
            log_agency_stream_name=log_agency_stream_name,
            log_group_id=log_group_id,
            log_group_name=log_group_name,
            log_stream_id=log_stream_id,
            log_stream_name=log_stream_name,
            name=name,
            id=id,
            tags=tags,
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
        '''Generates CDKTF code for importing a LtsCrossAccountAccessV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LtsCrossAccountAccessV2 to import.
        :param import_from_id: The id of the existing LtsCrossAccountAccessV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LtsCrossAccountAccessV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1b1e1c1e6fdd1209bb70b311904fe3c82506449738aa5a14cb1d430c903311)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="accessConfigType")
    def access_config_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessConfigType"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="agencyDomainNameInput")
    def agency_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyProjectIdInput")
    def agency_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logAgencyGroupIdInput")
    def log_agency_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAgencyGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logAgencyGroupNameInput")
    def log_agency_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAgencyGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logAgencyStreamIdInput")
    def log_agency_stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAgencyStreamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logAgencyStreamNameInput")
    def log_agency_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAgencyStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamIdInput")
    def log_stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyDomainName")
    def agency_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyDomainName"))

    @agency_domain_name.setter
    def agency_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cce1970261d8a6b309d3eba207fb847a1eb2e0f0aa816bf728a6a738d82e94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e784d81f68cb011d09b1ef2a945c07afa5d40df93c5c8596dc294d4be33820f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agencyProjectId")
    def agency_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyProjectId"))

    @agency_project_id.setter
    def agency_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5550183701e5bd55a3a055aac015dcf7c90526bab59cd2b96b17c34784b6d60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150be1a72ed6b66f8988f3e4d514d597eea8b890882a5da5fef3315b3a04c069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAgencyGroupId")
    def log_agency_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAgencyGroupId"))

    @log_agency_group_id.setter
    def log_agency_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3a1d9274ff47c2af78351a30e6f9a167e89ac595498b10b9d33b321e748218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAgencyGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAgencyGroupName")
    def log_agency_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAgencyGroupName"))

    @log_agency_group_name.setter
    def log_agency_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990a3ee844ec3efe0f16bab1959972916ebc5741b3e262d7c647e943f23715a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAgencyGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAgencyStreamId")
    def log_agency_stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAgencyStreamId"))

    @log_agency_stream_id.setter
    def log_agency_stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2a0e2b69bd612711825b1ce0a1afe220b60a731ce8c73920098088eaf8e313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAgencyStreamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAgencyStreamName")
    def log_agency_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAgencyStreamName"))

    @log_agency_stream_name.setter
    def log_agency_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4965ef7c299758427b4f181596af235e87369c4c4fc16c38a4c8de1080e0fa32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAgencyStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d77414d947ec32c08ef04a723b86803762fbe553c41d0a5d5c0a6d77cf34e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362b037e6ee1e72807f1a18f1fb3554d3b658a82f0ed5245d907cbc7537aadce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamId")
    def log_stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamId"))

    @log_stream_id.setter
    def log_stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a0dd3284331026243da67b499134dfdf35a89c2930f9fb85ae36237928f6a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3456c85fe42049d4cb33336ed07b5e040adffceb8d7381397554209973ce56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1604aed5cdfc7cd770cd528071131d79031c30a9227dc2a0931ef5145c7e203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b3da81e11bb6665149cc1dccfdd11bbcd31f8a31b1cd27bdb496ba250b42fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCrossAccountAccessV2.LtsCrossAccountAccessV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "agency_domain_name": "agencyDomainName",
        "agency_name": "agencyName",
        "agency_project_id": "agencyProjectId",
        "log_agency_group_id": "logAgencyGroupId",
        "log_agency_group_name": "logAgencyGroupName",
        "log_agency_stream_id": "logAgencyStreamId",
        "log_agency_stream_name": "logAgencyStreamName",
        "log_group_id": "logGroupId",
        "log_group_name": "logGroupName",
        "log_stream_id": "logStreamId",
        "log_stream_name": "logStreamName",
        "name": "name",
        "id": "id",
        "tags": "tags",
    },
)
class LtsCrossAccountAccessV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        agency_domain_name: builtins.str,
        agency_name: builtins.str,
        agency_project_id: builtins.str,
        log_agency_group_id: builtins.str,
        log_agency_group_name: builtins.str,
        log_agency_stream_id: builtins.str,
        log_agency_stream_name: builtins.str,
        log_group_id: builtins.str,
        log_group_name: builtins.str,
        log_stream_id: builtins.str,
        log_stream_name: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param agency_domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_domain_name LtsCrossAccountAccessV2#agency_domain_name}.
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_name LtsCrossAccountAccessV2#agency_name}.
        :param agency_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_project_id LtsCrossAccountAccessV2#agency_project_id}.
        :param log_agency_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_group_id LtsCrossAccountAccessV2#log_agency_group_id}.
        :param log_agency_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_group_name LtsCrossAccountAccessV2#log_agency_group_name}.
        :param log_agency_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_stream_id LtsCrossAccountAccessV2#log_agency_stream_id}.
        :param log_agency_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_stream_name LtsCrossAccountAccessV2#log_agency_stream_name}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_group_id LtsCrossAccountAccessV2#log_group_id}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_group_name LtsCrossAccountAccessV2#log_group_name}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_stream_id LtsCrossAccountAccessV2#log_stream_id}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_stream_name LtsCrossAccountAccessV2#log_stream_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#name LtsCrossAccountAccessV2#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#id LtsCrossAccountAccessV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#tags LtsCrossAccountAccessV2#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9a66de82f4c1569754438dd01497742f8eadaaae6ad90f555e5271cc31aae3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument agency_domain_name", value=agency_domain_name, expected_type=type_hints["agency_domain_name"])
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument agency_project_id", value=agency_project_id, expected_type=type_hints["agency_project_id"])
            check_type(argname="argument log_agency_group_id", value=log_agency_group_id, expected_type=type_hints["log_agency_group_id"])
            check_type(argname="argument log_agency_group_name", value=log_agency_group_name, expected_type=type_hints["log_agency_group_name"])
            check_type(argname="argument log_agency_stream_id", value=log_agency_stream_id, expected_type=type_hints["log_agency_stream_id"])
            check_type(argname="argument log_agency_stream_name", value=log_agency_stream_name, expected_type=type_hints["log_agency_stream_name"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_id", value=log_stream_id, expected_type=type_hints["log_stream_id"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agency_domain_name": agency_domain_name,
            "agency_name": agency_name,
            "agency_project_id": agency_project_id,
            "log_agency_group_id": log_agency_group_id,
            "log_agency_group_name": log_agency_group_name,
            "log_agency_stream_id": log_agency_stream_id,
            "log_agency_stream_name": log_agency_stream_name,
            "log_group_id": log_group_id,
            "log_group_name": log_group_name,
            "log_stream_id": log_stream_id,
            "log_stream_name": log_stream_name,
            "name": name,
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
    def agency_domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_domain_name LtsCrossAccountAccessV2#agency_domain_name}.'''
        result = self._values.get("agency_domain_name")
        assert result is not None, "Required property 'agency_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agency_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_name LtsCrossAccountAccessV2#agency_name}.'''
        result = self._values.get("agency_name")
        assert result is not None, "Required property 'agency_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agency_project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#agency_project_id LtsCrossAccountAccessV2#agency_project_id}.'''
        result = self._values.get("agency_project_id")
        assert result is not None, "Required property 'agency_project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_agency_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_group_id LtsCrossAccountAccessV2#log_agency_group_id}.'''
        result = self._values.get("log_agency_group_id")
        assert result is not None, "Required property 'log_agency_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_agency_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_group_name LtsCrossAccountAccessV2#log_agency_group_name}.'''
        result = self._values.get("log_agency_group_name")
        assert result is not None, "Required property 'log_agency_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_agency_stream_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_stream_id LtsCrossAccountAccessV2#log_agency_stream_id}.'''
        result = self._values.get("log_agency_stream_id")
        assert result is not None, "Required property 'log_agency_stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_agency_stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_agency_stream_name LtsCrossAccountAccessV2#log_agency_stream_name}.'''
        result = self._values.get("log_agency_stream_name")
        assert result is not None, "Required property 'log_agency_stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_group_id LtsCrossAccountAccessV2#log_group_id}.'''
        result = self._values.get("log_group_id")
        assert result is not None, "Required property 'log_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_group_name LtsCrossAccountAccessV2#log_group_name}.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_stream_id LtsCrossAccountAccessV2#log_stream_id}.'''
        result = self._values.get("log_stream_id")
        assert result is not None, "Required property 'log_stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#log_stream_name LtsCrossAccountAccessV2#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        assert result is not None, "Required property 'log_stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#name LtsCrossAccountAccessV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#id LtsCrossAccountAccessV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cross_account_access_v2#tags LtsCrossAccountAccessV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsCrossAccountAccessV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LtsCrossAccountAccessV2",
    "LtsCrossAccountAccessV2Config",
]

publication.publish()

def _typecheckingstub__54a47a7fc2cb516ab82f5842dd230f1899ef6a0af97c5802f5a027500fbaceeb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    agency_domain_name: builtins.str,
    agency_name: builtins.str,
    agency_project_id: builtins.str,
    log_agency_group_id: builtins.str,
    log_agency_group_name: builtins.str,
    log_agency_stream_id: builtins.str,
    log_agency_stream_name: builtins.str,
    log_group_id: builtins.str,
    log_group_name: builtins.str,
    log_stream_id: builtins.str,
    log_stream_name: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__2a1b1e1c1e6fdd1209bb70b311904fe3c82506449738aa5a14cb1d430c903311(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cce1970261d8a6b309d3eba207fb847a1eb2e0f0aa816bf728a6a738d82e94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e784d81f68cb011d09b1ef2a945c07afa5d40df93c5c8596dc294d4be33820f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5550183701e5bd55a3a055aac015dcf7c90526bab59cd2b96b17c34784b6d60c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150be1a72ed6b66f8988f3e4d514d597eea8b890882a5da5fef3315b3a04c069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3a1d9274ff47c2af78351a30e6f9a167e89ac595498b10b9d33b321e748218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990a3ee844ec3efe0f16bab1959972916ebc5741b3e262d7c647e943f23715a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2a0e2b69bd612711825b1ce0a1afe220b60a731ce8c73920098088eaf8e313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4965ef7c299758427b4f181596af235e87369c4c4fc16c38a4c8de1080e0fa32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d77414d947ec32c08ef04a723b86803762fbe553c41d0a5d5c0a6d77cf34e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362b037e6ee1e72807f1a18f1fb3554d3b658a82f0ed5245d907cbc7537aadce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a0dd3284331026243da67b499134dfdf35a89c2930f9fb85ae36237928f6a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3456c85fe42049d4cb33336ed07b5e040adffceb8d7381397554209973ce56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1604aed5cdfc7cd770cd528071131d79031c30a9227dc2a0931ef5145c7e203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b3da81e11bb6665149cc1dccfdd11bbcd31f8a31b1cd27bdb496ba250b42fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9a66de82f4c1569754438dd01497742f8eadaaae6ad90f555e5271cc31aae3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    agency_domain_name: builtins.str,
    agency_name: builtins.str,
    agency_project_id: builtins.str,
    log_agency_group_id: builtins.str,
    log_agency_group_name: builtins.str,
    log_agency_stream_id: builtins.str,
    log_agency_stream_name: builtins.str,
    log_group_id: builtins.str,
    log_group_name: builtins.str,
    log_stream_id: builtins.str,
    log_stream_name: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
