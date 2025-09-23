r'''
# `aws_appsync_api`

Refer to the Terraform Registry for docs: [`aws_appsync_api`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api).
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


class AppsyncApi(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApi",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api aws_appsync_api}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        event_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        owner_contact: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api aws_appsync_api} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#name AppsyncApi#name}.
        :param event_config: event_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#event_config AppsyncApi#event_config}
        :param owner_contact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#owner_contact AppsyncApi#owner_contact}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#region AppsyncApi#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#tags AppsyncApi#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca1c10c22362405c4a2e2e8484b3b1f072456b9a957c16c969f234a11cf7e49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AppsyncApiConfig(
            name=name,
            event_config=event_config,
            owner_contact=owner_contact,
            region=region,
            tags=tags,
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
        '''Generates CDKTF code for importing a AppsyncApi resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsyncApi to import.
        :param import_from_id: The id of the existing AppsyncApi that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsyncApi to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277e93108b7b223b8ed5bfd2b045f5c306357b2c54cd7a7c2d47f9652bd23a1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventConfig")
    def put_event_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fe6dcc9e0434c50ef092c46cdf5330f3f93fd7bb9076c789732d0daeb4adb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventConfig", [value]))

    @jsii.member(jsii_name="resetEventConfig")
    def reset_event_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventConfig", []))

    @jsii.member(jsii_name="resetOwnerContact")
    def reset_owner_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnerContact", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="apiArn")
    def api_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiArn"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="eventConfig")
    def event_config(self) -> "AppsyncApiEventConfigList":
        return typing.cast("AppsyncApiEventConfigList", jsii.get(self, "eventConfig"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="wafWebAclArn")
    def waf_web_acl_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wafWebAclArn"))

    @builtins.property
    @jsii.member(jsii_name="xrayEnabled")
    def xray_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "xrayEnabled"))

    @builtins.property
    @jsii.member(jsii_name="eventConfigInput")
    def event_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfig"]]], jsii.get(self, "eventConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerContactInput")
    def owner_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerContactInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee94b2ec335d433524d563474b0721151ee2c37a6d01e9e89fb1e435ca3d3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ownerContact")
    def owner_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerContact"))

    @owner_contact.setter
    def owner_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85585fcb79a76ca7bc15e534919b69dc7b5b763892b27c6c1cea3632700b474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerContact", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4374b7bbfb9078b7e91b60db9d01cbbc0c8e27a3b29a18a8646dd66849a31e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b104ebe7d5d91a306064af615dac9fa37fb991a24edfa04bfa8c9b33d011f771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "event_config": "eventConfig",
        "owner_contact": "ownerContact",
        "region": "region",
        "tags": "tags",
    },
)
class AppsyncApiConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        event_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        owner_contact: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#name AppsyncApi#name}.
        :param event_config: event_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#event_config AppsyncApi#event_config}
        :param owner_contact: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#owner_contact AppsyncApi#owner_contact}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#region AppsyncApi#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#tags AppsyncApi#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad87ebf36f83aa9d14c51acad2882816dd1f4cf6c20d8560913506ec82797c2b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument event_config", value=event_config, expected_type=type_hints["event_config"])
            check_type(argname="argument owner_contact", value=owner_contact, expected_type=type_hints["owner_contact"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if event_config is not None:
            self._values["event_config"] = event_config
        if owner_contact is not None:
            self._values["owner_contact"] = owner_contact
        if region is not None:
            self._values["region"] = region
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#name AppsyncApi#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfig"]]]:
        '''event_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#event_config AppsyncApi#event_config}
        '''
        result = self._values.get("event_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfig"]]], result)

    @builtins.property
    def owner_contact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#owner_contact AppsyncApi#owner_contact}.'''
        result = self._values.get("owner_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#region AppsyncApi#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#tags AppsyncApi#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auth_provider": "authProvider",
        "connection_auth_mode": "connectionAuthMode",
        "default_publish_auth_mode": "defaultPublishAuthMode",
        "default_subscribe_auth_mode": "defaultSubscribeAuthMode",
        "log_config": "logConfig",
    },
)
class AppsyncApiEventConfig:
    def __init__(
        self,
        *,
        auth_provider: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigAuthProvider", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigConnectionAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_publish_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigDefaultPublishAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_subscribe_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigDefaultSubscribeAuthMode", typing.Dict[builtins.str, typing.Any]]]]] = None,
        log_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigLogConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param auth_provider: auth_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_provider AppsyncApi#auth_provider}
        :param connection_auth_mode: connection_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#connection_auth_mode AppsyncApi#connection_auth_mode}
        :param default_publish_auth_mode: default_publish_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#default_publish_auth_mode AppsyncApi#default_publish_auth_mode}
        :param default_subscribe_auth_mode: default_subscribe_auth_mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#default_subscribe_auth_mode AppsyncApi#default_subscribe_auth_mode}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#log_config AppsyncApi#log_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5032e9a16cb19ed83db3c5ee9ad8dddf7741601e4fe759f495da1304296bb0fe)
            check_type(argname="argument auth_provider", value=auth_provider, expected_type=type_hints["auth_provider"])
            check_type(argname="argument connection_auth_mode", value=connection_auth_mode, expected_type=type_hints["connection_auth_mode"])
            check_type(argname="argument default_publish_auth_mode", value=default_publish_auth_mode, expected_type=type_hints["default_publish_auth_mode"])
            check_type(argname="argument default_subscribe_auth_mode", value=default_subscribe_auth_mode, expected_type=type_hints["default_subscribe_auth_mode"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_provider is not None:
            self._values["auth_provider"] = auth_provider
        if connection_auth_mode is not None:
            self._values["connection_auth_mode"] = connection_auth_mode
        if default_publish_auth_mode is not None:
            self._values["default_publish_auth_mode"] = default_publish_auth_mode
        if default_subscribe_auth_mode is not None:
            self._values["default_subscribe_auth_mode"] = default_subscribe_auth_mode
        if log_config is not None:
            self._values["log_config"] = log_config

    @builtins.property
    def auth_provider(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProvider"]]]:
        '''auth_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_provider AppsyncApi#auth_provider}
        '''
        result = self._values.get("auth_provider")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProvider"]]], result)

    @builtins.property
    def connection_auth_mode(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigConnectionAuthMode"]]]:
        '''connection_auth_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#connection_auth_mode AppsyncApi#connection_auth_mode}
        '''
        result = self._values.get("connection_auth_mode")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigConnectionAuthMode"]]], result)

    @builtins.property
    def default_publish_auth_mode(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigDefaultPublishAuthMode"]]]:
        '''default_publish_auth_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#default_publish_auth_mode AppsyncApi#default_publish_auth_mode}
        '''
        result = self._values.get("default_publish_auth_mode")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigDefaultPublishAuthMode"]]], result)

    @builtins.property
    def default_subscribe_auth_mode(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigDefaultSubscribeAuthMode"]]]:
        '''default_subscribe_auth_mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#default_subscribe_auth_mode AppsyncApi#default_subscribe_auth_mode}
        '''
        result = self._values.get("default_subscribe_auth_mode")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigDefaultSubscribeAuthMode"]]], result)

    @builtins.property
    def log_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigLogConfig"]]]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#log_config AppsyncApi#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigLogConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProvider",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "cognito_config": "cognitoConfig",
        "lambda_authorizer_config": "lambdaAuthorizerConfig",
        "openid_connect_config": "openidConnectConfig",
    },
)
class AppsyncApiEventConfigAuthProvider:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        cognito_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigAuthProviderCognitoConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_authorizer_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        openid_connect_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncApiEventConfigAuthProviderOpenidConnectConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.
        :param cognito_config: cognito_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#cognito_config AppsyncApi#cognito_config}
        :param lambda_authorizer_config: lambda_authorizer_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#lambda_authorizer_config AppsyncApi#lambda_authorizer_config}
        :param openid_connect_config: openid_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#openid_connect_config AppsyncApi#openid_connect_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d78675ff9b03c000d84912a098552c244d93794a9179265c5a0f09e980206c)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument cognito_config", value=cognito_config, expected_type=type_hints["cognito_config"])
            check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
            check_type(argname="argument openid_connect_config", value=openid_connect_config, expected_type=type_hints["openid_connect_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }
        if cognito_config is not None:
            self._values["cognito_config"] = cognito_config
        if lambda_authorizer_config is not None:
            self._values["lambda_authorizer_config"] = lambda_authorizer_config
        if openid_connect_config is not None:
            self._values["openid_connect_config"] = openid_connect_config

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cognito_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProviderCognitoConfig"]]]:
        '''cognito_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#cognito_config AppsyncApi#cognito_config}
        '''
        result = self._values.get("cognito_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProviderCognitoConfig"]]], result)

    @builtins.property
    def lambda_authorizer_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig"]]]:
        '''lambda_authorizer_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#lambda_authorizer_config AppsyncApi#lambda_authorizer_config}
        '''
        result = self._values.get("lambda_authorizer_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig"]]], result)

    @builtins.property
    def openid_connect_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProviderOpenidConnectConfig"]]]:
        '''openid_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#openid_connect_config AppsyncApi#openid_connect_config}
        '''
        result = self._values.get("openid_connect_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncApiEventConfigAuthProviderOpenidConnectConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigAuthProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderCognitoConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aws_region": "awsRegion",
        "user_pool_id": "userPoolId",
        "app_id_client_regex": "appIdClientRegex",
    },
)
class AppsyncApiEventConfigAuthProviderCognitoConfig:
    def __init__(
        self,
        *,
        aws_region: builtins.str,
        user_pool_id: builtins.str,
        app_id_client_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#aws_region AppsyncApi#aws_region}.
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#user_pool_id AppsyncApi#user_pool_id}.
        :param app_id_client_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#app_id_client_regex AppsyncApi#app_id_client_regex}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c22f989bda5580be9ac56f033350afe23ad873b678af937d455a0ca8b452d6)
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_region": aws_region,
            "user_pool_id": user_pool_id,
        }
        if app_id_client_regex is not None:
            self._values["app_id_client_regex"] = app_id_client_regex

    @builtins.property
    def aws_region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#aws_region AppsyncApi#aws_region}.'''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#user_pool_id AppsyncApi#user_pool_id}.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id_client_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#app_id_client_regex AppsyncApi#app_id_client_regex}.'''
        result = self._values.get("app_id_client_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigAuthProviderCognitoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigAuthProviderCognitoConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderCognitoConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__448fb1c88e6e600abd7951b5099de9d8198630dd8e2d6231c2dcd2fb78193668)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigAuthProviderCognitoConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd8a41934cbb6f10db172e674b067e1f9b539d46a3f87e4229b08369d38acbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigAuthProviderCognitoConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c843d3ac6f06533170d2999e0ca6fb2eafa6b836e4fbf1456b738fb4845db76b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a908ca8f86220ab45005625088bcd74f822f2a1ee14c2d9b4ef1d86530c7d164)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72002fa29c816d0099068a6108b1c939592c0f92cbdc306c440e9ef6677ce2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderCognitoConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderCognitoConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderCognitoConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484bd8eb980da6b8a8f7ae651aaafaee391f61dbea7b792c2d3b77d7c46365ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigAuthProviderCognitoConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderCognitoConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a44cb18f36fda165f5d90c6930ca85449a4d07940161625243e52d9ca28590)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAppIdClientRegex")
    def reset_app_id_client_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppIdClientRegex", []))

    @builtins.property
    @jsii.member(jsii_name="appIdClientRegexInput")
    def app_id_client_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdClientRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionInput")
    def aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolIdInput")
    def user_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appIdClientRegex")
    def app_id_client_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appIdClientRegex"))

    @app_id_client_regex.setter
    def app_id_client_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1d5200e7ec3ac607733283f812493ef1fb4b0fe7f840f2eff90d1cf2ddddc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appIdClientRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda88753f256fb2d6202f10f10304a4443c287c1b4362c002db0d7a9758b8508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolId"))

    @user_pool_id.setter
    def user_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6f18339eb0e9af5e79080ff1988a462142d56cf925f2da6eaee85b766df087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderCognitoConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderCognitoConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderCognitoConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1018cc7dbadf1438bc863a68c70f7cdb19bd077a550ba7c4311b65526008a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_uri": "authorizerUri",
        "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
        "identity_validation_expression": "identityValidationExpression",
    },
)
class AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig:
    def __init__(
        self,
        *,
        authorizer_uri: builtins.str,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#authorizer_uri AppsyncApi#authorizer_uri}.
        :param authorizer_result_ttl_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#authorizer_result_ttl_in_seconds AppsyncApi#authorizer_result_ttl_in_seconds}.
        :param identity_validation_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#identity_validation_expression AppsyncApi#identity_validation_expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbbdc01cc154c80cefd7b2666cbfa2ff7454e60476362970c4bb8df56df6cdf)
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
            check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
            check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_uri": authorizer_uri,
        }
        if authorizer_result_ttl_in_seconds is not None:
            self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if identity_validation_expression is not None:
            self._values["identity_validation_expression"] = identity_validation_expression

    @builtins.property
    def authorizer_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#authorizer_uri AppsyncApi#authorizer_uri}.'''
        result = self._values.get("authorizer_uri")
        assert result is not None, "Required property 'authorizer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#authorizer_result_ttl_in_seconds AppsyncApi#authorizer_result_ttl_in_seconds}.'''
        result = self._values.get("authorizer_result_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#identity_validation_expression AppsyncApi#identity_validation_expression}.'''
        result = self._values.get("identity_validation_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__905af29662f88d449b8d898178f62ee833a182ecabf915d143b8b5ce4ec3bf0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9985f6a79e6f6ac12d80ff35bde79d13c8448488dcf79786f042850b4f76c877)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1015cf6efc8e787f1695de107df987980461c4cb50c9250ac6c42f983c1acfa4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f6cfb12a75a4f69548ee857454e7b82eba65e2edb5bb8cf75977045e569dcba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a226ad95e02d8ab5143a5f7edbd721f53132df8f751f66e4b298b1fd2e857ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623a2198c523d11aa58cc9b0a49e0b3f35f5c5e475f6ee43e285328181705948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5aa54db8972c67764d9eb53f53e59138bba39f285ff65044bb7bc5481b8c289)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAuthorizerResultTtlInSeconds")
    def reset_authorizer_result_ttl_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerResultTtlInSeconds", []))

    @jsii.member(jsii_name="resetIdentityValidationExpression")
    def reset_identity_validation_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityValidationExpression", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSecondsInput")
    def authorizer_result_ttl_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authorizerResultTtlInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerUriInput")
    def authorizer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpressionInput")
    def identity_validation_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityValidationExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authorizerResultTtlInSeconds"))

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616eaca81317c549e056327c7e14fb76744f882ed7531420a852c13f9c8601a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerResultTtlInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerUri"))

    @authorizer_uri.setter
    def authorizer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69113aaebbd5446b0f485216b531be33e3a1b790ebefad7fa1bbab6f064ce1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityValidationExpression"))

    @identity_validation_expression.setter
    def identity_validation_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba9edeaef83b8eb6c52f18ffd71669d56ae4b8ba1c5d8c20baa0393c59e7409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityValidationExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1848f4255bcd3f1a012e6294d6a2ef9347444448ab8b63ce1135eb2b9e8dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigAuthProviderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe5f7f5e398e289dc0efba6b6d1349f25211c366e9dffb050c4955b2ef75bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigAuthProviderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4db985b52d328a11e1396e9b04ab56cf7220eeb1a924758d0bcd68c6438098f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigAuthProviderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150307156d0bece81636bec414b48955f8e973b8259a83760818fe2114b68c4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1114185f30e3cf82f8fc7a8776135099376fc4d6b2a59f812430da8799e92bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d378a9848a9e6976efd620bcf088e1f926e3cf66928fd4f04aa32a0339c878b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProvider]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProvider]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProvider]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b6f823553c441093829751b47aa096c4fd3053587a609cdd770c8e8f44a0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderOpenidConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "issuer": "issuer",
        "auth_ttl": "authTtl",
        "client_id": "clientId",
        "iat_ttl": "iatTtl",
    },
)
class AppsyncApiEventConfigAuthProviderOpenidConnectConfig:
    def __init__(
        self,
        *,
        issuer: builtins.str,
        auth_ttl: typing.Optional[jsii.Number] = None,
        client_id: typing.Optional[builtins.str] = None,
        iat_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#issuer AppsyncApi#issuer}.
        :param auth_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_ttl AppsyncApi#auth_ttl}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#client_id AppsyncApi#client_id}.
        :param iat_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#iat_ttl AppsyncApi#iat_ttl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123b35c9371ef324fab21b86da13347539dc4828bc9dba85877078ffd90a2548)
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument auth_ttl", value=auth_ttl, expected_type=type_hints["auth_ttl"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument iat_ttl", value=iat_ttl, expected_type=type_hints["iat_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer": issuer,
        }
        if auth_ttl is not None:
            self._values["auth_ttl"] = auth_ttl
        if client_id is not None:
            self._values["client_id"] = client_id
        if iat_ttl is not None:
            self._values["iat_ttl"] = iat_ttl

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#issuer AppsyncApi#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_ttl AppsyncApi#auth_ttl}.'''
        result = self._values.get("auth_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#client_id AppsyncApi#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iat_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#iat_ttl AppsyncApi#iat_ttl}.'''
        result = self._values.get("iat_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigAuthProviderOpenidConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigAuthProviderOpenidConnectConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderOpenidConnectConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55ce587e5431b5c7c0500ab858223cc0aaf8025b80999af70da52132239d18b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigAuthProviderOpenidConnectConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68fb528271a0c1a03ba91a29c37196d68dd57037aca16991fba9e58cc5cdbdf3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigAuthProviderOpenidConnectConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bc2b28dfb2422b4e6f53d21e7d05533dfa08be4e6e470040e819c4f38cc634)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c926b46d68ac2f336bbdbdd1dcf75941d375673293acbb3e089eeeb2cd32d97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6503884ddc8525428da13af472ed0998cd3bf87edfc742d27cd091b5db0ce83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb229baa116abfc962cd7152cbd9f47d94f5a2e475b4a7db75f3098955b4f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigAuthProviderOpenidConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderOpenidConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af67e8552e5db4671876e921d4bcb4ca8f88330f86b228b695e4987b06e0f8ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAuthTtl")
    def reset_auth_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthTtl", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetIatTtl")
    def reset_iat_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIatTtl", []))

    @builtins.property
    @jsii.member(jsii_name="authTtlInput")
    def auth_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="iatTtlInput")
    def iat_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iatTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="authTtl")
    def auth_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authTtl"))

    @auth_ttl.setter
    def auth_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137509a083e76db7f57fe1d6b624893d8097ab319d3ee95f248da3ebb3ac987d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824bff0e4ddd025859fdcf0a0f6e885a1ad056718584575aa610ead9f0b6347a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iatTtl")
    def iat_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iatTtl"))

    @iat_ttl.setter
    def iat_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d298350fcf4e5cbacd593c6fd3a5e06b82dbc24da39e32d9f7b6d624640002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iatTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c20048d4915756bcf7b500218e3ac13a320d7501a73a2ab0df09ea4c255e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderOpenidConnectConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderOpenidConnectConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9300caef9a80e5b601b9188f956d75f9f5fc8315239599b30a1e1d8422df934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigAuthProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigAuthProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dc7cfefbbe2767064b368da3857357a549b43c206f68881d2d9663c4eddc44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCognitoConfig")
    def put_cognito_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderCognitoConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfc313d0ae77d3e2989283553f88db6df0bd719b8927a4c16a8befc808bf612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCognitoConfig", [value]))

    @jsii.member(jsii_name="putLambdaAuthorizerConfig")
    def put_lambda_authorizer_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c1bfab01d76c05860bc8dadaf61b1e889941d37ff4130cb1432bfe155e5899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaAuthorizerConfig", [value]))

    @jsii.member(jsii_name="putOpenidConnectConfig")
    def put_openid_connect_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderOpenidConnectConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37be82fc520939a0929fd1a6bc7475d4dfe1cd6e84ab58fe63151ce1f734121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOpenidConnectConfig", [value]))

    @jsii.member(jsii_name="resetCognitoConfig")
    def reset_cognito_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCognitoConfig", []))

    @jsii.member(jsii_name="resetLambdaAuthorizerConfig")
    def reset_lambda_authorizer_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaAuthorizerConfig", []))

    @jsii.member(jsii_name="resetOpenidConnectConfig")
    def reset_openid_connect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenidConnectConfig", []))

    @builtins.property
    @jsii.member(jsii_name="cognitoConfig")
    def cognito_config(self) -> AppsyncApiEventConfigAuthProviderCognitoConfigList:
        return typing.cast(AppsyncApiEventConfigAuthProviderCognitoConfigList, jsii.get(self, "cognitoConfig"))

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfig")
    def lambda_authorizer_config(
        self,
    ) -> AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigList:
        return typing.cast(AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigList, jsii.get(self, "lambdaAuthorizerConfig"))

    @builtins.property
    @jsii.member(jsii_name="openidConnectConfig")
    def openid_connect_config(
        self,
    ) -> AppsyncApiEventConfigAuthProviderOpenidConnectConfigList:
        return typing.cast(AppsyncApiEventConfigAuthProviderOpenidConnectConfigList, jsii.get(self, "openidConnectConfig"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cognitoConfigInput")
    def cognito_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderCognitoConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderCognitoConfig]]], jsii.get(self, "cognitoConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfigInput")
    def lambda_authorizer_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]], jsii.get(self, "lambdaAuthorizerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="openidConnectConfigInput")
    def openid_connect_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]], jsii.get(self, "openidConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c849edfbaf41efd5e085b23df6d9bab1763f0623083d78ef2fbdc537bf1eb26f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProvider]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProvider]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProvider]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9be942dc08ad0025b11475ff662e39b93d7b199ff35272977854d23701a733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigConnectionAuthMode",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType"},
)
class AppsyncApiEventConfigConnectionAuthMode:
    def __init__(self, *, auth_type: builtins.str) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9509ffab43109087b07fc8bd1bef599b853061da7d61fe6dbd043dc3a6a55ae6)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigConnectionAuthMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigConnectionAuthModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigConnectionAuthModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a123f8616fa62d3b21cbe287eec45cbabbe2dd47c8f7cba4608364d98548e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigConnectionAuthModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae62be8afcbe243dc009d490c0ec22705d7bef348863c2a00169b983478ec22)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigConnectionAuthModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675571f58027ec7bdb9e4243aa4251babb6cbfcfb465f39d680dbd8f8edf0553)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5321948ff47bb90c96356288207dfd51f44db8a38f8cb9ad8e6b68caf1145f39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__966f1c9e53c6409717bca065c7a17ecbf526682087673bc779956d73f6602c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigConnectionAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigConnectionAuthMode]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigConnectionAuthMode]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e525bc2112dc9c3b9029a6a1bf2adab76ba5c2488aa8900388322b054f18414e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigConnectionAuthModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigConnectionAuthModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a3cd3380fdee2a04faab425d1e928e830a6355ad93b683f744f8ba31079d13e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22236b54a78adecf9177aef701ae7283de8a7577551da2292a84cec00c256d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigConnectionAuthMode]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigConnectionAuthMode]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigConnectionAuthMode]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79809dcc6423c61bf24a1e5fee5e83f7f35f4fcb5be4871221aafa9ca981f7d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigDefaultPublishAuthMode",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType"},
)
class AppsyncApiEventConfigDefaultPublishAuthMode:
    def __init__(self, *, auth_type: builtins.str) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4d428859dbdb10caa18089310ccb9e2fc8e159e2902039507b4570b19a4ca4)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigDefaultPublishAuthMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigDefaultPublishAuthModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigDefaultPublishAuthModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e50e97615abf288948bc99d7f855a6bf06397de5d7af02a58031ca23e9df18d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigDefaultPublishAuthModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30ca906a35405c07d57cf828c68d22431c9474638fc87caeebcf8a66fad1915)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigDefaultPublishAuthModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21d736e89772445bc54139e9d1df1ebd33c5e51459dccfbbf6a1deb98c343bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e22668bfdf789e5a365bb37fef83f417229ff8d2209504be24b5ebe525e6c55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06bb0012501a1add4d63a56c6d20952d8dce47b8fc36a25673fcf60875dd04f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultPublishAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultPublishAuthMode]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultPublishAuthMode]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42176bb911d490aba110c4402a4c57dd7de545d9f2e967deb734bd36a336f3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigDefaultPublishAuthModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigDefaultPublishAuthModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b9ec76043e52f356c9803096f9a7bc45de618ef1ad7b2ac197c9cf5887609af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b811fc964c7f3973a93d71efcf0813a33b6ba08941f9c765de37113feb9058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultPublishAuthMode]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultPublishAuthMode]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultPublishAuthMode]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632103b5dbd7c349d332eaf9db19fb220c3c780926d9ed7139ed0aff25119fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigDefaultSubscribeAuthMode",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType"},
)
class AppsyncApiEventConfigDefaultSubscribeAuthMode:
    def __init__(self, *, auth_type: builtins.str) -> None:
        '''
        :param auth_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715001a97e337306e8c58a95afbb81310368fa32b3adf24341631fb03fb5dabc)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#auth_type AppsyncApi#auth_type}.'''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigDefaultSubscribeAuthMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigDefaultSubscribeAuthModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigDefaultSubscribeAuthModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5332210a11ec3281ba5360a3a98d92aa1c21e5c91c29a238aafead942ad97fcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigDefaultSubscribeAuthModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341a3a4621a2ec50f181e8460922c675a55cfafe1c4d3e2f56193daaa063f34a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigDefaultSubscribeAuthModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6771cfda12ff2dd468ed3a3839a6e1d13f3fcc142ee3f147b6b028eb4ebf1d13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f747cd58b0d0e2f31ca8ceef3dbebd8a697b0db9cb9d48b6d44b0339d806072)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a26657199c74318fc09403494c261a57d19f6cb44cec4183fc3e63ba62019f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultSubscribeAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultSubscribeAuthMode]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultSubscribeAuthMode]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b513f2b1fd2267994763a85a44b1aa0dd2fd41fcd71cabedff602aa5cf60a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigDefaultSubscribeAuthModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigDefaultSubscribeAuthModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fc18d279f8cd64636666f8aa488620290296c494857f1c6c1500071d1955224)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96700511188fac90074a0de0b7998d5ac586862a97f5c354b09de140bca02a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultSubscribeAuthMode]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultSubscribeAuthMode]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultSubscribeAuthMode]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2af947f37a459483cc2ecf016d37ac4404450d48342e52c2762e2068cf7d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00209be086c32396516ff120a1de141b82b909700e54c825206d3a2e1d10e99e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppsyncApiEventConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c80bc3505c38ac5c6028582f8d4a8bcb5df23e04cf55871eacbcaaf6c0f6347)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3077bea4f1342536abc3f409b6bedd7fb2c062bc19e3203b4a0ebbe89cb183a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18cdfc311bfc9054410f71c374c262391499fb49a8d7dbf950a77134728ecb9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__526659054ef4c3fd7acff424ed55f4d1c98e6084d8f57f12484f8c7d3e65d622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63529404f410723245dd88a815dbfce41f98b1d28ed78f97b0e78764dd1aca77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_logs_role_arn": "cloudwatchLogsRoleArn",
        "log_level": "logLevel",
    },
)
class AppsyncApiEventConfigLogConfig:
    def __init__(
        self,
        *,
        cloudwatch_logs_role_arn: builtins.str,
        log_level: builtins.str,
    ) -> None:
        '''
        :param cloudwatch_logs_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#cloudwatch_logs_role_arn AppsyncApi#cloudwatch_logs_role_arn}.
        :param log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#log_level AppsyncApi#log_level}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a04742ba3f2faf5d8c13c4ec422650b313f6ba4301470bf7c4ec5a7b3dbdab)
            check_type(argname="argument cloudwatch_logs_role_arn", value=cloudwatch_logs_role_arn, expected_type=type_hints["cloudwatch_logs_role_arn"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudwatch_logs_role_arn": cloudwatch_logs_role_arn,
            "log_level": log_level,
        }

    @builtins.property
    def cloudwatch_logs_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#cloudwatch_logs_role_arn AppsyncApi#cloudwatch_logs_role_arn}.'''
        result = self._values.get("cloudwatch_logs_role_arn")
        assert result is not None, "Required property 'cloudwatch_logs_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/appsync_api#log_level AppsyncApi#log_level}.'''
        result = self._values.get("log_level")
        assert result is not None, "Required property 'log_level' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncApiEventConfigLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncApiEventConfigLogConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigLogConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f140ab100127ab7bdb1cc8e0c720adb9a489e8c2da01600ed0be5947a971a772)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncApiEventConfigLogConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0889f993f779d9cd41804eee5daf18ecef06faced549b6f6bea003c68bdf5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncApiEventConfigLogConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9dd11454f9737cf2e9b01561ae316ce8f77ba7fadf1eac7687647a3d0f263f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ae1c828c2c0d60b8d6952a0e7d575f31a201991ef91092895ff45fc64bba261)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb699b5315394b2c6bbd501e647a8abadbba31c0b9303789533527cbcfe4b0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigLogConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigLogConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigLogConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2638e55dd48cf1ee1a5e9a32cf753db7e29b608e61db36bfe51b7f1877cc63fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05f1aaf95c35517a4f36ed39169f09cd629cf73f65547e2ece59653e3ed580f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsRoleArnInput")
    def cloudwatch_logs_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsRoleArn")
    def cloudwatch_logs_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogsRoleArn"))

    @cloudwatch_logs_role_arn.setter
    def cloudwatch_logs_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f451bcadb3dad40b5ab2f94f91b10cdb382aa3726e0988683ea562419f20ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04fa13f5fae0614f9e28ba274ef17e824d95718e584d5fd0c59118b54a77310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigLogConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigLogConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigLogConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25017d89ff7f47c72f411be6837c777a4fe401d481756d83eabb05aa4932d227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncApiEventConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncApi.AppsyncApiEventConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0de02e9bfed7dc776259f7b280c6a28fff94db8245e4ff5c9698332ddc1ec3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuthProvider")
    def put_auth_provider(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProvider, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7961b7fa95229e4e6608b9e87d50dfd3807f5f30f4b744d1fe3491c005a3b187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthProvider", [value]))

    @jsii.member(jsii_name="putConnectionAuthMode")
    def put_connection_auth_mode(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigConnectionAuthMode, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9624fde68670d28d8e8dbf9205277d8c3024ec22a1ac0d880ae04fbae2d197a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectionAuthMode", [value]))

    @jsii.member(jsii_name="putDefaultPublishAuthMode")
    def put_default_publish_auth_mode(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigDefaultPublishAuthMode, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cbb67c7abdf3a1631bc73c4d32c81881c7a746053557f490aadab35f5f93cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultPublishAuthMode", [value]))

    @jsii.member(jsii_name="putDefaultSubscribeAuthMode")
    def put_default_subscribe_auth_mode(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigDefaultSubscribeAuthMode, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f74d905d9ad97bc29ee62023af51a075aa3ceb4912a49191d982f79980d84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultSubscribeAuthMode", [value]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigLogConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f3ae05eba43db48f63a629f82837c97ac465de63f7032da6bb260b082b1759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="resetAuthProvider")
    def reset_auth_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthProvider", []))

    @jsii.member(jsii_name="resetConnectionAuthMode")
    def reset_connection_auth_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionAuthMode", []))

    @jsii.member(jsii_name="resetDefaultPublishAuthMode")
    def reset_default_publish_auth_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPublishAuthMode", []))

    @jsii.member(jsii_name="resetDefaultSubscribeAuthMode")
    def reset_default_subscribe_auth_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSubscribeAuthMode", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @builtins.property
    @jsii.member(jsii_name="authProvider")
    def auth_provider(self) -> AppsyncApiEventConfigAuthProviderList:
        return typing.cast(AppsyncApiEventConfigAuthProviderList, jsii.get(self, "authProvider"))

    @builtins.property
    @jsii.member(jsii_name="connectionAuthMode")
    def connection_auth_mode(self) -> AppsyncApiEventConfigConnectionAuthModeList:
        return typing.cast(AppsyncApiEventConfigConnectionAuthModeList, jsii.get(self, "connectionAuthMode"))

    @builtins.property
    @jsii.member(jsii_name="defaultPublishAuthMode")
    def default_publish_auth_mode(
        self,
    ) -> AppsyncApiEventConfigDefaultPublishAuthModeList:
        return typing.cast(AppsyncApiEventConfigDefaultPublishAuthModeList, jsii.get(self, "defaultPublishAuthMode"))

    @builtins.property
    @jsii.member(jsii_name="defaultSubscribeAuthMode")
    def default_subscribe_auth_mode(
        self,
    ) -> AppsyncApiEventConfigDefaultSubscribeAuthModeList:
        return typing.cast(AppsyncApiEventConfigDefaultSubscribeAuthModeList, jsii.get(self, "defaultSubscribeAuthMode"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> AppsyncApiEventConfigLogConfigList:
        return typing.cast(AppsyncApiEventConfigLogConfigList, jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="authProviderInput")
    def auth_provider_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProvider]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProvider]]], jsii.get(self, "authProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionAuthModeInput")
    def connection_auth_mode_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigConnectionAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigConnectionAuthMode]]], jsii.get(self, "connectionAuthModeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPublishAuthModeInput")
    def default_publish_auth_mode_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultPublishAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultPublishAuthMode]]], jsii.get(self, "defaultPublishAuthModeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSubscribeAuthModeInput")
    def default_subscribe_auth_mode_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultSubscribeAuthMode]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultSubscribeAuthMode]]], jsii.get(self, "defaultSubscribeAuthModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigLogConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigLogConfig]]], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58a8f2d0efdd4d98248d2b96a2bf0a830a29d06e41f2155a58a65c1ff562b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsyncApi",
    "AppsyncApiConfig",
    "AppsyncApiEventConfig",
    "AppsyncApiEventConfigAuthProvider",
    "AppsyncApiEventConfigAuthProviderCognitoConfig",
    "AppsyncApiEventConfigAuthProviderCognitoConfigList",
    "AppsyncApiEventConfigAuthProviderCognitoConfigOutputReference",
    "AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig",
    "AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigList",
    "AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfigOutputReference",
    "AppsyncApiEventConfigAuthProviderList",
    "AppsyncApiEventConfigAuthProviderOpenidConnectConfig",
    "AppsyncApiEventConfigAuthProviderOpenidConnectConfigList",
    "AppsyncApiEventConfigAuthProviderOpenidConnectConfigOutputReference",
    "AppsyncApiEventConfigAuthProviderOutputReference",
    "AppsyncApiEventConfigConnectionAuthMode",
    "AppsyncApiEventConfigConnectionAuthModeList",
    "AppsyncApiEventConfigConnectionAuthModeOutputReference",
    "AppsyncApiEventConfigDefaultPublishAuthMode",
    "AppsyncApiEventConfigDefaultPublishAuthModeList",
    "AppsyncApiEventConfigDefaultPublishAuthModeOutputReference",
    "AppsyncApiEventConfigDefaultSubscribeAuthMode",
    "AppsyncApiEventConfigDefaultSubscribeAuthModeList",
    "AppsyncApiEventConfigDefaultSubscribeAuthModeOutputReference",
    "AppsyncApiEventConfigList",
    "AppsyncApiEventConfigLogConfig",
    "AppsyncApiEventConfigLogConfigList",
    "AppsyncApiEventConfigLogConfigOutputReference",
    "AppsyncApiEventConfigOutputReference",
]

publication.publish()

def _typecheckingstub__8ca1c10c22362405c4a2e2e8484b3b1f072456b9a957c16c969f234a11cf7e49(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    event_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    owner_contact: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__277e93108b7b223b8ed5bfd2b045f5c306357b2c54cd7a7c2d47f9652bd23a1f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fe6dcc9e0434c50ef092c46cdf5330f3f93fd7bb9076c789732d0daeb4adb0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee94b2ec335d433524d563474b0721151ee2c37a6d01e9e89fb1e435ca3d3f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85585fcb79a76ca7bc15e534919b69dc7b5b763892b27c6c1cea3632700b474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4374b7bbfb9078b7e91b60db9d01cbbc0c8e27a3b29a18a8646dd66849a31e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b104ebe7d5d91a306064af615dac9fa37fb991a24edfa04bfa8c9b33d011f771(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad87ebf36f83aa9d14c51acad2882816dd1f4cf6c20d8560913506ec82797c2b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    event_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    owner_contact: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5032e9a16cb19ed83db3c5ee9ad8dddf7741601e4fe759f495da1304296bb0fe(
    *,
    auth_provider: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigConnectionAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_publish_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigDefaultPublishAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_subscribe_auth_mode: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigDefaultSubscribeAuthMode, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigLogConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d78675ff9b03c000d84912a098552c244d93794a9179265c5a0f09e980206c(
    *,
    auth_type: builtins.str,
    cognito_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderCognitoConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    openid_connect_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderOpenidConnectConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c22f989bda5580be9ac56f033350afe23ad873b678af937d455a0ca8b452d6(
    *,
    aws_region: builtins.str,
    user_pool_id: builtins.str,
    app_id_client_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448fb1c88e6e600abd7951b5099de9d8198630dd8e2d6231c2dcd2fb78193668(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd8a41934cbb6f10db172e674b067e1f9b539d46a3f87e4229b08369d38acbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c843d3ac6f06533170d2999e0ca6fb2eafa6b836e4fbf1456b738fb4845db76b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a908ca8f86220ab45005625088bcd74f822f2a1ee14c2d9b4ef1d86530c7d164(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72002fa29c816d0099068a6108b1c939592c0f92cbdc306c440e9ef6677ce2e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484bd8eb980da6b8a8f7ae651aaafaee391f61dbea7b792c2d3b77d7c46365ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderCognitoConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a44cb18f36fda165f5d90c6930ca85449a4d07940161625243e52d9ca28590(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1d5200e7ec3ac607733283f812493ef1fb4b0fe7f840f2eff90d1cf2ddddc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda88753f256fb2d6202f10f10304a4443c287c1b4362c002db0d7a9758b8508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6f18339eb0e9af5e79080ff1988a462142d56cf925f2da6eaee85b766df087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1018cc7dbadf1438bc863a68c70f7cdb19bd077a550ba7c4311b65526008a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderCognitoConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbbdc01cc154c80cefd7b2666cbfa2ff7454e60476362970c4bb8df56df6cdf(
    *,
    authorizer_uri: builtins.str,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905af29662f88d449b8d898178f62ee833a182ecabf915d143b8b5ce4ec3bf0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985f6a79e6f6ac12d80ff35bde79d13c8448488dcf79786f042850b4f76c877(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1015cf6efc8e787f1695de107df987980461c4cb50c9250ac6c42f983c1acfa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6cfb12a75a4f69548ee857454e7b82eba65e2edb5bb8cf75977045e569dcba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a226ad95e02d8ab5143a5f7edbd721f53132df8f751f66e4b298b1fd2e857ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623a2198c523d11aa58cc9b0a49e0b3f35f5c5e475f6ee43e285328181705948(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5aa54db8972c67764d9eb53f53e59138bba39f285ff65044bb7bc5481b8c289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616eaca81317c549e056327c7e14fb76744f882ed7531420a852c13f9c8601a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69113aaebbd5446b0f485216b531be33e3a1b790ebefad7fa1bbab6f064ce1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba9edeaef83b8eb6c52f18ffd71669d56ae4b8ba1c5d8c20baa0393c59e7409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1848f4255bcd3f1a012e6294d6a2ef9347444448ab8b63ce1135eb2b9e8dc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe5f7f5e398e289dc0efba6b6d1349f25211c366e9dffb050c4955b2ef75bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4db985b52d328a11e1396e9b04ab56cf7220eeb1a924758d0bcd68c6438098f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150307156d0bece81636bec414b48955f8e973b8259a83760818fe2114b68c4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1114185f30e3cf82f8fc7a8776135099376fc4d6b2a59f812430da8799e92bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d378a9848a9e6976efd620bcf088e1f926e3cf66928fd4f04aa32a0339c878b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b6f823553c441093829751b47aa096c4fd3053587a609cdd770c8e8f44a0d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProvider]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123b35c9371ef324fab21b86da13347539dc4828bc9dba85877078ffd90a2548(
    *,
    issuer: builtins.str,
    auth_ttl: typing.Optional[jsii.Number] = None,
    client_id: typing.Optional[builtins.str] = None,
    iat_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ce587e5431b5c7c0500ab858223cc0aaf8025b80999af70da52132239d18b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fb528271a0c1a03ba91a29c37196d68dd57037aca16991fba9e58cc5cdbdf3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bc2b28dfb2422b4e6f53d21e7d05533dfa08be4e6e470040e819c4f38cc634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c926b46d68ac2f336bbdbdd1dcf75941d375673293acbb3e089eeeb2cd32d97(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6503884ddc8525428da13af472ed0998cd3bf87edfc742d27cd091b5db0ce83e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb229baa116abfc962cd7152cbd9f47d94f5a2e475b4a7db75f3098955b4f62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigAuthProviderOpenidConnectConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af67e8552e5db4671876e921d4bcb4ca8f88330f86b228b695e4987b06e0f8ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137509a083e76db7f57fe1d6b624893d8097ab319d3ee95f248da3ebb3ac987d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824bff0e4ddd025859fdcf0a0f6e885a1ad056718584575aa610ead9f0b6347a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d298350fcf4e5cbacd593c6fd3a5e06b82dbc24da39e32d9f7b6d624640002(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c20048d4915756bcf7b500218e3ac13a320d7501a73a2ab0df09ea4c255e0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9300caef9a80e5b601b9188f956d75f9f5fc8315239599b30a1e1d8422df934(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProviderOpenidConnectConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dc7cfefbbe2767064b368da3857357a549b43c206f68881d2d9663c4eddc44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfc313d0ae77d3e2989283553f88db6df0bd719b8927a4c16a8befc808bf612(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderCognitoConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c1bfab01d76c05860bc8dadaf61b1e889941d37ff4130cb1432bfe155e5899(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderLambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37be82fc520939a0929fd1a6bc7475d4dfe1cd6e84ab58fe63151ce1f734121(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProviderOpenidConnectConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c849edfbaf41efd5e085b23df6d9bab1763f0623083d78ef2fbdc537bf1eb26f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9be942dc08ad0025b11475ff662e39b93d7b199ff35272977854d23701a733(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigAuthProvider]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9509ffab43109087b07fc8bd1bef599b853061da7d61fe6dbd043dc3a6a55ae6(
    *,
    auth_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a123f8616fa62d3b21cbe287eec45cbabbe2dd47c8f7cba4608364d98548e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae62be8afcbe243dc009d490c0ec22705d7bef348863c2a00169b983478ec22(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675571f58027ec7bdb9e4243aa4251babb6cbfcfb465f39d680dbd8f8edf0553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5321948ff47bb90c96356288207dfd51f44db8a38f8cb9ad8e6b68caf1145f39(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966f1c9e53c6409717bca065c7a17ecbf526682087673bc779956d73f6602c99(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e525bc2112dc9c3b9029a6a1bf2adab76ba5c2488aa8900388322b054f18414e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigConnectionAuthMode]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3cd3380fdee2a04faab425d1e928e830a6355ad93b683f744f8ba31079d13e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22236b54a78adecf9177aef701ae7283de8a7577551da2292a84cec00c256d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79809dcc6423c61bf24a1e5fee5e83f7f35f4fcb5be4871221aafa9ca981f7d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigConnectionAuthMode]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4d428859dbdb10caa18089310ccb9e2fc8e159e2902039507b4570b19a4ca4(
    *,
    auth_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e50e97615abf288948bc99d7f855a6bf06397de5d7af02a58031ca23e9df18d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30ca906a35405c07d57cf828c68d22431c9474638fc87caeebcf8a66fad1915(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21d736e89772445bc54139e9d1df1ebd33c5e51459dccfbbf6a1deb98c343bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e22668bfdf789e5a365bb37fef83f417229ff8d2209504be24b5ebe525e6c55(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bb0012501a1add4d63a56c6d20952d8dce47b8fc36a25673fcf60875dd04f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42176bb911d490aba110c4402a4c57dd7de545d9f2e967deb734bd36a336f3b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultPublishAuthMode]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9ec76043e52f356c9803096f9a7bc45de618ef1ad7b2ac197c9cf5887609af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b811fc964c7f3973a93d71efcf0813a33b6ba08941f9c765de37113feb9058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632103b5dbd7c349d332eaf9db19fb220c3c780926d9ed7139ed0aff25119fe8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultPublishAuthMode]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715001a97e337306e8c58a95afbb81310368fa32b3adf24341631fb03fb5dabc(
    *,
    auth_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5332210a11ec3281ba5360a3a98d92aa1c21e5c91c29a238aafead942ad97fcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341a3a4621a2ec50f181e8460922c675a55cfafe1c4d3e2f56193daaa063f34a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6771cfda12ff2dd468ed3a3839a6e1d13f3fcc142ee3f147b6b028eb4ebf1d13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f747cd58b0d0e2f31ca8ceef3dbebd8a697b0db9cb9d48b6d44b0339d806072(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a26657199c74318fc09403494c261a57d19f6cb44cec4183fc3e63ba62019f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b513f2b1fd2267994763a85a44b1aa0dd2fd41fcd71cabedff602aa5cf60a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigDefaultSubscribeAuthMode]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc18d279f8cd64636666f8aa488620290296c494857f1c6c1500071d1955224(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96700511188fac90074a0de0b7998d5ac586862a97f5c354b09de140bca02a61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2af947f37a459483cc2ecf016d37ac4404450d48342e52c2762e2068cf7d0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigDefaultSubscribeAuthMode]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00209be086c32396516ff120a1de141b82b909700e54c825206d3a2e1d10e99e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c80bc3505c38ac5c6028582f8d4a8bcb5df23e04cf55871eacbcaaf6c0f6347(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3077bea4f1342536abc3f409b6bedd7fb2c062bc19e3203b4a0ebbe89cb183a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cdfc311bfc9054410f71c374c262391499fb49a8d7dbf950a77134728ecb9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526659054ef4c3fd7acff424ed55f4d1c98e6084d8f57f12484f8c7d3e65d622(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63529404f410723245dd88a815dbfce41f98b1d28ed78f97b0e78764dd1aca77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a04742ba3f2faf5d8c13c4ec422650b313f6ba4301470bf7c4ec5a7b3dbdab(
    *,
    cloudwatch_logs_role_arn: builtins.str,
    log_level: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f140ab100127ab7bdb1cc8e0c720adb9a489e8c2da01600ed0be5947a971a772(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0889f993f779d9cd41804eee5daf18ecef06faced549b6f6bea003c68bdf5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9dd11454f9737cf2e9b01561ae316ce8f77ba7fadf1eac7687647a3d0f263f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae1c828c2c0d60b8d6952a0e7d575f31a201991ef91092895ff45fc64bba261(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb699b5315394b2c6bbd501e647a8abadbba31c0b9303789533527cbcfe4b0d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2638e55dd48cf1ee1a5e9a32cf753db7e29b608e61db36bfe51b7f1877cc63fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncApiEventConfigLogConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f1aaf95c35517a4f36ed39169f09cd629cf73f65547e2ece59653e3ed580f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f451bcadb3dad40b5ab2f94f91b10cdb382aa3726e0988683ea562419f20ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04fa13f5fae0614f9e28ba274ef17e824d95718e584d5fd0c59118b54a77310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25017d89ff7f47c72f411be6837c777a4fe401d481756d83eabb05aa4932d227(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfigLogConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0de02e9bfed7dc776259f7b280c6a28fff94db8245e4ff5c9698332ddc1ec3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7961b7fa95229e4e6608b9e87d50dfd3807f5f30f4b744d1fe3491c005a3b187(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigAuthProvider, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9624fde68670d28d8e8dbf9205277d8c3024ec22a1ac0d880ae04fbae2d197a5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigConnectionAuthMode, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cbb67c7abdf3a1631bc73c4d32c81881c7a746053557f490aadab35f5f93cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigDefaultPublishAuthMode, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f74d905d9ad97bc29ee62023af51a075aa3ceb4912a49191d982f79980d84c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigDefaultSubscribeAuthMode, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f3ae05eba43db48f63a629f82837c97ac465de63f7032da6bb260b082b1759(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncApiEventConfigLogConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58a8f2d0efdd4d98248d2b96a2bf0a830a29d06e41f2155a58a65c1ff562b72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncApiEventConfig]],
) -> None:
    """Type checking stubs"""
    pass
